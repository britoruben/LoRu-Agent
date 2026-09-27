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
- **Proceso:**
  1. El `redactor` propone esquema, argumento central y asignación de fuentes por sección →
     **PC-3** (aprobación obligatoria).
  2. Redacta **sección a sección**. Tras cada sección muestra el texto y un informe breve de
     verificación de esa sección; el usuario puede intervenir o dejarle continuar (no es un punto
     de control obligatorio).
  3. Ensambla el borrador completo y pasa a R2–R4 → **PC-4**.
- **Regla de citación en borrador:** el redactor **no escribe referencias**; inserta claves
  `[@clave, p. 45]` que existen en `biblioteca.json`. Si necesita una fuente que no está, escribe
  `[FUENTE PENDIENTE: descripción]`.

## R2 · Adaptación a revista/editorial

- **Origen de las normas:** el usuario aporta la guía oficial para autores (PDF o URL). El agente
  la convierte en una ficha `estilos/revistas/<revista>.yaml` que **el usuario valida**; la ficha
  guarda la fuente y la fecha de la guía, y se reutiliza en futuros artículos. Si la guía tiene
  más de 12 meses, el agente avisa de que puede estar desactualizada.
- Contenido de la ficha: extensión, estructura (IMRyD u otra), resumen, palabras clave, estilo CSL,
  idioma, anonimización, normas de figuras/tablas, declaraciones exigidas (financiación, ética,
  conflicto de intereses, uso de IA), normas específicas.
- El formato de citas y bibliografía lo produce **Pandoc + citeproc** con el CSL correspondiente,
  no el modelo.
- Fuente de trabajo en **Markdown**; exportación con Pandoc a **`.docx`** (plantilla de referencia de la
  revista si existe) y a **LaTeX/PDF** (clase/plantilla de la revista si existe).
- Idioma de redacción: el de la revista objetivo (español o inglés).

## R3 · Cita literal con página

- Toda cita textual del borrador se compara con el texto extraído del documento fuente
  (coincidencia exacta tras normalizar espacios, guiones y comillas; tolerancia configurable para
  OCR).
- La página se toma del **mapa de páginas impresas**, no de la numeración del PDF.
- Si no se encuentra: la cita se marca como FALLO y no puede quedar en la versión final.

## R4 · Integridad de referencias

Ver el diseño completo en `05-verificacion-citas.md`. Las paráfrasis se tratan con
**verificación asistida**: el verificador localiza el pasaje fuente más probable y lo muestra
junto a la paráfrasis para que el usuario confirme.

## Revisor (8.º subagente — fase 8)

Tras la fase 6 se añadirá un subagente `revisor` que evalúa el borrador como un revisor de la
revista objetivo: originalidad frente al estado de la cuestión, coherencia argumental, adecuación
metodológica, cumplimiento de la ficha de revista y posibles objeciones. Produce un informe tipo
*peer review*; **no edita** el borrador.

Nota: muchas revistas exigen declarar el uso de IA en la redacción. La ficha de revista debe
recoger esa política y el borrador incluir la declaración correspondiente.
