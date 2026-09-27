"""
Read a draft and locate all its citations.

Why it exists: to check the citations, first they must be found. This module reads a draft
written in Markdown and notes:

- each citation label, for example [@arendt1958, p. 45] or [@a, pp. 3-4; @b];
- the literal quotes: the text in quotation marks («...», “...” or "...") or in a block
  quote (lines starting with >) that is followed by a label;
- the [FUENTE PENDIENTE: ...] gaps left by the writer;
- long texts in quotation marks that carry no label;
- @keys written in a format this program does not recognize.

About the last point: if a citation were written in a way the program does not understand,
it would escape the check without anyone noticing. So, instead of ignoring it, it warns.

Label format: Pandoc's, the program that will later format the citations.
"""

import re
from dataclasses import dataclass, field

# A citation label in square brackets containing at least one @key.
CITATION_PATTERN = re.compile(r"\[([^\[\]]*@[^\[\]]*)\]")

# The key of a work inside the label: @arendt1958
KEY_PATTERN = re.compile(r"@([A-Za-z0-9_][\w:.\-/]*)")

# The page: p. 45 · pp. 45-46 · pág. 45 · págs. 45-46 · p. xii
PAGE_PATTERN = re.compile(
    r"\b(?:p|pp|pág|págs|pag|pags)\.\s*([0-9]+|[ivxlcdm]+)"
    r"(?:\s*[-–]\s*([0-9]+|[ivxlcdm]+))?",
    re.IGNORECASE,
)

PENDING_SOURCE_PATTERN = re.compile(r"\[FUENTE PENDIENTE[^\]]*\]", re.IGNORECASE)

# Text in quotation marks: «...», “...” or "..."
QUOTES_PATTERN = re.compile(r"«([^»]+)»|“([^”]+)”|\"([^\"]+)\"")

# A block quote: one or more consecutive lines starting with >
BLOCKQUOTE_PATTERN = re.compile(r"(?:^>.*(?:\n|$))+", re.MULTILINE)

# A loose @key, outside square brackets. Does not confuse e-mail addresses (name@domain).
LOOSE_KEY_PATTERN = re.compile(r"(?<![\w.])@([A-Za-z][\w:.\-]*)")

# Between the closing quotation mark and the label there may only be spaces or one punctuation sign.
MAX_GAP = re.compile(r"^\s*[,.;:]?\s*$")

MIN_WORDS_TO_WARN = 5


@dataclass
class CitedWork:
    """A work mentioned inside a label, with the page if given."""
    key: str
    page_start: str | None = None
    page_end: str | None = None

    def describe_pages(self) -> str:
        """Return the pages as they would be written in a citation: 'p. 45' or 'pp. 45-46'."""
        if self.page_start is None:
            return "sin página"
        if self.page_end:
            return f"pp. {self.page_start}-{self.page_end}"
        return f"p. {self.page_start}"


@dataclass
class Citation:
    """A citation label in the draft and, if it comes with one, the literal quote."""
    label: str                         # the text as is, e.g. "[@arendt1958, p. 45]"
    line: int
    works: list[CitedWork] = field(default_factory=list)
    quote: str | None = None           # what is in quotation marks, if it is a literal quote


@dataclass
class UncitedQuote:
    """A long enough text in quotation marks that carries no label."""
    text: str
    line: int


@dataclass
class DraftContents:
    """Everything the verifier needs to know about a draft."""
    citations: list[Citation]
    pending_sources: list[tuple[int, str]]
    uncited_quotes: list[UncitedQuote]
    unrecognized_keys: list[tuple[int, str]]


def line_number(text: str, position: int) -> int:
    """Return the line of the text (starting at 1) where a position is."""
    return text.count("\n", 0, position) + 1


def parse_label(inside: str) -> list[CitedWork]:
    """
    Read the inside of a label and return the cited works.

    Example: "véase @a, pp. 3-4; @b" -> [CitedWork("a", "3", "4"), CitedWork("b")]
    """
    works = []
    for part in inside.split(";"):
        key = KEY_PATTERN.search(part)
        if not key:
            continue
        page = PAGE_PATTERN.search(part)
        works.append(CitedWork(
            key=key.group(1).rstrip(".:"),
            page_start=page.group(1) if page else None,
            page_end=page.group(2) if page else None,
        ))
    return works


def find_quotes(text: str) -> list[tuple[int, int, str]]:
    """
    Find the texts in quotation marks and the block quotes.

    Returns: a list of (start, end, quoted text). If some quotation marks are inside others
    («... “x” ...»), only the outer ones are kept.
    """
    found = []
    for match in QUOTES_PATTERN.finditer(text):
        content = next(g for g in match.groups() if g is not None)
        if "\n\n" in content:  # quotation marks do not cross from one paragraph to another
            continue
        found.append((match.start(), match.end(), content))

    for block in BLOCKQUOTE_PATTERN.finditer(text):
        lines = [re.sub(r"^>\s?", "", line) for line in block.group(0).splitlines()]
        content = " ".join(lines).strip()
        # In a block quote the label usually goes at the end, inside the block itself.
        final_label = re.search(r"\s*\[[^\[\]]*@[^\[\]]*\]\s*$", content)
        if final_label:
            content = content[: final_label.start()]
            end = block.start() + block.group(0).rfind("[")
        else:
            end = block.end()
        found.append((block.start(), end, content))

    found.sort()
    not_nested = []
    for start, end, content in found:
        if not_nested and start < not_nested[-1][1]:
            continue
        not_nested.append((start, end, content))
    return not_nested


def read_draft(text: str) -> DraftContents:
    """
    Analyse a whole draft.

    Receives: the text of the draft (Markdown).
    Returns: its citations, literal quotes, pending gaps and format warnings.
    """
    citations_by_position = {}
    for match in CITATION_PATTERN.finditer(text):
        citations_by_position[match.start()] = Citation(
            label=match.group(0),
            line=line_number(text, match.start()),
            works=parse_label(match.group(1)),
        )

    uncited_quotes = []
    for start, end, content in find_quotes(text):
        next_citation = next(
            (position for position in sorted(citations_by_position) if position >= end), None
        )
        gap = text[end:next_citation] if next_citation is not None else "x"
        if next_citation is not None and MAX_GAP.match(gap):
            citations_by_position[next_citation].quote = content
        elif len(content.split()) >= MIN_WORDS_TO_WARN:
            uncited_quotes.append(UncitedQuote(content, line_number(text, start)))

    pending_sources = [
        (line_number(text, m.start()), m.group(0))
        for m in PENDING_SOURCE_PATTERN.finditer(text)
    ]

    # Blank out the labels already recognized and look for loose @keys in what is left.
    rest = CITATION_PATTERN.sub(lambda m: " " * len(m.group(0)), text)
    unrecognized_keys = [
        (line_number(text, m.start()), m.group(0))
        for m in LOOSE_KEY_PATTERN.finditer(rest)
    ]

    return DraftContents(
        citations=[citations_by_position[p] for p in sorted(citations_by_position)],
        pending_sources=pending_sources,
        uncited_quotes=uncited_quotes,
        unrecognized_keys=unrecognized_keys,
    )
