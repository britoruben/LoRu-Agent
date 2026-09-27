# LoRu-Agent

Agente de investigación para **Claude Code** (uso local) que asiste en dos grandes flujos:

1. **Gestión bibliográfica** — búsqueda, selección, descarga legal, análisis de contenido y de referencias (snowballing), y generación de un *estado de la cuestión* con disputas, errores y vacíos.
2. **Génesis de artículos** — redacción a partir del estado de la cuestión y documentos propios, adaptada a revista/editorial, con citación literal paginada y **verificación de toda cita**.

> **Estado: FASE 0 — Diseño.** Este repositorio contiene solo arquitectura y documentación.
> Todavía no hay código ejecutable. Ver [`docs/06-roadmap.md`](docs/06-roadmap.md).

## Documentación

| Documento | Contenido |
|---|---|
| [`docs/00-vision.md`](docs/00-vision.md) | Objetivos, alcance, no-objetivos y principios |
| [`docs/01-arquitectura.md`](docs/01-arquitectura.md) | Componentes, flujo de datos, estructura del repo |
| [`docs/02-agente-bibliografico.md`](docs/02-agente-bibliografico.md) | Especificación tareas B1–B7 |
| [`docs/03-agente-redaccion.md`](docs/03-agente-redaccion.md) | Especificación tareas R1–R4 |
| [`docs/04-fuentes-y-acceso.md`](docs/04-fuentes-y-acceso.md) | Catálogo de fuentes por disciplina y modos de acceso |
| [`docs/05-verificacion-citas.md`](docs/05-verificacion-citas.md) | Diseño anti-alucinación de citas |
| [`docs/06-roadmap.md`](docs/06-roadmap.md) | Fases, entregables y criterios de aceptación |
| [`docs/07-preguntas-abiertas.md`](docs/07-preguntas-abiertas.md) | Decisiones pendientes (agenda reunión) |
| [`docs/decisiones/`](docs/decisiones/) | Registro de decisiones de arquitectura (ADR) |

## Equipo

- Rubén — arquitectura y documentación
- Lola — implementación y acceso a bases de datos (por confirmar)
