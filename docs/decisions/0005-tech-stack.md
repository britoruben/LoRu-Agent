# Decision 0005 · Tools, formats, languages and subscription

- **Status:** accepted
- **Date:** 2026-09-27
- **Decided by:** Rubén
- **Answers:** P-02, P-06, P-07 and P-08

## In short

The programs are written in **Python**; the article is delivered in **Word and PDF**; searches
are in **Spanish and English**; and Claude is used with a **Pro or Max subscription** (fixed
monthly price).

## Decision

| Topic | Decision | Why |
|---|---|---|
| Programming language (P-02) | **Python** | It is the most used for working with PDFs, texts and bibliographic data, and one of the easiest to read |
| Delivery formats (P-06) | **Word** and **PDF** (via LaTeX). The working text is kept in Markdown, a simple text format | Word to send to journals and review with track changes; LaTeX for science journals that require it |
| Languages (P-07) | Search in **Spanish and English**; write in the journal's language | Cover both Hispanic and international literature |
| Use of Claude (P-08) | **Pro or Max subscription** | Fixed, predictable cost |

## Other options considered

- **TypeScript** instead of Python: useful for certain "plugs" (MCP), but with fewer tools for
  academic work.
- **Pay per use (API)**: more control of spending per project, but variable cost and more
  configuration.

## Consequences

- Python and Pandoc (the converter to Word and PDF) will have to be installed. Later on, also a
  text recognition (OCR) tool and a search-by-meaning tool. Everything will be explained step by
  step in the installation guide.
- **Subscriptions have a usage limit every few hours.** So long processes (reading 40 documents
  or more) are **saved after each document** and can be resumed where they stopped.
- Each project's profile comes with Spanish and English as default languages.
