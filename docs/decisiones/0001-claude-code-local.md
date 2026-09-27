# ADR-0001 · Claude Code en local como entorno principal

- **Estado:** aceptada
- **Fecha:** 2026-09-27
- **Decisores:** Rubén

## Contexto

El agente necesita acceso a PDFs locales, al gestor bibliográfico y, potencialmente, a bases de
datos con acceso institucional (por IP/VPN/credenciales del usuario).

## Decisión

El entorno principal es **Claude Code ejecutado en local**. Se empaqueta como repositorio con
`CLAUDE.md`, subagentes, skills, hooks y servidores MCP.

## Alternativas consideradas

- **Nube (Claude Code en la web):** sin acceso a la red institucional ni a archivos locales. Útil
  solo para búsquedas en acceso abierto o para desarrollar el propio repositorio.
- **Aplicación de escritorio de Claude con MCP:** admite servidores MCP, pero no subagentes, skills
  de proyecto ni hooks con la misma flexibilidad.

## Consecuencias

- El acceso privado nunca se ejecuta en la nube.
- Cada usuario configura sus credenciales en `.env` local.
