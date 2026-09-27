# 06 · Phased plan: in what order it is built

> **In short:** the system is built in 9 phases (0 to 8). Each phase ends with something that
> already works and can be tried. The **citation verifier** is built first, because it is what
> makes everything else trustworthy. Then search, reading, snowballing and writing. Paid
> databases and the reviewer come last.

Plan rules:

- **Each phase ends with something usable** and with a clear test that it works ("How we will
  know it is right" column).
- **A phase is not started** while the questions blocking it remain unanswered (see
  [07 · Open questions](07-open-questions.md)).

| Phase | What is achieved | What is built | How we will know it is right | Needs first |
|---|---|---|---|---|
| **0 · Design** *(almost finished)* | Know what we are going to build | This documentation | Rubén and Lola approve the design | — |
| **1 · Foundations** | Be able to create a project and its shelf | Program structure, project profile, connection to the reference manager, installation guide | A project is created and 10 checked references are added | P-01 |
| **2 · Verifier** *(prototype under way, decision 0006)* | Check citations reliably | Citation verifier and text extraction with printed pages, with a collection of "trap citations" to test it (fake DOI, altered quote, wrong page) | It detects **every** trap citation | Phase 1 |
| **3 · Search** | Find and rank what is openly published | Connection to open catalogues, importance computation, `/search` command | With a real question, the researcher finds the list useful | Phase 1, P-05 |
| **4 · Reading and synthesis** | First state of the art | Reader (two levels) and synthesizer helpers, `/state-of-the-art` command; summary, report and tables | State of the art in the pilot project with every claim traceable to work and page | Phase 3 |
| **5 · Snowballing** | Find what the search did not | Citation network, limited rounds, visual map | Relevant works appear that the initial search had not found | Phase 4 |
| **6 · Writing** | Article draft | Writer helper (by sections), journal profiles from their guidelines, export to Word and PDF, automatic check before exporting | A full draft with **zero** verification failures | Phases 2 and 4 |
| **7 · Paid databases** | Use the institution's subscriptions | Official connection (API) or guided download, as decided | What is set when deciding P-03 | P-03 |
| **8 · Reviewer** | Journal-style prior assessment | Reviewer helper | Its objections essentially match those of a human referee in a test case | Phase 6 |

## Phase 2 status (prototype)

| Part | Status |
|---|---|
| Verify that works are on the shelf and checked | Done |
| Literal quotes: exact text, omissions, page, quotes spanning two pages | Done |
| Warnings: quotation marks without a source, citations in an unrecognized format, scanned texts | Done |
| Check DOIs in Crossref | Done, tested only with simulated answers |
| Commands `/verify-citations` and `/prepare-pdf`, `verifier` helper | Done |
| Automatic tests on GitHub (Windows only; see [testing policy](testing-policy.md)) | Done |
| Extract text and printed pages from PDFs (with pypdf, decision 0007) | Done, tested with test PDFs; **still to be tried with real publishers' PDFs** |
| Read scanned PDFs (OCR) | **Pending**: they are detected and a warning is given |
| Assisted paraphrase check | **Pending** |
| Automatic check before exporting (*hook*) | **Pending** (comes with phase 6) |

See the [examples](../ejemplos/LEEME.md) (in Spanish).

## Why the verifier comes so early

It is the piece that makes everything else reliable and it can be tested on its own, without
waiting for search or writing to exist. If it fails, the rest of the system is useless for
academic work.

## The pilot project

To check that phases 3 to 6 really work, **a real, bounded research question** is needed
(question P-05). It is best to start with **a single discipline** and widen later: testing all
of them at once multiplies the work and makes it hard to know what fails.
