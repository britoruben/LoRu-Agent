# Glosario

Palabras técnicas que aparecen en la documentación, explicadas sin dar nada por supuesto.
Ordenadas alfabéticamente.

---

**Acceso abierto (OA, *open access*)** — Publicaciones que se pueden leer y descargar gratis y
legalmente. Muchos artículos de pago tienen también una versión en acceso abierto (por ejemplo, la
que el autor deposita en el repositorio de su universidad).

**API** — Una "ventanilla" por la que un programa pide datos a otro servicio. Por ejemplo, en vez
de que una persona entre en la web de un catálogo y busque a mano, el programa hace la pregunta
por la API y recibe la respuesta ordenada. Muchas bases de datos ofrecen una API; algunas exigen
una **clave de API**, que funciona como una contraseña personal para usarla.

**Archivo `.env`** — Un archivo de texto en tu ordenador donde se guardan contraseñas y claves.
Nunca se comparte ni se sube a internet.

**Bola de nieve (*snowballing*)** — Técnica de revisión bibliográfica: a partir de las obras que ya
tienes, miras qué obras citan ellas (hacia atrás) y qué obras las citan a ellas (hacia delante).
Así aparecen obras importantes que la búsqueda inicial no encontró.

**Biblioteca verificada / estantería del proyecto** — La lista de obras que el sistema tiene
permitido citar. Una obra solo entra si se ha comprobado que existe. Técnicamente es un archivo en
formato *CSL-JSON* (ver abajo).

**Carpeta de datos (`LORU_DATOS`)** — La carpeta de tu ordenador donde se guardan los PDF, fichas y
borradores de cada investigación. Está separada de la carpeta del programa. En Claude Code en la
web es `Investigacion/`, dentro de la sesión, y es **temporal**: se borra al cerrar la sesión.

**Claude Code** — La versión de Claude que puede leer y crear archivos y ejecutar programas.
Se usa de dos formas: **en la web** (claude.ai/code), donde trabaja sobre una copia del proyecto
en la nube y basta con el navegador, o **en tu ordenador**, escribiendo `claude` en la terminal.
Ahora el equipo usa la versión web.

**Código / script** — Instrucciones escritas para que el ordenador haga una tarea. Un *script* es un
programa pequeño que hace una sola cosa (por ejemplo, "extraer el texto de un PDF").

**Comando (`/algo`)** — Una orden que se escribe en la conversación con Claude Code empezando por
barra, como `/verify-citations`. Pone en marcha un proceso ya preparado. En la documentación técnica
se llaman *skills*.

**CSL / citeproc / Pandoc** — Herramientas que dan formato a las citas y a la bibliografía.
*CSL* es un catálogo de miles de estilos de cita (APA, Chicago, Vancouver…); *citeproc* aplica el
estilo; *Pandoc* convierte el texto a Word, PDF o LaTeX. Lo importante: **el formato lo pone un
programa, no la IA**, y por eso no tiene errores.

**CSV** — Una tabla guardada como texto. Se abre con Excel, LibreOffice o Google Sheets.

**Determinista** — Que siempre da el mismo resultado con los mismos datos, como una calculadora.
Lo contrario de la IA, que puede responder distinto cada vez. En este proyecto, todo lo que se
puede comprobar se hace de forma determinista.

**DOI** — Un identificador único y permanente de una publicación, como un DNI. Por ejemplo
`10.1000/xyz123`. Sirve para comprobar que una obra existe y cuáles son sus datos exactos.

**Embeddings / búsqueda semántica** — Técnica que permite buscar un texto **por su significado** y
no solo por sus palabras exactas. Se usará para localizar en el original el pasaje que corresponde
a una paráfrasis.

**Entorno virtual (`.venv`)** — Una carpeta donde se instalan los paquetes de Python que necesita
este proyecto, separados del resto del ordenador. Así no se estropea nada fuera del proyecto.

**Estado de la cuestión** — Informe sobre qué se sabe de un tema: posiciones, consensos, disputas,
errores y preguntas sin responder.

**GitHub Actions** — Un servicio de GitHub que ejecuta las pruebas automáticas cada vez que se
suben cambios, en Windows, macOS y Linux. Si alguna falla, el cambio aparece marcado en rojo.

