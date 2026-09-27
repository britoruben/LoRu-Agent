# Tools

> **In short:** the programs that do the mechanical work, always in the same way. Each file
> starts with a plain-language explanation of what it does and why.

| Folder / file | What it does |
|---|---|
| `verification/verify_citations.py` | The verifier: checks every citation in a draft and writes the report |
| `verification/read_draft.py` | Finds the citations, literal quotes and pending gaps in the draft |
| `verification/search_text.py` | Searches for a quote in the original text and checks the page |
| `verification/normalize.py` | Removes unimportant typographic differences before comparing |
| `verification/shelf.py` | Loads the project's shelf and the text of each work |
| `pdf/extract_text.py` | Takes the text out of a PDF page by page, with its printed page, and warns about scans |
| `pdf/pagination.py` | Finds the printed page and removes headers and page numbers |
| `sources/crossref.py` | Asks Crossref whether a DOI exists and compares the data |
| `sources/check_dois.py` | Checks every DOI on a shelf |

Messages and reports shown to the person stay in Spanish, as do the data files of each
project (`biblioteca.json`, `texto/`, `borradores/`): see decision 0008.

The automatic tests of these programs are in the `tests/` folder.
