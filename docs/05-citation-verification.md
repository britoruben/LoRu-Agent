# 05 · Citation verification: how the AI is stopped from inventing

> **In short:** the AI **does not write references**. It can only point to works on a "shelf"
> that each book or article joins only after checking that it exists. A program formats the
> citations and another program, the verifier, compares each literal quote with the original
> text and checks the page. If something does not match, the article cannot be considered
> finished. It is the piece that makes the whole system reliable.

## The idea, with an analogy

Think of a very strict copy editor who has every cited book on the desk. For each quote in the
manuscript, they open the book at the given page and check that the text is there, verbatim. If
a cited work is not on the desk, the citation does not pass. That is what this system does,
automatically.

## The four protections

### 1. The project's shelf (verified library)

A work only joins the shelf if it has been checked that it exists:

- If it has a **DOI** (the "ID card" of a publication), the official registry (Crossref) is
  queried and it is checked that the title, year and first author match.
- If it has **no DOI** (many books, chapters and old works), it is checked by its **ISBN** or in
  library catalogues, or you add it by hand. In that case it is recorded that the check was
  manual.

For each work it also records how and when it was checked, where its PDF is and which version it
is (preprint, accepted or published).

### 2. The page map

Page 1 of the PDF is usually not page 1 of the book or journal. When extracting the text of a
PDF, the system records for each PDF page which **printed page** corresponds to it. To find out:

1. it looks at whether the PDF itself carries that information;
2. if not, it looks for the printed page number in the header or footer;
3. if that fails too, it asks you for the correspondence (for example, "page 1 of the PDF is
   printed page 45").

If it cannot be determined, the citations of that document are flagged for review by hand.

### 3. A program does the formatting

The AI only writes a label (for example `[@arendt1958, p. 45]`). A program turns it into the
citation in the right style (APA, Chicago…) and builds the final bibliography. So **there can be
no formatting errors or badly copied DOIs**.

### 4. The verifier

Before considering a draft finished, a program checks:

| What it checks | If it fails |
|---|---|
| That each cited work is on the shelf | **Failure:** non-existent work |
| That each work's DOI still works | Warning |
| That each literal quote appears in the original text | **Failure:** quote not found |
| That it appears on the given page | **Failure:** wrong page (and it proposes the right one) |
| Paraphrases (ideas attributed without a literal quote) | **Assisted check:** it looks in the original for the passage that probably corresponds and shows it next to it for you to confirm. If it does not find it, a prominent warning |
| That no `[FUENTE PENDIENTE]` gaps remain | **Blocks** the final version |

The result is a report with every issue, which you see at **checkpoint 4**.

The verifier **can only read** the draft, never modify it, and runs **automatically** before
exporting: if there are failures, it cannot be exported.

## Limits, honestly

- Checking that a **paraphrase** is faithful to the author cannot be fully automated: the system
  helps, but the last word is yours.
- With poor-quality **scanned books**, a correct quote may not be found because text recognition
  (OCR) made mistakes. Those quotes are flagged for manual review.

## Technical detail

- The shelf is `biblioteca.json` in CSL-JSON format, with additional fields (in Spanish, as the
  person's data): `verificacion` (doi | isbn | manual), `fecha_verificacion`, `pdf_local`,
  `texto_local` and `version` (preprint | aceptada | publicada).
- The page map is saved in `texto/<id>.json`:
  `{"paginas": [{"pdf": 1, "impresa": "45", "texto": "..."}], "calidad": "ok|ocr"}`. First the
  PDF's page labels are tried, then detection in header or footer, and finally the offset given
  by the person.
- Literal quote: exact match after normalizing spaces, hyphens and quotation marks; with
  configurable tolerance for OCR texts.
- Paraphrase: semantic search (*embeddings*) in the source text; the specific model is chosen in
  phase 2.
- Report in `borradores/<name>.verificacion.md`.
- The `verifier` subagent has no write permission; a Claude Code *hook* will run the verifier
  before exporting and block the export if there are failures.
