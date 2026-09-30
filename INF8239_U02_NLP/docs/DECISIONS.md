# Decisiones de LAB04
1. Mantener U02 en una carpeta separada dentro del repositorio existente de U01.
2. No se recibió el ZIP base. La estructura se creó según la guía, sin atribuirla al autor del material.
3. Proponer corpus de sentimiento, dejando aprobación docente pendiente. No entrenar un modelo.
4. Preservar ZIP, texto y etiquetas. Añadir metadatos de trazabilidad.
5. Separar filas por LF, no por todos los separadores Unicode: IMDb contiene separadores que pertenecen a la oración. Se agregó una prueba de regresión.
6. Retirar duplicados normalizados de la copia procesada antes de una futura división. El dataset original sigue intacto.
7. La suite del contrato es específica de este corpus de 3000 filas. Al cambiar DATA_SOURCE o columnas hay que adaptar contrato y ficha.
8. El hash verifica identidad de bytes, no veracidad, licencia ni ausencia de sesgo.
9. No publicar corpus completo ni .env; publicar scripts, lockfile, pruebas, auditoría y muestras revisadas.
10. No se comprobó ejecución real en Colab. Se proporcionan rutas relativas e instrucciones reproducibles para esa verificación.

