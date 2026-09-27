# 06 · Plan por fases: en qué orden se construye

> **En pocas palabras:** el sistema se construye en 9 fases (de la 0 a la 8). Cada fase termina con
> algo que ya funciona y que se puede probar. Primero se construye el **verificador de citas**,
> porque es lo que da confianza a todo lo demás. Después, la búsqueda, la lectura, la bola de nieve
> y la redacción. Las bases de datos de pago y el revisor van al final.

Reglas del plan:

- **Cada fase termina con algo usable** y con una prueba clara de que funciona (columna "Cómo
  sabremos que está bien").
- **No se empieza una fase** mientras sigan sin responder las preguntas que la bloquean (ver
  [07 · Preguntas abiertas](07-preguntas-abiertas.md)).

| Fase | Qué se consigue | Qué se construye | Cómo sabremos que está bien | Necesita antes |
|---|---|---|---|---|
| **0 · Diseño** *(casi terminada)* | Saber qué vamos a construir | Esta documentación | Rubén y Lola aprueban el diseño | — |
| **1 · Cimientos** | Poder crear un proyecto y su estantería | Estructura del programa, ficha de proyecto, conexión con el gestor bibliográfico, guía de instalación | Se crea un proyecto y se añaden 10 referencias comprobadas | P-01 |
| **2 · Verificador** *(prototipo en marcha, decisión 0006)* | Comprobar citas de forma fiable | Verificador de citas y extracción de texto con páginas impresas, con una colección de "citas trampa" para probarlo (DOI falso, cita alterada, página equivocada) | Detecta **todas** las citas trampa | Fase 1 |
| **3 · Búsqueda** | Encontrar y ordenar lo publicado en abierto | Conexión con los catálogos abiertos, cálculo de importancia, comando `/buscar` | Con una pregunta real, la investigadora considera útil la lista | Fase 1, P-05 |
| **4 · Lectura y síntesis** | Primer estado de la cuestión | Ayudantes lector (dos niveles) y sintetizador, comando `/estado-cuestion`; resumen, informe y tablas | Estado de la cuestión en el proyecto piloto con cada afirmación rastreable hasta obra y página | Fase 3 |
| **5 · Bola de nieve** | Encontrar lo que la búsqueda no encontró | Red de citas, rondas con límites, mapa visual | Aparecen obras relevantes que la búsqueda inicial no había encontrado | Fase 4 |
| **6 · Redacción** | Borrador de artículo | Ayudante redactor (por secciones), fichas de revista a partir de sus guías, exportación a Word y PDF, comprobación automática antes de exportar | Un borrador completo con **cero** fallos de verificación | Fases 2 y 4 |
| **7 · Bases de pago** | Usar las suscripciones de la institución | Conexión oficial (API) o descarga guiada, según lo que se decida | Lo que se fije al decidir P-03 | P-03 |
| **8 · Revisor** | Evaluación previa tipo revista | Ayudante revisor | Sus objeciones coinciden en lo esencial con las de un revisor humano en un caso de prueba | Fase 6 |

## Estado de la fase 2 (prototipo)

| Parte | Estado |
|---|---|
| Verificar que las obras están en la estantería y comprobadas | Hecho |
| Citas literales: texto exacto, omisiones, página, citas entre dos páginas | Hecho |
| Avisos: comillas sin fuente, citas en formato no reconocido, textos escaneados | Hecho |
| Comprobar DOI en Crossref | Hecho, probado solo con respuestas simuladas |
| Comando `/verificar-citas` y ayudante `verificador` en Claude Code | Hecho |
| Extraer texto y páginas impresas de PDF reales | **Pendiente** |
| Comprobación asistida de paráfrasis | **Pendiente** |
| Comprobación automática antes de exportar (*hook*) | **Pendiente** (llega con la fase 6) |

Ver [ejemplos](../ejemplos/LEEME.md).

## Por qué el verificador va tan pronto

Es la pieza que hace fiable todo lo demás y se puede probar sola, sin esperar a que exista la
búsqueda o la redacción. Si falla, el resto del sistema no sirve para un uso académico.

## El proyecto piloto

Para comprobar que las fases 3 a 6 funcionan de verdad hace falta **una pregunta de investigación
real y acotada** (pregunta P-05). Conviene empezar por **una sola disciplina** y ampliar después:
probar en todas a la vez multiplica el trabajo y hace difícil saber qué falla.
