# 04 · Sources: where the system gets publications from

> **In short:** the system first searches **open, free catalogues** of scientific
> publications, which can legally be queried by a program. For the university's **paid
> databases** (Scopus, Web of Science, JSTOR…) we still have to find out how access works;
> meanwhile, the plan is not to automate anything the licences forbid.

> **Note for programmers:** the terms of use of these services (limits, need for a key) change
> often. Before connecting each one, check its official documentation and write the date in the
> "Checked" column.

## Open catalogues

They are like a library catalogue, but of publications from all over the world, and they offer
a "counter" for programs (an **API**, see the [glossary](glosario.md)).

| Catalogue | What it contains | What we use it for | Checked |
|---|---|---|---|
| OpenAlex | Publications from every discipline; very broad | Search, count citations, see who cites whom | — |
| Crossref | Official data of publications with a DOI | **Check that a work exists** and that its data are correct | — |
| Semantic Scholar | Every discipline, strong in science and engineering | Citations and references | — |
| Unpaywall | Where the free, legal version of an article is | Get texts legally | — |
| PubMed / PubMed Central | Medicine and biology | Search and get free texts | — |
| arXiv | Physics, mathematics, computer science | Drafts prior to publication (*preprints*) | — |
| CORE | University repositories worldwide | Free full texts | — |
| DOAJ | Open access journals | Search | — |
| Dialnet | Publications in Spanish, strong in humanities and social sciences | Search | **Must find out whether it allows access from programs** |
| Google Scholar | Very broad | — | **Offers no counter for programs and forbids automation: will not be used** |

## Which catalogues to use by discipline

This is the default configuration that will be proposed; each project can change it.

| Discipline | Catalogues | Usual citation style | To bear in mind |
|---|---|---|---|
| Humanities | OpenAlex, Crossref, Dialnet, library catalogues | Chicago, MLA, footnotes | Many books and chapters have no DOI; citing with a page is essential |
| Social sciences | OpenAlex, Crossref, Semantic Scholar, Dialnet | APA 7 | Mix of articles and books |
| Health and biomedicine | PubMed, PubMed Central, OpenAlex, Semantic Scholar | Vancouver, AMA | In systematic reviews (PRISMA protocol) the whole process must be repeatable |
| Engineering and computer science | OpenAlex, Semantic Scholar, arXiv, Crossref | IEEE, ACM | Many *preprints* and conference proceedings |

## Paid databases — pending

See questions P-03 and P-04 in [07 · Open questions](07-open-questions.md). These are the
options:

| Option | Can it be automated? | Is it legal? | Comment |
|---|---|---|---|
| **Official counter for programs (API)** with an institutional key (e.g. Scopus, Web of Science) | Yes | Yes, within the licence | The best option if the university offers it |
| **Logging in through the web** with the university account | Technically fragile | Licences **usually forbid** automatic or mass downloading | Not automated; the guided download option is used |
| **Guided download** | Partly | Yes | The system prepares the ranked list with links and you download the PDFs |
| **Export results** from the database (RIS, BibTeX or table file) | Yes, the part of reading the file | Yes | Very useful: you search the database, export the list and the system processes it |

## Access rules

1. The **free, legal version** is always preferred.
2. Catalogues are not abused: the number of queries is limited and answers are kept so as not
   to repeat them.
3. Keys and passwords are kept only on your computer, in the `.env` file, and are never
   published.
4. Access to paid databases only works **on your computer**, with your connection and your
   university credentials.
