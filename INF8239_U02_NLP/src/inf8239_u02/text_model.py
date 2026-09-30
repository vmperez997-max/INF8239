from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.dummy import DummyClassifier
from sklearn.naive_bayes import ComplementNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from inf8239_u02.corpus import ROOT, normalized, sha

def pipelines():
    models = {'Dummy':DummyClassifier(strategy='most_frequent'),
              'ComplementNB':ComplementNB(alpha=1.0),
              'LogisticRegression':LogisticRegression(C=1.0,max_iter=2000,random_state=42)}
    return {name:Pipeline([('tfidf',TfidfVectorizer(ngram_range=(1,2),min_df=2,sublinear_tf=True)),
                           ('model',model)]) for name,model in models.items()}

def train():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    frame=pd.read_csv(ROOT/'data/processed/dataset.csv',keep_default_na=False)
    if not {'text','label'}<=set(frame) or frame.empty:
        raise ValueError('Falta texto/target o corpus vacío')
    if not frame.text.map(lambda x:bool(str(x).strip())).all() or frame.label.nunique()!=2:
        raise ValueError('Texto vacío o clases inválidas')
    keys=frame.text.map(normalized)
    if keys.duplicated().any():
        raise ValueError('Retire duplicados mediante audit_data.py antes de entrenar')
    train_ids,test_ids=train_test_split(np.arange(len(frame)),test_size=.2,random_state=42,stratify=frame.label)
    Xtr,Xte=frame.text.iloc[train_ids],frame.text.iloc[test_ids]
    ytr,yte=frame.label.iloc[train_ids],frame.label.iloc[test_ids]
    report=ROOT/'reports';report.mkdir(exist_ok=True)
    pd.DataFrame({'row':np.concatenate([train_ids,test_ids]),
        'split':['train']*len(train_ids)+['test']*len(test_ids)}).to_csv(report/'text_split.csv',index=False)
    rows=[]; predictions={}; fitted={}
    for name,model in pipelines().items():
        model.fit(Xtr,ytr)
        pred=model.predict(Xte)
        stats=classification_report(yte,pred,output_dict=True,zero_division=0)
        rows.append(dict(model=name,f1_macro=f1_score(yte,pred,average='macro'),
            accuracy=stats['accuracy'],
            precision_0=stats['0']['precision'],recall_0=stats['0']['recall'],f1_0=stats['0']['f1-score'],support_0=stats['0']['support'],
            precision_1=stats['1']['precision'],recall_1=stats['1']['recall'],f1_1=stats['1']['f1-score'],support_1=stats['1']['support']))
        predictions[name]=pred;fitted[name]=model
        print(name);print(classification_report(yte,pred,digits=4,zero_division=0))
    metrics=pd.DataFrame(rows).sort_values('f1_macro',ascending=False,kind='stable')
    metrics.to_csv(report/'text_metrics.csv',index=False)
    winner=metrics.iloc[0]['model']; model=fitted[winner];pred=predictions[winner]
    # Single held-out partition used for model comparison: selected score is exploratory.
    errors=frame.iloc[test_ids].copy()
    errors['row']=test_ids;errors['prediction']=pred
    errors=errors.loc[errors.label!=errors.prediction]
    errors['category']='pendiente';errors['rationale']=''
    errors.to_csv(report/'error_analysis.csv',index=False)
    fig,ax=plt.subplots(figsize=(6,4.5))
    ConfusionMatrixDisplay.from_predictions(yte,pred,labels=[0,1],
        display_labels=['Negativo','Positivo'],cmap='Blues',colorbar=False,ax=ax)
    ax.set(title=winner+' · partición de evaluación',xlabel='Predicción',ylabel='Clase real')
    fig.tight_layout();fig.savefig(report/'confusion_text.png',dpi=180);plt.close(fig)
    (ROOT/'models').mkdir(exist_ok=True)
    target=ROOT/'models/text_model.joblib'
    joblib.dump(model,target,compress=3)
    assert np.array_equal(joblib.load(target).predict(Xte),pred)
    meta=dict(selected=winner,train=len(train_ids),test=len(test_ids),
        classes={str(k):int(v) for k,v in frame.label.value_counts().items()},
        confusion=confusion_matrix(yte,pred,labels=[0,1]).tolist(),errors=len(errors),
        vocabulary=len(model.named_steps['tfidf'].vocabulary_),model_bytes=target.stat().st_size,
        model_sha256=sha(target.read_bytes()),processed_sha256=sha((ROOT/'data/processed/dataset.csv').read_bytes()),
        selection='Mayor F1 macro en la partición compartida; sin test independiente posterior.',
        language='English',scope='Amazon, IMDb, Yelp; etiquetas polarizadas')
    (ROOT/'models/model_metadata.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    (report/'text_summary.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    return metrics

