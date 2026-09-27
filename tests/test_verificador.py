"""
Pruebas automáticas del verificador de citas.

Qué son: pequeños casos preparados de antemano, con la respuesta correcta conocida. Si el
verificador deja de detectar alguno, la prueba falla y avisa. Así, cada vez que alguien
cambia el programa, se comprueba en segundos que sigue funcionando.

Cómo se ejecutan (desde la carpeta de LoRu-Agent):
    python3 -m unittest -v

La mayoría de las pruebas usan el proyecto de ejemplo de ejemplos/proyecto-demo, cuyas obras
y textos son ficticios.
"""

import unittest
from pathlib import Path

from herramientas.verificacion.buscar_en_texto import (
    CRUZA_DE_PAGINA, EN_OTRA_PAGINA, EN_SU_PAGINA, NO_ENCONTRADA, PAGINA_INEXISTENTE, PARECIDA,
    buscar_cita,
)
from herramientas.verificacion.estanteria import cargar_estanteria, cargar_texto
from herramientas.verificacion.leer_borrador import leer_borrador
from herramientas.verificacion.normalizar import dividir_en_fragmentos, normalizar_texto
from herramientas.verificacion.verificar_citas import AVISO, FALLO, verificar_borrador

PROYECTO_DEMO = Path(__file__).resolve().parent.parent / "ejemplos" / "proyecto-demo"


def texto_de(clave):
    """Carga el texto de una obra del proyecto de ejemplo."""
    return cargar_texto(PROYECTO_DEMO, cargar_estanteria(PROYECTO_DEMO)[clave])


def incidencias_de(borrador):
    """Verifica un borrador breve contra el proyecto de ejemplo."""
    return verificar_borrador(borrador, PROYECTO_DEMO).incidencias


class PruebasDeNormalizacion(unittest.TestCase):

    def test_ignora_diferencias_tipograficas(self):
        self.assertEqual(normalizar_texto("«Hola»  —dijo—\nel ﬁlósofo"), '"hola" -dijo- el filósofo')

    def test_une_palabras_partidas_al_final_de_linea(self):
        self.assertEqual(normalizar_texto("de pri-\nmer orden"), "de primer orden")

    def test_une_palabras_partidas_con_saltos_de_linea_de_windows(self):
        self.assertEqual(normalizar_texto("de pri-\r\nmer orden"), "de primer orden")

    def test_no_une_palabras_separadas_por_una_raya_de_dialogo(self):
        self.assertEqual(normalizar_texto("dijo—\nel filósofo"), "dijo- el filósofo")

    def test_separa_la_cita_por_las_omisiones(self):
        self.assertEqual(
            dividir_en_fragmentos("La razón [...] pero [la técnica] nada … más"),
            ["la razón", "pero", "nada", "más"],
        )

    def test_descarta_trozos_de_una_sola_letra(self):
        # Un trozo como "y" aparece en cualquier texto: no sirve para comprobar nada.
        self.assertEqual(dividir_en_fragmentos("la razón [...] y [...] la técnica"),
                         ["la razón", "la técnica"])


class PruebasDeLecturaDelBorrador(unittest.TestCase):

    def test_reconoce_una_cita_literal_con_su_pagina(self):
        cita = leer_borrador("Dice que «algo importante» [@a, p. 4].").citas[0]
        self.assertEqual(cita.texto_literal, "algo importante")
        self.assertEqual((cita.obras[0].clave, cita.obras[0].pagina_inicio), ("a", "4"))

    def test_reconoce_varias_obras_y_rangos_de_paginas(self):
        obras = leer_borrador("[véase @a, pp. 3-5; @b]").citas[0].obras
        self.assertEqual([(o.clave, o.pagina_inicio, o.pagina_fin) for o in obras],
                         [("a", "3", "5"), ("b", None, None)])

    def test_reconoce_un_bloque_de_cita(self):
        cita = leer_borrador("> Texto largo citado\n> en dos líneas. [@a, p. 2]\n").citas[0]
        self.assertEqual(cita.texto_literal, "Texto largo citado en dos líneas.")

    def test_no_confunde_un_correo_con_una_cita(self):
        self.assertEqual(leer_borrador("Escribe a ana@ejemplo.org").claves_no_reconocidas, [])

    def test_ignora_comillas_cortas_sin_cita(self):
        self.assertEqual(leer_borrador("La llamada «caja negra» es un mito.").textos_sin_cita, [])


