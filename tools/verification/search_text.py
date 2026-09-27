"""
Search for a literal quote in the original text.

Why it exists: it is the heart of the verifier. Given a quote and the page it gives, it
answers three questions:

1. Is the quote, verbatim, on that page?
2. If not, is it on another page? (then the quote's page is wrong)
3. If it is not verbatim anywhere, is there a very similar passage? (then the quote has
   been altered, or the text of the original has scanning errors)

How it compares: first it normalizes both texts (see normalize.py). If the quote has
omissions ([...]), it checks that each piece appears in the original, in the same order.
"""

from dataclasses import dataclass
from difflib import SequenceMatcher

from .normalize import normalize_text, split_into_fragments
from .shelf import Page, WorkText

# Similarity (from 0 to 1) from which a passage "almost matches".
MIN_SIMILARITY = 0.85
# Similarity from which the closest passage is shown as a hint.
HINT_SIMILARITY = 0.6

PUNCTUATION = ".,;:!?¡¿\"'()"

# Possible outcomes of the search.
ON_CITED_PAGE = "on_cited_page"
SPANS_PAGES = "spans_pages"
ON_OTHER_PAGE = "on_other_page"
SIMILAR = "similar"
NOT_FOUND = "not_found"
PAGE_MISSING = "page_missing"


@dataclass
class SearchResult:
    """What was found when searching for a quote in the original."""
    outcome: str
    pages_found: list[str]
    original_passage: str = ""
    similarity: float = 0.0


def is_number(page: str | None) -> bool:
    return page is not None and page.isdigit()


def page_positions(text: WorkText, start: str, end: str | None) -> list[int]:
    """
    Return the positions (0, 1, 2...) of the cited pages within the document.

    If the citation says "pp. 45-47", it returns the positions of pages 45, 46 and 47.
    Returns an empty list if the page does not exist in the available text.
    """
    if end and is_number(start) and is_number(end):
        wanted = range(int(start), int(end) + 1)
        return [i for i, p in enumerate(text.pages) if is_number(p.printed) and int(p.printed) in wanted]
    return [i for i, p in enumerate(text.pages) if p.printed.casefold() == start.casefold()]


def join_pages(pages: list[Page]) -> str:
    """Join several pages into a single normalized text (keeps hyphenated words whole)."""
    return normalize_text("\n".join(p.text for p in pages))


def contains_in_order(text: str, fragments: list[str]) -> bool:
    """Check that all the pieces appear in the text, one after another."""
    position = 0
    for fragment in fragments:
        found = text.find(fragment, position)
        if found == -1:
            return False
        position = found + len(fragment)
    return True


def strip_punctuation(words: list[str]) -> str:
    """Join the words without the punctuation attached to them."""
    return " ".join(word.strip(PUNCTUATION) for word in words)


def most_similar_passage(quote: str, text: str) -> tuple[str, float]:
    """
    Find the passage in the text that most resembles the quote.

    Returns: the passage and its similarity, from 0 (unrelated) to 1 (identical).

    How: it slides a "window" with the same number of words as the quote over the text and
    compares letter by letter, without punctuation. Letter by letter (not word by word) so
    that a scanning error such as "prornete" instead of "promete" counts as a small
    difference and not as a whole different word.
    """
    quote_words = quote.split()
    text_words = text.split()
    size = len(quote_words)
    if size == 0 or not text_words:
        return "", 0.0
    bare_quote = strip_punctuation(quote_words)
    best_passage, best_similarity = "", 0.0
    for start in range(max(1, len(text_words) - size + 1)):
        window = text_words[start: start + size]
        matcher = SequenceMatcher(None, bare_quote, strip_punctuation(window))
        if matcher.quick_ratio() <= best_similarity:
            continue
        similarity = matcher.ratio()
        if similarity > best_similarity:
            best_passage, best_similarity = " ".join(window), similarity
    return best_passage, best_similarity


def find_on_single_page(text: WorkText, fragments: list[str]) -> list[str] | None:
    """Look for the whole quote within a single page. Return that page or None."""
    for page in text.pages:
        if contains_in_order(join_pages([page]), fragments):
            return [page.printed]
    return None


def find_across_two_pages(text: WorkText, fragments: list[str]) -> list[str] | None:
    """Look for the quote split across two consecutive pages. Return both or None."""
    for i in range(len(text.pages) - 1):
        pair = text.pages[i: i + 2]
        if contains_in_order(join_pages(pair), fragments):
            return [p.printed for p in pair]
    return None


def find_quote(quote: str, text: WorkText, start: str, end: str | None = None) -> SearchResult:
    """
    Search for a literal quote in the original and tell whether the page is right.

    Receives: the quote, the text of the work and the page (or pages) the draft gives.
    Returns: a SearchResult with what was found.
    """
    fragments = split_into_fragments(quote)
    positions = page_positions(text, start, end)

    if positions:
        cited = [text.pages[i] for i in positions]
        if contains_in_order(join_pages(cited), fragments):
            return SearchResult(ON_CITED_PAGE, [p.printed for p in cited])

    # If it is whole on another page, the cited page is wrong.
    elsewhere = find_on_single_page(text, fragments)
    if elsewhere:
        return SearchResult(ON_OTHER_PAGE if positions else PAGE_MISSING, elsewhere)

    if positions:
        # Does it start on the cited page and continue on the next (or start on the previous)?
        first, last = positions[0], positions[-1]
        for since, until in ((first, last + 1), (first - 1, last)):
            if 0 <= since and until < len(text.pages):
                widened = text.pages[since: until + 1]
                if contains_in_order(join_pages(widened), fragments):
                    return SearchResult(SPANS_PAGES, [p.printed for p in widened])

    across_two = find_across_two_pages(text, fragments)
    if across_two:
        return SearchResult(ON_OTHER_PAGE if positions else PAGE_MISSING, across_two)

    # Not verbatim: look for the most similar passage, first on the cited pages.
    full_quote = " ".join(fragments)
    zones = [[text.pages[i] for i in positions]] if positions else []
    zones.append(text.pages)
    best = ("", 0.0, [])
    for zone in zones:
        for page in zone:
            passage, similarity = most_similar_passage(full_quote, join_pages([page]))
            if similarity > best[1]:
                best = (passage, similarity, [page.printed])
        if best[1] >= MIN_SIMILARITY:
            break

    passage, similarity, pages = best
    if similarity >= MIN_SIMILARITY:
        return SearchResult(SIMILAR, pages, passage, similarity)
    if not positions:
        return SearchResult(PAGE_MISSING, [], passage if similarity >= HINT_SIMILARITY else "", similarity)
    hint = passage if similarity >= HINT_SIMILARITY else ""
    return SearchResult(NOT_FOUND, pages if hint else [], hint, similarity)
