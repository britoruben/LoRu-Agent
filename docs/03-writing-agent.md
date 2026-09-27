# 03 · Writing workflow: from the state of the art to the article

> **In short:** with the state of the art, your own materials and your goals, the system
> proposes an outline. When you approve it, it writes the article section by section following
> the rules of the journal you choose. The AI never writes a reference on its own: it can only
> use works from the project's verified "shelf". Before finishing, a verifier checks each
> citation against the original text.

The tasks are numbered **R1 to R4** ("R" for *redacción*, writing).

| Step | Task | Who does it | Design status |
|---|---|---|---|
| R1 | Write integrating the state of the art and your materials | AI + you | Defined |
| R2 | Adapt to the journal's or publisher's rules | Programs + AI | Defined |
| R3 | Literal quotes with their page | Programs + AI | Defined |
| R4 | Avoid invented or badly formatted citations | Programs | Defined (it is the key piece) |

---

## R1 · Write the article

**What it needs from you:** besides the state of the art, your own materials (drafts, notes,
data) and some basic guidance: goals, hypotheses or thesis, methodology, article type
(empirical, review, theoretical essay…) and length.

**How it works:**

1. The writer proposes an **outline**: structure, central argument and which works are used in
   each section.
2. **Checkpoint 3:** you approve or correct the outline. Without your approval it does not start
   writing.
3. It writes **section by section**. After each one it shows it to you, together with the check
   of its citations. You can step in or let it continue.
4. It assembles the full article and prepares it for the journal (R2–R4).
5. **Checkpoint 4:** you review the final version.

**How the writer cites.** It never writes a full reference. It puts a "label" pointing to a work
on the project's shelf, for example `[@arendt1958, p. 45]`. Afterwards, a program turns those
labels into citations with the right format. If it needs a work that is not on the shelf, it
writes `[FUENTE PENDIENTE: description]` for you to decide.

## R2 · Adapt to the journal or publisher

**Where the rules come from.** You provide the journal's official author guidelines (as a PDF or
a link). The system summarizes them in a **journal profile** that you check. The profile is saved
and serves for future articles in that journal. If the guidelines are more than a year old, the
system warns that they may be out of date.

**What the journal profile records:** length, mandatory structure, abstract and keywords,
citation style, language, anonymization for blind review, rules for figures and tables, required
statements (funding, ethics, conflict of interest and **use of AI**) and specific rules.

**Use of AI:** many journals require declaring whether AI was used in writing. The profile
records each journal's policy and the draft will include the corresponding statement.

**Format and delivery:**

- The **format of citations and bibliography** (APA, Chicago, Vancouver…) is applied by a
  program, not the AI, so it is always correct.
- The article is delivered in **Word** and **PDF (LaTeX)**, using the journal's template if it has
  one.
- It is written in the journal's language (Spanish or English).

**Technical detail:** profile in `estilos/revistas/<journal>.yaml` with the source and date of
the guidelines. Citation formatting with Pandoc + citeproc and the journal's CSL style. The
working text is in Markdown and is exported with Pandoc to `.docx` (reference template) and to
LaTeX/PDF (journal class).

## R3 · Literal quotes with their page

- Each verbatim quote in the draft is searched **word for word** in the text of the original
  document. Minor differences such as spaces, hyphens or quotation mark types are tolerated, and
  somewhat more if the document is a scan.
- The page is taken from the **printed page**, not the PDF numbering.
- If the quote does not appear, it is marked as a **failure** and cannot stay in the final
  version.

## R4 · Avoid invented citations

It is the most important part of the system and is explained in detail in
[05 · Citation verification](05-citation-verification.md).

A special case is **paraphrases** (when an idea is attributed to an author without quoting them
literally). They cannot be checked one hundred per cent automatically. The verifier looks in the
original text for the passage that probably corresponds, places it next to the paraphrase and
**you confirm** whether it is faithful.

## The reviewer (eighth helper, phase 8)

Later on a helper will be added that reads the draft as the journal's referee would:
originality with respect to the state of the art, coherence of the argument, suitability of the
method, compliance with the rules and foreseeable objections. It delivers a report **and does not
touch the draft**.
