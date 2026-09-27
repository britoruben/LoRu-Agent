"""
Find the printed page of each page of a PDF and clean headers and footers.

Why it exists: citations must use the printed page (the one in the book or journal), not
the PDF's. Page 1 of a PDF may be page 45 of the book. Besides, each page usually carries a
repeated header (the book title, the author's name) and the page number, which are not part
of the text and get in the way when searching for quotes.

How it finds the printed page, in this order of preference:
1. If the person gives it ("page 1 of the PDF is printed page 45").
2. If the PDF carries its own page numbering (many publishers' PDFs do).
3. If it finds page numbers in the first or last lines and they fit together.
   Each page keeps the number printed on it; pages without a number are filled in from
   their neighbours (45, 46, no number, 48 → the third is 47). If the numbering jumps
   (50 → 52), it warns: a page may be missing from the PDF.
4. If none of the above works, it uses the PDF numbering and records it as
   "sin_determinar" (undetermined), so that citations of that document are checked by hand.

Known limitations:
- It does not recognize Roman numerals (pages of prefaces or introductions).
- If a PDF joins several documents, the pages of the unnumbered document get numbers
  deduced from the other one.
"""

import re
from collections import Counter

# How many lines at the start and end of each page are examined for headers, footers and
# page numbers.
LINES_TO_CHECK = 2

# Page number alone ("45", "- 45 -", "— 45 —") or at the start/end of the header
# ("112   REVISTA...", "...COMPRENSIÓN   113").
NUMBER_ALONE = re.compile(r"^[\s\-–—]*(\d{1,4})[\s\-–—]*$")
NUMBER_AT_START = re.compile(r"^(\d{1,4})\s+\S")
NUMBER_AT_END = re.compile(r"\S\s+(\d{1,4})$")

# Minimum share of pages on which a line must appear to be taken as a header. It is low
# (40 %) because many books alternate two headers: author on even pages, title on odd ones.
HEADER_SHARE = 0.4

# Maximum distance between the number expected on a page and the one printed on it to
# accept it as its page number. Avoids mistaking a year, a figure in the text or a
# printer's mark for the page number.
MAX_DISTANCE = 5

# Values stored in the text file ("origen_paginacion"); they stay in Spanish (decision 0008).
SOURCE_MANUAL = "indicada_a_mano"
SOURCE_PDF = "numeracion_del_pdf"
SOURCE_DETECTED = "numeros_detectados"
SOURCE_UNDETERMINED = "sin_determinar"


def edge_lines(lines: list[str]) -> list[str]:
    """Return the first and last lines of a page (where headers and footers go)."""
    if len(lines) <= 2 * LINES_TO_CHECK:
        return lines
    return lines[:LINES_TO_CHECK] + lines[-LINES_TO_CHECK:]


def candidate_numbers(line: str) -> set[int]:
    """Return the numbers in a line that could be a page number."""
    line = line.strip()
    candidates = set()
    for pattern in (NUMBER_ALONE, NUMBER_AT_START, NUMBER_AT_END):
        match = pattern.search(line)
        if match:
            candidates.add(int(match.group(1)))
    return candidates


def detect_offset(pages_as_lines: list[list[str]]) -> int | None:
    """
    Find the constant difference between the PDF page and the printed page.

    Receives: the lines of each page.
    Returns: the offset (printed page = PDF page + offset), or None if there are not enough
    numbers that fit together.

    Why this way: a lone number at the top of a page may be a year or a note. But if on
    almost every page there is a number that is "PDF page + 44", that is the book's
    numbering.
    """
    votes = Counter()
    pages_with_text = 0
    for position, lines in enumerate(pages_as_lines, start=1):
        if not lines:
            continue
        pages_with_text += 1
        offsets = {n - position for line in edge_lines(lines) for n in candidate_numbers(line)}
        votes.update(offsets)
    if not votes:
        return None
    offset, support = votes.most_common(1)[0]
    minimum = 1 if pages_with_text == 1 else max(2, pages_with_text / 2)
    return offset if support >= minimum else None


