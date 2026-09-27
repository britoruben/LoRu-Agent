"""
Automatic tests of the citation verifier.

What they are: small cases prepared in advance, with the right answer known. If the
verifier stops detecting any of them, the test fails and warns. So, every time someone
changes the program, it takes seconds to check that it still works.

How to run them (from the LoRu-Agent folder):
    python3 -m unittest -v

Most tests use the example project in ejemplos/proyecto-demo, whose works and texts are
fictitious.
"""

import unittest
from pathlib import Path

from tools.verification.normalize import normalize_text, split_into_fragments
from tools.verification.read_draft import read_draft
from tools.verification.search_text import (
    NOT_FOUND, ON_CITED_PAGE, ON_OTHER_PAGE, PAGE_MISSING, SIMILAR, SPANS_PAGES, find_quote,
)
from tools.verification.shelf import load_shelf, load_text
from tools.verification.verify_citations import FAIL, WARNING, verify_draft

DEMO_PROJECT = Path(__file__).resolve().parent.parent / "ejemplos" / "proyecto-demo"


def text_of(key):
    """Load the text of a work from the example project."""
    return load_text(DEMO_PROJECT, load_shelf(DEMO_PROJECT)[key])


def issues_of(draft):
    """Verify a short draft against the example project."""
    return verify_draft(draft, DEMO_PROJECT).issues


class NormalizationTests(unittest.TestCase):

    def test_ignores_typographic_differences(self):
        self.assertEqual(normalize_text("«Hola»  —dijo—\nel ﬁlósofo"), '"hola" -dijo- el filósofo')

    def test_joins_words_hyphenated_at_line_end(self):
        self.assertEqual(normalize_text("de pri-\nmer orden"), "de primer orden")

    def test_joins_hyphenated_words_with_windows_line_breaks(self):
        self.assertEqual(normalize_text("de pri-\r\nmer orden"), "de primer orden")

    def test_does_not_join_words_separated_by_a_dialogue_dash(self):
        self.assertEqual(normalize_text("dijo—\nel filósofo"), "dijo- el filósofo")

    def test_splits_the_quote_at_omissions(self):
        self.assertEqual(
            split_into_fragments("La razón [...] pero [la técnica] nada … más"),
            ["la razón", "pero", "nada", "más"],
        )

    def test_discards_single_letter_pieces(self):
        # A piece such as "y" appears in any text: it proves nothing.
        self.assertEqual(split_into_fragments("la razón [...] y [...] la técnica"),
                         ["la razón", "la técnica"])


class DraftReadingTests(unittest.TestCase):

    def test_recognizes_a_literal_quote_with_its_page(self):
        citation = read_draft("Dice que «algo importante» [@a, p. 4].").citations[0]
        self.assertEqual(citation.quote, "algo importante")
        self.assertEqual((citation.works[0].key, citation.works[0].page_start), ("a", "4"))

    def test_recognizes_several_works_and_page_ranges(self):
        works = read_draft("[véase @a, pp. 3-5; @b]").citations[0].works
        self.assertEqual([(w.key, w.page_start, w.page_end) for w in works],
                         [("a", "3", "5"), ("b", None, None)])

    def test_recognizes_a_block_quote(self):
        citation = read_draft("> Texto largo citado\n> en dos líneas. [@a, p. 2]\n").citations[0]
        self.assertEqual(citation.quote, "Texto largo citado en dos líneas.")

    def test_does_not_mistake_an_email_for_a_citation(self):
        self.assertEqual(read_draft("Escribe a ana@ejemplo.org").unrecognized_keys, [])

    def test_ignores_short_quotes_without_citation(self):
        self.assertEqual(read_draft("La llamada «caja negra» es un mito.").uncited_quotes, [])


class SearchInOriginalTests(unittest.TestCase):

    def test_finds_an_exact_quote_on_its_page(self):
        r = find_quote("es la condición de posibilidad de la crítica", text_of("ficticia2021"), "46")
        self.assertEqual(r.outcome, ON_CITED_PAGE)

    def test_finds_a_quote_with_a_word_hyphenated_in_the_pdf(self):
        r = find_quote("consecuencias morales de primer orden", text_of("ficticia2021"), "45")
        self.assertEqual(r.outcome, ON_CITED_PAGE)

    def test_accepts_omissions_marked_with_brackets(self):
        r = find_quote("Cuando esa relación se rompe [...] nadie responde de nada",
                       text_of("ficticia2021"), "46", "47")
        self.assertEqual(r.outcome, ON_CITED_PAGE)

    def test_detects_a_wrong_page_and_gives_the_right_one(self):
        r = find_quote("exigir una explicación no es un capricho", text_of("ficticia2021"), "45")
        self.assertEqual((r.outcome, r.pages_found), (ON_OTHER_PAGE, ["46"]))

    def test_detects_a_quote_that_spans_pages(self):
        r = find_quote("Cuando esa relación se rompe", text_of("ficticia2021"), "46")
        self.assertEqual((r.outcome, r.pages_found), (SPANS_PAGES, ["46", "47"]))

    def test_detects_an_altered_quote(self):
        r = find_quote("sus resultados son verificables pero sus motivos no lo son",
                       text_of("ficticia2021"), "45")
        self.assertEqual(r.outcome, SIMILAR)
        self.assertIn("razones", r.original_passage)

    def test_detects_an_invented_quote(self):
        r = find_quote("la máquina tiene intencionalidad genuina", text_of("ejemplar2019"), "113")
        self.assertEqual(r.outcome, NOT_FOUND)

    def test_detects_a_page_that_does_not_exist(self):
        r = find_quote("la opacidad técnica exime de culpa", text_of("ejemplar2019"), "200")
        self.assertEqual((r.outcome, r.pages_found), (PAGE_MISSING, ["113"]))


class FullVerifierTests(unittest.TestCase):

    def test_accepts_the_correct_draft(self):
        draft = (DEMO_PROJECT / "borradores" / "borrador-correcto.md").read_text(encoding="utf-8")
        self.assertEqual(issues_of(draft), [])

    def test_detects_every_error_in_the_draft_with_errors(self):
        draft = (DEMO_PROJECT / "borradores" / "borrador-con-errores.md").read_text(encoding="utf-8")
        result = verify_draft(draft, DEMO_PROJECT)
        self.assertEqual((len(result.failures), len(result.warnings)), (8, 4))

    def test_detects_a_work_not_on_the_shelf(self):
        [issue] = issues_of("Según «algo» [@inventado2020, p. 3].")
        self.assertEqual(issue.severity, FAIL)
        self.assertIn("no está en la estantería", issue.problem)

    def test_detects_an_unchecked_work(self):
        [issue] = issues_of("Lo confirma [@sincomprobar2023].")
        self.assertEqual(issue.severity, FAIL)

    def test_requires_a_page_for_literal_quotes(self):
        [issue] = issues_of("Dice «podemos ser responsables» [@ejemplar2019].")
        self.assertIn("sin página", issue.problem)

    def test_blocks_if_a_pending_source_remains(self):
        [issue] = issues_of("Esto ha crecido [FUENTE PENDIENTE: datos].")
        self.assertEqual(issue.severity, FAIL)

    def test_only_warns_if_the_original_is_a_scan(self):
        [issue] = issues_of("«Toda técnica promete descargarnos de una tarea» [@escaneo1975, p. 9].")
        self.assertEqual(issue.severity, WARNING)

    def test_warns_of_citations_in_an_unrecognized_format(self):
        [issue] = issues_of("Como defiende @ejemplar2019, no hace falta comprender.")
        self.assertEqual(issue.severity, WARNING)


if __name__ == "__main__":
    unittest.main()
