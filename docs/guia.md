# Guía: qué es LoRu-Agent y cómo funciona

> Empieza por aquí. Esta guía no da nada por supuesto: no hace falta saber programar ni conocer
> términos técnicos. Si aparece una palabra que no conoces, búscala en el [glosario](glosario.md).

## 1. Qué es, en una frase

LoRu-Agent es un **asistente de investigación** basado en Claude (la IA de Anthropic) que ayuda a
hacer dos cosas:

1. **Revisar la bibliografía de un tema**: buscar lo que se ha publicado, elegir lo importante,
   leerlo, seguir las referencias y escribir un *estado de la cuestión*.
2. **Escribir un artículo** a partir de ese estado de la cuestión, adaptado a una revista, y
   **comprobando que cada cita es real y exacta**.

## 2. Una imagen para entenderlo: un pequeño equipo de ayudantes

Imagina que diriges un equipo de ayudantes de investigación. Cada uno tiene un único oficio:

| Ayudante | Qué hace | Cómo se llama en la documentación técnica |
|---|---|---|
| El **buscador** | Busca en catálogos y bases de datos lo publicado sobre el tema | `searcher` |
| El **bibliotecario** | Consigue los textos (solo por vías legales) | `retriever` |
| El **lector** | Lee cada texto y rellena una ficha de lectura | `reader` |
| El **rastreador** | Mira a quién citan los textos y quién los cita a ellos, para encontrar obras que faltan | `tracker` |
| El **sintetizador** | Junta todas las fichas y redacta el estado de la cuestión | `synthesizer` |
| El **redactor** | Escribe el artículo sección a sección | `writer` |
| El **verificador** | Comprueba cada cita contra el texto original, como un corrector muy estricto | `verifier` |
| El **revisor** *(más adelante)* | Lee el borrador como lo haría el revisor de una revista | `reviewer` |

Tú eres quien dirige el equipo: das la pregunta de investigación, y el equipo **se para y te
consulta en cuatro momentos clave** antes de seguir (ver apartado 4).

En la documentación técnica a estos ayudantes se les llama **subagentes**: son copias de Claude a
las que se da una única tarea y unas instrucciones concretas.

## 3. Cómo se usará (cuando esté construido)

> De momento solo funcionan el verificador de citas y la preparación de PDF (apartado 7). Los pasos de este apartado
> describen el sistema completo, que todavía se está construyendo.

1. Abres una conversación con Claude Code, en la web o en tu ordenador. Es como un chat, pero
   Claude puede leer y crear archivos del proyecto.
2. Escribes un comando que empieza por barra, por ejemplo `/state-of-the-art`, y respondes a lo que
   te pregunta: tu pregunta de investigación, la disciplina, el periodo, los idiomas…
3. El equipo trabaja. Te va informando de lo que hace y **se detiene en los puntos de control**.
4. Al final, recibes los resultados como documentos normales (Word, PDF, tablas).

## 4. Los cuatro momentos en que el sistema te consulta

| Momento | Qué te enseña | Qué decides tú |
|---|---|---|
| **1. Antes de buscar** | Las palabras de búsqueda que propone, en español e inglés, y dónde va a buscar | Si son las adecuadas; puedes añadir o quitar |
| **2. Tras la búsqueda** | Una lista de obras ordenadas por importancia, cada una con una frase que explica por qué está ahí | Qué obras entran en el estudio |
| **3. Antes de escribir** | El esquema del artículo y el argumento central | Si la estructura te convence |
| **4. Antes de dar el texto por terminado** | El borrador final y un informe de todas las citas comprobadas | Si se da por bueno |

Entre un momento y otro, el sistema trabaja solo.

## 5. Recorrido completo, de la pregunta al artículo

