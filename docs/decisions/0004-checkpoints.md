# Decision 0004 · The system works alone, but stops at four moments

- **Status:** accepted
- **Date:** 2026-09-27
- **Decided by:** Rubén

## In short

The system does the work without asking at every step, but it stops for you to decide at four
key moments: before searching, when choosing the works, before writing and before considering
the text finished.

## Situation

Speed and control must be balanced. An early mistake (badly chosen search terms, an important
work left out) carries its consequences into the state of the art and the article.

## Decision

Four **checkpoints** at which the system waits for your approval:

1. the search terms;
2. the works that enter the study (at each round);
3. the article's outline;
4. the final version, with the citation-check report.

Between them, the system works alone. Details in [00 · Vision](../00-vision.md).

## Other options considered

- **Asking at every step:** safer, but too slow for everyday use.
- **Asking only at the end:** early mistakes would stay hidden.
- **Letting each project choose how often it is asked:** useful in the future, but it
  complicates building now.

## Consequences

- Commands are split into stretches that end at a checkpoint.
- Work is saved in the project folder so it can be resumed after each approval.
