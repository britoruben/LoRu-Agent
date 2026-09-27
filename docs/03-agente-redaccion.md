# 03 · Flujo de redacción: del estado de la cuestión al artículo

> **En pocas palabras:** con el estado de la cuestión, tus propios materiales y tus objetivos, el
> sistema propone un esquema. Cuando lo apruebas, redacta el artículo sección a sección siguiendo
> las normas de la revista que elijas. La IA nunca escribe una referencia por su cuenta: solo puede
> usar obras de la "estantería" verificada del proyecto. Antes de terminar, un verificador comprueba
> cada cita contra el texto original.

Las tareas se numeran **R1 a R4** ("R" de redacción).

| Paso | Tarea | Quién la hace | Estado del diseño |
|---|---|---|---|
| R1 | Escribir integrando el estado de la cuestión y tus materiales | IA + tú | Definido |
| R2 | Adaptar a las normas de la revista o editorial | Programas + IA | Definido |
| R3 | Citas literales con su página | Programas + IA | Definido |
| R4 | Evitar citas inventadas o mal formateadas | Programas | Definido (es la pieza clave) |

---

## R1 · Escribir el artículo

**Qué necesita de ti:** además del estado de la cuestión, tus propios materiales (borradores,
notas, datos) y unas indicaciones básicas: objetivos, hipótesis o tesis, metodología, tipo de
artículo (empírico, revisión, ensayo teórico…) y extensión.

**Cómo trabaja:**

1. El redactor propone un **esquema**: estructura, argumento central y qué obras se usan en cada
   sección.
2. **Punto de control 3:** apruebas o corriges el esquema. Sin tu aprobación no empieza a escribir.
3. Redacta **sección a sección**. Después de cada una te la enseña, junto con la comprobación de
   sus citas. Puedes intervenir o dejarle continuar.
4. Junta el artículo completo y lo prepara para la revista (R2–R4).
5. **Punto de control 4:** revisas la versión final.

**Cómo cita el redactor.** Nunca escribe una referencia completa. Pone una "etiqueta" que remite a
una obra de la estantería del proyecto, por ejemplo `[@arendt1958, p. 45]`. Después, un programa
convierte esas etiquetas en citas con el formato correcto. Si necesita una obra que no está en la
estantería, escribe `[FUENTE PENDIENTE: descripción]` para que tú decidas.

## R2 · Adaptar a la revista o editorial

**De dónde salen las normas.** Tú aportas la guía oficial para autores de la revista (en PDF o con
su enlace). El sistema la resume en una **ficha de revista** que tú compruebas. La ficha se guarda
y sirve para futuros artículos en esa revista. Si la guía tiene más de un año, el sistema avisa de
que puede estar desactualizada.

**Qué recoge la ficha de revista:** extensión, estructura obligatoria, resumen y palabras clave,
estilo de cita, idioma, anonimización para la revisión ciega, normas de figuras y tablas,
declaraciones exigidas (financiación, ética, conflicto de intereses y **uso de IA**) y normas
específicas.

**Uso de IA:** muchas revistas exigen declarar si se ha usado IA en la redacción. La ficha recoge
la política de cada revista y el borrador incluirá la declaración correspondiente.

**Formato y entrega:**

- El **formato de las citas y de la bibliografía** (APA, Chicago, Vancouver…) lo aplica un
  programa, no la IA, así que es siempre correcto.
- El artículo se entrega en **Word** y en **PDF (LaTeX)**, usando la plantilla de la revista si la
  tiene.
- Se escribe en el idioma de la revista (español o inglés).

**Detalle técnico:** ficha en `estilos/revistas/<revista>.yaml` con la fuente y la fecha de la
guía. Formato de citas con Pandoc + citeproc y el estilo CSL de la revista. El texto de trabajo
está en Markdown y se exporta con Pandoc a `.docx` (plantilla de referencia) y a LaTeX/PDF (clase
de la revista).

## R3 · Citas literales con su página

- Cada cita textual del borrador se busca **palabra por palabra** en el texto del documento
  original. Se toleran diferencias menores como espacios, guiones o tipos de comillas, y algo más
  si el documento es un escaneo.
- La página se toma de la **página impresa**, no de la numeración del PDF.
- Si la cita no aparece, se marca como **fallo** y no puede quedar en la versión final.

## R4 · Evitar citas inventadas

Es la parte más importante del sistema y se explica con detalle en
[05 · Verificación de citas](05-verificacion-citas.md).

Un caso especial son las **paráfrasis** (cuando se atribuye una idea a un autor sin citarlo
literalmente). No se pueden comprobar al cien por cien de forma automática. El verificador busca
en el texto original el pasaje que probablemente corresponde, lo pone al lado de la paráfrasis y
**tú confirmas** si es fiel.

## El revisor (octavo ayudante, fase 8)

Más adelante se añadirá un ayudante que lee el borrador como lo haría el revisor de la revista:
originalidad respecto al estado de la cuestión, coherencia del argumento, adecuación del método,
cumplimiento de las normas y objeciones previsibles. Entrega un informe **y no toca el borrador**.
