# Ficha del dataset

- **Dominio:** Salud; clasificación de muestras de masas mamarias con el dataset Breast Cancer Wisconsin (Diagnostic), disponible en scikit-learn mediante `load_breast_cancer`.
- **Unidad de análisis:** Una muestra de masa mamaria, representada por características numéricas de núcleos celulares extraídas de una imagen digitalizada de una aspiración con aguja fina. Cada fila corresponde a una muestra.
- **Decisión:** En un escenario hipotético, apoyar la priorización de muestras para revisión especializada según su clasificación estimada como benignas o malignas. En esta práctica se evalúa el modelo con fines educativos.
- **Target:** Variable objetivo tentativa: clase de la muestra, con la codificación de scikit-learn `0 = maligno` y `1 = benigno`.
- **Tipo de tarea:** Aprendizaje supervisado de clasificación binaria.
- **Error más costoso:** Clasificar una muestra maligna como benigna, porque en el escenario planteado podría retrasar su revisión. Es un falso negativo respecto a la detección de malignidad; para calcular métricas con ese significado se debe considerar la clase maligna (`0`) como positiva.
- **Usuario:** En esta práctica, estudiantes y docentes de ciencia de datos. En el escenario hipotético de apoyo, profesionales de salud responsables de revisar las muestras.

> **Advertencia:** Este ejemplo es exclusivamente educativo y no constituye un diagnóstico médico ni sustituye la evaluación de un profesional de la salud.
