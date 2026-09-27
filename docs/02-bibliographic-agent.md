# 02 · Bibliographic workflow: from the question to the state of the art

> **In short:** starting from your question, the system searches what has been published in
> Spanish and English, ranks it by importance explaining why, gets the texts through legal
> channels, reads them (some lightly, the most important in depth), follows their bibliographies
> to find missing works and writes a state of the art with consensus, disputes, errors and gaps.
> It asks you before searching and each time it must be decided which works go in.

The tasks are numbered **B1 to B7** ("B" for bibliographic) and correspond to the seven tasks of
the original idea.

| Step | Task | Who does it | Design status |
|---|---|---|---|
| B1 | Search open catalogues | Programs | Defined |
| B2 | Search private databases | Programs | **Pending** (question P-03) |
| B3 | Rank by importance and choose | Programs + AI + you | Defined (to be tuned with the pilot project) |
| B4 | Get the texts | Programs | Partial (depends on B2) |
| B5 | Read and write notes | AI | Defined |
| B6 | Follow references (snowballing) | Programs + AI | Defined |
| B7 | Write the state of the art | AI | Defined |

---

## B1 · Search open catalogues

1. The AI turns your question into **search terms**, with synonyms and an English translation.
2. **Checkpoint 1:** it shows them to you and you approve or correct them.
3. The programs search the catalogues chosen in the project profile (see
   [04 · Sources](04-sources-and-access.md)).
4. The results are merged and **duplicates are removed** (the same work found in several
   catalogues).
5. Result: a **table of candidate works** (`candidatos.csv`), which opens in Excel.

**Technical detail:** per-source queries via API; normalization to a common schema;
de-duplication by DOI → PMID → normalized title + year. Columns: id, title, authors, year, type,
DOI, source(s), citations, open access yes/no, URL.

## B2 · Search private databases — pending

Depends on how the institution's databases are accessed (question P-03). There are two paths:

- **If the database offers an official API** (a "counter" for programs, such as Scopus's or Web
  of Science's): it connects like the open catalogues.
- **If it can only be accessed through the web with a university account:** the system will
  **not** try to log in or download by itself, because licences usually forbid it and access
  could be cut for the whole institution. Instead, it prepares a ranked list with links and you
  download the documents into the project's `pdf/` folder.

## B3 · Rank by importance and choose

"The most cited" is not enough as a criterion: it favours old works (they have had more time to
accumulate citations), counts change between catalogues and many books, especially in the
humanities, barely appear. So importance is computed by combining five signals:

| Signal | What it measures | Why |
|---|---|---|
| Total citations | How much it has been cited overall | Accumulated impact |
| Citations per year | Citations divided by the years since publication | So as not to bury recent work |
| Weight within the topic | How much **the other works on the same topic** cite it | Usually the most reliable signal; only available after snowballing (B6) |
| Relevance | How well it fits your question, according to the AI after reading title and abstract | Filters out what is off topic |
| Recency | How recent it is | To reflect the current debate (weighs little) |

Each work in the list carries **a sentence explaining why it is where it is**, for example:
"Highly cited by the other works on the topic (12 of 40) and deals directly with question X". A
score without an explanation is not shown.

**Checkpoint 2:** you review the table and decide which works enter the study. That decision is
saved in `seleccion.csv`.

**Technical detail:** default weights, to be calibrated with the pilot project: citations 0.2 ·
citations/year 0.25 · centrality 0.25 · relevance 0.25 · recency 0.05. In the first search, when
there is no citation network yet, the centrality weight is shared among the other signals. The
table shows each signal's score separately and the reason.

## B4 · Get the texts

It tries, in this order:

1. The **open access version** (free and legal), if it exists.
2. Open repositories of universities and disciplines (arXiv, PubMed Central, CORE…).
3. The institution's private access, as decided in B2.
4. If it cannot be obtained: it is noted in a **"not available" list** to be handled by hand
   (interlibrary loan, asking the author…).

For each document it records where it comes from and **which version it is**. An article may
exist as a draft prior to review (*preprint*), accepted version or published version, and **only
the published one has the right pagination for citing**.

## B5 · Read and write notes

Each document is read by a reader helper, which fills in a **reading note**. There are two levels:

| Level | Which documents | What is read | What the note contains |
|---|---|---|---|
| **Light reading** | All those chosen | Abstract, introduction and conclusions | Thesis, method, main findings, concepts and stance |
| **Full reading** | The 40 most important (adjustable) and those you mark | The whole text | All of the above plus verbatim quotes with their page, who it argues with, limitations… |

If during synthesis a lightly read document turns out to be key in a dispute, it moves to full
reading.

Every page that appears in a note **is checked** against the document's text (see
[05](05-citation-verification.md)).

