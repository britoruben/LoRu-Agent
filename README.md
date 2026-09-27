# LoRu-Agent

Asistente de investigación basado en **Claude** para dos tareas:

1. **Revisión bibliográfica:** buscar lo publicado sobre un tema, elegir lo importante, conseguir
   los textos por vías legales, leerlos, seguir sus referencias y redactar un **estado de la
   cuestión** con sus consensos, disputas, errores y vacíos.
2. **Redacción de artículos:** escribir a partir de ese estado de la cuestión y de tus materiales,
   según las normas de la revista elegida y **comprobando que cada cita es real y exacta**.

> **Estado actual:** diseño casi terminado y **primer prototipo del verificador de citas**
> funcionando, con un proyecto de ejemplo. Ver [qué se puede probar ya](ejemplos/LEEME.md) y
> el [plan por fases](docs/06-phased-plan.md).

## Por dónde empezar

1. **[Guía: qué es y cómo funciona](docs/guia.md)**, escrita para cualquier lector, sin
   conocimientos técnicos.
2. **[Glosario](docs/glosario.md)**: todas las palabras técnicas explicadas.
3. **[Instalación](docs/instalacion.md)**: cómo tenerlo en tu ordenador.
4. **[Ejemplos](ejemplos/LEEME.md)**: lo que ya funciona, con un borrador lleno de errores a
   propósito y el informe del verificador.
5. **[Preguntas abiertas](docs/07-open-questions.md)**: lo que falta por decidir.

## Toda la documentación

Cada documento empieza con un recuadro **"En pocas palabras"**. Las secciones marcadas
**"Detalle técnico"** son para quien programe y se pueden saltar.
Los documentos técnicos (00 a 07 y decisiones) están en inglés; las guías, en español
(decisión 0008).

| Documento | De qué trata |
|---|---|
| [Guía](docs/guia.md) | Qué es, cómo se usa y por qué te puedes fiar de las citas |
| [Glosario](docs/glosario.md) | Palabras técnicas explicadas |
| [00 · Visión](docs/00-vision.md) | Qué perseguimos, qué no y los cuatro momentos en que el sistema te consulta |
| [01 · Arquitectura](docs/01-architecture.md) | Cómo encajan las piezas y dónde se guarda el trabajo |
| [02 · Flujo bibliográfico](docs/02-bibliographic-agent.md) | De la pregunta al estado de la cuestión, paso a paso |
| [03 · Flujo de redacción](docs/03-writing-agent.md) | Del estado de la cuestión al artículo |
| [04 · Fuentes](docs/04-sources-and-access.md) | Dónde se buscan las publicaciones y cómo se accede a ellas |
| [05 · Verificación de citas](docs/05-citation-verification.md) | Cómo se evita que la IA invente citas |
| [06 · Plan por fases](docs/06-phased-plan.md) | En qué orden se construye |
| [07 · Preguntas abiertas](docs/07-open-questions.md) | Lo que falta por decidir |
| [Decisiones](docs/decisions/) | Qué se ha decidido y por qué |

## In English

LoRu-Agent is a Claude-based research assistant for literature reviews and academic writing
that **never invents citations**: it can only cite works on a verified shelf, a program formats
the citations and a verifier checks every literal quote and page against the original text.
The core (code in `tools/`, tests, `.claude/`, `CLAUDE.md` and the technical documents
`docs/00`–`07` and `docs/decisions/`) is in English; guides for people and user-facing messages
are in Spanish (decision 0008). Status: design phase, with a working citation-verifier prototype.

## Equipo

Rubén y Lola.
