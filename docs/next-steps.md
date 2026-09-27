# Next steps (hand-over note between sessions)

> **In short:** what is done, what is missing and in what order. A new Claude session should
> read this file first so as not to have to go over earlier conversations.

## Status (2026-09-27)

- All work is on `main`. Design documented (`docs/`), decisions 0001–0008.
- Working prototype: citation verifier, PDF extractor (pypdf), DOI checker (not tried against
  the real Crossref), commands `/verify-citations` and `/prepare-pdf`, `verifier` helper.
- Web sessions prepare themselves (`.claude/hooks/session-start.sh`).
- **Current stage: design review by the team.** The team reads the guide
  (`docs/guia.md`), tries the demo (`ejemplos/LEEME.md`) and discusses the design.

## How to help during the review

- Answer questions about the project in plain Spanish, using the Spanish guides first.
- Show the demo when asked (see `ejemplos/LEEME.md`, section "Probarlo en Claude Code en la web").
- Help decide the open questions, the most important being **P-05** (pilot project and
  discipline); then P-01, P-03, P-04 and P-09 (`docs/07-open-questions.md`). Recommend, but
  do not decide: record each decision only when a team member takes it.
- Do not start building the next phases until the review ends and the team asks for it.

## After the review, in order

1. Apply the changes the review asks for.
2. **Try a real, short academic PDF** (open access, few pages), once.
3. **Real Crossref**, when the environment's network allows `api.crossref.org`.

## Team constraints

- Cloud only (no local computer for now); both use Windows.
- Save tokens: short sessions, minimal tests (`docs/testing-policy.md`), no long documents.