**Technical detail:** format of the full note (`fichas/<id>.yaml`); its field names stay in
Spanish because it is the person's data (decision 0008):

```yaml
id: doi:10.xxxx/yyyy
nivel: completo                      # ligero | completo
tesis_principal: "..."
preguntas: [...]
metodologia: "..."
datos_o_corpus: "..."
hallazgos: [{afirmacion: "...", pagina: 12}]
conceptos_clave: [...]
posiciona_contra: [{id: ..., en_que: "..."}]
posiciona_a_favor: [{id: ..., en_que: "..."}]
limitaciones_declaradas: [...]
limitaciones_detectadas: [...]
citas_textuales_relevantes: [{texto: "...", pagina_impresa: 45}]
calidad_extraccion: ok               # ok | ocr | parcial
```

## B6 · Follow references ("snowballing")

The idea is the same as when, reading a good article, you note down the works it cites:

- **Backwards:** which works the documents we already have cite.
- **Forwards:** which later works cite those documents.

If a work is cited by many documents on the topic and was not in our list, it is proposed as a
new candidate. With all these relations the **citation network** (who cites whom) is built,
which is used to compute B3's "weight within the topic" and to draw the visual map.

**When it stops.** Without limits, snowballing would grow endlessly. By default the
**moderate** mode is used:

- at most **2 rounds**;
- at most **30 new works per round**;
- it stops earlier if a round contributes **fewer than 3** relevant works (a sign that the topic
  is "saturated").

There are two other modes, chosen in the project profile: **light** (1 round, backwards only) and
**exhaustive** (up to 5 rounds, for systematic reviews).

Each round goes again through **checkpoint 2**: you decide which new works go in.

**Technical detail:** references preferably taken from OpenAlex/Crossref metadata; as an
alternative, extraction of the bibliography from the PDF itself (tool to be evaluated, e.g.
GROBID; question P-09). The network is saved in `grafo.json`.

## B7 · The state of the art

Four products are generated, all from the same reading notes:

| Product | What it is | When it will be ready |
|---|---|---|
| **One-page summary** | Where the debate stands, 5 key works, main disputes and gaps, and a recommendation | Phase 4 |
| **Full report** (text and Word) | The state of the art in academic prose (structure below) | Phase 4 |
| **Synthesis tables** | What each work says: stance, method and findings; table of disputes and gaps | Phase 4 |
| **Visual map** | Interactive drawing of the citation network, coloured by school or stance; opens in the browser | Phase 5 (needs B6's citation network) |

Structure of the full report:

1. **Map of the field:** lines, schools or approaches, with their reference works.
2. **Consensus:** what the literature agrees on.
3. **Disputes:** opposing positions, who holds what, with quote and page.
4. **Errors:** refuted claims or misattributed quotes in the literature, with the evidence.
5. **Gaps:** unaddressed questions; missing populations, periods or methods.
6. **Traceability table:** each claim of the report → work → page.

**Warning:** the "errors" and "gaps" the AI detects are **hypotheses to be reviewed**, not
conclusions. The report will say so explicitly.
