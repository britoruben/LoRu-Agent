"""
Load the project's "shelf" and the text of each work.

Why it exists: the verifier needs two things from each project:

1. The shelf (file biblioteca.json): the list of works that may be cited, each with a key
   (for example "arendt1958") and a note of whether it has been checked that it exists.
2. The text of each work, page by page, with the printed page that corresponds to each
   PDF page (files in the texto/ folder).

biblioteca.json format: a list of works in the standard CSL-JSON format (the same one
Zotero exports), with some fields of this project:
    "verificacion": "doi" | "isbn" | "manual" | "pendiente"
    "texto_local": path to the text file, relative to the project folder

Format of a text file (texto/<key>.json), created by tools/pdf/extract_text.py:
    {"calidad": "ok" | "ocr" | "sin_texto",
     "origen_paginacion": "indicada_a_mano" | "numeracion_del_pdf" | "numeros_detectados"
                          | "sin_determinar",
     "paginas": [{"pdf": 1, "impresa": "45", "texto": "..."}, ...]}

The field names and values of these files stay in Spanish: they are the person's data
(decision 0008).
"""

import json
from dataclasses import dataclass
from pathlib import Path

VALID_VERIFICATIONS = {"doi", "isbn", "manual"}


class ShelfError(Exception):
    """A problem with the project files, explained in plain language."""


@dataclass
class Page:
    """A page of the document: its number in the PDF, its printed number and its text."""
    pdf: int
    printed: str
    text: str


@dataclass
class WorkText:
    """The full text of a work, page by page."""
    pages: list[Page]
    quality: str  # "ok" if the text is reliable; "ocr" if it comes from a scan; "sin_texto" if there is no text
    pagination_source: str = "sin_dato"  # how the printed page was found

    @property
    def pagination_confirmed(self) -> bool:
        """Tell whether the printed page of each page is known for sure."""
        return self.pagination_source != "sin_determinar"


def read_json(path: Path, what: str):
    """Read a JSON file and, if it fails, explain the problem in Spanish."""
    if not path.exists():
        raise ShelfError(f"No encuentro {what} en {path}.")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ShelfError(
            f"El archivo {path} ({what}) está mal escrito cerca de la línea {error.lineno}. "
            "Revisa que no falten comillas, comas o llaves."
        ) from error


def load_shelf(project_folder: Path) -> dict[str, dict]:
    """
    Load the project's works.

    Receives: the project folder.
    Returns: a dictionary that maps each key to the data of its work.
    """
    works = read_json(project_folder / "biblioteca.json", "la estantería del proyecto")
    if not isinstance(works, list):
        raise ShelfError("biblioteca.json debe contener una lista de obras entre [ ].")
    shelf = {}
    for work in works:
        if "id" not in work:
            raise ShelfError(
                f"Hay una obra sin clave (campo \"id\") en biblioteca.json: {work.get('title', work)}"
            )
        shelf[work["id"]] = work
    return shelf


def work_is_verified(work: dict) -> bool:
    """Tell whether it has been checked that the work exists (by DOI, ISBN or by hand)."""
    return work.get("verificacion") in VALID_VERIFICATIONS


def load_text(project_folder: Path, work: dict) -> WorkText | None:
    """
    Load the text of a work, if there is one.

    Returns: the text page by page, or None if the work has no text available.
    """
    relative_path = work.get("texto_local")
    if not relative_path:
        return None
    data = read_json(project_folder / relative_path, f"el texto de la obra {work['id']}")
    pages = [
        Page(pdf=p["pdf"], printed=str(p["impresa"]), text=p["texto"])
        for p in data.get("paginas", [])
    ]
    return WorkText(
        pages=pages,
        quality=data.get("calidad", "ok"),
        pagination_source=data.get("origen_paginacion", "sin_dato"),
    )
