# Decision 0001 · The system runs on your computer with Claude Code

- **Status:** accepted
- **Date:** 2026-09-27
- **Decided by:** Rubén

## In short

The assistant will be used with **Claude Code on each person's computer**, not in the cloud,
because it needs access to your PDFs, your reference manager and, where applicable, the
university's databases.

## Situation

The system has to read documents on your computer, connect to the reference manager and,
perhaps, use the university's paid databases, which only work with your connection or your
institutional account.

## Decision

**Claude Code on the local computer** will be used (see the [glossary](../glosario.md)). The
project is prepared as a folder that includes the instructions, helpers, commands, automatic
checks and the "plugs" (MCP) needed.

## Other options considered

- **Claude Code in the cloud** (from the web): it has no access to the university network or to
  your files. It would only serve to search open catalogues or to build the project itself.
- **The Claude desktop app:** it supports "plugs" (MCP), but does not allow organizing the work
  into helpers, commands and automatic checks with the same flexibility.

## Consequences

- Access to paid databases will never be done from the cloud.
- Each person keeps their keys and passwords on their own computer (`.env` file).
