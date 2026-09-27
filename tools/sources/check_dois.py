"""
Check the DOIs of every work on a shelf.

What it does: goes through biblioteca.json and, for each work with a DOI, asks Crossref
whether it exists and whether the title, year and first author match. It shows the result
for each work.

With the --save option, it marks the confirmed works as checked in biblioteca.json
("verificacion": "doi"), with the date. It never marks those with mismatches: a person has
to review them.

How to use it (from the LoRu-Agent folder, with an internet connection):
    python3 -m tools.sources.check_dois PATH/TO/biblioteca.json
    python3 -m tools.sources.check_dois PATH/TO/biblioteca.json --save

The e-mail used to identify yourself to Crossref comes from the LORU_CORREO variable or the
--email option.

Exit code: 0 if every work with a DOI is confirmed; 1 if any fails; 2 if the check could
not be done.
"""

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

from .crossref import CONFIRMED, MISMATCHED, NOT_FOUND, CrossrefConnectionError, check_work

MESSAGES = {
    CONFIRMED: "CONFIRMADA: el DOI existe y los datos coinciden.",
    MISMATCHED: "DISCREPANCIAS: el DOI existe, pero los datos no coinciden.",
    NOT_FOUND: "NO EXISTE: Crossref no conoce este DOI. Puede ser inventado o estar mal copiado.",
}


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Comprueba en Crossref los DOI de una estantería.")
    parser.add_argument("library", type=Path, help="el archivo biblioteca.json")
    parser.add_argument("--email", default=os.environ.get("LORU_CORREO"),
                        help="correo para identificarse ante Crossref (por defecto, LORU_CORREO)")
    parser.add_argument("--save", action="store_true",
                        help="marcar como comprobadas en biblioteca.json las obras confirmadas")
    options = parser.parse_args(arguments)

    if not options.email:
        print("Falta un correo para identificarse ante Crossref. Añade LORU_CORREO a tu archivo "
              ".env o usa la opción --email tu@correo.org", file=sys.stderr)
        return 2
    if not options.library.exists():
        print(f"No encuentro {options.library}. Revisa la ruta.", file=sys.stderr)
        return 2

    works = json.loads(options.library.read_text(encoding="utf-8"))
    any_problem = False
    today = datetime.date.today().isoformat()

    for work in works:
        if not work.get("DOI"):
            print(f"· {work['id']}: sin DOI. Hay que comprobarla por ISBN o a mano.")
            continue
        try:
            result = check_work(work, options.email)
        except CrossrefConnectionError as error:
            print(f"No he podido terminar la comprobación: {error}", file=sys.stderr)
            return 2
        print(f"· {work['id']} ({result.doi}): {MESSAGES[result.outcome]}")
        for difference in result.mismatches:
            print(f"    - {difference}")
        if result.outcome == CONFIRMED and options.save:
            work["verificacion"], work["fecha_verificacion"] = "doi", today
        if result.outcome != CONFIRMED:
            any_problem = True

    if options.save:
        options.library.write_text(json.dumps(works, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Estantería actualizada: {options.library}")
    return 1 if any_problem else 0


if __name__ == "__main__":
    sys.exit(main())
