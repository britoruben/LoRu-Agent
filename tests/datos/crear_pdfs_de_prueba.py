"""
Crea los PDF de prueba que usan las pruebas automáticas del extractor de PDF.

Por qué existe: para probar el extractor hacen falta PDF con características conocidas
(número de página en el pie, cabeceras repetidas, numeración propia del PDF, páginas
escaneadas...). Crearlos con un programa permite saber exactamente qué debe salir.
Todos los textos son ficticios, escritos para estas pruebas.

También crea el PDF del proyecto de ejemplo (ejemplos/proyecto-demo/pdf/ficticia2021.pdf).

Solo hace falta ejecutarlo si se quieren regenerar los PDF (ya están guardados). Necesita el paquete reportlab (ver requirements-desarrollo.txt):
    python3 tests/datos/crear_pdfs_de_prueba.py
"""

from pathlib import Path

from pypdf import PdfWriter
from pypdf.constants import PageLabelStyle
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas

CARPETA = Path(__file__).resolve().parent
PDF_DEL_PROYECTO_DE_EJEMPLO = CARPETA.parent.parent / "ejemplos" / "proyecto-demo" / "pdf" / "ficticia2021.pdf"
ANCHO, ALTO = A5

# El mismo texto que la obra ficticia "ficticia2021" del proyecto de ejemplo
# (ejemplos/proyecto-demo), repartido en líneas como en un libro. La página 45 termina una
# línea con una palabra partida ("pri-" / "mer"), como pasa en los libros impresos.
PAGINAS_DEL_LIBRO = [
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


def escribir_lineas(lienzo, lineas, y_inicial=500):
    lienzo.setFont("Helvetica", 10)
    y = y_inicial
    for linea in lineas:
        lienzo.drawString(40, y, linea)
        y -= 14


def libro_con_numero_al_pie(ruta=CARPETA / "libro_numero_al_pie.pdf"):
    """Páginas 45-48 impresas al pie; cabeceras alternas (autora / título), como en un libro.
    La página 47 no lleva número, como pasa a menudo en las páginas de inicio de capítulo."""
    lienzo = canvas.Canvas(str(ruta), pagesize=A5)
    for posicion, lineas in enumerate(PAGINAS_DEL_LIBRO):
        impresa = 45 + posicion
        lienzo.setFont("Helvetica", 8)
        cabecera = "ANA FICTICIA" if impresa % 2 == 0 else "LA OPACIDAD DE LAS MÁQUINAS"
        lienzo.drawString(40, 560, cabecera)
        escribir_lineas(lienzo, lineas)
        if impresa != 47:
            lienzo.setFont("Helvetica", 9)
            lienzo.drawCentredString(ANCHO / 2, 30, str(impresa))
        lienzo.showPage()
    lienzo.save()


def libro_con_numero_en_la_cabecera():
    """Número de página dentro de la línea de cabecera: '112  RESPONSABILIDAD...'."""
    lienzo = canvas.Canvas(str(CARPETA / "articulo_numero_en_cabecera.pdf"), pagesize=A5)
    for posicion, lineas in enumerate(PAGINAS_DEL_LIBRO[:3]):
        impresa = 112 + posicion
        lienzo.setFont("Helvetica", 8)
        if impresa % 2 == 0:
            lienzo.drawString(40, 560, f"{impresa}   REVISTA IMAGINARIA DE FILOSOFÍA")
        else:
            lienzo.drawString(40, 560, f"RESPONSABILIDAD SIN COMPRENSIÓN   {impresa}")
        escribir_lineas(lienzo, lineas)
        lienzo.showPage()
    lienzo.save()


def pdf_sin_numeros(nombre):
    lienzo = canvas.Canvas(str(CARPETA / nombre), pagesize=A5)
    for lineas in PAGINAS_DEL_LIBRO[:2]:
        escribir_lineas(lienzo, lineas)
        lienzo.showPage()
    lienzo.save()


def pdf_con_numeracion_propia():
    """Sin números impresos, pero el propio PDF dice que su primera página es la 101."""
    pdf_sin_numeros("temporal.pdf")
    escritor = PdfWriter(clone_from=str(CARPETA / "temporal.pdf"))
    escritor.set_page_label(0, 1, style=PageLabelStyle.DECIMAL, start=101)
    escritor.write(str(CARPETA / "numeracion_propia.pdf"))
    (CARPETA / "temporal.pdf").unlink()


def pdf_escaneado():
    """Una página que es solo una imagen (un rectángulo gris): no contiene texto."""
    lienzo = canvas.Canvas(str(CARPETA / "escaneado.pdf"), pagesize=A5)
    for _ in range(2):
        lienzo.setFillGray(0.8)
        lienzo.rect(40, 200, 300, 300, fill=1)
        lienzo.showPage()
    lienzo.save()


if __name__ == "__main__":
    libro_con_numero_al_pie()
    PDF_DEL_PROYECTO_DE_EJEMPLO.parent.mkdir(parents=True, exist_ok=True)
    libro_con_numero_al_pie(PDF_DEL_PROYECTO_DE_EJEMPLO)
    libro_con_numero_en_la_cabecera()
    pdf_sin_numeros("sin_numeros.pdf")
    pdf_con_numeracion_propia()
    pdf_escaneado()
    print("PDF de prueba creados en", CARPETA)
