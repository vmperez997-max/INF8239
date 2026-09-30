# Diccionario
| Columna | Tipo | Significado | Unidad/categorías | Disponibilidad | Uso y riesgo |
|---|---|---|---|---|---|
| text | texto UTF-8 | Oración de reseña | caracteres; inglés | Al recibir reseña | Futuro predictor; riesgo de identificadores, insultos y duplicados |
| label | entero representado en CSV | Sentimiento anotado | 0 negativo, 1 positivo | Anotación del corpus | Solo target; excluir de X |
| source | texto | Dominio de procedencia | amazon, imdb, yelp | Ingesta del archivo | Auditoría/estratificación por dominio; no predictor |
| source_row | entero | Línea del archivo fuente | 1 a 1000 por dominio | Ingesta | Trazabilidad; no predictor |

Longitud: número de caracteres Unicode, incluyendo espacios. p50/p90/p99 usa interpolación lineal. No son tokens.
Nulo: valor ausente o cadena vacía tras strip. CSV es textual; no se inventan tipos numéricos para text.
Fuente de definiciones: ficha UCI y transformación documentada en DATASET_CARD.md.

