# 05 · Verificación de citas: cómo se evita que la IA invente

> **En pocas palabras:** la IA **no escribe referencias**. Solo puede señalar obras de una
> "estantería" en la que cada libro o artículo ha entrado después de comprobar que existe. Un
> programa da formato a las citas y otro programa, el verificador, compara cada cita literal con el
> texto original y comprueba la página. Si algo no cuadra, el artículo no se puede dar por
> terminado. Es la pieza que hace fiable todo el sistema.

## La idea, con una analogía

Piensa en un corrector editorial muy estricto que tiene sobre la mesa todos los libros citados.
Por cada cita del manuscrito, abre el libro por la página indicada y comprueba que el texto está
ahí, tal cual. Si una obra citada no está sobre la mesa, la cita no pasa. Eso es lo que hace este
sistema, de forma automática.

## Las cuatro protecciones

### 1. La estantería del proyecto (biblioteca verificada)

Una obra solo entra en la estantería si se ha comprobado que existe:

- Si tiene **DOI** (el "DNI" de una publicación), se consulta el registro oficial (Crossref) y se
  comprueba que el título, el año y el primer autor coinciden.
- Si **no tiene DOI** (muchos libros, capítulos y obras antiguas), se comprueba por su **ISBN** o
  en catálogos de bibliotecas, o la añades tú a mano. En ese caso queda anotado que la comprobación
  fue manual.

De cada obra se anota además cómo y cuándo se comprobó, dónde está su PDF y qué versión es
(borrador previo, aceptada o publicada).

### 2. El mapa de páginas

La página 1 del PDF no suele ser la página 1 del libro o de la revista. Al extraer el texto de un
PDF, el sistema anota para cada página del PDF qué **página impresa** le corresponde. Para
averiguarlo:

1. mira si el propio PDF trae esa información;
2. si no, busca el número de página impreso en la cabecera o el pie;
3. si tampoco, te pregunta la correspondencia (por ejemplo, "la página 1 del PDF es la 45").

Si no se puede determinar, las citas de ese documento se marcan para revisarlas a mano.

### 3. El formato lo pone un programa

La IA solo escribe una etiqueta (por ejemplo `[@arendt1958, p. 45]`). Un programa la convierte en
la cita con el estilo que toque (APA, Chicago…) y compone la bibliografía final. Así **no puede
haber errores de formato ni DOI mal copiados**.

### 4. El verificador

Antes de dar un borrador por terminado, un programa revisa:

| Qué comprueba | Si falla |
|---|---|
| Que cada obra citada está en la estantería | **Fallo:** obra inexistente |
| Que el DOI de cada obra sigue funcionando | Aviso |
| Que cada cita literal aparece en el texto original | **Fallo:** cita no encontrada |
| Que aparece en la página indicada | **Fallo:** página incorrecta (y propone la correcta) |
| Paráfrasis (ideas atribuidas sin cita literal) | **Comprobación asistida:** busca en el original el pasaje que probablemente corresponde y te lo muestra al lado para que confirmes. Si no lo encuentra, aviso destacado |
| Que no quedan huecos `[FUENTE PENDIENTE]` | **Bloquea** la versión final |

El resultado es un informe con todas las incidencias, que ves en el **punto de control 4**.

El verificador **solo puede leer** el borrador, nunca modificarlo, y se ejecuta **automáticamente**
antes de exportar: si hay fallos, no se puede exportar.

## Límites, con honestidad

- Comprobar que una **paráfrasis** es fiel al autor no se puede automatizar del todo: el sistema
  ayuda, pero la última palabra es tuya.
- Con **libros escaneados** de mala calidad, una cita correcta puede no encontrarse porque el
  reconocimiento de texto (OCR) cometió errores. Esas citas se señalan para revisión manual.

## Detalle técnico

- La estantería es `biblioteca.json` en formato CSL-JSON, con campos adicionales: `verificacion`
  (doi | isbn | manual), `fecha_verificacion`, `pdf_local`, `texto_local` y `version` (preprint |
  aceptada | publicada).
- El mapa de páginas se guarda en `texto/<id>.json`:
  `{"paginas": [{"pdf": 1, "impresa": "45", "texto": "..."}], "calidad": "ok|ocr"}`. Primero se
  intentan las etiquetas de página del PDF, luego la detección en cabecera o pie y por último el
  desfase indicado por la persona usuaria.
- Cita literal: coincidencia exacta tras normalizar espacios, guiones y comillas; con tolerancia
  configurable para textos de OCR.
- Paráfrasis: búsqueda semántica (*embeddings*) en el texto de la fuente; el modelo concreto se
  elige en la fase 2.
- Informe en `borradores/<nombre>.verificacion.md`.
- El subagente `verificador` no tiene permiso de escritura; un *hook* de Claude Code ejecuta el
  verificador antes de exportar y bloquea la exportación si hay fallos.
