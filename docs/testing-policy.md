# Testing policy

> **In short:** while the project is in design and may change a lot, tests are **minimal**:
> just enough not to break what already works. They are not expanded and no long tests are
> run, because they cost time and tokens and would have to be redone when the design changes.
> They will be expanded when the project is more advanced and defined.

## Current rules

1. **Do not add new tests** unless a real bug is being fixed (a test that stops that bug from
   coming back).
2. **No long PDFs or long tests.** If a real document is needed, a short one (few pages) and
   only once.
3. **Windows only**, the team's system. No testing on macOS or Linux.
4. **Work happens in the cloud** (Claude Code on the web). Do not assume a computer is
   available to test locally.
5. Before pushing a change to the programs, run the existing tests (they take seconds). If any
   fails, do not push.

## When this policy will be reviewed

When the design is closed (open questions answered and pilot project chosen). Then a fuller set
of tests will be prepared, with real documents from the pilot project.
