# LoRu-Agent

Asistente de investigación basado en **Claude** para dos tareas:

1. **Revisión bibliográfica:** buscar lo publicado sobre un tema, elegir lo importante, conseguir
   los textos por vías legales, leerlos, seguir sus referencias y redactar un **estado de la
   cuestión** con sus consensos, disputas, errores y vacíos.
2. **Redacción de artículos:** escribir a partir de ese estado de la cuestión y de tus materiales,
   según las normas de la revista elegida y **comprobando que cada cita es real y exacta**.

> **Estado actual:** diseño casi terminado y **primer prototipo del verificador de citas**
> funcionando, con un proyecto de ejemplo. Ver [qué se puede probar ya](ejemplos/LEEME.md) y
> el [plan por fases](docs/06-plan-por-fases.md).

## Por dónde empezar

1. **[Guía: qué es y cómo funciona](docs/guia.md)**, escrita para cualquier lector, sin
   conocimientos técnicos.
2. **[Glosario](docs/glosario.md)**: todas las palabras técnicas explicadas.
3. **[Instalación](docs/instalacion.md)**: cómo tenerlo en tu ordenador.
4. **[Ejemplos](ejemplos/LEEME.md)**: lo que ya funciona, con un borrador lleno de errores a
   propósito y el informe del verificador.
5. **[Preguntas abiertas](docs/07-preguntas-abiertas.md)**: lo que falta por decidir.

## Toda la documentación

Cada documento empieza con un recuadro **"En pocas palabras"**. Las secciones marcadas
**"Detalle técnico"** son para quien programe y se pueden saltar.

| Documento | De qué trata |
|---|---|
| [Guía](docs/guia.md) | Qué es, cómo se usa y por qué te puedes fiar de las citas |
| [Glosario](docs/glosario.md) | Palabras técnicas explicadas |
| [00 · Visión](docs/00-vision.md) | Qué perseguimos, qué no y los cuatro momentos en que el sistema te consulta |
| [01 · Arquitectura](docs/01-arquitectura.md) | Cómo encajan las piezas y dónde se guarda el trabajo |
| [02 · Flujo bibliográfico](docs/02-agente-bibliografico.md) | De la pregunta al estado de la cuestión, paso a paso |
| [03 · Flujo de redacción](docs/03-agente-redaccion.md) | Del estado de la cuestión al artículo |
| [04 · Fuentes](docs/04-fuentes-y-acceso.md) | Dónde se buscan las publicaciones y cómo se accede a ellas |
| [05 · Verificación de citas](docs/05-verificacion-citas.md) | Cómo se evita que la IA invente citas |
| [06 · Plan por fases](docs/06-plan-por-fases.md) | En qué orden se construye |
| [07 · Preguntas abiertas](docs/07-preguntas-abiertas.md) | Lo que falta por decidir |
| [Decisiones](docs/decisiones/) | Qué se ha decidido y por qué |

## Equipo

Rubén y Lola.
