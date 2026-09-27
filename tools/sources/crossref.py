"""
Check in Crossref that a work with a DOI exists and that its data are correct.

What Crossref is: the official registry where publishers record their publications with a
DOI (the "ID card" of each publication). If a DOI is not in Crossref, it almost certainly
does not exist.

Why this module exists: an AI may invent a DOI, or give a real one that belongs to another
work, or get the DOI right and the year or author wrong. This module asks Crossref about
the DOI and compares its answer with the data on our shelf: title, year and surname of the
first author.

It needs an internet connection. Crossref asks callers to identify themselves with an
e-mail address: it is taken from the LORU_CORREO variable in the .env file.
"""

import json
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from difflib import SequenceMatcher

CROSSREF_URL = "https://api.crossref.org/works/"
MIN_TITLE_SIMILARITY = 0.85

CONFIRMED = "confirmed"
MISMATCHED = "mismatched"
NOT_FOUND = "not_found"


class CrossrefConnectionError(Exception):
    """Could not talk to Crossref (no internet, service down...)."""


@dataclass
class CheckResult:
    key: str
    doi: str
    outcome: str
    mismatches: list[str] = field(default_factory=list)


def query_doi(doi: str, email: str, timeout: int = 20) -> dict | None:
    """
    Ask Crossref about a DOI.

    Returns: the data Crossref has on that work, or None if the DOI does not exist.
    Raises CrossrefConnectionError if the query cannot be made.
    """
    url = CROSSREF_URL + urllib.parse.quote(doi) + "?" + urllib.parse.urlencode({"mailto": email})
    request = urllib.request.Request(url, headers={"User-Agent": f"LoRu-Agent (mailto:{email})"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.load(response)["message"]
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise CrossrefConnectionError(
            f"Crossref ha respondido con un error ({error.code}). Inténtalo más tarde."
        ) from error
    except (urllib.error.URLError, TimeoutError) as error:
        raise CrossrefConnectionError(
            "No he podido conectar con Crossref. Comprueba tu conexión a internet."
        ) from error


def simplify(text: str) -> str:
    """Remove accents, capitals and signs to compare names and titles."""
    no_accents = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return " ".join("".join(c if c.isalnum() else " " for c in no_accents.casefold()).split())


def year_of(data: dict, *fields: str) -> int | None:
    """Get the publication year from a work's data (CSL or Crossref format)."""
    for name in fields:
        try:
            return int(data[name]["date-parts"][0][0])
        except (KeyError, IndexError, TypeError, ValueError):
            continue
    return None


def compare_with_crossref(work: dict, crossref_data: dict) -> list[str]:
    """
    Compare a work on the shelf with what Crossref says.

    Returns: the list of differences, explained in Spanish. Empty if everything matches.
    """
    differences = []

    our_title = simplify(work.get("title", ""))
    crossref_title = simplify(" ".join(crossref_data.get("title", [])))
    similarity = SequenceMatcher(None, our_title, crossref_title).ratio()
    if similarity < MIN_TITLE_SIMILARITY:
        differences.append(
            f"Título distinto. Estantería: «{work.get('title', '')}». "
            f"Crossref: «{' '.join(crossref_data.get('title', []))}»."
        )

    our_year = year_of(work, "issued")
    crossref_year = year_of(crossref_data, "issued", "published-print", "published-online")
    if our_year and crossref_year and our_year != crossref_year:
        differences.append(f"Año distinto. Estantería: {our_year}. Crossref: {crossref_year}.")

    our_authors = work.get("author", [])
    crossref_authors = crossref_data.get("author", [])
    if our_authors and crossref_authors:
        our_surname = simplify(our_authors[0].get("family", ""))
        crossref_surname = simplify(crossref_authors[0].get("family", ""))
        if our_surname != crossref_surname:
            differences.append(
                f"Primer autor distinto. Estantería: {our_authors[0].get('family')}. "
                f"Crossref: {crossref_authors[0].get('family')}."
            )
    return differences


def check_work(work: dict, email: str, query=query_doi) -> CheckResult:
    """
    Check a work that has a DOI.

    The "query" parameter lets the automatic tests replace the real internet query with
    prepared answers.
    """
    doi = work["DOI"].strip()
    data = query(doi, email)
    if data is None:
        return CheckResult(work["id"], doi, NOT_FOUND)
    differences = compare_with_crossref(work, data)
    return CheckResult(work["id"], doi, MISMATCHED if differences else CONFIRMED, differences)
