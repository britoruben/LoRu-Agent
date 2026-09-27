"""
Comprobar los DOI de todas las obras de una estantería.

Qué hace: recorre biblioteca.json y, para cada obra con DOI, pregunta a Crossref si existe
y si coinciden el título, el año y el primer autor. Muestra el resultado de cada obra.

Con la opción --guardar, marca en biblioteca.json como comprobadas ("verificacion": "doi")
las obras confirmadas, con la fecha. Nunca marca las que tienen discrepancias: esas las
tiene que revisar una persona.

Cómo se usa (desde la carpeta de LoRu-Agent, con conexión a internet):
    python3 -m herramientas.fuentes.comprobar_dois RUTA/A/biblioteca.json
    python3 -m herramientas.fuentes.comprobar_dois RUTA/A/biblioteca.json --guardar

El correo para identificarse ante Crossref se toma de la variable LORU_CORREO o de la
opción --correo.

Resultado: 0 si todas las obras con DOI se confirman; 1 si alguna falla; 2 si no se ha
podido hacer la comprobación.
"""

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

from .crossref import CON_DISCREPANCIAS, CONFIRMADA, NO_EXISTE, ErrorDeConexion, comprobar_obra

MENSAJES = {
    CONFIRMADA: "CONFIRMADA: el DOI existe y los datos coinciden.",
    CON_DISCREPANCIAS: "DISCREPANCIAS: el DOI existe, pero los datos no coinciden.",
    NO_EXISTE: "NO EXISTE: Crossref no conoce este DOI. Puede ser inventado o estar mal copiado.",
}


def main(argumentos: list[str] | None = None) -> int:
    lector = argparse.ArgumentParser(description="Comprueba en Crossref los DOI de una estantería.")
    lector.add_argument("biblioteca", type=Path, help="el archivo biblioteca.json")
    lector.add_argument("--correo", default=os.environ.get("LORU_CORREO"),
                        help="correo para identificarse ante Crossref (por defecto, LORU_CORREO)")
    lector.add_argument("--guardar", action="store_true",
                        help="marcar como comprobadas en biblioteca.json las obras confirmadas")
    opciones = lector.parse_args(argumentos)

    if not opciones.correo:
        print("Falta un correo para identificarse ante Crossref. Añade LORU_CORREO a tu archivo "
              ".env o usa la opción --correo tu@correo.org", file=sys.stderr)
        return 2
    if not opciones.biblioteca.exists():
        print(f"No encuentro {opciones.biblioteca}. Revisa la ruta.", file=sys.stderr)
        return 2

    obras = json.loads(opciones.biblioteca.read_text(encoding="utf-8"))
    hay_problemas = False
    hoy = datetime.date.today().isoformat()

    for obra in obras:
        if not obra.get("DOI"):
            print(f"· {obra['id']}: sin DOI. Hay que comprobarla por ISBN o a mano.")
            continue
        try:
            resultado = comprobar_obra(obra, opciones.correo)
        except ErrorDeConexion as error:
            print(f"No he podido terminar la comprobación: {error}", file=sys.stderr)
            return 2
        print(f"· {obra['id']} ({resultado.doi}): {MENSAJES[resultado.resultado]}")
        for diferencia in resultado.discrepancias:
            print(f"    - {diferencia}")
        if resultado.resultado == CONFIRMADA and opciones.guardar:
            obra["verificacion"], obra["fecha_verificacion"] = "doi", hoy
        if resultado.resultado != CONFIRMADA:
            hay_problemas = True

    if opciones.guardar:
        opciones.biblioteca.write_text(json.dumps(obras, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Estantería actualizada: {opciones.biblioteca}")
    return 1 if hay_problemas else 0


if __name__ == "__main__":
    sys.exit(main())
