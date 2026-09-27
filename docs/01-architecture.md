# 01 · Architecture: how the pieces fit together

> **In short:** the system has five pieces. **General instructions**, **commands** that you
> launch, a **team of helpers** (subagents), each with a single task, **tools** that do the
> mechanical work always the same way (searching catalogues, extracting text from a PDF,
> checking citations) and a **data folder** on your computer where all the work is kept. The AI
> is used to read, summarize and write; what can be checked is done by programs.

If you do not know a word, see the [glossary](glosario.md) (in Spanish).

## Overview

```
                        You (the researcher)
                                │
                 you type a command, e.g. /state-of-the-art
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │   Claude Code (coordinator)  │  follows the general instructions
                 └──────────────┬───────────────┘
                                │ hands out the work
          ┌─────────────────────┴───────────────────────┐
          ▼                                             ▼
  Literature review helpers                   Writing helpers
  (searcher, retriever, reader,               (writer, verifier,
   tracker, synthesizer)                        reviewer)
          │                                             │
          └──────────────────┬──────────────────────────┘
                             ▼
             Tools (programs that do mechanical tasks)
                             │
     ┌──────────────┬────────┴─────────┬─────────────────────┐
     ▼              ▼                  ▼                     ▼
 Open           Private            Project               Your data
 catalogues     databases          "shelf"               folder
 (free)         (pending)          (verified works)      (PDFs, notes,
                                                          drafts)
```

The verifier checks the draft before it is considered finished: if it finds a failure, the
draft goes back to the writer.

## The five pieces

| Piece | What it is, in simple words | Where it is (technical detail) |
|---|---|---|
| **General instructions** | The rules Claude must always follow in this project (for example, "never invent a quote") | File `CLAUDE.md` |
| **Commands** | Ready-made processes you launch by typing `/name` | Folder `.claude/skills/` |
| **Helpers (subagents)** | Copies of Claude with a single task and their own instructions | Folder `.claude/agents/` |
| **Tools** | Programs that do mechanical tasks always the same way, and "plugs" to connect to other services | Folder `tools/` (Python programs) and file `.mcp.json` (MCP plugs) |
| **Automatic checks** | Controls that trigger by themselves at certain moments, for example verifying citations before exporting | File `.claude/settings.json` (*hooks*) |

Your research data (PDFs, notes, drafts) are **not** in the program folder, but in a separate
folder on your computer (see below).

### Why a team of helpers and not a single AI?

Claude, like any AI, can only "keep in mind" a limited amount of text at once (what is called
its **context**). If it read 40 articles in a row, it would forget the first ones. So each
article is read by a different helper, which delivers a short **reading note**. The coordinator
works with the notes, not with the full articles. Besides, several helpers can work at once.

### Why programs as well as the AI?

Because the AI may answer differently each time and sometimes gets it wrong, whereas a program
always does the same thing and its result can be checked. So searching catalogues, removing
duplicates, computing the importance of a work, extracting the text of a PDF and verifying
citations are tasks for **programs**. The AI is kept for reading, interpreting, summarizing and
writing.

## The team of helpers

| Helper | Technical name | Receives | Delivers |
|---|---|---|---|
| Searcher | `searcher` | Your question and the project profile | List of works ranked by importance |
| Retriever | `retriever` | The works you chose | The PDFs that can be obtained legally and a list of those that cannot |
| Reader | `reader` | A document | Its reading note |
| Tracker | `tracker` | The notes and their bibliographies | New works worth adding (snowballing) |
| Synthesizer | `synthesizer` | All the notes | The state of the art |
| Writer | `writer` | State of the art, your goals and the journal's rules | The article draft |
| Verifier | `verifier` | The draft | A report of correct and wrong citations. **It cannot modify the draft**, only point out |
| Reviewer *(phase 8)* | `reviewer` | The draft and the journal's rules | A report like a journal referee's. **Read only** |

Decision: these seven helpers plus the reviewer are kept, so that each can be tested separately.

## Each project's profile (disciplinary profile)

Each research project has a configuration profile. That way the same system works for
philosophy, sociology, medicine or engineering: what changes is the profile. It records:

