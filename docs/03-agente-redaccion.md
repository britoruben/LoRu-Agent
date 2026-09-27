# 03 · Flujo R — Génesis de artículos

| # | Tarea | Tipo | Estado de diseño |
|---|---|---|---|
| R1 | Integrar estado de la cuestión + documentos propios según objetivos/metodología | LLM | Definido |
| R2 | Adaptar a nivel y formato de revista/editorial | Mixto | Definido |
| R3 | Citación literal con paginación | Determinista + LLM | Definido |
| R4 | Evitar citas inexistentes o mal formateadas | Determinista | Definido (núcleo del sistema) |

## R1 · Integración y redacción

- **Entrada:** `estado-cuestion.md`, fichas, documentos propios del usuario (borradores, datos,
  notas), y un *brief*: objetivos, hipótesis, metodología, tipo de artículo (empírico, revisión,
  ensayo teórico…), extensión.
- **Proceso:** esquema → aprobación del usuario → redacción por secciones.
- **Regla de citación en borrador:** el redactor **no escribe referencias**; inserta claves
  `[@clave, p. 45]` que existen en `biblioteca.json`. Si necesita una fuente que no está, escribe
  `[FUENTE PENDIENTE: descripción]`.

## R2 · Adaptación a revista/editorial

- Ficha de revista en `estilos/revistas/<revista>.yaml`: extensión, estructura (IMRyD u otra),
  resumen, palabras clave, estilo CSL, idioma, anonimización, normas específicas.
- El formato de citas y bibliografía lo produce **Pandoc + citeproc** con el CSL correspondiente,
  no el modelo.
- Salida en Markdown y `.docx` (plantilla de la revista si existe).

## R3 · Cita literal con página

- Toda cita textual del borrador se compara con el texto extraído del documento fuente
  (coincidencia exacta tras normalizar espacios, guiones y comillas; tolerancia configurable para
  OCR).
- La página se toma del **mapa de páginas impresas**, no de la numeración del PDF.
- Si no se encuentra: la cita se marca como FALLO y no puede quedar en la versión final.

## R4 · Integridad de referencias

Ver el diseño completo en `05-verificacion-citas.md`.
