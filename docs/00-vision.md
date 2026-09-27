# 00 · Visión: qué perseguimos y qué no

> **En pocas palabras:** queremos un asistente que haga el trabajo mecánico de la investigación
> bibliográfica y de la redacción (buscar, cribar, conseguir textos, extraer, comprobar citas) sin
> el gran peligro de las IA: inventar referencias o citas. Las decisiones intelectuales siguen
> siendo de la persona que investiga.

## El problema

Revisar la bibliografía y redactar un artículo exige mucho trabajo mecánico: buscar en catálogos,
descartar lo que no sirve, conseguir los textos, tomar notas, comprobar citas y páginas… Las IA
pueden ayudar mucho, pero tienen un defecto grave: a veces **se inventan referencias** que no
existen, dan **identificadores de publicación (DOI) incorrectos** o **alteran citas literales**.
En un trabajo académico eso es inadmisible.

## El objetivo

Que al descargar este proyecto y abrirlo con Claude Code en tu ordenador tengas un equipo de
ayudantes capaz de:

- **Revisión bibliográfica:** pasar de una pregunta de investigación a un estado de la cuestión
  en el que cada afirmación remita a una obra y una página, con las disputas, errores y vacíos del
  debate.
- **Redacción:** pasar de ese estado de la cuestión y tus propios materiales a un borrador de
  artículo adaptado a una revista concreta, con **todas las citas comprobadas**.

## Para todas las disciplinas

Debe servir para humanidades, ciencias sociales, salud y biomedicina, e ingeniería e informática.
Como cada disciplina tiene sus catálogos, sus estilos de cita y su manera de valorar las obras,
nada de esto está fijado de antemano: se configura en la **ficha de cada proyecto** (ver
[01 · Arquitectura](01-arquitectura.md)).

## Lo que NO pretende

- **No** producir artículos publicables sin revisión humana. Es un asistente: la autoría y las
  decisiones intelectuales son de quien investiga.
- **No** saltarse licencias: nada de descargas masivas desde plataformas de pago ni de webs
  piratas.
- **No** usar el acceso de la universidad desde la nube: el acceso a bases de datos privadas solo
  funcionará en tu ordenador, con tus credenciales.

## Principios

1. **Programas para lo comprobable, IA para lo interpretativo.** Buscar, extraer texto, dar
   formato a las citas y verificarlas lo hacen programas, que siempre dan el mismo resultado. La
   IA lee, clasifica, resume y redacta.
2. **Las citas se protegen con el diseño, no con buenas intenciones.** No basta con pedirle a la
   IA que "no invente". El sistema debe impedir que una cita no comprobada llegue al texto final.
3. **Todo se puede rastrear.** Cada afirmación remite a una obra y una página.
4. **La persona decide en momentos fijos** (ver abajo). Entre ellos, el sistema trabaja solo.
5. **Siempre con límites.** Cada proceso tiene un máximo de documentos, de rondas y de uso, para
   no desbordarse.

## Los cuatro puntos de control (decisión 0004)

El sistema se detiene y espera tu aprobación solo en estos momentos:

| Punto | Cuándo | Qué decides | Pasos afectados |
|---|---|---|---|
| **1** | Antes de buscar | Las palabras de búsqueda, los catálogos, el periodo y los idiomas | B1–B2 |
| **2** | Después de ordenar los resultados, y en cada ronda de bola de nieve | Qué obras entran en el estudio | B3, B6 |
| **3** | Antes de escribir | El esquema del artículo y su argumento central | R1 |
| **4** | Antes de dar el texto por terminado | La versión final, junto con el informe de comprobación de citas | R2–R4 |

Entre un punto y otro, el sistema te informa de lo que hace pero no te pregunta. Si tropieza con
un problema (una obra que no se consigue, un PDF ilegible, un límite alcanzado), lo apunta y sigue
con lo demás.

En la documentación técnica estos puntos se llaman **PC-1, PC-2, PC-3 y PC-4**.
