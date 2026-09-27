# Decision 0006 · Bring forward a prototype of the citation verifier

- **Status:** accepted
- **Date:** 2026-09-27
- **Decided by:** Rubén

## In short

Before finishing phase 1, a first prototype of the citation verifier (phase 2) has been built,
with an example project, to be able to show something that works early on.

## Situation

The plan puts the verifier in phase 2, after choosing a reference manager (phase 1). But an
early demonstration was needed, and the verifier does not depend on that choice: it works with
the standard reference format (CSL-JSON), which Zotero and the other managers export.

## Decision

Build now a prototype of the verifier and a DOI checker, with automatic tests and a fictitious
example project. They are integrated into Claude Code as the `/verify-citations` command
(originally `/verificar-citas`) and the `verifier` helper.

## Other options considered

- **Start with catalogue search:** more eye-catching, but it could not be tested from the build
  environment (no access to the catalogues) and it depends on the pilot project.
- **Wait for phase 1:** it delayed any demonstration.

## Consequences

- Phase 2 is not finished: extracting text and pages from real PDFs and the assisted paraphrase
  check are still missing.
- If the chosen manager forces a change in the shelf format, `tools/verification/shelf.py` will
  have to be adapted.
