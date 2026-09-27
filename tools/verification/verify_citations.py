"""
LoRu-Agent citation verifier.

What it does: reads a draft and checks each citation against the project's shelf and the
original text of each work. It writes a report with every problem found, next to the draft
(same name ending in .verificacion.md).

Why it exists: AIs sometimes invent references or alter quotes. This program is not an AI:
it always runs the same checks and cannot be talked into anything. If it finds a FALLO
(failure), the draft must not be considered finished.

What it checks:
- that each cited work is on the shelf (biblioteca.json);
- that it has been checked that the work exists (by DOI, ISBN or by hand);
- that each literal quote has a page;
- that the literal quote is, word for word, in the original;
- that it is on the given page (and, if not, on which page it is);
- that no [FUENTE PENDIENTE] gaps remain.

What it does NOT check yet: whether a paraphrase (an idea attributed without quoting it
literally) is faithful to the author. That needs assisted checking, to be built later.
Meanwhile, the report counts them so that the person reviews them.

How to use it (from the LoRu-Agent folder):
    python3 -m tools.verification.verify_citations PATH/TO/DRAFT.md

If the draft is in a project's "borradores" folder, the program finds the shelf by itself.
Otherwise, give the project folder with --project PATH.

The report and messages are in Spanish, because the person reads them (decision 0008).

Exit code: 0 if there are no failures; 1 if there are; 2 if the check could not be done.
"""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from . import search_text as search
from .read_draft import Citation, CitedWork, read_draft
from .shelf import ShelfError, load_shelf, load_text, work_is_verified

FAIL = "FALLO"
WARNING = "AVISO"


@dataclass
class Issue:
    """A problem found: what it is, where it is and what to do."""
    severity: str   # FAIL (blocks finishing) or WARNING (review it)
    line: int
    citation: str
    problem: str
    action: str


@dataclass
class VerificationResult:
    issues: list[Issue]
    total_citations: int
    quotes_checked: int
    citations_without_quote: int

    @property
    def failures(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == FAIL]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == WARNING]


def shorten(text: str, maximum: int = 90) -> str:
    """Shorten a long text to show it in the report."""
    text = " ".join(text.split())
    return text if len(text) <= maximum else text[: maximum - 1] + "…"


def check_work(citation: Citation, cited: CitedWork, shelf: dict) -> Issue | None:
    """Check that the work is on the shelf and that it has been verified that it exists."""
    work = shelf.get(cited.key)
    if work is None:
        return Issue(
            FAIL, citation.line, citation.label,
            f"La obra «{cited.key}» no está en la estantería del proyecto. "
            "Puede ser una referencia inventada o una clave mal escrita.",
            "Comprueba la clave. Si la obra existe, añádela a biblioteca.json y verifícala; "
            "si no, elimina la cita.",
        )
    if not work_is_verified(work):
        return Issue(
            FAIL, citation.line, citation.label,
            f"La obra «{cited.key}» está en la estantería, pero nadie ha comprobado "
            "que exista (su campo \"verificacion\" no es doi, isbn ni manual).",
            "Compruébala con el comprobador de DOI o a mano, y anótalo en biblioteca.json.",
        )
    return None


