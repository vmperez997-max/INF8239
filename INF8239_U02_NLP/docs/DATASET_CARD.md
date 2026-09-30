# Ficha del corpus - U02.LAB04

**Estudiante:** Victor Manuel Perez Padilla, 100801946.
**Corpus propuesto:** Sentiment Labelled Sentences.
**Pregunta:** ¿Qué características de un corpus de reseñas permiten preparar una clasificación binaria de sentimiento reproducible sin confundir duplicados con evidencia independiente?
**Unidad:** una oración extraída de una reseña. **Target:** label (0 negativo; 1 positivo).
**Uso previsto:** auditoría y preparación educativa; no se entrenó un modelo en LAB04.
**Responsable:** Dimitrios Kotzias. Publicación de referencia: Kotzias, Denil, de Freitas y Smyth, *From Group to Individual Labels Using Deep Features* (2015).
**Procedencia:** UCI; oraciones de Amazon, IMDb y Yelp; 1000 por dominio.
**Fecha de ficha:** 29 de mayo de 2015. El periodo de escritura de cada reseña no está documentado; no se infiere a partir de esta fecha.
**Licencia:** CC BY 4.0 según UCI; atribuir dataset y publicación.
**Ficha:** https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences
**Descarga:** https://archive.ics.uci.edu/static/public/331/sentiment+labelled+sentences.zip
**Cita:** Kotzias, D. (2015). Sentiment Labelled Sentences. UCI. https://doi.org/10.24432/C57604
**Versión:** bytes identificados mediante SHA-256 en reports/download_manifest.json; no hay versión numerada declarada por el proyecto.

## Transformación
Se conserva source.zip. Se leen tres archivos TSV línea a línea separando por el último tabulador; las comillas del texto no son delimitadores CSV. Se agregan source y source_row para trazabilidad. El CSV derivado preserva el texto original; no se traduce ni se convierte a minúsculas. El hash del ZIP y del CSV se registra por separado.
La normalización casefold y de espacios solo calcula claves de duplicados. Se conserva la primera aparición por clave; si hubiera etiquetas incompatibles, se excluiría todo el grupo para revisión. No se altera data/raw manualmente.
Resultado: 3000 filas originales, 2979 procesadas. No hay nulos ni conflictos de etiqueta; 17 repeticiones exactas de texto y 21 normalizadas. La unicidad de fila completa es engañosa porque source_row distingue registros repetidos.

## Cinco ejemplos revisados
Textos cortos sin nombres de persona, contactos ni identificadores visibles; revisión manual de esta muestra, no garantía de anonimato del corpus entero. No se reemplazó texto en estos cinco ejemplos.
| Texto | Etiqueta |
|---|---|
| Good case, Excellent value. | 1 |
| The mic is great. | 1 |
| Needless to say, I wasted my money. | 0 |
| What a waste of money and time!. | 0 |
| Waste of money. | 0 |

Los cinco ejemplos se comprobaron contra el CSV descargado; reports/examples.csv registra dominio y línea de origen.

## Riesgos y límites
Inglés, tres dominios y etiquetas polarizadas seleccionadas: no representa español dominicano, opiniones neutrales, todas las edades o el presente. No hay metadatos de grupo para medir equidad por población. Los duplicados se retiran antes de dividir; falta revisar casi duplicados y posibles reseñas compartidas.
source y source_row no son predictores: pueden revelar el dominio o el orden y permitir atajos. El futuro vocabulario/TF-IDF se ajustará solo con entrenamiento.
No usar para decisiones sobre personas, inferir atributos sensibles, reidentificar autores ni afirmar representatividad clínica, demográfica o nacional.

## Estado de aprobación
Selección técnica propuesta, no aprobación docente. El estudiante no confirmó todavía la aprobación de este corpus ni la disponibilidad del ZIP base del curso. Se reconstruyó la arquitectura descrita por la guía; no se afirma equivalencia con el proyecto base.

