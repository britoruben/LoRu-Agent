# 00 · Vision: what we aim for and what we don't

> **In short:** we want an assistant that does the mechanical work of literature research and
> writing (searching, screening, getting texts, extracting, checking citations) without the big
> danger of AIs: inventing references or quotes. The intellectual decisions remain with the
> researcher.

## The problem

Reviewing the literature and writing an article demands a lot of mechanical work: searching
catalogues, discarding what is not useful, getting the texts, taking notes, checking quotes and
pages… AIs can help a lot, but they have a serious flaw: sometimes they **invent references**
that do not exist, give **wrong publication identifiers (DOI)** or **alter literal quotes**. In
academic work that is unacceptable.

## The goal

That when you download this project and open it with Claude Code on your computer you get a team
of helpers able to:

- **Literature review:** go from a research question to a state of the art in which every claim
  points to a work and a page, with the disputes, errors and gaps of the debate.
- **Writing:** go from that state of the art and your own materials to an article draft adapted
  to a specific journal, with **every citation checked**.

## For every discipline

It must work for the humanities, social sciences, health and biomedicine, and engineering and
computer science. Since each discipline has its own catalogues, citation styles and ways of
valuing works, none of this is fixed in advance: it is configured in **each project's profile**
(see [01 · Architecture](01-architecture.md)).

## What it does NOT aim for

- **Not** producing publishable articles without human review. It is an assistant: authorship
  and intellectual decisions belong to the researcher.
- **Not** bypassing licences: no mass downloads from paid platforms or pirate sites.
- **Not** using the university's access from the cloud: access to private databases will only
  work on your computer, with your credentials.

## Principles

1. **Programs for what can be checked, AI for what must be interpreted.** Searching, extracting
   text, formatting citations and verifying them are done by programs, which always give the
   same result. The AI reads, classifies, summarizes and writes.
2. **Citations are protected by design, not by good intentions.** Asking the AI "not to invent"
   is not enough. The system must prevent an unchecked citation from reaching the final text.
3. **Everything can be traced.** Every claim points to a work and a page.
4. **The person decides at fixed moments** (see below). Between them, the system works alone.
5. **Always with limits.** Each process has a maximum of documents, rounds and usage, so it does
   not run away.

## The four checkpoints (decision 0004)

The system stops and waits for your approval only at these moments:

| Point | When | What you decide | Steps affected |
|---|---|---|---|
| **1** | Before searching | Search terms, catalogues, period and languages | B1–B2 |
| **2** | After ranking the results, and at each snowball round | Which works enter the study | B3, B6 |
| **3** | Before writing | The article's outline and its central argument | R1 |
| **4** | Before considering the text finished | The final version, together with the citation-check report | R2–R4 |

Between one point and the next, the system tells you what it is doing but does not ask. If it
hits a problem (a work that cannot be obtained, an unreadable PDF, a limit reached), it notes it
and carries on with the rest.

In the technical documentation these points are called **PC-1, PC-2, PC-3 and PC-4**.