def check_quote(
    citation: Citation, cited: CitedWork, project_folder: Path, shelf: dict
) -> Issue | None:
    """Check that the literal quote is in the original and on the given page."""
    literal = shorten(citation.quote or "")
    if cited.page_start is None:
        return Issue(
            FAIL, citation.line, citation.label,
            f"Cita literal sin página: «{literal}».",
            "Añade la página impresa donde aparece, por ejemplo [@clave, p. 45].",
        )

    text = load_text(project_folder, shelf[cited.key])
    if text is None:
        return Issue(
            WARNING, citation.line, citation.label,
            f"No hay texto de «{cited.key}» para comprobar la cita «{literal}».",
            "Compruébala a mano con el libro o el PDF, o añade su texto al proyecto.",
        )

    if text.quality == "sin_texto":
        return Issue(
            WARNING, citation.line, citation.label,
            f"El PDF de «{cited.key}» parece escaneado y no tiene texto, así que no se ha "
            f"podido comprobar la cita «{literal}».",
            "Compruébala a mano con el libro o el PDF.",
        )

    cited_pages = cited.describe_pages()
    found = search.find_quote(citation.quote, text, cited.page_start, cited.page_end)
    where = ", ".join(found.pages_found)

    if found.outcome == search.ON_CITED_PAGE:
        if text.pagination_confirmed:
            return None
        return Issue(
            WARNING, citation.line, citation.label,
            f"La cita es exacta, pero no se sabe con seguridad la paginación impresa de "
            f"«{cited.key}» (se ha usado la numeración del PDF).",
            "Comprueba la página en el libro o el PDF, o vuelve a extraer el texto indicando "
            "la primera página impresa (--first-page).",
        )
    if found.outcome == search.SPANS_PAGES:
        pages = found.pages_found
        return Issue(
            WARNING, citation.line, citation.label,
            f"La cita es correcta, pero ocupa más de una página (pp. {pages[0]}-{pages[-1]}).",
            f"Cambia «{cited_pages}» por «pp. {pages[0]}-{pages[-1]}».",
        )
    if found.outcome == search.ON_OTHER_PAGE:
        return Issue(
            FAIL, citation.line, citation.label,
            f"Página incorrecta: la cita «{literal}» no está en {cited_pages}, "
            f"sino en la página {where}.",
            f"Corrige la página: debe ser {where}.",
        )
    if found.outcome == search.PAGE_MISSING:
        hint = f" La cita sí aparece en la página {where}." if where else ""
        return Issue(
            FAIL, citation.line, citation.label,
            f"La página {cited.page_start} no existe en el texto disponible de "
            f"«{cited.key}».{hint}",
            "Revisa el número de página.",
        )
    if found.outcome == search.SIMILAR:
        similarity = round(found.similarity * 100)
        if text.quality == "ocr":
            return Issue(
                WARNING, citation.line, citation.label,
                f"La cita casi coincide ({similarity} %) con la página {where}, pero el original "
                f"es un escaneo y puede tener errores. El texto escaneado dice: "
                f"«{shorten(found.original_passage, 200)}».",
                "Compruébala a mano con el libro o el PDF.",
            )
        return Issue(
            FAIL, citation.line, citation.label,
            f"La cita está alterada: se parece en un {similarity} % a un pasaje de la página "
            f"{where}, pero no es idéntica. El original dice: "
            f"«{shorten(found.original_passage, 200)}».",
            "Copia la cita exactamente como está en el original.",
        )
    hint = (
        f" Lo más parecido está en la página {where}: «{shorten(found.original_passage, 200)}»."
        if found.original_passage else ""
    )
    return Issue(
        FAIL, citation.line, citation.label,
        f"La cita «{literal}» no aparece en «{cited.key}».{hint}",
        "Comprueba la cita en el original. Si no está, elimínala o conviértela en paráfrasis.",
    )


def verify_draft(draft_text: str, project_folder: Path) -> VerificationResult:
    """
    Run every check on a draft.

    Receives: the text of the draft and the project folder.
    Returns: the list of issues and a count of citations.
    """
    shelf = load_shelf(project_folder)
    contents = read_draft(draft_text)
    issues = []
    quotes_checked = 0

    for line, gap in contents.pending_sources:
        issues.append(Issue(
            FAIL, line, gap,
            "Queda una fuente pendiente: el texto necesita una obra que no está en la estantería.",
            "Busca una obra que respalde la afirmación y añádela a la estantería, o reformula la frase.",
        ))

    for citation in contents.citations:
        valid_works = []
        for cited in citation.works:
            problem = check_work(citation, cited, shelf)
            if problem:
                issues.append(problem)
            else:
                valid_works.append(cited)

        if citation.quote is None or not valid_works:
            continue
        quotes_checked += 1
        # If the label cites several works, it is enough for the quote to be in one of them.
        problems = [check_quote(citation, work, project_folder, shelf) for work in valid_works]
        if all(problems):
            issues.append(problems[0])

    for uncited in contents.uncited_quotes:
        issues.append(Issue(
            WARNING, uncited.line, f"«{shorten(uncited.text, 60)}»",
            "Texto entre comillas sin etiqueta de cita. Si es una cita literal, falta la fuente.",
            "Añade la etiqueta con la página, o quita las comillas si no es una cita.",
        ))

    for line, key in contents.unrecognized_keys:
        issues.append(Issue(
            WARNING, line, key,
            "Parece una cita, pero no está escrita entre corchetes, así que no se ha comprobado.",
            f"Escríbela como [{key}, p. X] para que el verificador pueda revisarla.",
        ))

    issues.sort(key=lambda i: (i.line, i.severity != FAIL))
    return VerificationResult(
        issues=issues,
        total_citations=len(contents.citations),
        quotes_checked=quotes_checked,
        citations_without_quote=sum(1 for c in contents.citations if c.quote is None),
    )


