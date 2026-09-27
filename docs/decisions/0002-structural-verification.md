# Decision 0002 · Citations are protected by the system's design

- **Status:** accepted
- **Date:** 2026-09-27
- **Decided by:** Rubén

## In short

Asking the AI not to invent citations is not enough. The system is built so that it **cannot**
slip in a fake citation: it only cites checked works, a program does the formatting and another
program reviews each citation before finishing.

## Situation

AIs sometimes invent references, give wrong DOIs, alter literal quotes or get the page wrong.
Asking them in the instructions not to do so reduces the problem, but does not remove it.

## Decision

1. The AI can only cite works from the project's **verified shelf**, through labels.
2. The **format** of citations is applied by a program with the right style (APA, Chicago…).
3. A **verifier** (a program, not the AI) checks that the work exists, that the DOI is correct,
   that the literal quote is in the original and that the page is right. If there are failures,
   the text cannot be considered finished.

Full explanation in [05 · Citation verification](../05-citation-verification.md).

## Other options considered

- **Instructions to the AI only:** insufficient.
- **Human review only:** with dozens of citations it is slow and errors are easily missed.

## Consequences

- The project's shelf and the text of each cited work are needed.
- A work whose text is not available cannot be quoted literally without checking it by hand.
