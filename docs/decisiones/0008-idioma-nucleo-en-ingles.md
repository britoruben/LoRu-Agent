# Decisión 0008 · El núcleo del agente, en inglés; las guías para personas, en español

- **Estado:** aceptada (pendiente de aplicar)
- **Fecha:** 2026-09-27
- **Quién decide:** Rubén

## En pocas palabras

El código, las skills (comandos), los ayudantes, `CLAUDE.md` y los documentos técnicos pasan a
inglés, que es lo estándar y facilita compartir el proyecto. Las guías para personas (guía,
glosario, instalación, ejemplos) y los mensajes que ve la persona usuaria siguen en español.

## Situación

El proyecto mezclaba criterios: código con nombres en español (regla de claridad) y la
intención de que el núcleo del agente sea reutilizable y estándar.

## Decisión

| En inglés | En español |
|---|---|
| Código Python (nombres, comentarios, docstrings), pruebas | Mensajes que ve la persona usuaria (errores, informes) |
| Skills y ayudantes (`.claude/`), `CLAUDE.md` | `docs/guia.md`, `docs/glosario.md`, `docs/instalacion.md` |
| Documentos técnicos (arquitectura, especificaciones, decisiones) | `ejemplos/LEEME.md` y `README.md` (con un resumen en inglés) |

Se mantiene la regla de claridad: código sencillo, comentado y con nombres descriptivos,
ahora en inglés.

## Otras opciones que se valoraron

- **Documentación bilingüe completa:** duplica el trabajo en cada cambio.
- **Dejarlo todo en español:** el núcleo sería menos reutilizable.

## Consecuencias

- Se hará en una **sesión nueva** (más barata que seguir esta conversación tan larga).
- Hay que renombrar archivos, funciones y comandos (`/verificar-citas` → `/verify-citations`,
  `/preparar-pdf` → `/prepare-pdf`) y actualizar los enlaces de la documentación.
- Las pruebas existentes deben seguir pasando tras el cambio.