def write_report(result: VerificationResult, draft_name: str) -> str:
    """Write the verification report in Markdown, in plain Spanish."""
    failures, warnings = result.failures, result.warnings
    if failures:
        verdict = (f"**NO APTO.** Hay {len(failures)} fallo(s). El borrador no debe darse por "
                   "terminado hasta corregirlos.")
    elif warnings:
        verdict = (f"**APTO CON AVISOS.** No hay fallos, pero hay {len(warnings)} aviso(s) que "
                   "conviene revisar.")
    else:
        verdict = "**APTO.** No se ha encontrado ningún problema en las citas comprobadas."

    lines = [
        f"# Informe de verificación de citas: {draft_name}",
        "",
        verdict,
        "",
        "| Qué se ha revisado | Cantidad |",
        "|---|---|",
        f"| Etiquetas de cita | {result.total_citations} |",
        f"| Citas literales comprobadas contra el original | {result.quotes_checked} |",
        f"| Citas sin texto literal (paráfrasis o referencias generales) | {result.citations_without_quote} |",
        f"| Fallos | {len(failures)} |",
        f"| Avisos | {len(warnings)} |",
        "",
    ]
    for title, group in (("Fallos (hay que corregirlos)", failures), ("Avisos (conviene revisarlos)", warnings)):
        if not group:
            continue
        lines += [f"## {title}", ""]
        for number, issue in enumerate(group, start=1):
            lines += [
                f"{number}. **Línea {issue.line}** · `{shorten(issue.citation, 120)}`",
                f"   - Problema: {issue.problem}",
                f"   - Qué hacer: {issue.action}",
                "",
            ]
    lines += [
        "## Lo que este informe NO garantiza",
        "",
        f"- Las {result.citations_without_quote} citas sin texto literal solo se han comprobado en cuanto "
        "a que la obra existe. **Nadie ha comprobado todavía que el autor diga lo que se le atribuye**: "
        "revísalas tú (la comprobación asistida de paráfrasis aún no está construida).",
        "- El verificador compara con el texto disponible de cada obra. Si ese texto está incompleto "
        "o mal escaneado, puede haber errores que no detecte.",
        "",
    ]
    return "\n".join(lines)


def default_project_folder(draft: Path) -> Path:
    """If the draft is in project/borradores/, the project folder is the one above."""
    folder = draft.resolve().parent
    return folder.parent if folder.name == "borradores" else folder


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Comprueba las citas de un borrador contra la estantería y los textos originales.",
    )
    parser.add_argument("draft", type=Path, help="el borrador en Markdown (.md)")
    parser.add_argument("--project", type=Path, help="carpeta del proyecto (si no se indica, se deduce)")
    options = parser.parse_args(arguments)

    draft = options.draft
    if not draft.exists():
        print(f"No encuentro el borrador {draft}. Revisa la ruta.", file=sys.stderr)
        return 2
    project_folder = options.project or default_project_folder(draft)

    try:
        result = verify_draft(draft.read_text(encoding="utf-8"), project_folder)
    except ShelfError as error:
        print(f"No he podido hacer la comprobación: {error}", file=sys.stderr)
        return 2

    report = write_report(result, draft.name)
    report_path = draft.with_name(draft.stem + ".verificacion.md")
    report_path.write_text(report, encoding="utf-8")

    print(f"Fallos: {len(result.failures)} · Avisos: {len(result.warnings)} · "
          f"Citas: {result.total_citations}")
    print(f"Informe completo en: {report_path}")
    return 1 if result.failures else 0


if __name__ == "__main__":
    sys.exit(main())
