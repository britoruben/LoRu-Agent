# Decisiones del proyecto

Cada archivo de esta carpeta explica **una decisión importante**: qué se decidió, por qué y qué
otras opciones había. Así, dentro de unos meses, cualquiera puede entender por qué el sistema es
como es sin tener que recordarlo.

En la jerga de la programación se llaman **ADR** (*Architecture Decision Record*, "registro de
decisiones de arquitectura").

| Nº | Decisión | Estado |
|---|---|---|
| [0001](0001-claude-code-local.md) | El sistema funciona en tu ordenador con Claude Code | Aceptada |
| [0002](0002-verificacion-estructural.md) | Las citas se protegen con el diseño del sistema, no pidiéndole a la IA que no invente | Aceptada |
| [0003](0003-datos-fuera-del-repo.md) | Los datos de investigación se guardan aparte del programa | Aceptada |
| [0004](0004-puntos-de-control.md) | El sistema trabaja solo, pero se detiene en cuatro momentos para que decidas | Aceptada |
| [0005](0005-stack-tecnico.md) | Python, Word/PDF, español e inglés y suscripción Pro/Max | Aceptada |
| [0006](0006-adelantar-verificador.md) | Adelantar un prototipo del verificador de citas | Aceptada |
| [0007](0007-pypdf-para-leer-pdf.md) | Usar pypdf (y no MarkItDown) para leer los PDF | Aceptada |
| [0008](0008-idioma-nucleo-en-ingles.md) | Núcleo del agente en inglés; guías para personas en español | Aceptada, pendiente de aplicar |

Para añadir una decisión, copia [`0000-plantilla.md`](0000-plantilla.md) con el número siguiente.
