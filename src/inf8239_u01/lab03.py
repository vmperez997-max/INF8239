"""Comparación reproducible de modelos, reducción y costos computacionales."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import sys
from time import perf_counter

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.datasets import load_breast_cancer
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.manifold import TSNE, trustworthiness
from sklearn.metrics import accuracy_score, f1_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from threadpoolctl import threadpool_limits


def approved_split():
    """Reproduce exactamente test_size=.20, stratify=y, random_state=42."""
    bunch = load_breast_cancer(as_frame=True)
    return train_test_split(bunch.data, bunch.target, test_size=.20,
                            stratify=bunch.target, random_state=42)


def configurations():
    def svm(c, gamma, pca=False):
        steps = [('scale', StandardScaler())]
        if pca:
            steps.append(('pca', PCA(n_components=.95, svd_solver='full')))
        return Pipeline(steps + [('model', SVC(C=c, gamma=gamma, probability=False))])
    forest = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=1)
    return {
        'SVM base': svm(1, 'scale'),
        'SVM ajustado': svm(10, .01),
        'Random Forest': Pipeline([('model', forest)]),
        'Boosting': Pipeline([('model', GradientBoostingClassifier(
            n_estimators=100, learning_rate=.1, max_depth=2, random_state=42))]),
        'PCA + SVM': svm(10, .01, True),
        'PCA + RF': Pipeline([('scale', StandardScaler()),
                              ('pca', PCA(n_components=.95, svd_solver='full')),
                              ('model', clone(forest))]),
    }


def pareto_mask(values):
    """Todas las columnas se minimizan; los empates no se dominan entre sí."""
    a = np.asarray(values, dtype=float)
    if a.ndim != 2 or not np.isfinite(a).all():
        raise ValueError('Se requiere una matriz finita de objetivos.')
    return np.array([not np.any(np.all(a <= row, axis=1) & np.any(a < row, axis=1))
                     for row in a])


def run_experiment(output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import sklearn
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    models_dir = output / 'models'
    models_dir.mkdir(exist_ok=True)
    Xtr, Xte, ytr, yte = approved_split()
    split = pd.DataFrame({'fila': list(Xtr.index) + list(Xte.index),
                          'particion': ['train']*len(Xtr) + ['test']*len(Xte)})
    split.to_csv(output/'particion.csv', index=False)
    cv = StratifiedKFold(5, shuffle=True, random_state=42)
    configs = configurations()
    timings, records, cv_rows = [], [], []
    with threadpool_limits(limits=1):
        for number, (name, estimator) in enumerate(configs.items(), 1):
            # CV is recorded separately, never included in final fit timing.
            cv_start = perf_counter()
            scores = cross_val_score(estimator, Xtr, ytr, cv=cv, scoring='f1_macro', n_jobs=1)
            cv_seconds = perf_counter()-cv_start
            for fold, score in enumerate(scores, 1):
                cv_rows.append(dict(modelo=name, pliegue=fold, f1_macro=float(score)))
            paths, fitted = [], []
            for repeat in range(1, 4):
                model = clone(estimator)
                start = perf_counter(); model.fit(Xtr, ytr); fit_time = perf_counter()-start
                model.predict(Xte)  # warm-up excluded from measurement
                start = perf_counter()
                for _ in range(50):
                    model.predict(Xte)
                infer_ms = (perf_counter()-start)/50*1000
                path = models_dir/f'config_{number:02d}_rep_{repeat}.joblib'
                joblib.dump(model, path, compress=3)
                restored = joblib.load(path)
                assert np.array_equal(model.predict(Xte), restored.predict(Xte))
                timings.append(dict(modelo=name, repeticion=repeat, train_s=fit_time,
                    infer_ms_lote=infer_ms, infer_us_fila=infer_ms*1000/len(Xte),
                    size_kib=path.stat().st_size/1024))
                fitted.append(model); paths.append(path)
            latest = timings[-3:]
            selected_repeat = int(np.argsort([x['train_s'] for x in latest])[1])
            model = fitted[selected_repeat]
            pred = model.predict(Xte)
            score = (-model.decision_function(Xte) if hasattr(model, 'decision_function')
                     else model.predict_proba(Xte)[:,0])
            records.append(dict(modelo=name, cv_f1=float(scores.mean()), cv_std=float(scores.std()),
                cv_total_s=cv_seconds, test_f1=f1_score(yte,pred,average='macro'),
                accuracy=accuracy_score(yte,pred), recall_maligno=recall_score(yte,pred,pos_label=0),
                auc=roc_auc_score((yte==0).astype(int),score),
                falsos_negativos=int(((yte==0)&(pred==1)).sum()),
                componentes=int(model.named_steps['pca'].n_components_) if 'pca' in model.named_steps else 30,
                modelo_archivo=str(paths[selected_repeat].relative_to(output)),
                confusion=json.dumps(confusion_matrix(yte,pred,labels=[0,1]).tolist())))
            print(name, 'terminado', flush=True)
        raw = pd.DataFrame(timings)
        raw.to_csv(output/'mediciones.csv', index=False)
        medians = raw.groupby('modelo',sort=False)[['train_s','infer_ms_lote','infer_us_fila','size_kib']].median()
        result = pd.DataFrame(records).merge(medians,on='modelo')
        result['pareto'] = pareto_mask(result[['cv_f1','train_s','infer_ms_lote','size_kib']].to_numpy()*[-1,1,1,1])
        # Declared rule: within 0.01 CV F1 of best, Pareto-efficient, then
        # minimize equal-weight relative train / inference / serialized size.
        costs=result[['train_s','infer_ms_lote','size_kib']]
        result['costo_relativo']=(costs/costs.min()).mean(axis=1)
        result['elegible'] = result['pareto'] & (result.cv_f1 >= result.cv_f1.max()-.01)
        choice=result.loc[result.elegible].sort_values('costo_relativo').iloc[0]
        result['seleccionado']=result.modelo.eq(choice.modelo)
        result.to_csv(output/'resultados.csv',index=False)
        pd.DataFrame(cv_rows).to_csv(output/'validacion_cruzada.csv',index=False)
        pd.DataFrame(configs.keys(),columns=['modelo']).assign(
            parametros=[str(m.get_params()) for m in configs.values()]).to_csv(output/'configuraciones.csv',index=False)

        scaled=StandardScaler().fit_transform(Xtr)
        pca=PCA(n_components=2,svd_solver='full').fit(scaled)
        coords=pca.transform(scaled)
        fig,ax=plt.subplots(figsize=(7,4.3))
        colors=['#bd473f','#247a98']
        def scatter(ax,xy):
            for target,label,color in [(0,'Maligno',colors[0]),(1,'Benigno',colors[1])]:
                ax.scatter(xy[ytr.to_numpy()==target,0],xy[ytr.to_numpy()==target,1],
                           s=16,alpha=.7,label=label,c=color)
            ax.legend(frameon=False)
        scatter(ax,coords)
        ax.set(xlabel=f'PC1 ({pca.explained_variance_ratio_[0]:.1%})',
               ylabel=f'PC2 ({pca.explained_variance_ratio_[1]:.1%})',title='PCA 2D · solo entrenamiento')
        fig.tight_layout();fig.savefig(output/'pca.png',dpi=180);plt.close(fig)
        embeddings=[]
        for perplexity in (10,30):
            xy=TSNE(n_components=2,perplexity=perplexity,init='pca',learning_rate='auto',
                    max_iter=1000,random_state=42,n_jobs=1).fit_transform(scaled)
            trust=float(trustworthiness(scaled,xy,n_neighbors=5))
            embeddings.append(dict(perplexity=perplexity,trustworthiness=trust))
            fig,ax=plt.subplots(figsize=(7,4.3));scatter(ax,xy)
            ax.set(title=f't-SNE · perplexity={perplexity} · confianza local={trust:.3f}',
                   xlabel='Dimensión 1 (sin unidad)',ylabel='Dimensión 2 (sin unidad)')
            fig.tight_layout();fig.savefig(output/f'tsne_{perplexity}.png',dpi=180);plt.close(fig)
            pd.DataFrame({'fila':Xtr.index,'x':xy[:,0],'y':xy[:,1],'target':ytr.to_numpy()}).to_csv(
                output/f'tsne_{perplexity}.csv',index=False)
        fig,axes=plt.subplots(1,3,figsize=(12,4.2),sharey=True)
        for ax,cost,label in zip(axes,['train_s','infer_ms_lote','size_kib'],
                                ['Entrenamiento (s)','Inferencia / lote (ms)','Modelo (KiB)']):
            for i,row in result.iterrows():
                ax.scatter(row[cost],row.cv_f1,c='#247a98' if row.pareto else '#999999',
                           marker='*' if row.seleccionado else 'o',s=130 if row.seleccionado else 55)
                ax.annotate(str(i+1),(row[cost],row.cv_f1),xytext=(4,5),textcoords='offset points')
            ax.set_xscale('log');ax.set_xlabel(label);ax.grid(alpha=.2)
        axes[0].set_ylabel('F1 macro medio CV (mayor es mejor)')
        fig.suptitle('Pareto 4D: proyecciones · azul=no dominado · estrella=decisión')
        fig.tight_layout();fig.savefig(output/'pareto.png',dpi=180);plt.close(fig)
        summary=dict(dataset='Breast Cancer Wisconsin (Diagnostic)',train=455,test=114,
            python=sys.version,platform=platform.platform(),sklearn=sklearn.__version__,
            cpu=platform.processor(),threads=1,repetitions=3,inference_batch=114,inference_loops=50,
            selected=choice.modelo,pca_2d_variance=float(pca.explained_variance_ratio_.sum()),tsne=embeddings,
            split_sha256=hashlib.sha256(split.to_csv(index=False).encode()).hexdigest(),
            rule='Pareto sobre -F1 CV, train_s, infer_ms_lote, size_kib; tolerancia F1=0.01; costo relativo medio mínimo',
            limitations='Tiempo de pared, no energía. Orden fijo; variación térmica y de carga posible. Test previamente consultado en Ejercicio 01.')
        (output/'resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    return result


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='reports/lab03')
    args=parser.parse_args()
    print(run_experiment(args.output).to_string(index=False))
