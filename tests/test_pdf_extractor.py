"""
Automatic tests of the PDF text extractor.

They use the fictitious PDFs in tests/data, created with tests/data/make_test_pdfs.py,
whose printed pages are known in advance. The last test runs the whole path:
PDF → text with pages → citation verification.

They need the pypdf package (see requirements.txt).
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.pdf import pagination
from tools.pdf.extract_text import PdfError, extract_text
from tools.verification.verify_citations import WARNING, verify_draft

DATA = Path(__file__).resolve().parent / "data"
DEMO_PROJECT = Path(__file__).resolve().parent.parent / "ejemplos" / "proyecto-demo"


def printed_pages(extracted):
    return [p["impresa"] for p in extracted.pages]


class PaginationTests(unittest.TestCase):

    def test_deduces_the_printed_page_from_footer_numbers(self):
        extracted = extract_text(DATA / "libro_numero_al_pie.pdf")
        self.assertEqual(printed_pages(extracted), ["45", "46", "47", "48"])
        self.assertEqual(extracted.pagination_source, pagination.SOURCE_DETECTED)

    def test_fills_in_an_unnumbered_page_between_numbered_ones(self):
        # Page 47 of the test book carries no number (start of a chapter).
        self.assertEqual(extract_text(DATA / "libro_numero_al_pie.pdf").pages[2]["impresa"], "47")

    def test_recognizes_the_number_inside_the_header(self):
        extracted = extract_text(DATA / "articulo_numero_en_cabecera.pdf")
        self.assertEqual(printed_pages(extracted), ["112", "113", "114"])

    def test_uses_the_pdfs_own_numbering(self):
        extracted = extract_text(DATA / "numeracion_propia.pdf")
        self.assertEqual(printed_pages(extracted), ["101", "102"])
        self.assertEqual(extracted.pagination_source, pagination.SOURCE_PDF)

    def test_does_not_invent_pagination_without_clues(self):
        extracted = extract_text(DATA / "sin_numeros.pdf")
        self.assertEqual(extracted.pagination_source, pagination.SOURCE_UNDETERMINED)
        self.assertTrue(extracted.warnings)

    def test_the_page_given_by_hand_takes_precedence(self):
        extracted = extract_text(DATA / "numeracion_propia.pdf", first_page=7)
        self.assertEqual(printed_pages(extracted), ["7", "8"])

    def test_keeps_each_pages_number_even_if_a_page_is_missing(self):
        # Real case (a scanned book from 1863, included in pypdf's tests): the PDF lacks
        # page 51. Before, everything was numbered with the same offset and the first two
        # pages came out wrong (50 and 51 instead of 49 and 50).
        pages = [
            ["THE SIEGE OF VICKSBURG. 49", "however, did not last long;", "—4"],
            ["50 THE SIEGE OF VICKSBUEG.", "buried itself in the earth,"],
            ["52 THE SIEGE OF VICKSBURG.", "I have a great curiosity"],
            ["THE SIEGE OP VICKSBURG. 53", "We are doing all we can"],
            ["54 THE SIEGE OF VICKSBURG.", "a good housekeeper,"],
            ["THE SIEGE OF VICKSBURG. 55", "watched the beauty above."],
        ]
        printed, warnings = pagination.assign_printed_pages(pages)
        self.assertEqual(printed, ["49", "50", "52", "53", "54", "55"])
        self.assertIn("de la página 50 a la 52", warnings[0])

    def test_fills_in_unnumbered_pages_at_the_start(self):
        pages = [["Portadilla sin número", "texto"], ["texto", "11"], ["texto", "12"], ["texto", "13"]]
        printed, warnings = pagination.assign_printed_pages(pages)
        self.assertEqual(printed, ["10", "11", "12", "13"])
        self.assertEqual(len(warnings), 1)
        self.assertIn("por deducción: 1 (→ 10)", warnings[0])

    def test_warns_of_a_page_inserted_from_another_document(self):
        pages = [["Libro 49", "texto"], ["Otro documento", "sin número"],
                 ["50 Libro", "texto"], ["Libro 51", "texto"]]
        printed, warnings = pagination.assign_printed_pages(pages)
        self.assertTrue(any("otro documento intercaladas" in warning for warning in warnings))

    def test_does_not_mistake_a_year_for_a_page_number(self):
        pages = [["1984 fue un año decisivo", "texto"], ["más texto", "y más"]]
        self.assertIsNone(pagination.detect_offset(pages))


class CleaningTests(unittest.TestCase):

    def test_removes_headers_and_page_numbers(self):
        text = "\n".join(p["texto"] for p in extract_text(DATA / "libro_numero_al_pie.pdf").pages)
        self.assertNotIn("ANA FICTICIA", text)
        self.assertNotIn("LA OPACIDAD DE LAS MÁQUINAS", text)
        self.assertNotIn("\n45", text)

    def test_removes_the_header_that_carries_the_page_number(self):
        text = "\n".join(p["texto"] for p in extract_text(DATA / "articulo_numero_en_cabecera.pdf").pages)
        self.assertNotIn("REVISTA IMAGINARIA", text)
        self.assertNotIn("RESPONSABILIDAD SIN COMPRENSIÓN", text)

    def test_keeps_the_body_text(self):
        first = extract_text(DATA / "libro_numero_al_pie.pdf").pages[0]["texto"]
        self.assertTrue(first.startswith("Capítulo 3. La caja negra"))
        self.assertIn("de pri-\nmer orden.", first)


class ProblemTests(unittest.TestCase):

    def test_detects_a_scanned_pdf(self):
        extracted = extract_text(DATA / "escaneado.pdf")
        self.assertEqual(extracted.quality, "sin_texto")
        self.assertIn("escaneado", extracted.warnings[0])

    def test_explains_that_the_pdf_does_not_exist(self):
        with self.assertRaises(PdfError):
            extract_text(DATA / "no_existe.pdf")

    def test_explains_that_the_file_is_not_a_pdf(self):
        with self.assertRaises(PdfError):
            extract_text(Path(__file__))


class WholePathTest(unittest.TestCase):
    """PDF → text with pages → verification of the correct draft's citations."""

    def setUp(self):
        self.folder = Path(tempfile.mkdtemp())
        shutil.copy(DEMO_PROJECT / "biblioteca.json", self.folder)
        shutil.copytree(DEMO_PROJECT / "texto", self.folder / "texto")

    def tearDown(self):
        shutil.rmtree(self.folder)

    def save_extracted_text(self, pdf, key):
        extracted = extract_text(pdf)
        path = self.folder / "texto" / f"{key}.json"
        path.write_text(json.dumps(extracted.as_dict(), ensure_ascii=False), encoding="utf-8")

    def test_citations_are_checked_against_the_text_taken_from_the_pdf(self):
        self.save_extracted_text(DEMO_PROJECT / "pdf" / "ficticia2021.pdf", "ficticia2021")
        draft = (DEMO_PROJECT / "borradores" / "borrador-correcto.md").read_text(encoding="utf-8")
        self.assertEqual(verify_draft(draft, self.folder).issues, [])

    def test_warns_if_the_pagination_is_not_confirmed(self):
        self.save_extracted_text(DATA / "sin_numeros.pdf", "ficticia2021")
        issues = verify_draft(
            "«Llamamos opacidad a la distancia» [@ficticia2021, p. 1].", self.folder).issues
        self.assertEqual([i.severity for i in issues], [WARNING])
        self.assertIn("paginación", issues[0].problem)

    def test_warns_if_the_pdf_was_a_scan(self):
        self.save_extracted_text(DATA / "escaneado.pdf", "ficticia2021")
        [issue] = verify_draft("«Algo citado» [@ficticia2021, p. 1].", self.folder).issues
        self.assertIn("escaneado", issue.problem)


if __name__ == "__main__":
    unittest.main()
