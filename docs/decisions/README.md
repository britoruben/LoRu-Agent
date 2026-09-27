# Project decisions

Each file in this folder explains **one important decision**: what was decided, why and what
other options there were. That way, months from now, anyone can understand why the system is
the way it is without having to remember.

In programming jargon they are called **ADRs** (*Architecture Decision Records*).

| No. | Decision | Status |
|---|---|---|
| [0001](0001-local-claude-code.md) | The system runs on your computer with Claude Code | Accepted |
| [0002](0002-structural-verification.md) | Citations are protected by the system's design, not by asking the AI not to invent | Accepted |
| [0003](0003-data-outside-repo.md) | Research data are kept apart from the program | Accepted |
| [0004](0004-checkpoints.md) | The system works alone, but stops at four moments for you to decide | Accepted |
| [0005](0005-tech-stack.md) | Python, Word/PDF, Spanish and English, and Pro/Max subscription | Accepted |
| [0006](0006-verifier-first.md) | Bring forward a prototype of the citation verifier | Accepted |
| [0007](0007-pypdf-for-pdf.md) | Use pypdf (and not MarkItDown) to read PDFs | Accepted |
| [0008](0008-english-core.md) | Agent core in English; guides for people in Spanish | Accepted, applied |

To add a decision, copy [`0000-template.md`](0000-template.md) with the next number.