- the research question, the discipline, the languages and the period;
- where to search (which catalogues);
- how to decide which works are most important;
- how many works are read in depth and how many snowball rounds are done;
- which products you want at the end;
- the citation style and the journal the article is aimed at.

### Technical detail: profile format (`proyecto.yaml`)

The profile is the person's data, so its field names stay in Spanish (decision 0008).

```yaml
nombre: ejemplo-proyecto
pregunta: "¿...?"
disciplina: humanidades           # humanidades | sociales | salud | ingenieria | mixta
idiomas: [es, en]
periodo: {desde: 2000, hasta: 2026}
fuentes: [openalex, crossref, semantic_scholar, pubmed]   # depending on the discipline
relevancia:
  pesos: {citas: 0.2, citas_por_anio: 0.25, centralidad_red: 0.25, pertinencia: 0.25, recencia: 0.05}
limites:
  max_candidatos: 200
  max_lectura_completa: 40        # the rest get a light reading
snowballing: moderado             # ligero | moderado | exhaustivo
salidas_b7: [resumen, informe, tablas, mapa]
estilo_cita: apa-7th-edition      # style identifier in the CSL catalogue
revista_objetivo: null
```

## Where the work is kept: your data folder

The program folder and your research folder are **separate**:

- If you delete or update the program, **you do not lose your work**.
- The data folder can be synced (Drive, OneDrive, Nextcloud…) and shared with the team.
- PDFs, which are copyrighted, are never mixed with the program, which is published on GitHub.

By default the folder is `Investigacion`, inside your home folder, with one subfolder per
project (the names are in Spanish because the person uses them):

```
Investigacion/
└── nombre-del-proyecto/
    ├── proyecto.yaml         the project profile
    ├── candidatos.csv        works found, with their score and the reason (table)
    ├── seleccion.csv         the works you approved (table)
    ├── pdf/                  the documents obtained
    ├── texto/                the text extracted from each PDF, with its pages
    ├── fichas/               one reading note per document
    ├── grafo.json            the citation network (who cites whom)
    ├── biblioteca.json       the "shelf": the only works that may be cited
    ├── resumen-ejecutivo.md  one-page state of the art
    ├── estado-cuestion.md    full state of the art (also in Word)
    ├── tablas/               synthesis tables
    ├── mapa.html             visual map of the citation network (opens in the browser)
    └── borradores/           article drafts and verification reports
```

`.md` files are text with simple formatting (*Markdown*) and can be opened with any text
editor; the system also generates Word versions.

## Risks and how they are avoided

| Risk | What it means | How it is avoided |
|---|---|---|
| Too many documents at once | The AI "forgets" if given too much text, and usage has a cost | Helpers with short notes and limits in the project profile |
| Usage quota runs out mid-process | Claude subscriptions have a usage limit every few hours | Work is saved after each document and can be **resumed where it stopped** (decision 0005) |
| The PDF page is not the book page | Page 1 of the PDF may be printed page 45 | The system works out the correspondence (see [05](05-citation-verification.md)) |
| Scanned books | The PDF is a photo and must be "read" (OCR), with possible errors | Quality is recorded and those quotes are checked by hand |
| Works missing from catalogues | Common with books and in the humanities | Several catalogues and the option to add works by hand |
| Catalogues limit how many queries they accept | If abused, they block access temporarily | Keep the answers so as not to repeat questions, and identify with an e-mail |

## Technical detail: structure of the program folder

```
LoRu-Agent/
├── CLAUDE.md                   general instructions
├── README.md                   presentation (in Spanish)
├── .mcp.json                   project MCP plugs                     (phase 1+)
├── .claude/
│   ├── settings.json           permissions and automatic checks
│   ├── agents/                 helpers (subagents)
│   └── skills/                 commands /verify-citations, /prepare-pdf…
├── tools/                      Python programs
│   ├── sources/                connection to each catalogue
│   ├── pdf/                    text and page extraction
│   ├── relevance/              importance and citation network     (phase 1+)
│   └── verification/           citation verifier
├── estilos/                    citation styles and journal profiles (phase 1+)
├── plantillas/                 project and reading-note templates   (phase 1+)
├── .env.ejemplo                template of the keys and data-path file (phase 1+)
├── tests/                      automatic tests of the programs
└── docs/                       this documentation
```
