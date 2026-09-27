# ADR-0004 · Autonomía con puntos de control fijos

- **Estado:** aceptada
- **Fecha:** 2026-09-27
- **Decisores:** Rubén

## Contexto

Hay que equilibrar velocidad y control. Un error en la selección de términos o del corpus se
propaga a todo el estado de la cuestión y al artículo.

## Decisión

Cuatro puntos de control humano: PC-1 (términos de búsqueda), PC-2 (selección del corpus, en cada
ronda), PC-3 (esquema del artículo) y PC-4 (versión final + informe de verificación). Entre ellos,
el agente es autónomo. Detalle en `docs/00-vision.md`.

## Alternativas consideradas

- **Control en cada tarea:** más seguro, demasiado lento para el uso habitual.
- **Solo revisión final:** los errores tempranos quedan ocultos.
- **Nivel configurable:** útil en el futuro, pero añade complejidad ahora.

## Consecuencias

- Las skills de orquestación se dividen en fases que terminan en un punto de control.
- El estado del proyecto debe persistir en disco para poder reanudar tras cada aprobación.
