# CLAUDE.md — LoRu-Agent

Instrucciones para Claude Code al trabajar en este repositorio.

## Estado del proyecto

FASE 0 (diseño). El repositorio contiene documentación, no código. Para entender el proyecto,
empieza por `docs/guia.md`. Antes de implementar algo, comprueba en `docs/06-plan-por-fases.md`
en qué fase estamos y en `docs/07-preguntas-abiertas.md` si la decisión que necesitas sigue
abierta. Si está abierta, pregunta; no la tomes por tu cuenta.

## Reglas no negociables (aplican a todo el código y agentes futuros)

1. **Nunca inventar referencias.** Solo se cita lo que existe en la biblioteca verificada del
   proyecto (ver `docs/05-verificacion-citas.md`). Si falta una fuente, se marca `[FUENTE PENDIENTE]`.
2. **Nunca inventar citas literales ni páginas.** Toda cita textual debe poder localizarse en el
   texto extraído del documento, con su página impresa.
3. **El formato de las citas lo pone un programa**, no la IA (estilos CSL con Pandoc/citeproc).
4. **Solo acceso legal.** APIs oficiales, acceso abierto y la suscripción legítima del usuario.
   Nada de Sci-Hub, LibGen ni scraping masivo de plataformas con licencia.
5. **Los datos de investigación viven fuera del repo**, en `$LORU_DATOS/<proyecto>/` (decisión 0003).
   Nunca copies PDFs ni texto con copyright al repositorio.
6. **Trazabilidad.** Cada afirmación del estado de la cuestión debe enlazar a documento + página.
7. **Respeta los puntos de control PC-1…PC-4** (`docs/00-vision.md`): detente y pide aprobación
   en ellos; entre ellos, trabaja sin preguntar.

## Convenciones

- Documentación en español.
- Decisiones importantes: una nota en `docs/decisiones/` (plantilla `0000-plantilla.md`) y una
  línea en `docs/decisiones/README.md`.

## Claridad: todo debe entenderse sin formación técnica

Este proyecto está pensado para investigadores de cualquier disciplina, programen o no. Todo lo
que se escriba en este repositorio (documentación, código, mensajes que ve la persona usuaria)
debe poder entenderlo alguien que no programa.

**Documentación**
- Cada documento empieza con un recuadro `> **En pocas palabras:** …` de 2 a 4 frases.
- Primero, qué hace y por qué, en lenguaje llano; lo técnico va al final, en secciones tituladas
  "Detalle técnico".
- Si una palabra corriente sirve, se usa esa en lugar de la jerga ("plan por fases", no "roadmap";
  "comprobación automática", no "hook").
- Todo término técnico inevitable se explica en su primera aparición y se añade a
  `docs/glosario.md`.
- Nada de siglas sin explicar. Frases cortas. Ejemplos concretos y analogías.
- Todo proceso nuevo que use la persona usuaria se documenta paso a paso en `docs/guia.md` o en
  una guía propia.

**Código (Python)**
- Nombres de archivos, funciones y variables en español y descriptivos
  (`comprobar_cita_literal`, no `chk_q`).
- Cada archivo empieza con un comentario que explica en lenguaje llano qué hace, por qué existe
  y cómo se usa.
- Cada función lleva un comentario (*docstring*) en español que dice qué recibe, qué devuelve y
  qué hace, sin jerga.
- Funciones cortas, de una sola tarea. Se prefiere código sencillo y explícito a código ingenioso.
- Los comentarios explican el **porqué**, no repiten lo que hace cada línea.
- Los mensajes de error dicen qué ha pasado y qué hacer, en español: "No encuentro el PDF de
  'Arendt 1958' en la carpeta pdf/. Descárgalo o márcalo como no disponible", no
  "FileNotFoundError".
- Las pruebas (`tests/`) llevan nombres que se leen como frases: `test_detecta_una_cita_alterada`.
