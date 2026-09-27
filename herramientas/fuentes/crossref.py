"""
Comprobar en Crossref que una obra con DOI existe y que sus datos son correctos.

Qué es Crossref: el registro oficial donde las editoriales inscriben sus publicaciones con
DOI (el "DNI" de cada publicación). Si un DOI no está en Crossref, casi seguro que no existe.

Por qué existe este módulo: una IA puede inventar un DOI, o dar uno real pero de otra obra,
o acertar el DOI y equivocarse en el año o el autor. Este módulo pregunta a Crossref por el
DOI y compara lo que responde con los datos de nuestra estantería: título, año y apellido
del primer autor.

Necesita conexión a internet. Crossref pide que quien consulta se identifique con un
correo electrónico: se toma de la variable LORU_CORREO del archivo .env.
"""

import json
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from difflib import SequenceMatcher

DIRECCION_CROSSREF = "https://api.crossref.org/works/"
PARECIDO_MINIMO_DE_TITULO = 0.85

CONFIRMADA = "confirmada"
CON_DISCREPANCIAS = "con_discrepancias"
NO_EXISTE = "no_existe"


class ErrorDeConexion(Exception):
    """No se ha podido hablar con Crossref (sin internet, servicio caído...)."""


@dataclass
class ResultadoDeComprobacion:
    clave: str
    doi: str
    resultado: str
    discrepancias: list[str] = field(default_factory=list)


def consultar_doi(doi: str, correo: str, espera_maxima: int = 20) -> dict | None:
    """
    Pregunta a Crossref por un DOI.

    Devuelve: los datos que Crossref tiene de esa obra, o None si el DOI no existe.
    Lanza ErrorDeConexion si no se puede consultar.
    """
    direccion = DIRECCION_CROSSREF + urllib.parse.quote(doi) + "?" + urllib.parse.urlencode({"mailto": correo})
    peticion = urllib.request.Request(direccion, headers={"User-Agent": f"LoRu-Agent (mailto:{correo})"})
    try:
        with urllib.request.urlopen(peticion, timeout=espera_maxima) as respuesta:
            return json.load(respuesta)["message"]
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise ErrorDeConexion(f"Crossref ha respondido con un error ({error.code}). Inténtalo más tarde.") from error
    except (urllib.error.URLError, TimeoutError) as error:
        raise ErrorDeConexion(
            "No he podido conectar con Crossref. Comprueba tu conexión a internet."
        ) from error


def simplificar(texto: str) -> str:
    """Quita tildes, mayúsculas y signos para comparar nombres y títulos."""
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return " ".join("".join(c if c.isalnum() else " " for c in sin_tildes.casefold()).split())


def anio_de(datos: dict, *campos: str) -> int | None:
    """Saca el año de publicación de los datos de una obra (formato CSL o Crossref)."""
    for campo in campos:
        try:
            return int(datos[campo]["date-parts"][0][0])
        except (KeyError, IndexError, TypeError, ValueError):
            continue
    return None


def comparar_con_crossref(obra: dict, datos_crossref: dict) -> list[str]:
    """
    Compara una obra de la estantería con lo que dice Crossref.

    Devuelve: la lista de diferencias, explicadas en español. Vacía si todo coincide.
    """
    diferencias = []

    titulo_nuestro = simplificar(obra.get("title", ""))
    titulo_crossref = simplificar(" ".join(datos_crossref.get("title", [])))
    parecido = SequenceMatcher(None, titulo_nuestro, titulo_crossref).ratio()
    if parecido < PARECIDO_MINIMO_DE_TITULO:
        diferencias.append(
            f"Título distinto. Estantería: «{obra.get('title', '')}». "
            f"Crossref: «{' '.join(datos_crossref.get('title', []))}»."
        )

    anio_nuestro = anio_de(obra, "issued")
    anio_crossref = anio_de(datos_crossref, "issued", "published-print", "published-online")
    if anio_nuestro and anio_crossref and anio_nuestro != anio_crossref:
        diferencias.append(f"Año distinto. Estantería: {anio_nuestro}. Crossref: {anio_crossref}.")

    autores_nuestros = obra.get("author", [])
    autores_crossref = datos_crossref.get("author", [])
    if autores_nuestros and autores_crossref:
        apellido_nuestro = simplificar(autores_nuestros[0].get("family", ""))
        apellido_crossref = simplificar(autores_crossref[0].get("family", ""))
        if apellido_nuestro != apellido_crossref:
            diferencias.append(
                f"Primer autor distinto. Estantería: {autores_nuestros[0].get('family')}. "
                f"Crossref: {autores_crossref[0].get('family')}."
            )
    return diferencias


def comprobar_obra(obra: dict, correo: str, consultar=consultar_doi) -> ResultadoDeComprobacion:
    """
    Comprueba una obra con DOI.

    El parámetro "consultar" permite, en las pruebas automáticas, sustituir la consulta
    real a internet por respuestas preparadas.
    """
    doi = obra["DOI"].strip()
    datos = consultar(doi, correo)
    if datos is None:
        return ResultadoDeComprobacion(obra["id"], doi, NO_EXISTE)
    diferencias = comparar_con_crossref(obra, datos)
    return ResultadoDeComprobacion(obra["id"], doi, CON_DISCREPANCIAS if diferencias else CONFIRMADA, diferencias)
