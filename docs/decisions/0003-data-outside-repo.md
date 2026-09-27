# Decision 0003 · Research data are kept apart from the program

- **Status:** accepted
- **Date:** 2026-09-27
- **Decided by:** Rubén

## In short

The program is in one folder and your research in another (by default, `Investigacion`, inside
your home folder). That way no work is lost when updating the program, and copyrighted PDFs are
never published by mistake.

## Situation

Each research project generates PDFs (copyrighted), extracted texts, reading notes and drafts.
The program, instead, is stored and shared on GitHub. They must be kept apart.

## Decision

The data of each research project are kept in a **separate folder**, with one subfolder per
project. The location can be changed in the `.env` file (in the `LORU_DATOS` line).

## Other options considered

- **Inside the program folder**, excluded from GitHub: simpler, but it mixes program and data,
  and deleting the program loses the work.
- **One GitHub folder per research project** (without the PDFs): keeps the change history of
  notes and drafts, but is more complicated. It can be added later without changing anything in
  the design.

## Consequences

- Every tool looks for the data in the folder given in `LORU_DATOS`.
- The folder can be synced (Drive, OneDrive…) for teamwork.
- For safety, the program folder is configured never to publish PDF files, even if someone
  copies them into it by mistake (`.gitignore` file).
