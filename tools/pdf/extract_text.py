"""
Extract the text of a PDF, page by page, with its printed page.

What it does: reads a PDF and creates the text file used by the citation verifier
(texto/<key>.json), with each page, its number in the PDF and its printed page. It removes
repeated headers and page numbers, and warns about problems.

Why it exists: the verifier compares each quote with the original text. This program is
the bridge between the PDF you download and that text.

What it does NOT do:
- It does not read scanned PDFs (photos of pages). It detects them and warns: text
  recognition (OCR) will be needed, and it is not built yet.
- It does not recognize pages numbered with Roman numerals.
- It does not properly separate two-column text or footnotes: they may end up mixed.

How to use it (from the LoRu-Agent folder):
    python3 -m tools.pdf.extract_text BOOK.pdf --project FOLDER --key ficticia2021
Options:
    --first-page 45     if you know that page 1 of the PDF is printed page 45
    --output FILE.json  to save the result somewhere else

Exit code: 0 if all went well; 1 if extracted with important warnings (scan or
undetermined pagination); 2 if the PDF could not be read.
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError
except ImportError:
    raise ImportError(
        "Falta el paquete pypdf, que sirve para leer PDF. Instálalo con:\n"
        "    python3 -m pip install -r requirements.txt\n"
        "(ver docs/instalacion.md)"
    ) from None

# pypdf writes technical warnings in English when a PDF has minor defects. They are
# silenced because this program already explains, in Spanish, the problems that matter.
logging.getLogger("pypdf").setLevel(logging.ERROR)

from . import pagination

# A page with fewer letters than this is taken as empty (probably an image).
MIN_LETTERS_PER_PAGE = 20


class PdfError(Exception):
    """A problem reading the PDF, explained in plain language."""


@dataclass
class ExtractedText:
    source: str
    pages: list[dict]
    quality: str                 # "ok" or "sin_texto" (looks scanned)
    pagination_source: str
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        """Return the content with the field names of the text file (in Spanish, decision 0008)."""
        return {
            "fuente": self.source,
            "calidad": self.quality,
            "origen_paginacion": self.pagination_source,
            "avisos": self.warnings,
            "paginas": self.pages,
        }


def open_pdf(path: Path) -> PdfReader:
    """Open a PDF or explain why it cannot be opened."""
    if not path.exists():
        raise PdfError(f"No encuentro el PDF {path}. Revisa la ruta.")
    try:
        reader = PdfReader(str(path))
        if reader.is_encrypted:
            raise PdfError(f"El PDF {path.name} está protegido con contraseña. Ábrelo y guárdalo sin protección.")
        return reader
    except PdfReadError as error:
        raise PdfError(f"No he podido leer {path.name}: el archivo parece dañado o no es un PDF.") from error


def pdf_own_labels(reader: PdfReader) -> list[str] | None:
    """
    Return the page numbering carried by the PDF itself, if any.

    Important: if the PDF defines no numbering, pypdf still returns "1", "2", "3"...
    That is why it first checks that the PDF really defines one.
    """
    if "/PageLabels" not in reader.trailer["/Root"]:
        return None
    return list(reader.page_labels)


def read_lines(reader: PdfReader) -> list[list[str]]:
    """Return the text lines of each page (empty list if the page has no text)."""
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        lines = [line for line in text.splitlines() if line.strip()]
        letters = sum(c.isalpha() for c in text)
        pages.append(lines if letters >= MIN_LETTERS_PER_PAGE else [])
    return pages


def decide_printed_pages(
    reader: PdfReader, lines: list[list[str]], first_page: int | None
) -> tuple[list[str], str, list[str]]:
    """
    Decide the printed page of each PDF page (see pagination.py).

    Returns: the list of printed pages, how it was found and the warnings.
    """
    total = len(lines)
    if first_page is not None:
        return [str(first_page + i) for i in range(total)], pagination.SOURCE_MANUAL, []
    own = pdf_own_labels(reader)
    if own:
        return own, pagination.SOURCE_PDF, []
    detected = pagination.assign_printed_pages(lines)
    if detected is not None:
        printed, warnings = detected
        return printed, pagination.SOURCE_DETECTED, warnings
    return [str(i + 1) for i in range(total)], pagination.SOURCE_UNDETERMINED, []


def extract_text(pdf_path: Path, first_page: int | None = None) -> ExtractedText:
    """
    Extract the text of a PDF with its printed pagination.

    Receives: the path of the PDF and, optionally, the printed page of the first page.
    Returns: an ExtractedText ready to be saved as texto/<key>.json.
    """
    reader = open_pdf(pdf_path)
    lines = read_lines(reader)
    printed, source, warnings = decide_printed_pages(reader, lines, first_page)

    lines = [pagination.remove_page_number(l, p) for l, p in zip(lines, printed)]
    lines = pagination.remove_repeated_headers(lines)

    pages = [
        {"pdf": position, "impresa": p, "texto": "\n".join(l)}
        for position, (l, p) in enumerate(zip(lines, printed), start=1)
    ]
    empty = [p["pdf"] for p in pages if not p["texto"]]
    quality = "ok"
    if len(empty) > len(pages) / 2:
        quality = "sin_texto"
        warnings.append("La mayoría de las páginas no tienen texto: el PDF parece escaneado. "
                        "Hará falta reconocimiento de texto (OCR), que aún no está disponible.")
    elif empty:
        warnings.append(f"Páginas del PDF sin texto (quizá imágenes o páginas en blanco): {empty}.")
    if source == pagination.SOURCE_UNDETERMINED:
        warnings.append("No he podido averiguar la página impresa: uso la numeración del PDF. "
                        "Si sabes qué página impresa es la primera, repite con --first-page.")
    return ExtractedText(pdf_path.name, pages, quality, source, warnings)


SOURCE_EXPLANATION = {
    pagination.SOURCE_MANUAL: "la has indicado tú",
    pagination.SOURCE_PDF: "la trae el propio PDF",
    pagination.SOURCE_DETECTED: "la he deducido de los números de página impresos",
    pagination.SOURCE_UNDETERMINED: "NO se ha podido averiguar",
}


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extrae el texto de un PDF con su página impresa.")
    parser.add_argument("pdf", type=Path, help="el PDF")
    parser.add_argument("--project", type=Path, help="carpeta del proyecto (guarda en su carpeta texto/)")
    parser.add_argument("--key", help="clave de la obra en la estantería (nombre del archivo de salida)")
    parser.add_argument("--output", type=Path, help="archivo de salida (en lugar de --project y --key)")
    parser.add_argument("--first-page", type=int, help="página impresa de la primera página del PDF")
    options = parser.parse_args(arguments)

    if options.output:
        output = options.output
    elif options.project and options.key:
        output = options.project / "texto" / f"{options.key}.json"
    else:
        print("Indica dónde guardar el resultado: --project CARPETA --key CLAVE, o --output ARCHIVO.json",
              file=sys.stderr)
        return 2

    try:
        extracted = extract_text(options.pdf, options.first_page)
    except PdfError as error:
        print(error, file=sys.stderr)
        return 2

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(extracted.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    pages = extracted.pages
    print(f"Páginas: {len(pages)} (impresas {pages[0]['impresa']} a {pages[-1]['impresa']}).")
    print(f"Paginación: {SOURCE_EXPLANATION[extracted.pagination_source]}.")
    for warning in extracted.warnings:
        print(f"AVISO: {warning}")
    print(f"Texto guardado en: {output}")
    important = extracted.quality != "ok" or extracted.pagination_source == pagination.SOURCE_UNDETERMINED
    return 1 if important else 0


if __name__ == "__main__":
    sys.exit(main())
