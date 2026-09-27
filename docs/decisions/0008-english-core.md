# Decision 0008 · The agent's core in English; guides for people in Spanish

- **Status:** accepted (applied on 2026-09-27)
- **Date:** 2026-09-27
- **Decided by:** Rubén

## In short

The code, the skills (commands), the helpers, `CLAUDE.md` and the technical documents move to
English, which is the standard and makes the project easier to share. The guides for people
(guide, glossary, installation, examples) and the messages the person sees stay in Spanish.

## Situation

The project mixed criteria: code with Spanish names (clarity rule) and the intention that the
agent's core be reusable and standard.

## Decision

| In English | In Spanish |
|---|---|
| Python code (names, comments, docstrings), tests | Messages the person sees (errors, reports) |
| Skills and helpers (`.claude/`), `CLAUDE.md` | `docs/guia.md`, `docs/glosario.md`, `docs/instalacion.md` |
| Technical documents (architecture, specifications, decisions) | `ejemplos/LEEME.md` and `README.md` (with a summary in English) |

The clarity rule is kept: simple, commented code with descriptive names, now in English.

## Other options considered

- **Full bilingual documentation:** doubles the work on every change.
- **Keep everything in Spanish:** the core would be less reusable.

## Consequences

- Files, functions and commands renamed: `herramientas/` → `tools/`
  (`verification/`, `pdf/`, `sources/`), `/verificar-citas` → `/verify-citations`,
  `/preparar-pdf` → `/prepare-pdf`, helper `verificador` → `verifier`, `docs/decisiones/` →
  `docs/decisions/`. Program options too: `--project`, `--key`, `--first-page`, `--output`,
  `--email`, `--save`.
- **Applied criterion — the person's data stay in Spanish:** folder and file names of each
  project (`biblioteca.json`, `texto/`, `borradores/`, `pdf/`, `*.verificacion.md`) and the
  field names inside them (`verificacion`, `texto_local`, `paginas`, `impresa`, `calidad`…).
  The person sees and edits them, and changing them would break existing projects.
- Existing tests keep passing after the change (only their names were translated).
