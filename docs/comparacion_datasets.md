# Comparación y selección de datasets

| Criterio | Breast Cancer Wisconsin (Diagnostic) | Wine |
|---|---|---|
| Procedencia | UCI; Wolberg, Mangasarian y Street | UCI; Aeberhard y Forina |
| Tamaño | 569 muestras; 30 variables | 178 muestras; 13 variables |
| Dominio y unidad | Salud; muestra de masa mamaria | Química; muestra de vino |
| Target | Maligno (0) o benigno (1) en scikit-learn | Tres cultivares (0, 1, 2) en scikit-learn |
| Pregunta | ¿Puede un SVM distinguir muestras benignas y malignas? | ¿Puede un SVM identificar el cultivar por su composición química? |
| Tarea | Clasificación binaria | Clasificación multiclase |
| Error relevante | Maligno clasificado como benigno | Asignación del cultivar incorrecto |
| Licencia | CC BY 4.0; requiere atribución | CC BY 4.0; requiere atribución |
| Acceso reproducible | load_breast_cancer(as_frame=True) | load_wine(as_frame=True) |

Se selecciona Breast Cancer Wisconsin (Diagnostic) por continuidad con LAB01 y LAB02, mayor tamaño y posibilidad de analizar el costo desigual de los errores. Wine se propone como alternativa comparativa, no como un experimento ejecutado.

**Dataset aprobado: `load_breast_cancer`, según confirmación del estudiante.** No se adjuntó una constancia docente; se registra la declaración, sin inventar firma ni fecha de aprobación.

Fuentes: https://doi.org/10.24432/C5DW2B y https://doi.org/10.24432/C5PC7J.
Uso exclusivamente educativo; no constituye diagnóstico médico.
