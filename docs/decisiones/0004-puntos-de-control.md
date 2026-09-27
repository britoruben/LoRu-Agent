# Decisión 0004 · El sistema trabaja solo, pero se detiene en cuatro momentos

- **Estado:** aceptada
- **Fecha:** 2026-09-27
- **Quién decide:** Rubén

## En pocas palabras

El sistema hace el trabajo sin preguntar a cada paso, pero se detiene para que decidas en cuatro
momentos clave: antes de buscar, al elegir las obras, antes de escribir y antes de dar el texto por
terminado.

## Situación

Hay que equilibrar rapidez y control. Un error al principio (palabras de búsqueda mal elegidas, una
obra importante que se queda fuera) arrastra sus consecuencias al estado de la cuestión y al
artículo.

## Decisión

Cuatro **puntos de control** en los que el sistema espera tu aprobación:

1. las palabras de búsqueda;
2. las obras que entran en el estudio (en cada ronda);
3. el esquema del artículo;
4. la versión final, con el informe de comprobación de citas.

Entre ellos, el sistema trabaja solo. Detalle en [00 · Visión](../00-vision.md).

## Otras opciones que se valoraron

- **Consultar en cada paso:** más seguro, pero demasiado lento para el uso habitual.
- **Consultar solo al final:** los errores del principio quedarían ocultos.
- **Que cada proyecto elija cuánto se le consulta:** útil en el futuro, pero ahora complica la
  construcción.

## Consecuencias

- Los comandos se dividen en tramos que terminan en un punto de control.
- El trabajo se guarda en la carpeta del proyecto para poder retomarlo después de cada aprobación.
