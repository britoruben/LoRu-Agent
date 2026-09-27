# CLAUDE.md — LoRu-Agent

Instrucciones para Claude Code al trabajar en este repositorio.

## Estado del proyecto

FASE 0 (diseño). El repositorio contiene documentación, no código. Antes de implementar
algo, comprueba en `docs/06-roadmap.md` en qué fase estamos y en `docs/07-preguntas-abiertas.md`
si la decisión que necesitas sigue abierta. Si está abierta, pregunta; no la tomes por tu cuenta.

## Reglas no negociables (aplican a todo el código y agentes futuros)

1. **Nunca inventar referencias.** Solo se cita lo que existe en la biblioteca verificada del
   proyecto (ver `docs/05-verificacion-citas.md`). Si falta una fuente, se marca `[FUENTE PENDIENTE]`.
2. **Nunca inventar citas literales ni páginas.** Toda cita textual debe poder localizarse en el
   texto extraído del documento, con su página impresa.
3. **Formato de cita determinista.** Lo genera CSL/citeproc, no el modelo.
4. **Solo acceso legal.** APIs oficiales, acceso abierto y la suscripción legítima del usuario.
   Nada de Sci-Hub, LibGen ni scraping masivo de plataformas con licencia.
5. **Los PDF y datos con copyright no se suben a git** (`corpus/` está en `.gitignore`).
6. **Trazabilidad.** Cada afirmación del estado de la cuestión debe enlazar a documento + página.

## Convenciones

- Documentación en español.
- Decisiones de arquitectura: un ADR en `docs/decisiones/` (plantilla `0000-plantilla.md`).
