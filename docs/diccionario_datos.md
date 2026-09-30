# Diccionario de datos

Cada fila es una muestra. Las 30 variables numéricas combinan diez medidas con tres resúmenes: `mean` (media), `error` (error estándar) y `worst` (media de los tres valores mayores). Las unidades físicas no están especificadas aquí; no se atribuyen milímetros u otras unidades sin documentación.

| Medida base | Interpretación |
|---|---|
| radius | Distancia del centro al perímetro |
| texture | Dispersión de niveles de gris |
| perimeter | Perímetro del núcleo |
| area | Área del núcleo |
| smoothness | Variación local de radios |
| compactness | Medida de compacidad basada en perímetro y área |
| concavity | Intensidad de concavidades del contorno |
| concave points | Puntos cóncavos del contorno |
| symmetry | Simetría |
| fractal dimension | Complejidad del contorno |

`target`: entero, 0 maligno y 1 benigno. No es predictor. El identificador original de UCI no se incluye entre las variables de scikit-learn.

La auditoría completa por columna se genera en `reports/auditoria.csv`. Se inspeccionan ausentes y duplicados; no se imputan ni eliminan observaciones con reglas aprendidas del test. StandardScaler se ajusta dentro de cada pliegue mediante Pipeline. No se realiza selección de variables fuera de la validación cruzada. El loader no aporta identificadores de paciente que permitan verificar agrupamientos clínicos; no se afirma generalización entre hospitales o pacientes nuevos.

Fuente: https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic
