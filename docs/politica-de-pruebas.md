# Política de pruebas

> **En pocas palabras:** mientras el proyecto está en diseño y puede cambiar mucho, las pruebas
> son **mínimas**: solo las justas para no romper lo que ya funciona. No se amplían ni se
> hacen pruebas largas, porque cuestan tiempo y tokens y habría que rehacerlas cuando el
> diseño cambie. Se ampliarán cuando el proyecto esté más avanzado y definido.

## Reglas actuales

1. **No añadir pruebas nuevas** salvo que se corrija un error real (una prueba que impida que
   ese error vuelva).
2. **Nada de PDF largos ni pruebas largas.** Si hace falta probar con un documento real, uno
   corto (pocas páginas) y una sola vez.
3. **Solo Windows**, que es el sistema del equipo. No se prueba en macOS ni en Linux.
4. **Se trabaja en la nube** (Claude Code en la web). No se da por supuesto que haya un
   ordenador disponible para probar en local.
5. Antes de subir un cambio a los programas, se ejecutan las pruebas que ya existen (tardan
   segundos). Si alguna falla, no se sube.

## Cuándo se revisará esta política

Cuando el diseño esté cerrado (preguntas abiertas resueltas y proyecto piloto elegido). Entonces
se preparará un conjunto de pruebas más completo, con documentos reales del proyecto piloto.
