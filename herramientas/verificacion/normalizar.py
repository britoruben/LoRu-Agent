"""
Normalizar textos antes de comparar una cita con el original.

Por qué existe: una cita puede ser fiel al original y, aun así, no coincidir letra por letra
con el texto sacado del PDF por detalles de tipografía: comillas rectas o curvas, guiones de
distinto tamaño, saltos de línea, palabras partidas con guion al final de una línea...
Este módulo borra esas diferencias sin importancia para que la comparación se fije solo en
las palabras.

Lo que NO hace: no quita ni cambia palabras, ni corrige la ortografía. Si la cita cambia una
palabra del original, la diferencia se mantiene y el verificador la detectará.
"""

import re
import unicodedata

# Signos tipográficos que se sustituyen por su versión simple.
SIGNOS_EQUIVALENTES = {
    "“": '"', "”": '"', "«": '"', "»": '"', "„": '"',
    "‘": "'", "’": "'", "‚": "'",
    "–": "-", "—": "-", "‐": "-", "‑": "-",
    "­": "",  # guion "invisible" que algunos PDF insertan para partir palabras
}

# Marcas con las que se indica, dentro de una cita, que se ha omitido o añadido texto:
# [...]  […]  (...)  (…)  ...  …  y cualquier aclaración entre corchetes, como [la razón].
MARCAS_DE_OMISION = re.compile(
    r"\[\s*(?:\.\.\.|…)\s*\]"      # [...] o […]
    r"|\(\s*(?:\.\.\.|…)\s*\)"     # (...) o (…)
    r"|\.\.\.|…"                   # ... o …
    r"|\[[^\]]*\]"                 # [aclaración de quien cita]
)

SIGNOS_EN_LOS_EXTREMOS = " .,;:!?¡¿\"'()"


def normalizar_texto(texto: str) -> str:
    """
    Prepara un texto para compararlo con otro.

    Recibe: un texto cualquiera (una cita o una página del original).
    Devuelve: el mismo texto sin diferencias tipográficas y en minúsculas.

    Se pasa a minúsculas porque al citar a mitad de frase es habitual cambiar la
    mayúscula inicial, y eso no altera la cita.
    """
    texto = unicodedata.normalize("NFKC", texto)  # unifica ligaduras como "ﬁ" -> "fi"
    # Une las palabras partidas con guion al final de línea: "concien-\ncia" -> "conciencia".
    # Se hace antes de unificar los guiones para no confundirlos con una raya (—) de
    # diálogo o de inciso que caiga a final de línea.
    texto = re.sub(r"(\w)[-‐‑\u00ad][ \t\r]*\n\s*(\w)", r"\1\2", texto)
    for signo, sustituto in SIGNOS_EQUIVALENTES.items():
        texto = texto.replace(signo, sustituto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip().casefold()


def dividir_en_fragmentos(cita: str) -> list[str]:
    """
    Separa una cita en los trozos que deben aparecer tal cual en el original.

    Recibe: el texto de una cita literal, que puede contener omisiones ([...]) o
    aclaraciones de quien cita ([la razón]).
    Devuelve: la lista de trozos normalizados, en orden. Cada trozo debe encontrarse en el
    original, y en ese mismo orden.
    """
    fragmentos = []
    for trozo in MARCAS_DE_OMISION.split(cita):
        trozo = normalizar_texto(trozo).strip(SIGNOS_EN_LOS_EXTREMOS)
        if len(trozo) >= 2:
            fragmentos.append(trozo)
    return fragmentos
