"""
Cargar la "estantería" del proyecto y el texto de cada obra.

Por qué existe: el verificador necesita dos cosas de cada proyecto:

1. La estantería (archivo biblioteca.json): la lista de obras que se pueden citar, cada
   una con una clave (por ejemplo "arendt1958") y la indicación de si ya se comprobó que
   existe.
2. El texto de cada obra, página a página, con la página impresa que corresponde a cada
   página del PDF (archivos de la carpeta texto/).

Formato de biblioteca.json: una lista de obras en el formato estándar CSL-JSON (el mismo
que exporta Zotero), con algunos campos propios de este proyecto:
    "verificacion": "doi" | "isbn" | "manual" | "pendiente"
    "texto_local": ruta al archivo con el texto, relativa a la carpeta del proyecto

Formato de un archivo de texto (texto/<clave>.json), que crea herramientas/pdf/extraer_texto.py:
    {"calidad": "ok" | "ocr" | "sin_texto",
     "origen_paginacion": "indicada_a_mano" | "numeracion_del_pdf" | "numeros_detectados"
                          | "sin_determinar",
     "paginas": [{"pdf": 1, "impresa": "45", "texto": "..."}, ...]}
"""

import json
from dataclasses import dataclass
from pathlib import Path

VERIFICACIONES_VALIDAS = {"doi", "isbn", "manual"}


class ErrorDeEstanteria(Exception):
    """Un problema con los archivos del proyecto, explicado en lenguaje llano."""


@dataclass
class Pagina:
    """Una página del documento: su número en el PDF, su número impreso y su texto."""
    pdf: int
    impresa: str
    texto: str


@dataclass
class TextoDeObra:
    """El texto completo de una obra, página a página."""
    paginas: list[Pagina]
    calidad: str  # "ok" si el texto es fiable; "ocr" si viene de un escaneo; "sin_texto" si no hay texto
    origen_paginacion: str = "sin_dato"  # cómo se averiguó la página impresa

    @property
    def paginacion_confirmada(self) -> bool:
        """Indica si se sabe con seguridad la página impresa de cada página."""
        return self.origen_paginacion != "sin_determinar"


def leer_json(ruta: Path, que_es: str):
    """Lee un archivo JSON y, si falla, explica el problema en español."""
    if not ruta.exists():
        raise ErrorDeEstanteria(f"No encuentro {que_es} en {ruta}.")
    try:
        return json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ErrorDeEstanteria(
            f"El archivo {ruta} ({que_es}) está mal escrito cerca de la línea {error.lineno}. "
            "Revisa que no falten comillas, comas o llaves."
        ) from error


def cargar_estanteria(carpeta_proyecto: Path) -> dict[str, dict]:
    """
    Carga las obras del proyecto.

    Recibe: la carpeta del proyecto.
    Devuelve: un diccionario que relaciona cada clave con los datos de su obra.
    """
    obras = leer_json(carpeta_proyecto / "biblioteca.json", "la estantería del proyecto")
    if not isinstance(obras, list):
        raise ErrorDeEstanteria("biblioteca.json debe contener una lista de obras entre [ ].")
    estanteria = {}
    for obra in obras:
        if "id" not in obra:
            raise ErrorDeEstanteria(
                f"Hay una obra sin clave (campo \"id\") en biblioteca.json: {obra.get('title', obra)}"
            )
        estanteria[obra["id"]] = obra
    return estanteria


def obra_comprobada(obra: dict) -> bool:
    """Indica si se ha comprobado que la obra existe (por DOI, ISBN o a mano)."""
    return obra.get("verificacion") in VERIFICACIONES_VALIDAS


def cargar_texto(carpeta_proyecto: Path, obra: dict) -> TextoDeObra | None:
    """
    Carga el texto de una obra, si lo hay.

    Devuelve: el texto página a página, o None si la obra no tiene texto disponible.
    """
    ruta_relativa = obra.get("texto_local")
    if not ruta_relativa:
        return None
    datos = leer_json(carpeta_proyecto / ruta_relativa, f"el texto de la obra {obra['id']}")
    paginas = [
        Pagina(pdf=p["pdf"], impresa=str(p["impresa"]), texto=p["texto"])
        for p in datos.get("paginas", [])
    ]
    return TextoDeObra(
        paginas=paginas,
        calidad=datos.get("calidad", "ok"),
        origen_paginacion=datos.get("origen_paginacion", "sin_dato"),
    )