def own_number(lines: list[str], expected: int) -> int | None:
    """
    Return the page number printed on this page, if there is one close to the expected one.

    If there are several candidates, it picks the closest to the expected one.
    """
    candidates = {n for line in edge_lines(lines) for n in candidate_numbers(line)}
    close = [n for n in candidates if abs(n - expected) <= MAX_DISTANCE]
    return min(close, key=lambda n: abs(n - expected)) if close else None


def assign_printed_pages(pages_as_lines: list[list[str]]) -> tuple[list[str], list[str]] | None:
    """
    Give each PDF page its printed page from the numbers it carries.

    Receives: the lines of each page.
    Returns: (printed pages, warnings), or None if there are no reliable page numbers.

    How: first it checks that the document has numbering (detect_offset). Then each page
    keeps its own number; pages without a number are filled in by counting from the
    previous one (or backwards from the first numbered one).
    """
    offset = detect_offset(pages_as_lines)
    if offset is None:
        return None

    own = []
    previous = None
    for position, lines in enumerate(pages_as_lines, start=1):
        expected = previous + 1 if previous is not None else position + offset
        number = own_number(lines, expected) if lines else None
        own.append(number)
        previous = number if number is not None else expected

    printed = []
    first_numbered = next(i for i, n in enumerate(own) if n is not None)
    for position, number in enumerate(own):
        if number is not None:
            printed.append(number)
        elif position < first_numbered:
            printed.append(own[first_numbered] - (first_numbered - position))
        else:
            printed.append(printed[-1] + 1)

    warnings = numbering_warnings(printed)
    deduced = [f"{position} (→ {printed[position - 1]})"
               for position, number in enumerate(own, start=1)
               if number is None and pages_as_lines[position - 1]]
    if deduced:
        warnings.append("Páginas del PDF sin número impreso, numeradas por deducción: "
                        f"{', '.join(deduced)}. Si citas alguna, comprueba la página.")
    return [str(n) for n in printed], warnings


def numbering_warnings(printed: list[int]) -> list[str]:
    """Point out jumps and repetitions in the page numbering."""
    warnings = []
    for position in range(1, len(printed)):
        previous, current = printed[position - 1], printed[position]
        where = f"(páginas {position} y {position + 1} del PDF)"
        if current > previous + 1:
            warnings.append(f"La numeración salta de la página {previous} a la {current} {where}: "
                            "puede faltar alguna página en el PDF.")
        elif current <= previous:
            warnings.append(f"La numeración se repite o retrocede, de la página {previous} a la {current} "
                            f"{where}: puede haber páginas de otro documento intercaladas.")
    return warnings


def remove_page_number(lines: list[str], printed: str) -> list[str]:
    """
    Remove, among the header or footer lines, the one carrying the printed page number.

    The whole line is removed, also when the number comes with text
    ("112   REVISTA DE FILOSOFÍA"): such a line is almost always a header.
    """
    if not printed.isdigit():
        return lines
    edges = set(range(LINES_TO_CHECK)) | set(range(len(lines) - LINES_TO_CHECK, len(lines)))
    return [line for index, line in enumerate(lines)
            if not (index in edges and int(printed) in candidate_numbers(line))]


def header_shape(line: str) -> str:
    """Simplify a line to recognize repeated headers (without numbers or capitals)."""
    return re.sub(r"\d+", "", line).strip(" -–—").casefold()


def remove_repeated_headers(pages_as_lines: list[list[str]]) -> list[list[str]]:
    """
    Remove header or footer lines that repeat on many pages.

    Only acts if the document has at least 3 pages: with fewer, a header cannot be told
    apart from a sentence that happens to repeat.
    """
    with_text = [lines for lines in pages_as_lines if lines]
    if len(with_text) < 3:
        return pages_as_lines
    occurrences = Counter()
    for lines in with_text:
        occurrences.update({header_shape(l) for l in edge_lines(lines) if header_shape(l)})
    headers = {shape for shape, times in occurrences.items()
               if times >= 2 and times >= HEADER_SHARE * len(with_text)}

    cleaned = []
    for lines in pages_as_lines:
        edges = set(range(LINES_TO_CHECK)) | set(range(len(lines) - LINES_TO_CHECK, len(lines)))
        cleaned.append([l for i, l in enumerate(lines)
                        if not (i in edges and header_shape(l) in headers)])
    return cleaned
