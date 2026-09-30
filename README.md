# INF-8239 · Entrega individual LAB01 y LAB02

**Estudiante:** Victor Manuel Perez Padilla · **Matrícula:** 100801946

## Acceso y estado

Notebook en Colab facilitado por el estudiante: https://colab.research.google.com/drive/1kb44TW4-tWTv62YG1D83EllbzLojxVNS?usp=sharing

**Enlace del repositorio Git: pendiente.** Existe un repositorio local, pero no tiene remoto configurado. Colab no sustituye el repositorio solicitado. No se ha verificado que el notebook remoto coincida con esta versión local.

## Entorno e instalación (Windows / PowerShell)

Verificado con Windows 11, Python 3.14.0 y Git 2.55.0.windows.5. Abra la carpeta que contiene este README. En una copia nueva:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-lock.txt
python -m pytest -q -p no:cacheprovider
```

`requirements-lock.txt` registra las versiones del entorno ejecutado; `requirements.txt` contiene las dependencias directas mínimas. La disponibilidad de esas versiones depende del índice de paquetes usado.

En la estructura actual del equipo, el entorno utilizado está dos niveles arriba del proyecto. Para reutilizarlo:

```powershell
..\..\.venv\Scripts\Activate.ps1
python -m pytest -q -p no:cacheprovider
```

## Datos y descarga reproducible

Se utiliza Breast Cancer Wisconsin (Diagnostic), UCI, DOI https://doi.org/10.24432/C5DW2B, licencia CC BY 4.0. Autores: Wolberg, Mangasarian y Street (1993). Los datos vienen incluidos en scikit-learn: instalar la dependencia obtiene la copia usada por el loader; no se descarga un CSV manual ni se necesitan credenciales.

```python
from sklearn.datasets import load_breast_cancer
bunch = load_breast_cancer(as_frame=True)
X, y = bunch.data.copy(), bunch.target.copy()
```

Tiene 569 muestras, 30 variables y target 0=maligno / 1=benigno. Fuente original: https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic

## Ejecución

Abra `notebooks/01_svm_guiada.ipynb` en VS Code con las extensiones Python y Jupyter, seleccione el intérprete del entorno instalado y use «Reiniciar kernel» y «Ejecutar todo». Ejecute desde la raíz del proyecto o desde `notebooks`. El notebook local entregado ya contiene salidas de una ejecución completa y usa `build_svm` de `src`.

Se separa 80/20 con estratificación y semilla 42. El baseline predice la clase más frecuente. Se ajusta StandardScaler dentro de Pipeline y se comparan nueve configuraciones mediante cinco pliegues de entrenamiento, con F1 macro. El AUC usa decision_function; no requiere probabilidades. La selección no usa las métricas del test. El test había sido consultado en la práctica previa, por lo que no constituye una validación externa independiente.

## Estructura y resultados

```text
notebooks/  Notebook de verificación y experimento ejecutado
src/inf8239_u01/  environment.py y models.py
tests/  Una prueba de entorno y tres pruebas del modelo
reports/  Resultados CSV, auditoría, errores, figuras y modelo regenerable
docs/  Ficha, comparación, diccionario e informe Word
requirements.txt
requirements-lock.txt
pytest.ini
README.md
```

Se generan `resultados_finales.csv`, `svm_cv_results.csv`, `auditoria.csv`, `errores_svm.csv`, `resumen.json`, `matriz_confusion.png`, `curva_roc.png` y `svm_best.joblib`. El archivo joblib está ignorado por Git y se regenera al ejecutar el notebook.

## Verificación y Git

```powershell
python --version
git --version
python -m pytest tests/test_environment.py -q -p no:cacheprovider
python -m pytest -q -p no:cacheprovider
tree /F
git log --oneline
```

Resultado verificado: una prueba de entorno aprobada; cuatro pruebas totales aprobadas. Se desactiva solo la caché para evitar los avisos de permisos observados. La función permite probability=True por compatibilidad con la práctica inicial; scikit-learn avisa su futura retirada. El notebook utiliza probability=False.

Primer commit local: `8121c7a chore: create INF-8239 reproducible environment`. Las mejoras de esta entrega no se han confirmado ni publicado automáticamente.

Uso educativo: no constituye diagnóstico médico. Véanse `docs/comparacion_datasets.md` y `docs/diccionario_datos.md` para selección, aprobación declarada y prevención de fuga.