class PruebasDeBusquedaEnElOriginal(unittest.TestCase):

    def test_encuentra_una_cita_exacta_en_su_pagina(self):
        r = buscar_cita("es la condición de posibilidad de la crítica", texto_de("ficticia2021"), "46")
        self.assertEqual(r.resultado, EN_SU_PAGINA)

    def test_encuentra_una_cita_con_palabra_partida_en_el_pdf(self):
        r = buscar_cita("consecuencias morales de primer orden", texto_de("ficticia2021"), "45")
        self.assertEqual(r.resultado, EN_SU_PAGINA)

    def test_acepta_omisiones_marcadas_con_corchetes(self):
        r = buscar_cita("Cuando esa relación se rompe [...] nadie responde de nada",
                        texto_de("ficticia2021"), "46", "47")
        self.assertEqual(r.resultado, EN_SU_PAGINA)

    def test_detecta_una_pagina_equivocada_y_dice_la_correcta(self):
        r = buscar_cita("exigir una explicación no es un capricho", texto_de("ficticia2021"), "45")
        self.assertEqual((r.resultado, r.paginas_encontradas), (EN_OTRA_PAGINA, ["46"]))

    def test_detecta_una_cita_que_cruza_de_pagina(self):
        r = buscar_cita("Cuando esa relación se rompe", texto_de("ficticia2021"), "46")
        self.assertEqual((r.resultado, r.paginas_encontradas), (CRUZA_DE_PAGINA, ["46", "47"]))

    def test_detecta_una_cita_alterada(self):
        r = buscar_cita("sus resultados son verificables pero sus motivos no lo son",
                        texto_de("ficticia2021"), "45")
        self.assertEqual(r.resultado, PARECIDA)
        self.assertIn("razones", r.pasaje_del_original)

    def test_detecta_una_cita_inventada(self):
        r = buscar_cita("la máquina tiene intencionalidad genuina", texto_de("ejemplar2019"), "113")
        self.assertEqual(r.resultado, NO_ENCONTRADA)

    def test_detecta_una_pagina_que_no_existe(self):
        r = buscar_cita("la opacidad técnica exime de culpa", texto_de("ejemplar2019"), "200")
        self.assertEqual((r.resultado, r.paginas_encontradas), (PAGINA_INEXISTENTE, ["113"]))


class PruebasDelVerificadorCompleto(unittest.TestCase):

    def test_da_por_bueno_el_borrador_correcto(self):
        borrador = (PROYECTO_DEMO / "borradores" / "borrador-correcto.md").read_text(encoding="utf-8")
        self.assertEqual(incidencias_de(borrador), [])

    def test_detecta_todos_los_errores_del_borrador_con_errores(self):
        borrador = (PROYECTO_DEMO / "borradores" / "borrador-con-errores.md").read_text(encoding="utf-8")
        resultado = verificar_borrador(borrador, PROYECTO_DEMO)
        self.assertEqual((len(resultado.fallos), len(resultado.avisos)), (8, 4))

    def test_detecta_una_obra_que_no_esta_en_la_estanteria(self):
        [incidencia] = incidencias_de("Según «algo» [@inventado2020, p. 3].")
        self.assertEqual(incidencia.gravedad, FALLO)
        self.assertIn("no está en la estantería", incidencia.problema)

    def test_detecta_una_obra_sin_comprobar(self):
        [incidencia] = incidencias_de("Lo confirma [@sincomprobar2023].")
        self.assertEqual(incidencia.gravedad, FALLO)

    def test_exige_pagina_en_las_citas_literales(self):
        [incidencia] = incidencias_de("Dice «podemos ser responsables» [@ejemplar2019].")
        self.assertIn("sin página", incidencia.problema)

    def test_bloquea_si_queda_una_fuente_pendiente(self):
        [incidencia] = incidencias_de("Esto ha crecido [FUENTE PENDIENTE: datos].")
        self.assertEqual(incidencia.gravedad, FALLO)

    def test_solo_avisa_si_el_original_es_un_escaneo(self):
        [incidencia] = incidencias_de("«Toda técnica promete descargarnos de una tarea» [@escaneo1975, p. 9].")
        self.assertEqual(incidencia.gravedad, AVISO)

    def test_avisa_de_citas_escritas_en_un_formato_no_reconocido(self):
        [incidencia] = incidencias_de("Como defiende @ejemplar2019, no hace falta comprender.")
        self.assertEqual(incidencia.gravedad, AVISO)


if __name__ == "__main__":
    unittest.main()
