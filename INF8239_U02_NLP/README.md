# INF-8239 U02.LAB04 - Corpus público
Victor Manuel Perez Padilla · 100801946

Subproyecto dentro de https://github.com/vmperez997-max/INF8239.
La guía base es de Edwin Ramón José Nolasco; este código se construyó a partir de sus requisitos porque no se suministró INF8239_U02_NLP_Proyecto_Base.zip.
Corpus propuesto: UCI Sentiment Labelled Sentences. Aprobación docente pendiente; no se entrenó ningún modelo.

## Windows / Linux / macOS
Instale uv mediante el procedimiento oficial de https://docs.astral.sh/uv/getting-started/installation/.
Desde esta carpeta:
```powershell
uv --version
uv python install 3.12
uv sync --locked
Copy-Item .env.example .env
uv run python --version
uv run python scripts/download_data.py
uv run python scripts/audit_data.py
uv run pytest tests/test_data_contract.py -q
uv run pytest -q
```
En Linux/macOS use `cp .env.example .env`. uv crea .venv automáticamente. No cree ni copie manualmente el entorno.
La primera ejecución de pruebas del corpus requiere descargar y auditar antes; las pruebas unitarias del parser pueden ejecutarse antes con `uv run pytest tests/test_parser.py -q`.
El corpus usa solo la biblioteca estándar. pytest es dependencia de desarrollo; uv.lock fija las versiones del entorno.

## Fuente y configuración
.env.example documenta URL y columnas reales: text y label. .env se ignora en Git.
DATA_SOURCE=url admite el ZIP de UCI elegido o un CSV UTF-8 público. El adaptador ZIP es específico del corpus seleccionado.
DATA_SOURCE=local valida el archivo relativo indicado por DATASET_PATH. Variables de entorno prevalecen sobre .env.
Ficha y licencia CC BY 4.0: https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences.
Descarga directa: https://archive.ics.uci.edu/static/public/331/sentiment+labelled+sentences.zip.
Atribución: Kotzias (2015), DOI https://doi.org/10.24432/C57604.
Los datos no requieren Drive ni cuenta personal.

## Resultados y estructura
- data/raw/source.zip: bytes originales; no editar.
- data/raw/dataset.csv: conversión trazable.
- data/processed/dataset.csv: textos únicos por clave normalizada.
- docs/: candidatos, ficha, diccionario y decisiones.
- reports/: hash de descarga, auditoría, ejemplos y evidencia de pruebas.
- src/inf8239_u02/: funciones reutilizables.
- scripts/: descarga y auditoría.
- tests/: contrato y pruebas del parser.
- app/: reservada, sin aplicación implementada en este laboratorio.

## Colab
Suba un ZIP del subproyecto sin .venv ni .env, o clone el repositorio una vez publicados los cambios. Cambie al directorio que contiene este README:
```python
%pip install -r requirements-colab.txt
!python scripts/download_data.py
!python scripts/audit_data.py
!python -m pytest -q
```
El entorno de Colab lo administra Google; no se exige allí .venv ni Python 3.12 exacto. La prueba real en Colab queda pendiente.
No hay rutas personales ni credenciales en el código. Los datos y entornos están ignorados; se conserva uv.lock.

## Interpretación
3000 filas originales; clases 1500/1500; 21 repeticiones normalizadas; 2979 filas procesadas.
Deduplicación no prueba independencia entre autores. Antes de modelar, comprobar casi duplicados y separación por reseña/dominio, y aprender vocabulario solo con entrenamiento.
Las pruebas validan reglas programadas, no representatividad ni verdad del corpus.