```
Tu pregunta de investigación
      │
      ▼
 [1] Buscar publicaciones ──► Momento 1: ¿buenas palabras de búsqueda?
      │
      ▼
 [2] Ordenar por importancia ──► Momento 2: ¿qué obras entran?
      │
      ▼
 [3] Conseguir los textos (solo acceso legal)
      │
      ▼
 [4] Leer y hacer fichas de lectura
      │
      ▼
 [5] Seguir las referencias ("bola de nieve") ──► vuelve al Momento 2 con las obras nuevas
      │
      ▼
 [6] Estado de la cuestión: consensos, disputas, errores y vacíos
      │
      ▼
 [7] Esquema del artículo ──► Momento 3: ¿te convence?
      │
      ▼
 [8] Redacción sección a sección
      │
      ▼
 [9] Verificación de todas las citas ──► Momento 4: ¿se da por bueno?
      │
      ▼
 Artículo en Word / PDF
```

## 6. Por qué te puedes fiar de las citas

Las IA a veces **inventan** referencias que no existen o citas que el autor nunca escribió. Este
sistema evita el problema así:

- **Solo se puede citar lo que está en la "estantería" del proyecto.** Cada obra entra en esa
  estantería después de comprobar que existe de verdad (en registros oficiales de publicaciones).
- **Las citas literales se comparan con el texto original**, palabra por palabra, y se comprueba
  la página.
- **El formato de las citas (APA, Chicago…) lo pone un programa, no la IA**, así que no hay
  errores de formato.
- Si algo no cuadra, el texto **no se puede dar por terminado** hasta que se corrija.

Más detalle en [05 · Verificación de citas](05-citation-verification.md).

## 7. Qué se puede probar ya

La forma más sencilla es **Claude Code en la web**, sin instalar nada: los pasos están en
[ejemplos](../ejemplos/LEEME.md), apartado 4. Si prefieres tu ordenador, sigue la
[guía de instalación](instalacion.md).

Ya funciona un primer prototipo del **verificador de citas**, con un proyecto de ejemplo con
errores puestos a propósito. Ver [ejemplos](../ejemplos/LEEME.md): se puede ver el resultado
sin instalar nada.

## 8. Qué NO hace

- **No escribe artículos listos para publicar sin revisión.** Es un asistente; la autoría y las
  decisiones intelectuales son tuyas.
- **No se salta licencias**: no usa webs piratas ni descarga masivamente de plataformas de pago.
- **No accede a bases de datos privadas desde la nube**: eso solo funcionará en tu ordenador, con
  tu acceso de la universidad.

## 9. Dónde está cada cosa

| Si quieres saber… | Lee |
|---|---|
| Qué persigue el proyecto y qué no | [00 · Visión](00-vision.md) |
| Cómo encajan las piezas | [01 · Arquitectura](01-architecture.md) |
| Cómo funciona la revisión bibliográfica | [02 · Flujo bibliográfico](02-bibliographic-agent.md) |
| Cómo funciona la escritura del artículo | [03 · Flujo de redacción](03-writing-agent.md) |
| De dónde saca las publicaciones | [04 · Fuentes y acceso](04-sources-and-access.md) |
| Cómo se comprueban las citas | [05 · Verificación de citas](05-citation-verification.md) |
| En qué orden se construye | [06 · Plan por fases](06-phased-plan.md) |
| Qué falta por decidir | [07 · Preguntas abiertas](07-open-questions.md) |
| Qué se ha decidido y por qué | [Decisiones](decisions/) |
| Qué significa una palabra | [Glosario](glosario.md) |
| Qué se puede probar ya | [Ejemplos](../ejemplos/LEEME.md) |
| Cómo se instala | [Instalación](instalacion.md) |

**Cómo leer los documentos:** cada uno empieza con un recuadro **"En pocas palabras"** y está
escrito para cualquier lector. Las partes marcadas **"Detalle técnico"** son para quien programe;
se pueden saltar sin perder el hilo.

**Idioma:** los documentos 00 a 07 y las decisiones están en inglés (decisión 0008); las guías
(esta, el glosario, la instalación y los ejemplos) siguen en español.
