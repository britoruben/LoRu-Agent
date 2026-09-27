"""
Pruebas automáticas del comprobador de DOI.

No se conectan a internet: en lugar de preguntar a Crossref, usan respuestas preparadas que
imitan las de Crossref. Así las pruebas funcionan en cualquier ordenador y siempre igual.
Para probarlo contra el Crossref real, ver ejemplos/comprobar-doi/LEEME.md.
"""

import unittest

from herramientas.fuentes.crossref import (
    CON_DISCREPANCIAS, CONFIRMADA, NO_EXISTE, comparar_con_crossref, comprobar_obra,
)

OBRA = {
    "id": "searle1980",
    "title": "Minds, brains, and programs",
    "author": [{"family": "Searle", "given": "John R."}],
    "issued": {"date-parts": [[1980]]},
    "DOI": "10.1017/S0140525X00005756",
}

RESPUESTA_DE_CROSSREF = {
    "title": ["Minds, brains, and programs"],
    "author": [{"family": "Searle", "given": "John R."}],
    "issued": {"date-parts": [[1980, 9]]},
}


def crossref_que_responde(respuesta):
    """Imita a Crossref devolviendo siempre la misma respuesta."""
    return lambda doi, correo: respuesta


class PruebasDelComprobadorDeDOI(unittest.TestCase):

    def test_confirma_una_obra_cuyos_datos_coinciden(self):
        resultado = comprobar_obra(OBRA, "prueba@ejemplo.org", crossref_que_responde(RESPUESTA_DE_CROSSREF))
        self.assertEqual(resultado.resultado, CONFIRMADA)

    def test_detecta_un_doi_que_no_existe(self):
        resultado = comprobar_obra(OBRA, "prueba@ejemplo.org", crossref_que_responde(None))
        self.assertEqual(resultado.resultado, NO_EXISTE)

    def test_detecta_un_anio_equivocado(self):
        obra = dict(OBRA, issued={"date-parts": [[1981]]})
        resultado = comprobar_obra(obra, "prueba@ejemplo.org", crossref_que_responde(RESPUESTA_DE_CROSSREF))
        self.assertEqual(resultado.resultado, CON_DISCREPANCIAS)
        self.assertIn("Año distinto", resultado.discrepancias[0])

    def test_detecta_un_doi_real_pero_de_otra_obra(self):
        otra = {"title": ["Deep learning"], "author": [{"family": "LeCun"}], "issued": {"date-parts": [[2015]]}}
        diferencias = comparar_con_crossref(OBRA, otra)
        self.assertEqual(len(diferencias), 3)  # título, año y autor

    def test_no_se_confunde_por_tildes_ni_mayusculas(self):
        obra = dict(OBRA, title="MINDS, BRAINS AND PROGRAMS", author=[{"family": "Séarle"}])
        self.assertEqual(comparar_con_crossref(obra, RESPUESTA_DE_CROSSREF), [])


if __name__ == "__main__":
    unittest.main()