**Git / repositorio (repo)** — Git es un sistema que guarda el historial de cambios de un conjunto
de archivos, como el "control de cambios" de Word pero para una carpeta entera. Un *repositorio* es
esa carpeta con su historial. Este proyecto vive en un repositorio en GitHub (una web que los
aloja).

**Grafo / red de citas** — Un dibujo de puntos y flechas: cada punto es una obra y cada flecha
significa "esta obra cita a aquella". Permite ver qué obras son centrales en un debate.

**Centralidad** — En la red de citas, cuánto se cita una obra **dentro del propio tema** estudiado.
Suele indicar mejor su importancia que el número total de citas.

**Hook (guardarraíl)** — Una comprobación automática que se ejecuta en un momento concreto, por
ejemplo "antes de exportar el artículo, pasa el verificador". Si falla, impide continuar.

**LLM / modelo de IA** — El tipo de inteligencia artificial que es Claude: un programa que lee y
escribe texto. En la documentación decimos "el modelo" o "la IA".

**MCP** — Un "enchufe" estándar para conectar Claude con otros programas o servicios (por ejemplo,
con un gestor bibliográfico como Zotero). Un *servidor MCP* es el adaptador que hace esa conexión.

**OCR** — Reconocimiento de texto en imágenes. Hace falta cuando un PDF es un libro escaneado (una
foto de cada página) y no contiene texto que se pueda copiar. Puede cometer errores.

**Markdown (`.md`)** — Texto con formato muy sencillo: `# Título`, `**negrita**`, `> cita`.
Se abre con cualquier editor de texto y GitHub lo muestra con formato.

**Paquete / dependencia** — Un programa ya hecho por otras personas que este proyecto usa, como
`pypdf` para leer PDF. Se instalan con la lista de `requirements.txt`.

**Página impresa vs. página del PDF** — La página 1 del PDF puede ser la página 45 del libro o de la
revista. Para citar hay que usar siempre la **página impresa**.

**Perfil disciplinar (`proyecto.yaml`)** — Una ficha con la configuración de cada investigación:
pregunta, disciplina, idiomas, periodo, dónde buscar, estilo de cita, límites. Permite que el mismo
sistema sirva para filosofía o para medicina.

**Prueba automática (*test*)** — Un caso preparado de antemano con la respuesta correcta
conocida ("esta cita tiene la página equivocada: el programa debe detectarlo"). Se ejecutan todas
a la vez en segundos; si alguna falla, algo se ha estropeado. Están en la carpeta `tests/`.

**Punto de control** — Momento en que el sistema se detiene y te pide que apruebes algo antes de
seguir. Hay cuatro (ver la [guía](guia.md)).

**Registro de decisiones (ADR)** — Una nota breve que explica una decisión importante del proyecto:
qué se decidió, qué alternativas había y por qué. Están en `docs/decisions/`. "ADR" son las
siglas en inglés de *Architecture Decision Record*.

**Sesión** — Una conversación con Claude Code. En la web, cada sesión trabaja en una copia del
proyecto preparada para ella; lo que no se guarda en GitHub o no descargas se pierde al cerrarla.

**Subagente** — Una copia de Claude a la que se encarga una única tarea con instrucciones
concretas (leer un documento, verificar citas…). Es cada uno de los "ayudantes" del equipo.

**Terminal** — Una ventana donde se escriben órdenes al ordenador en texto, en lugar de usar el
ratón. Claude Code se abre desde ahí.

**Versión (preprint / aceptada / publicada)** — Un artículo puede existir en varias versiones: el
*preprint* (antes de la revisión), la aceptada (tras la revisión, sin maquetar) y la publicada
(la de la revista). **Solo la publicada tiene la paginación correcta para citar.**

**YAML / JSON** — Formatos para guardar información ordenada en un archivo de texto, legibles
tanto por personas como por programas. Ejemplo de YAML: `idiomas: [es, en]`.

**Zotero** — Un gestor bibliográfico gratuito: guarda tus referencias y PDF y da formato a las
citas. Es el candidato recomendado para este proyecto.
