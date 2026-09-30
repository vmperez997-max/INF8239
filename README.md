# INF-8239 - Ciencia de Datos II

## LAB00 - Configuración del entorno reproducible

Este proyecto corresponde a la asignatura **INF-8239 - Ciencia de Datos II**.

El objetivo de este laboratorio es preparar y verificar un entorno de desarrollo reproducible utilizando Python, entornos virtuales, Jupyter, Pytest y Git.

## Sistema operativo

- Sistema operativo: Windows
- Terminal utilizada: PowerShell
- Editor: Visual Studio Code
- Python: Python 3
- Entorno virtual: `.venv`
- Pruebas: Pytest

## Estructura del proyecto

```text
INF8239_U01/
├── data/
├── notebooks/
│   └── 00_verificacion.ipynb
├── reports/
├── src/
│   └── inf8239_u01/
│       ├── __init__.py
│       └── environment.py
├── tests/
│   └── test_environment.py
├── .gitignore
├── README.md
└── requirements.txt

# Crear las carpetas del proyecto
mkdir data, notebooks, reports, src, tests

# Crear el entorno virtual
python -m venv .venv

# Permitir temporalmente la ejecución de scripts en PowerShell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# Activar el entorno virtual
.venv\Scripts\Activate.ps1

# Actualizar pip
python -m pip install --upgrade pip

# Instalar las dependencias del proyecto
python -m pip install -r requirements.txt

# Instalar pytest
python -m pip install pytest

# Verificar la versión de pytest
python -m pytest --version

# Crear el paquete principal
mkdir src\inf8239_u01

# Crear __init__.py
New-Item src\inf8239_u01\__init__.py

# Crear el módulo environment.py
New-Item src\inf8239_u01\environment.py

# Crear la prueba
New-Item tests\test_environment.py

# Crear el notebook de verificación
New-Item notebooks\00_verificacion.ipynb

# Indicar que los módulos están dentro de src
$env:PYTHONPATH="src"

# Ejecutar las pruebas
python -m pytest -q

# Verificar la versión de Python
python --version

# Verificar la versión de Git
git --version

# Mostrar la estructura del proyecto
tree /F

# Crear el archivo .gitignore
New-Item .gitignore

# Crear el README
New-Item README.md

# Inicializar el repositorio Git
git init

# Verificar el estado de Git
git status

# Agregar todos los archivos al repositorio
git add .

# Crear el primer commit
git commit -m "chore: create INF-8239 reproducible environment"

# Verificar que el repositorio esté limpio
git status

# Mostrar el historial de commits
git log --oneline