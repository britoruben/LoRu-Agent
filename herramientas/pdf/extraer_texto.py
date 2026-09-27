"""
Extraer el texto de un PDF, página a página, con su página impresa.

Qué hace: lee un PDF y crea el archivo de texto que usa el verificador de citas
(texto/<clave>.json), con cada página, su número en el PDF y su página impresa. Quita las
cabeceras que se repiten y los números de página, y avisa de los problemas.

Por qué existe: el verificador compara cada cita con el texto original. Este programa es el
puente entre el PDF que descargas y ese texto.

Qué NO hace:
- No lee PDF escaneados (fotos de páginas). Los detecta y avisa: hará falta reconocimiento
  de texto (OCR), que todavía no está construido.
- No reconoce páginas numeradas con números romanos.
- No separa bien el texto de PDF a dos columnas ni las notas al pie: pueden quedar mezclados.

Cómo se usa (desde la carpeta de LoRu-Agent):
    python3 -m herramientas.pdf.extraer_texto LIBRO.pdf --proyecto CARPETA --clave ficticia2021
Opciones:
    --primera-pagina 45   si sabes que la página 1 del PDF es la 45 impresa
    --salida ARCHIVO.json para guardar el resultado en otro sitio

Resultado: 0 si todo ha ido bien; 1 si se ha extraído con avisos importantes (escaneo o
paginación sin determinar); 2 si no se ha podido leer el PDF.
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError
except ImportError:
    raise ImportError(
        "Falta el paquete pypdf, que sirve para leer PDF. Instálalo con:\n"
        "    python3 -m pip install -r requirements.txt\n"
        "(ver docs/instalacion.md)"
    ) from None

# pypdf escribe avisos técnicos en inglés cuando un PDF tiene defectos menores. Se silencian
# porque este programa ya explica en español los problemas que importan.
logging.getLogger("pypdf").setLevel(logging.ERROR)

from . import paginacion

# Una página con menos letras que esto se considera vacía (probablemente, una imagen).
LETRAS_MINIMAS_POR_PAGINA = 20


class ErrorDePdf(Exception):
    """Un problema al leer el PDF, explicado en lenguaje llano."""


@dataclass
class TextoExtraido:
    fuente: str
    paginas: list[dict]
    calidad: str                 # "ok" o "sin_texto" (parece escaneado)
    origen_paginacion: str
    avisos: list[str] = field(default_factory=list)

    def como_diccionario(self) -> dict:
        return {
            "fuente": self.fuente,
            "calidad": self.calidad,
            "origen_paginacion": self.origen_paginacion,
            "avisos": self.avisos,
            "paginas": self.paginas,
        }


def abrir_pdf(ruta: Path) -> PdfReader:
    """Abre un PDF o explica por qué no se puede."""
    if not ruta.exists():
        raise ErrorDePdf(f"No encuentro el PDF {ruta}. Revisa la ruta.")
    try:
        lector = PdfReader(str(ruta))
        if lector.is_encrypted:
            raise ErrorDePdf(f"El PDF {ruta.name} está protegido con contraseña. Ábrelo y guárdalo sin protección.")
        return lector
    except PdfReadError as error:
        raise ErrorDePdf(f"No he podido leer {ruta.name}: el archivo parece dañado o no es un PDF.") from error


def numeracion_propia_del_pdf(lector: PdfReader) -> list[str] | None:
    """
    Devuelve la numeración de páginas que trae el propio PDF, si la trae.

    Importante: si el PDF no define numeración, pypdf devuelve igualmente "1", "2", "3"...
    Por eso se comprueba antes que el PDF la define de verdad.
    """
    if "/PageLabels" not in lector.trailer["/Root"]:
        return None
    return list(lector.page_labels)


def leer_lineas(lector: PdfReader) -> list[list[str]]:
    """Devuelve las líneas de texto de cada página (lista vacía si la página no tiene texto)."""
    paginas = []
    for pagina in lector.pages:
        texto = pagina.extract_text() or ""
        lineas = [linea for linea in texto.splitlines() if linea.strip()]
        letras = sum(c.isalpha() for c in texto)
        paginas.append(lineas if letras >= LETRAS_MINIMAS_POR_PAGINA else [])
    return paginas


def decidir_paginas_impresas(
    lector: PdfReader, lineas: list[list[str]], primera_pagina: int | None
) -> tuple[list[str], str, list[str]]:
    """
    Decide la página impresa de cada página del PDF (ver paginacion.py).

    Devuelve: la lista de páginas impresas, cómo se ha averiguado y los avisos.
    """
    total = len(lineas)
    if primera_pagina is not None:
        return [str(primera_pagina + i) for i in range(total)], paginacion.ORIGEN_INDICADO, []
    propia = numeracion_propia_del_pdf(lector)
    if propia:
        return propia, paginacion.ORIGEN_PDF, []
    detectadas = paginacion.asignar_paginas_impresas(lineas)
    if detectadas is not None:
        impresas, avisos = detectadas
        return impresas, paginacion.ORIGEN_DETECTADO, avisos
    return [str(i + 1) for i in range(total)], paginacion.ORIGEN_SIN_DETERMINAR, []


def extraer_texto(ruta_pdf: Path, primera_pagina: int | None = None) -> TextoExtraido:
    """
    Extrae el texto de un PDF con su paginación impresa.

    Recibe: la ruta del PDF y, opcionalmente, la página impresa de la primera página.
    Devuelve: un TextoExtraido listo para guardar como texto/<clave>.json.
    """
    lector = abrir_pdf(ruta_pdf)
    lineas = leer_lineas(lector)
    impresas, origen, avisos = decidir_paginas_impresas(lector, lineas, primera_pagina)

    lineas = [paginacion.quitar_numero_de_pagina(l, impresa) for l, impresa in zip(lineas, impresas)]
    lineas = paginacion.quitar_cabeceras_repetidas(lineas)

    paginas = [
        {"pdf": posicion, "impresa": impresa, "texto": "\n".join(l)}
        for posicion, (l, impresa) in enumerate(zip(lineas, impresas), start=1)
    ]
    vacias = [p["pdf"] for p in paginas if not p["texto"]]
    calidad = "ok"
    if len(vacias) > len(paginas) / 2:
        calidad = "sin_texto"
        avisos.append("La mayoría de las páginas no tienen texto: el PDF parece escaneado. "
                      "Hará falta reconocimiento de texto (OCR), que aún no está disponible.")
    elif vacias:
        avisos.append(f"Páginas del PDF sin texto (quizá imágenes o páginas en blanco): {vacias}.")
    if origen == paginacion.ORIGEN_SIN_DETERMINAR:
        avisos.append("No he podido averiguar la página impresa: uso la numeración del PDF. "
                      "Si sabes qué página impresa es la primera, repite con --primera-pagina.")
    return TextoExtraido(ruta_pdf.name, paginas, calidad, origen, avisos)


EXPLICACION_DEL_ORIGEN = {
    paginacion.ORIGEN_INDICADO: "la has indicado tú",
    paginacion.ORIGEN_PDF: "la trae el propio PDF",
    paginacion.ORIGEN_DETECTADO: "la he deducido de los números de página impresos",
    paginacion.ORIGEN_SIN_DETERMINAR: "NO se ha podido averiguar",
}


def main(argumentos: list[str] | None = None) -> int:
    lector = argparse.ArgumentParser(description="Extrae el texto de un PDF con su página impresa.")
    lector.add_argument("pdf", type=Path, help="el PDF")
    lector.add_argument("--proyecto", type=Path, help="carpeta del proyecto (guarda en su carpeta texto/)")
    lector.add_argument("--clave", help="clave de la obra en la estantería (nombre del archivo de salida)")
    lector.add_argument("--salida", type=Path, help="archivo de salida (en lugar de --proyecto y --clave)")
    lector.add_argument("--primera-pagina", type=int, help="página impresa de la primera página del PDF")
    opciones = lector.parse_args(argumentos)

    if opciones.salida:
        salida = opciones.salida
    elif opciones.proyecto and opciones.clave:
        salida = opciones.proyecto / "texto" / f"{opciones.clave}.json"
    else:
        print("Indica dónde guardar el resultado: --proyecto CARPETA --clave CLAVE, o --salida ARCHIVO.json",
              file=sys.stderr)
        return 2

    try:
        extraido = extraer_texto(opciones.pdf, opciones.primera_pagina)
    except ErrorDePdf as error:
        print(error, file=sys.stderr)
        return 2

    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(extraido.como_diccionario(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    paginas = extraido.paginas
    print(f"Páginas: {len(paginas)} (impresas {paginas[0]['impresa']} a {paginas[-1]['impresa']}).")
    print(f"Paginación: {EXPLICACION_DEL_ORIGEN[extraido.origen_paginacion]}.")
    for aviso in extraido.avisos:
        print(f"AVISO: {aviso}")
    print(f"Texto guardado en: {salida}")
    importante = extraido.calidad != "ok" or extraido.origen_paginacion == paginacion.ORIGEN_SIN_DETERMINAR
    return 1 if importante else 0


if __name__ == "__main__":
    sys.exit(main())
