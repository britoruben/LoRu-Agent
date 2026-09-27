# 07 · Open questions

> **In short:** the list of what is still to be decided. It serves as the agenda for team
> meetings. The most important question is P-11 (what the project should focus on), based on
> the review of similar tools at the end of this document. When a question is answered, a
> decision note is written in [`decisions/`](decisions/) and it is marked as closed here.

## Pending

### P-01 · Which reference manager do we use?

A reference manager is a program that stores your references and PDFs and formats citations.

- **Options:** Zotero, Mendeley, EndNote or none (the system would keep its own list).
- **Recommendation: Zotero.** It is free, widely used in universities and other programs can
  connect to it easily. That lets the system read and add references automatically.
- **Blocks:** phase 1.

### P-03 · How are the institution's paid databases accessed?

- **Options:** official counter for programs (API), logging in through the web with the
  university account, exporting result lists or guided download (see
  [04 · Sources](04-sources-and-access.md)).
- **Recommendation:** the official counter if it exists; otherwise, exporting results and guided
  download.
- **Who:** Lola asks the library (see the questions below).
- **Blocks:** phase 7.

### P-04 · Which specific paid databases do we have?

- For example: Scopus, Web of Science, JSTOR, EBSCO, ProQuest, Dialnet Plus…
- **Blocks:** phase 7.

### P-05 · What is the pilot project and which discipline do we start with?

- A real, bounded research question to test the system with.
- **Recommendation:** start with the discipline in which it will be used first.
- **Blocks:** phase 3. **It is the most important question**: without it we cannot check whether
  the system is useful.

### P-09 · How is the bibliography of each PDF extracted?

- **Options:** take it from the catalogues (OpenAlex, Crossref) or read it from the PDF itself
  with a specialized tool (for example GROBID).
- **Recommendation:** catalogues first; the specialized tool only if many references are missing
  (likely in the humanities).
- **Blocks:** phase 5. It is a technical decision: whoever programs can take it.

### P-11 · Full pipeline, or the best citation-verification layer? *(most important)*

