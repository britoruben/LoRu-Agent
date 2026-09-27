# Decision 0007 · Use pypdf (and not MarkItDown) to read PDFs

- **Status:** accepted
- **Date:** 2026-09-27
- **Decided by:** Rubén

## In short

**pypdf** is used to take the text out of PDFs, because it reads the page numbering many PDFs
carry and allows working page by page. **MarkItDown** (by Microsoft) was considered, but in the
tests it did not know which printed page number each page has and, with a scanned PDF, it
returned an empty document without warning.

## Situation

The citation verifier needs the text of each work **page by page** and with its **printed
page**. The tool that reads PDFs had to be chosen.

## What was tested (2026-09-27, MarkItDown 0.1.8 and pypdf 6.19)

With test PDFs created for the occasion:

| Test | MarkItDown | pypdf |
|---|---|---|
| Text of a normal PDF | Correct | Correct |
| Separating pages | Yes, with an invisible character, but it is a side effect of the internal library it uses and is not documented | Yes, page by page |
| Reading the PDF's own numbering (pdf 1 = "45") | No | Yes (although, if the PDF has none, it makes up "1, 2, 3…": this must be checked first) |
| Scanned PDF (image only) | Returns an empty document **without warning** | Returns empty pages; our program detects it and warns |
| Additional packages it installs | 6 (and more with the PDF module) | None |

In both cases our own program was needed to find the printed page, remove headers and warn about
scans: MarkItDown did not save that work.

## Decision

- **pypdf** for PDFs, with the program `tools/pdf/extract_text.py`.
- **MarkItDown** remains a candidate for other formats (Word, EPUB, web pages), useful for the
  person's own documents, which have no printed pages to cite.

## Consequences

- One package has to be installed: `pypdf` (see `docs/instalacion.md`).
- Scanned PDFs still cannot be read: text recognition (OCR) tools will be needed, to be decided
  later.
