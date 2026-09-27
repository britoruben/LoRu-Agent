# 02 · Flujo bibliográfico: de la pregunta al estado de la cuestión

> **En pocas palabras:** a partir de tu pregunta, el sistema busca lo publicado en español e
> inglés, lo ordena por importancia explicando el motivo, consigue los textos por vías legales, los
> lee (unos por encima y los más importantes a fondo), sigue sus bibliografías para encontrar obras
> que faltan y redacta un estado de la cuestión con consensos, disputas, errores y vacíos. Te
> consulta antes de buscar y cada vez que hay que decidir qué obras entran.

Las tareas se numeran **B1 a B7** ("B" de bibliográfico) y corresponden a las siete tareas de la
idea original.

| Paso | Tarea | Quién la hace | Estado del diseño |
|---|---|---|---|
| B1 | Buscar en catálogos abiertos | Programas | Definido |
| B2 | Buscar en bases de datos privadas | Programas | **Pendiente** (pregunta P-03) |
| B3 | Ordenar por importancia y elegir | Programas + IA + tú | Definido (a ajustar con el proyecto piloto) |
| B4 | Conseguir los textos | Programas | Parcial (depende de B2) |
| B5 | Leer y hacer fichas | IA | Definido |
| B6 | Seguir las referencias (bola de nieve) | Programas + IA | Definido |
| B7 | Escribir el estado de la cuestión | IA | Definido |

---

## B1 · Buscar en catálogos abiertos

1. La IA convierte tu pregunta en **palabras de búsqueda**, con sinónimos y traducción al inglés.
2. **Punto de control 1:** te las enseña y tú las apruebas o corriges.
3. Los programas buscan en los catálogos elegidos en la ficha del proyecto (ver
   [04 · Fuentes](04-fuentes-y-acceso.md)).
4. Se juntan los resultados y **se eliminan los duplicados** (la misma obra encontrada en varios
   catálogos).
5. Resultado: una **tabla de obras candidatas** (`candidatos.csv`), que se abre con Excel.

**Detalle técnico:** consultas por fuente vía API; normalización a un esquema común; eliminación de
duplicados por DOI → PMID → título normalizado + año. Columnas: id, título, autores, año, tipo, DOI,
fuente(s), citas, acceso abierto sí/no, URL.

## B2 · Buscar en bases de datos privadas — pendiente

Depende de cómo se acceda a las bases de datos de la institución (pregunta P-03). Hay dos caminos:

- **Si la base de datos ofrece una API oficial** (una "ventanilla" para programas, como la de
  Scopus o Web of Science): se conecta igual que los catálogos abiertos.
- **Si solo se puede entrar por la web con usuario de la universidad:** el sistema **no** intentará
  entrar ni descargar solo, porque las licencias suelen prohibirlo y podrían cortar el acceso a
  toda la institución. En su lugar, prepara una lista ordenada con enlaces y tú descargas los
  documentos en la carpeta `pdf/` del proyecto.

## B3 · Ordenar por importancia y elegir

"El más citado" no basta como criterio: favorece a las obras antiguas (han tenido más tiempo para
acumular citas), los recuentos cambian según el catálogo y muchos libros, sobre todo de
humanidades, apenas aparecen. Por eso la importancia se calcula combinando cinco señales:

| Señal | Qué mide | Por qué |
|---|---|---|
| Citas totales | Cuánto se ha citado en general | Impacto acumulado |
| Citas por año | Citas divididas por los años desde su publicación | Para no enterrar lo reciente |
| Peso dentro del tema | Cuánto la citan **las demás obras del propio tema** | Suele ser la señal más fiable; solo está disponible tras la bola de nieve (B6) |
| Pertinencia | Cuánto se ajusta a tu pregunta, según la IA tras leer título y resumen | Filtra lo que no viene al caso |
| Actualidad | Cuán reciente es | Para reflejar el debate actual (pesa poco) |

Cada obra de la lista lleva **una frase que explica por qué está donde está**, por ejemplo: "Muy
citada por las demás obras del tema (12 de 40) y trata directamente la cuestión X". Una puntuación
sin explicación no se muestra.

**Punto de control 2:** revisas la tabla y decides qué obras entran en el estudio. Esa decisión se
guarda en `seleccion.csv`.

**Detalle técnico:** pesos por defecto, a calibrar con el proyecto piloto: citas 0,2 · citas/año
0,25 · centralidad 0,25 · pertinencia 0,25 · recencia 0,05. En la primera búsqueda, cuando todavía
no hay red de citas, el peso de la centralidad se reparte entre las demás señales. En la tabla se
muestra la puntuación de cada señal por separado y el motivo.

## B4 · Conseguir los textos

Se intenta, por este orden:

1. La **versión en acceso abierto** (gratuita y legal), si existe.
2. Repositorios abiertos de universidades y de disciplinas (arXiv, PubMed Central, CORE…).
3. El acceso privado de la institución, según se decida en B2.
4. Si no se consigue: se apunta en una **lista de "no disponibles"** para gestionarla a mano
   (préstamo interbibliotecario, pedírsela al autor…).