The review of similar tools (see [Similar tools](#similar-tools-review-of-2026-09-27) below)
shows that the **full pipeline** (search → reading → synthesis → writing → verification)
already exists as free software on the same platform, with far more people behind it. What
we did **not** find is a tool that checks, always the same way, that each **literal quote**
is word for word in the original and on the right **printed page**. That is our strongest
contribution, especially for philosophy and the humanities.

- **Options:**
  1. **Full pipeline**, as designed in phases 3–8.
  2. **Verification layer:** make LoRu-Agent the best tool for checking quotes and pages,
     working on its own and connecting to what already exists (Zotero, reference checkers,
     paraphrase checkers, and possibly the pipeline of another project).
  3. **Mixed:** the verification layer as the core, plus only those pipeline pieces no other
     tool covers well for our disciplines (for example, Spanish-language sources such as
     Dialnet, or classical citation systems).
- **Recommendation:** option 3. The project is volunteer work by two people: effort should
  go where we can be the best, and everything else should be reused rather than rebuilt.
- **Consequences if chosen:** phases 3–8 of the [phased plan](06-phased-plan.md) and
  several documents must be rewritten; a decision note is written.
- **Blocks:** planning of everything after phase 2. Decide before P-05 if possible.

### P-12 · Which disciplines, and what does each really need?

The goal is a top-quality tool for **philosophy, biology and AI-related fields**. Their
needs differ a lot, and the current design fits philosophy best:

| Discipline | What matters most | What we lack today |
|---|---|---|
| Philosophy | Literal quotes with printed page; books, editions and translations | **Classical citation systems** (Stephanus *Rep.* 514a, Bekker 1094a1, Kant A/B, *Akademie-Ausgabe*, Diels-Kranz); editions and translations on the shelf; Roman numerals; Greek and German text; footnotes |
| Biology | Whether the source really supports the claim; retractions; data | Claim-support checking (paraphrases), retraction and erratum checks, PubMed |
| AI-related fields | Fast-moving preprints; conference papers without DOI | arXiv versions (v1, v2…), DBLP, proceedings |

- **Recommendation:** start with philosophy (where we are strongest and least covered) and
  add biology and AI by reusing existing tools for their needs.
- **Blocks:** P-05 (the pilot project should be in the first discipline chosen).

### P-13 · Licence and openness

The repository has **no licence file**, so nobody can legally reuse the code, even though the
project is meant to be volunteer, open work.

- **Options:** MIT or Apache-2.0 (anyone can reuse it, even commercially); a copyleft licence
  such as GPL (derived works must stay open); a non-commercial licence (not "open source" in
  the strict sense).
- **Recommendation:** Apache-2.0 or MIT, the most common for research tools and compatible
  with reusing tools such as PaperQA2 (Apache-2.0) and SemanticCite (MIT). Decide before
  making the repository public.
- **Also:** a `CITATION.cff` file so others can cite the project, and a short guide for
  contributors.

### P-14 · How will we show that the tool works?

Today the verifier has only been tested with fictitious texts. A top-quality tool, and a
publishable one, needs evidence.

- **Proposal:** build a small collection of real quotation errors from published articles
  in our disciplines, measure how many the verifier detects and how many false alarms it
  raises, and compare with the tools below. Later, a trial with 5–10 researchers per
  discipline using their own texts.
- **Why it matters:** it would turn the project from a tool into a research contribution
  (an article), and it tells us honestly where it fails.
- **Blocks:** nothing now; it depends on P-05 and P-11.

## Questions for the university library (P-03 and P-04)

1. Which databases are we subscribed to?
2. Does any offer researchers a **counter for programs (API)** with their own key? For example,
   Elsevier offers one for Scopus and Clarivate for Web of Science.
3. What do the licences say about **automatic text analysis and automatic downloading**
   (*text and data mining*, TDM)?
4. How is access from off campus: through VPN, the library portal or the institutional account?
5. Is there a download limit per person?

## Similar tools (review of 2026-09-27)

A web search for free-software tools that do the same or something similar. **Limits:** one
session's search, not a systematic review; star counts are those shown on each public page
that day and were not cross-checked. Not finding a tool does not prove it does not exist.
To be reviewed again before deciding P-11.

| Project | Stars | What it does | Compared with LoRu-Agent |
|---|---|---|---|
| [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) | ~49.6k (to be confirmed) | Full pipeline on Claude Code: systematic review (PRISMA), writing, simulated peer review, human checkpoints, APA/Chicago/MLA, Spanish interface | **Essentially our full-pipeline idea, already built.** Checks that references exist and that claims match sources; no literal-quote or printed-page checking found. Non-commercial licence (CC-BY-NC) |
| [PaperQA2](https://github.com/future-house/paper-qa) | ~9k | Answers questions over papers with page citations; contradiction and retraction checks | Far ahead in reading and synthesis of science; made for articles, not books. Apache-2.0 |
| [STORM](https://github.com/stanford-oval/storm) | ~31.5k | Wikipedia-style reports with citations from web search | Automatic synthesis, no rigorous academic verification. MIT |
| [AI Research Skills](https://github.com/orchestra-research/AI-research-SKILLs) | ~13.1k | Research skills for AI, including reference verification | Strong in AI, nothing for the humanities. MIT |
| [RefChecker](https://github.com/markrussinovich/refchecker), [Hallucinator](https://github.com/emidec/hallucinator), [HalRef](https://github.com/davidjurgens/hallucinated-reference-finder), [refaudit](https://github.com/uw-share-lab/refaudit), [HalluCite](https://github.com/se-uhd/hallucite) | RefChecker ~524 | Check that references exist and their data match (Crossref, OpenAlex, DBLP, retractions) | **Better than our DOI checker** at the same job, with more catalogues: reuse rather than extend ours |
| [SemanticCite](https://github.com/sebhaan/semanticcite) | — | Checks whether the full text of a source supports a claim (supported / partly / not / uncertain) | This is our pending "assisted paraphrase check", already built. MIT |
| [Zotero MCP](https://github.com/54yyyu/zotero-mcp) and variants | — | Connect Zotero to Claude | Covers our phase 1 (P-01) without building anything |

A July 2026 review of five of these checkers ([Badalova & Mayr](https://arxiv.org/abs/2607.22693))
found they all stop at checking that references exist, with errors in extracting references
and limited catalogue coverage; quotations and pages are not assessed. Research on quotation
errors exists ([arXiv 2606.08589](https://arxiv.org/pdf/2606.08589),
[CiteCheck](https://arxiv.org/pdf/2605.27700)), but we found no ready-to-use tool.

### Assessment (0–10), as of 2026-09-27

| Aspect | Score | Why |
|---|---|---|
| Novelty of the full pipeline | 3 | Already built by another free project on the same platform |
| Novelty of literal-quote and printed-page verification | 7 | A real, useful gap, especially in the humanities |
| Usefulness for philosophy / biology / AI today | 6 / 3 / 3 | See P-12 |
| Technical state | 3 | Solid prototype, tested only with fictitious PDFs |
| Documentation | 7 | Clear and honest; describes much more than exists; no licence |
| **Overall** | **5** | Good core, scope too wide for two people |

### What a 10 would need

- **Technical:** classical citation systems and editions/translations (P-12); real PDFs (OCR,
  two columns, footnotes, non-Latin scripts); reuse existing tools for reference checking,
  paraphrases and Zotero; per-discipline catalogues (PubMed, arXiv versions, DBLP); a test
  collection of real errors with measured results (P-14).
- **Research:** a real pilot project (P-05); a publishable evaluation against the tools above
  (P-14); trials with researchers from each discipline.
- **Documentation and project:** a licence, `CITATION.cff` and a contributors' guide (P-13);
  documents trimmed to what will really be built once P-11 is decided; a demo video or
  screenshots; an honest comparison with other tools in the repository (this section is a
  first version).
- **Constraint to respect:** volunteer work by two people. Choose depth in one area over
  breadth, and prefer reusing tools over building them.

## Closed

| Question | Decision | Note |
|---|---|---|
| P-02 · In which language are the tools programmed? | Python | [Decision 0005](decisions/0005-tech-stack.md) |
| P-06 · In which formats is the article delivered? | Word and PDF (the working text in Markdown) | [Decision 0005](decisions/0005-tech-stack.md) |
| P-07 · In which languages do we search and write? | Search in Spanish and English; write in the journal's language | [Decision 0005](decisions/0005-tech-stack.md) |
| P-08 · How is the use of Claude paid for? | Pro or Max subscription | [Decision 0005](decisions/0005-tech-stack.md) |
| P-10 · Where are the data kept? | In a folder separate from the program | [Decision 0003](decisions/0003-data-outside-repo.md) |
