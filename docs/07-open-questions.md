# 07 · Open questions

> **In short:** the list of what is still to be decided. It serves as the agenda for team
> meetings. When a question is answered, a decision note is written in
> [`decisions/`](decisions/) and it is marked as closed here.

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

## Questions for the university library (P-03 and P-04)

1. Which databases are we subscribed to?
2. Does any offer researchers a **counter for programs (API)** with their own key? For example,
   Elsevier offers one for Scopus and Clarivate for Web of Science.
3. What do the licences say about **automatic text analysis and automatic downloading**
   (*text and data mining*, TDM)?
4. How is access from off campus: through VPN, the library portal or the institutional account?
5. Is there a download limit per person?

## Closed

| Question | Decision | Note |
|---|---|---|
| P-02 · In which language are the tools programmed? | Python | [Decision 0005](decisions/0005-tech-stack.md) |
| P-06 · In which formats is the article delivered? | Word and PDF (the working text in Markdown) | [Decision 0005](decisions/0005-tech-stack.md) |
| P-07 · In which languages do we search and write? | Search in Spanish and English; write in the journal's language | [Decision 0005](decisions/0005-tech-stack.md) |
| P-08 · How is the use of Claude paid for? | Pro or Max subscription | [Decision 0005](decisions/0005-tech-stack.md) |
| P-10 · Where are the data kept? | In a folder separate from the program | [Decision 0003](decisions/0003-data-outside-repo.md) |
