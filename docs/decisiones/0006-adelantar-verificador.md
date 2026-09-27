# Decisión 0006 · Adelantar un prototipo del verificador de citas

- **Estado:** aceptada
- **Fecha:** 2026-09-27
- **Quién decide:** Rubén

## En pocas palabras

Antes de terminar la fase 1 se ha construido un primer prototipo del verificador de citas
(fase 2), con un proyecto de ejemplo, para poder enseñar pronto algo que funcione.

## Situación

El plan pone el verificador en la fase 2, después de elegir gestor bibliográfico (fase 1). Pero
hacía falta una demostración temprana, y el verificador no depende de esa elección: trabaja con
el formato estándar de referencias (CSL-JSON), que exportan Zotero y los demás gestores.

## Decisión

Construir ya un prototipo del verificador y un comprobador de DOI, con pruebas automáticas y un
proyecto de ejemplo ficticio. Se integran en Claude Code como el comando `/verificar-citas` y
el ayudante `verificador`.

## Otras opciones que se valoraron

- **Empezar por la búsqueda en catálogos:** más vistosa, pero no se podía probar desde el
  entorno de construcción (sin acceso a los catálogos) y depende del proyecto piloto.
- **Esperar a la fase 1:** retrasaba cualquier demostración.

## Consecuencias

- La fase 2 no está terminada: falta extraer texto y páginas de PDF reales y la comprobación
  asistida de paráfrasis.
- Si el gestor que se elija obliga a cambiar el formato de la estantería, habrá que adaptar
  `herramientas/verificacion/estanteria.py`.
