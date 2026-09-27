---
name: prepare-pdf
description: Extracts the text of a PDF page by page, with its printed page, so that the citation verifier can check quotes from that work. Use when a PDF is added to a project or when asked to prepare, read or extract the text of a PDF (preparar, leer o extraer el texto de un PDF).
---

# Prepare the text of a PDF

Talk to the person in Spanish.

1. Find out: the PDF path, the project folder and the work's key in `biblioteca.json`.
   If the work is not on the shelf, say so: it must be added and checked first.
2. Run (with the `.venv` virtual environment if it exists):
   `python -m tools.pdf.extract_text PATH.pdf --project FOLDER --key KEY`
3. Explain the result in plain language:
   - how many pages and which printed pages;
   - **how the pagination was found** (given by hand, from the PDF, deduced or undetermined);
   - the warnings, without softening them. If the PDF looks scanned, say clearly that its
     quotes cannot be checked automatically.
4. If the pagination is "sin determinar" (undetermined), ask the person which printed page
   is the first page of the PDF and repeat with `--first-page N`. Do not guess it.
5. If the work had no `texto_local` in `biblioteca.json`, say that
   `"texto_local": "texto/KEY.json"` must be added, and do it only if asked.
6. Open the extracted text and look at one page: if you see repeated headers, mixed-in
   footnotes or scrambled two-column text, say so.
