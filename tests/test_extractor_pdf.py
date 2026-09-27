"""
Pruebas automáticas del extractor de texto de PDF.

Usan los PDF ficticios de tests/datos, creados con tests/datos/crear_pdfs_de_prueba.py,
cuyas páginas impresas se conocen de antemano. La última prueba recorre el camino completo:
PDF → texto con páginas → verificación de citas.

Necesitan el paquete pypdf (ver requirements.txt).
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from herramientas.pdf import paginacion
from herramientas.pdf.extraer_texto import ErrorDePdf, extraer_texto
from herramientas.verificacion.verificar_citas import AVISO, verificar_borrador

DATOS = Path(__file__).resolve().parent / "datos"
PROYECTO_DEMO = Path(__file__).resolve().parent.parent / "ejemplos" / "proyecto-demo"


def paginas_impresas(extraido):
    return [p["impresa"] for p in extraido.paginas]


class PruebasDePaginacion(unittest.TestCase):

    def test_deduce_la_pagina_impresa_de_los_numeros_al_pie(self):
        extraido = extraer_texto(DATOS / "libro_numero_al_pie.pdf")
        self.assertEqual(paginas_impresas(extraido), ["45", "46", "47", "48"])
        self.assertEqual(extraido.origen_paginacion, paginacion.ORIGEN_DETECTADO)

    def test_completa_una_pagina_sin_numero_entre_otras_numeradas(self):
        # La página 47 del libro de prueba no lleva número (inicio de capítulo).
        self.assertEqual(extraer_texto(DATOS / "libro_numero_al_pie.pdf").paginas[2]["impresa"], "47")

    def test_reconoce_el_numero_dentro_de_la_cabecera(self):
        extraido = extraer_texto(DATOS / "articulo_numero_en_cabecera.pdf")
        self.assertEqual(paginas_impresas(extraido), ["112", "113", "114"])

    def test_usa_la_numeracion_que_trae_el_propio_pdf(self):
        extraido = extraer_texto(DATOS / "numeracion_propia.pdf")
        self.assertEqual(paginas_impresas(extraido), ["101", "102"])
        self.assertEqual(extraido.origen_paginacion, paginacion.ORIGEN_PDF)

    def test_no_se_inventa_la_paginacion_si_no_hay_pistas(self):
        extraido = extraer_texto(DATOS / "sin_numeros.pdf")
        self.assertEqual(extraido.origen_paginacion, paginacion.ORIGEN_SIN_DETERMINAR)
        self.assertTrue(extraido.avisos)

    def test_la_pagina_indicada_a_mano_tiene_preferencia(self):
        extraido = extraer_texto(DATOS / "numeracion_propia.pdf", primera_pagina=7)
        self.assertEqual(paginas_impresas(extraido), ["7", "8"])

    def test_respeta_el_numero_de_cada_pagina_aunque_falte_una_pagina(self):
        # Caso real (un libro escaneado de 1863, incluido en las pruebas de pypdf): al PDF le
        # falta la página 51. Antes se numeraba todo con la misma diferencia y las dos
        # primeras páginas quedaban mal (50 y 51 en lugar de 49 y 50).
        paginas = [
            ["THE SIEGE OF VICKSBURG. 49", "however, did not last long;", "—4"],
            ["50 THE SIEGE OF VICKSBUEG.", "buried itself in the earth,"],
            ["52 THE SIEGE OF VICKSBURG.", "I have a great curiosity"],
            ["THE SIEGE OP VICKSBURG. 53", "We are doing all we can"],
            ["54 THE SIEGE OF VICKSBURG.", "a good housekeeper,"],
            ["THE SIEGE OF VICKSBURG. 55", "watched the beauty above."],
        ]
        impresas, avisos = paginacion.asignar_paginas_impresas(paginas)
        self.assertEqual(impresas, ["49", "50", "52", "53", "54", "55"])
        self.assertIn("de la página 50 a la 52", avisos[0])

    def test_completa_las_paginas_sin_numero_al_principio(self):
        paginas = [["Portadilla sin número", "texto"], ["texto", "11"], ["texto", "12"], ["texto", "13"]]
        impresas, avisos = paginacion.asignar_paginas_impresas(paginas)
        self.assertEqual(impresas, ["10", "11", "12", "13"])
        self.assertEqual(len(avisos), 1)
        self.assertIn("por deducción: 1 (→ 10)", avisos[0])

    def test_avisa_de_una_pagina_intercalada_de_otro_documento(self):
        paginas = [["Libro 49", "texto"], ["Otro documento", "sin número"],
                   ["50 Libro", "texto"], ["Libro 51", "texto"]]
        impresas, avisos = paginacion.asignar_paginas_impresas(paginas)
        self.assertTrue(any("otro documento intercaladas" in aviso for aviso in avisos))

    def test_no_confunde_un_anio_con_un_numero_de_pagina(self):
        paginas = [["1984 fue un año decisivo", "texto"], ["más texto", "y más"]]
        self.assertIsNone(paginacion.detectar_desfase(paginas))


class PruebasDeLimpieza(unittest.TestCase):

    def test_quita_las_cabeceras_y_los_numeros_de_pagina(self):
        texto = "\n".join(p["texto"] for p in extraer_texto(DATOS / "libro_numero_al_pie.pdf").paginas)
        self.assertNotIn("ANA FICTICIA", texto)
        self.assertNotIn("LA OPACIDAD DE LAS MÁQUINAS", texto)
        self.assertNotIn("\n45", texto)

    def test_quita_la_cabecera_que_lleva_el_numero_de_pagina(self):
        texto = "\n".join(p["texto"] for p in extraer_texto(DATOS / "articulo_numero_en_cabecera.pdf").paginas)
        self.assertNotIn("REVISTA IMAGINARIA", texto)
        self.assertNotIn("RESPONSABILIDAD SIN COMPRENSIÓN", texto)

    def test_conserva_el_texto_del_cuerpo(self):
        primera = extraer_texto(DATOS / "libro_numero_al_pie.pdf").paginas[0]["texto"]
        self.assertTrue(primera.startswith("Capítulo 3. La caja negra"))
        self.assertIn("de pri-\nmer orden.", primera)


class PruebasDeProblemas(unittest.TestCase):

    def test_detecta_un_pdf_escaneado(self):
        extraido = extraer_texto(DATOS / "escaneado.pdf")
        self.assertEqual(extraido.calidad, "sin_texto")
        self.assertIn("escaneado", extraido.avisos[0])

    def test_explica_que_el_pdf_no_existe(self):
        with self.assertRaises(ErrorDePdf):
            extraer_texto(DATOS / "no_existe.pdf")

    def test_explica_que_el_archivo_no_es_un_pdf(self):
        with self.assertRaises(ErrorDePdf):
            extraer_texto(Path(__file__))


class PruebaDelCaminoCompleto(unittest.TestCase):
    """PDF → texto con páginas → verificación de las citas del borrador correcto."""

    def setUp(self):
        self.carpeta = Path(tempfile.mkdtemp())
        shutil.copy(PROYECTO_DEMO / "biblioteca.json", self.carpeta)
        shutil.copytree(PROYECTO_DEMO / "texto", self.carpeta / "texto")

    def tearDown(self):
        shutil.rmtree(self.carpeta)

    def guardar_texto_extraido(self, pdf, clave):
        extraido = extraer_texto(pdf)
        ruta = self.carpeta / "texto" / f"{clave}.json"
        ruta.write_text(json.dumps(extraido.como_diccionario(), ensure_ascii=False), encoding="utf-8")

    def test_las_citas_se_comprueban_contra_el_texto_sacado_del_pdf(self):
        self.guardar_texto_extraido(PROYECTO_DEMO / "pdf" / "ficticia2021.pdf", "ficticia2021")
        borrador = (PROYECTO_DEMO / "borradores" / "borrador-correcto.md").read_text(encoding="utf-8")
        self.assertEqual(verificar_borrador(borrador, self.carpeta).incidencias, [])

    def test_avisa_si_la_paginacion_no_esta_confirmada(self):
        self.guardar_texto_extraido(DATOS / "sin_numeros.pdf", "ficticia2021")
        incidencias = verificar_borrador(
            "«Llamamos opacidad a la distancia» [@ficticia2021, p. 1].", self.carpeta).incidencias
        self.assertEqual([i.gravedad for i in incidencias], [AVISO])
        self.assertIn("paginación", incidencias[0].problema)

    def test_avisa_si_el_pdf_era_un_escaneo(self):
        self.guardar_texto_extraido(DATOS / "escaneado.pdf", "ficticia2021")
        [incidencia] = verificar_borrador("«Algo citado» [@ficticia2021, p. 1].", self.carpeta).incidencias
        self.assertIn("escaneado", incidencia.problema)


if __name__ == "__main__":
    unittest.main()
