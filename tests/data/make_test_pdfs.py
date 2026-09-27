"""
Create the test PDFs used by the automatic tests of the PDF extractor.

Why it exists: testing the extractor needs PDFs with known features (page number in the
footer, repeated headers, the PDF's own numbering, scanned pages...). Creating them with a
program lets us know exactly what must come out. All texts are fictitious, written for
these tests.

It also creates the example project's PDF (ejemplos/proyecto-demo/pdf/ficticia2021.pdf).

It only needs to be run to regenerate the PDFs (they are already saved). It needs the
reportlab package (see requirements-desarrollo.txt):
    python3 tests/data/make_test_pdfs.py
"""

from pathlib import Path

from pypdf import PdfWriter
from pypdf.constants import PageLabelStyle
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas

FOLDER = Path(__file__).resolve().parent
EXAMPLE_PROJECT_PDF = FOLDER.parent.parent / "ejemplos" / "proyecto-demo" / "pdf" / "ficticia2021.pdf"
WIDTH, HEIGHT = A5

# The same text as the fictitious work "ficticia2021" of the example project
# (ejemplos/proyecto-demo), split into lines as in a book. Page 45 ends a line with a
# hyphenated word ("pri-" / "mer"), as happens in printed books.
BOOK_PAGES = [
    ["Capítulo 3. La caja negra",
     "Llamamos opacidad a la distancia que separa lo que un sistema",
     "hace de lo que podemos decir sobre por qué lo hace. Un sistema",
     "es opaco cuando sus resultados son verificables pero sus",
     "razones no lo son. Esta distinción, que parece meramente",
     "técnica, tiene consecuencias morales de pri-",
     "mer orden."],
    ["En efecto, exigir una explicación no es un capricho",
     "epistemológico: es la condición de posibilidad de la crítica.",
     "Quien no puede preguntar por las razones de una decisión solo",
     "puede aceptarla o rechazarla en bloque. La opacidad, por tanto,",
     "no es un defecto del sistema, sino una propiedad de la relación",
     "entre el sistema y quienes deben responder por él. Cuando esa",
     "relación se"],
    ["rompe, la responsabilidad se diluye entre el diseñador, el",
     "usuario y la máquina, y nadie responde de nada. Conviene no",
     "confundir, sin embargo, la transparencia con la inteligibilidad:",
     "un código abierto puede ser perfectamente ininteligible."],
    ["Página añadida para las pruebas: con cuatro páginas se puede",
     "comprobar que las cabeceras alternas se reconocen y se quitan."],
]


def write_lines(pdf_canvas, lines, first_y=500):
    pdf_canvas.setFont("Helvetica", 10)
    y = first_y
    for line in lines:
        pdf_canvas.drawString(40, y, line)
        y -= 14


def book_with_footer_number(path=FOLDER / "libro_numero_al_pie.pdf"):
    """Pages 45-48 printed in the footer; alternating headers (author / title), as in a book.
    Page 47 carries no number, as often happens on chapter opening pages."""
    pdf_canvas = canvas.Canvas(str(path), pagesize=A5)
    for position, lines in enumerate(BOOK_PAGES):
        printed = 45 + position
        pdf_canvas.setFont("Helvetica", 8)
        header = "ANA FICTICIA" if printed % 2 == 0 else "LA OPACIDAD DE LAS MÁQUINAS"
        pdf_canvas.drawString(40, 560, header)
        write_lines(pdf_canvas, lines)
        if printed != 47:
            pdf_canvas.setFont("Helvetica", 9)
            pdf_canvas.drawCentredString(WIDTH / 2, 30, str(printed))
        pdf_canvas.showPage()
    pdf_canvas.save()


def book_with_number_in_header():
    """Page number inside the header line: '112  RESPONSABILIDAD...'."""
    pdf_canvas = canvas.Canvas(str(FOLDER / "articulo_numero_en_cabecera.pdf"), pagesize=A5)
    for position, lines in enumerate(BOOK_PAGES[:3]):
        printed = 112 + position
        pdf_canvas.setFont("Helvetica", 8)
        if printed % 2 == 0:
            pdf_canvas.drawString(40, 560, f"{printed}   REVISTA IMAGINARIA DE FILOSOFÍA")
        else:
            pdf_canvas.drawString(40, 560, f"RESPONSABILIDAD SIN COMPRENSIÓN   {printed}")
        write_lines(pdf_canvas, lines)
        pdf_canvas.showPage()
    pdf_canvas.save()


def pdf_without_numbers(name):
    pdf_canvas = canvas.Canvas(str(FOLDER / name), pagesize=A5)
    for lines in BOOK_PAGES[:2]:
        write_lines(pdf_canvas, lines)
        pdf_canvas.showPage()
    pdf_canvas.save()


def pdf_with_own_numbering():
    """No printed numbers, but the PDF itself says its first page is 101."""
    pdf_without_numbers("temporal.pdf")
    writer = PdfWriter(clone_from=str(FOLDER / "temporal.pdf"))
    writer.set_page_label(0, 1, style=PageLabelStyle.DECIMAL, start=101)
    writer.write(str(FOLDER / "numeracion_propia.pdf"))
    (FOLDER / "temporal.pdf").unlink()


def scanned_pdf():
    """A page that is only an image (a grey rectangle): it contains no text."""
    pdf_canvas = canvas.Canvas(str(FOLDER / "escaneado.pdf"), pagesize=A5)
    for _ in range(2):
        pdf_canvas.setFillGray(0.8)
        pdf_canvas.rect(40, 200, 300, 300, fill=1)
        pdf_canvas.showPage()
    pdf_canvas.save()


if __name__ == "__main__":
    book_with_footer_number()
    EXAMPLE_PROJECT_PDF.parent.mkdir(parents=True, exist_ok=True)
    book_with_footer_number(EXAMPLE_PROJECT_PDF)
    book_with_number_in_header()
    pdf_without_numbers("sin_numeros.pdf")
    pdf_with_own_numbering()
    scanned_pdf()
    print("Test PDFs created in", FOLDER)