De cada documento se anota de dónde viene y **qué versión es**. Un artículo puede existir como
borrador previo a la revisión (*preprint*), versión aceptada o versión publicada, y **solo la
publicada tiene la paginación correcta para citar**.

## B5 · Leer y hacer fichas

Cada documento lo lee un ayudante lector, que rellena una **ficha de lectura**. Hay dos niveles:

| Nivel | Qué documentos | Qué se lee | Qué contiene la ficha |
|---|---|---|---|
| **Lectura ligera** | Todos los elegidos | Resumen, introducción y conclusiones | Tesis, método, hallazgos principales, conceptos y postura |
| **Lectura completa** | Los 40 más importantes (ajustable) y los que tú marques | Todo el texto | Todo lo anterior y además citas textuales con su página, con quién discute, limitaciones… |

Si durante la síntesis se ve que un documento de lectura ligera es clave en una disputa, pasa a
lectura completa.

Todas las páginas que aparecen en una ficha **se comprueban** contra el texto del documento (ver
[05](05-verificacion-citas.md)).

**Detalle técnico:** formato de la ficha completa (`fichas/<id>.yaml`):

```yaml
id: doi:10.xxxx/yyyy
nivel: completo                      # ligero | completo
tesis_principal: "..."
preguntas: [...]
metodologia: "..."
datos_o_corpus: "..."
hallazgos: [{afirmacion: "...", pagina: 12}]
conceptos_clave: [...]
posiciona_contra: [{id: ..., en_que: "..."}]
posiciona_a_favor: [{id: ..., en_que: "..."}]
limitaciones_declaradas: [...]
limitaciones_detectadas: [...]
citas_textuales_relevantes: [{texto: "...", pagina_impresa: 45}]
calidad_extraccion: ok               # ok | ocr | parcial
```

## B6 · Seguir las referencias ("bola de nieve")

La idea es la misma que cuando, leyendo un buen artículo, apuntas las obras que cita:

- **Hacia atrás:** qué obras citan los documentos que ya tenemos.
- **Hacia delante:** qué obras posteriores citan a esos documentos.

Si una obra aparece citada por muchos documentos del tema y no estaba en nuestra lista, se propone
como nueva candidata. Con todas estas relaciones se construye la **red de citas** (quién cita a
quién), que sirve para calcular el "peso dentro del tema" de B3 y para dibujar el mapa visual.

**Cuándo se para.** Sin límites, la bola de nieve crecería sin fin. Por defecto se usa el modo
**moderado**:

- como máximo **2 rondas**;
- como máximo **30 obras nuevas por ronda**;
- se para antes si una ronda aporta **menos de 3** obras relevantes (señal de que el tema está
  "saturado").

Hay otros dos modos, que se eligen en la ficha del proyecto: **ligero** (1 ronda, solo hacia atrás)
y **exhaustivo** (hasta 5 rondas, para revisiones sistemáticas).

Cada ronda pasa otra vez por el **punto de control 2**: tú decides qué obras nuevas entran.

**Detalle técnico:** referencias obtenidas preferentemente de los metadatos de OpenAlex/Crossref;
como alternativa, extracción de la bibliografía del propio PDF (herramienta a evaluar, p. ej.
GROBID; pregunta P-09). La red se guarda en `grafo.json`.

## B7 · El estado de la cuestión

Se generan cuatro productos, todos a partir de las mismas fichas de lectura:

| Producto | Qué es | Cuándo estará |
|---|---|---|
| **Resumen de una página** | Cómo está el debate, 5 obras clave, principales disputas y vacíos, y una recomendación | Fase 4 |
| **Informe completo** (texto y Word) | El estado de la cuestión en prosa académica (estructura abajo) | Fase 4 |
| **Tablas de síntesis** | Qué dice cada obra: postura, método y hallazgos; tabla de disputas y de vacíos | Fase 4 |
| **Mapa visual** | Dibujo interactivo de la red de citas, coloreado por escuela o postura; se abre en el navegador | Fase 5 (necesita la red de citas de B6) |

Estructura del informe completo:

1. **Mapa del campo:** líneas, escuelas o enfoques, con sus obras de referencia.
2. **Consensos:** en qué está de acuerdo la literatura.
3. **Disputas:** posiciones enfrentadas, quién sostiene qué, con cita y página.
4. **Errores:** afirmaciones refutadas o citas mal atribuidas en la literatura, con la prueba.
5. **Vacíos:** preguntas sin tratar; poblaciones, periodos o métodos ausentes.
6. **Tabla de trazabilidad:** cada afirmación del informe → obra → página.

**Advertencia:** los "errores" y "vacíos" que detecta la IA son **hipótesis que hay que revisar**,
no conclusiones. El informe lo indicará expresamente.
