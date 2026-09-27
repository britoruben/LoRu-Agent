# ADR-0002 · Verificación estructural de citas

- **Estado:** aceptada
- **Fecha:** 2026-09-27
- **Decisores:** Rubén

## Contexto

Los LLM pueden generar referencias inexistentes, DOIs incorrectos, citas literales alteradas y
páginas erróneas. Las instrucciones en el prompt reducen el problema pero no lo eliminan.

## Decisión

1. El modelo solo cita mediante claves de una biblioteca verificada (CSL-JSON).
2. El formato de cita lo genera CSL/citeproc (Pandoc).
3. Un verificador determinista comprueba existencia, DOI, literalidad y página, y bloquea la
   versión final si hay fallos.

Detalle en `docs/05-verificacion-citas.md`.

## Alternativas consideradas

- Solo instrucciones en el prompt: insuficiente.
- Revisión exclusivamente humana: no escala y es propensa a errores con decenas de citas.

## Consecuencias

- Hace falta una biblioteca local y el texto extraído de cada fuente citada.
- Las fuentes sin PDF disponible no pueden citarse literalmente sin verificación manual.
