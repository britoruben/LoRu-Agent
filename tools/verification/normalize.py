"""
Normalize texts before comparing a quote with the original.

Why it exists: a quote can be faithful to the original and still not match the text taken
from the PDF letter by letter, because of typographic details: straight or curly quotes,
dashes of different lengths, line breaks, words hyphenated at the end of a line...
This module removes those unimportant differences so that the comparison looks only at
the words.

What it does NOT do: it does not remove or change words, nor fix spelling. If the quote
changes a word of the original, the difference remains and the verifier will detect it.
"""

import re
import unicodedata

# Typographic signs replaced by their simple version.
EQUIVALENT_SIGNS = {
    "“": '"', "”": '"', "«": '"', "»": '"', "„": '"',
    "‘": "'", "’": "'", "‚": "'",
    "–": "-", "—": "-", "‐": "-", "‑": "-",
    "­": "",  # "invisible" hyphen that some PDFs insert to split words
}

# Marks used inside a quote to show that text was omitted or added:
# [...]  […]  (...)  (…)  ...  …  and any clarification in square brackets, such as [la razón].
OMISSION_MARKS = re.compile(
    r"\[\s*(?:\.\.\.|…)\s*\]"      # [...] or […]
    r"|\(\s*(?:\.\.\.|…)\s*\)"     # (...) or (…)
    r"|\.\.\.|…"                   # ... or …
    r"|\[[^\]]*\]"                 # [clarification by whoever quotes]
)

EDGE_SIGNS = " .,;:!?¡¿\"'()"


def normalize_text(text: str) -> str:
    """
    Prepare a text to be compared with another.

    Receives: any text (a quote or a page of the original).
    Returns: the same text without typographic differences and in lowercase.

    Lowercase because, when quoting mid-sentence, it is usual to change the initial
    capital, and that does not alter the quote.
    """
    text = unicodedata.normalize("NFKC", text)  # unifies ligatures such as "ﬁ" -> "fi"
    # Joins words hyphenated at the end of a line: "concien-\ncia" -> "conciencia".
    # Done before unifying dashes so as not to confuse them with an em dash (—) of
    # dialogue or aside that happens to fall at the end of a line.
    text = re.sub(r"(\w)[-‐‑­][ \t\r]*\n\s*(\w)", r"\1\2", text)
    for sign, replacement in EQUIVALENT_SIGNS.items():
        text = text.replace(sign, replacement)
    text = re.sub(r"\s+", " ", text)
    return text.strip().casefold()


def split_into_fragments(quote: str) -> list[str]:
    """
    Split a quote into the pieces that must appear verbatim in the original.

    Receives: the text of a literal quote, which may contain omissions ([...]) or
    clarifications by whoever quotes ([la razón]).
    Returns: the list of normalized pieces, in order. Each piece must be found in the
    original, and in that same order.
    """
    fragments = []
    for piece in OMISSION_MARKS.split(quote):
        piece = normalize_text(piece).strip(EDGE_SIGNS)
        if len(piece) >= 2:
            fragments.append(piece)
    return fragments
