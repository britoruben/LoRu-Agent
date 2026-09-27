# ADR-0003 · Datos de investigación fuera del repositorio

- **Estado:** aceptada
- **Fecha:** 2026-09-27
- **Decisores:** Rubén

## Contexto

Cada investigación genera PDFs (con copyright), texto extraído, fichas, biblioteca y borradores.
Hay que separar la herramienta (compartible, versionada) de los datos (privados, voluminosos).

## Decisión

Los datos viven en una carpeta externa configurable mediante `LORU_DATOS` (por defecto
`~/Investigacion`), con un subdirectorio por proyecto.

## Alternativas consideradas

- **Dentro del repo, ignorado por git:** más simple, pero mezcla herramienta y datos y se pierde al
  borrar el clon.
- **Repo de datos separado por proyecto:** buen versionado de fichas y borradores, pero añade
  complejidad; puede adoptarse más adelante sobre la carpeta externa sin cambiar la arquitectura.

## Consecuencias

- Todas las herramientas resuelven rutas a partir de `LORU_DATOS`.
- La carpeta se puede sincronizar para trabajar en equipo (Rubén y Lola).
- `.gitignore` mantiene reglas de seguridad por si alguien copia datos al repo por error.
