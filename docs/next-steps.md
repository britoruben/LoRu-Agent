# Next steps (hand-over note between sessions)

> **In short:** what is done, what is missing and in what order. A new Claude session should
> read this file first so as not to have to go over earlier conversations.

## Status (2026-09-27)

- Design documented (`docs/`), decisions 0001–0008.
- Decision 0008 applied: core in English (`tools/`, `tests/`, `.claude/`, `CLAUDE.md`,
  technical docs); guides, messages and the person's data in Spanish.
- Working prototype: citation verifier, PDF extractor (pypdf), DOI checker (not tried against
  the real Crossref), commands `/verify-citations` and `/prepare-pdf`.
- Minimal tests (`docs/testing-policy.md`), Windows only, cloud work.

## Next, in order

1. **Try a real, short academic PDF** (open access, few pages), once.
2. **Real Crossref**, when the environment's network allows `api.crossref.org`.
3. **Code review** and pull request to `main`.

## Team constraints

- Cloud only (no local computer for now); both use Windows.
- Save tokens: short sessions, minimal tests, no long documents.
- Pending the meeting with Lola: questions P-01, P-03, P-04, P-05, P-09.
