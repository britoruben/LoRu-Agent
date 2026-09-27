"""
Verificador de citas de LoRu-Agent.

Qué hace: lee un borrador y comprueba cada cita contra la estantería del proyecto y contra el
texto original de cada obra. Escribe un informe con todos los problemas encontrados, al lado
del borrador (mismo nombre terminado en .verificacion.md).

Por qué existe: las IA a veces inventan referencias o alteran citas. Este programa no es una
IA: hace siempre las mismas comprobaciones y no se deja convencer. Si encuentra un FALLO, el
borrador no debe darse por terminado.

Qué comprueba:
- que cada obra citada está en la estantería (biblioteca.json);
- que se ha comprobado que esa obra existe (por DOI, ISBN o a mano);
- que cada cita literal lleva página;
- que la cita literal está, palabra por palabra, en el original;
- que está en la página indicada (y, si no, en cuál está);
- que no quedan huecos [FUENTE PENDIENTE].

Qué NO comprueba todavía: si una paráfrasis (una idea atribuida sin citarla literalmente)
es fiel al autor. Eso requiere comprobación asistida, que se construirá más adelante.
Mientras tanto, el informe cuenta cuántas hay para que las revises tú.

Cómo se usa (desde la carpeta de LoRu-Agent):
    python3 -m herramientas.verificacion.verificar_citas RUTA/AL/BORRADOR.md

Si el borrador está en la carpeta "borradores" de un proyecto, el programa encuentra solo la
estantería. Si no, indica la carpeta del proyecto con --proyecto RUTA.

Resultado: 0 si no hay fallos; 1 si hay fallos; 2 si no se ha podido hacer la comprobación.
"""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from . import buscar_en_texto as busqueda
from .estanteria import ErrorDeEstanteria, cargar_estanteria, cargar_texto, obra_comprobada
from .leer_borrador import Cita, ObraCitada, leer_borrador

FALLO = "FALLO"
AVISO = "AVISO"


@dataclass
class Incidencia:
    """Un problema encontrado: qué es, dónde está y qué hacer."""
    gravedad: str   # FALLO (impide terminar) o AVISO (revísalo)
    linea: int
    cita: str
    problema: str
    que_hacer: str


@dataclass
class ResultadoDeVerificacion:
    incidencias: list[Incidencia]
    total_citas: int
    citas_literales_comprobadas: int
    citas_sin_literal: int

    @property
    def fallos(self) -> list[Incidencia]:
        return [i for i in self.incidencias if i.gravedad == FALLO]

    @property
    def avisos(self) -> list[Incidencia]:
        return [i for i in self.incidencias if i.gravedad == AVISO]


def recortar(texto: str, maximo: int = 90) -> str:
    """Acorta un texto largo para mostrarlo en el informe."""
    texto = " ".join(texto.split())
    return texto if len(texto) <= maximo else texto[: maximo - 1] + "…"


def comprobar_obra(cita: Cita, obra_citada: ObraCitada, estanteria: dict) -> Incidencia | None:
    """Comprueba que la obra está en la estantería y que se ha verificado que existe."""
    obra = estanteria.get(obra_citada.clave)
    if obra is None:
        return Incidencia(
            FALLO, cita.linea, cita.etiqueta,
            f"La obra «{obra_citada.clave}» no está en la estantería del proyecto. "
            "Puede ser una referencia inventada o una clave mal escrita.",
            "Comprueba la clave. Si la obra existe, añádela a biblioteca.json y verifícala; "
            "si no, elimina la cita.",
        )
    if not obra_comprobada(obra):
        return Incidencia(
            FALLO, cita.linea, cita.etiqueta,
            f"La obra «{obra_citada.clave}» está en la estantería, pero nadie ha comprobado "
            "que exista (su campo \"verificacion\" no es doi, isbn ni manual).",
            "Compruébala con el comprobador de DOI o a mano, y anótalo en biblioteca.json.",
        )
    return None


def comprobar_cita_literal(
    cita: Cita, obra_citada: ObraCitada, carpeta_proyecto: Path, estanteria: dict
) -> Incidencia | None:
    """Comprueba que la cita literal está en el original y en la página indicada."""
    literal = recortar(cita.texto_literal or "")
    if obra_citada.pagina_inicio is None:
        return Incidencia(
            FALLO, cita.linea, cita.etiqueta,
            f"Cita literal sin página: «{literal}».",
            "Añade la página impresa donde aparece, por ejemplo [@clave, p. 45].",
        )

    texto = cargar_texto(carpeta_proyecto, estanteria[obra_citada.clave])
    if texto is None:
        return Incidencia(
            AVISO, cita.linea, cita.etiqueta,
            f"No hay texto de «{obra_citada.clave}» para comprobar la cita «{literal}».",
            "Compruébala a mano con el libro o el PDF, o añade su texto al proyecto.",
        )

    if texto.calidad == "sin_texto":
        return Incidencia(
            AVISO, cita.linea, cita.etiqueta,
            f"El PDF de «{obra_citada.clave}» parece escaneado y no tiene texto, así que no se ha "
            f"podido comprobar la cita «{literal}».",
            "Compruébala a mano con el libro o el PDF.",
        )

    paginas_citadas = obra_citada.describir_paginas()
    encontrado = busqueda.buscar_cita(
        cita.texto_literal, texto, obra_citada.pagina_inicio, obra_citada.pagina_fin
    )
    donde = ", ".join(encontrado.paginas_encontradas)

    if encontrado.resultado == busqueda.EN_SU_PAGINA:
        if texto.paginacion_confirmada:
            return None
        return Incidencia(
            AVISO, cita.linea, cita.etiqueta,
            f"La cita es exacta, pero no se sabe con seguridad la paginación impresa de "
            f"«{obra_citada.clave}» (se ha usado la numeración del PDF).",
            "Comprueba la página en el libro o el PDF, o vuelve a extraer el texto indicando "
            "la primera página impresa (--primera-pagina).",
        )
    if encontrado.resultado == busqueda.CRUZA_DE_PAGINA:
        paginas = encontrado.paginas_encontradas
        return Incidencia(
            AVISO, cita.linea, cita.etiqueta,
            f"La cita es correcta, pero ocupa más de una página (pp. {paginas[0]}-{paginas[-1]}).",
            f"Cambia «{paginas_citadas}» por «pp. {paginas[0]}-{paginas[-1]}».",
        )
    if encontrado.resultado == busqueda.EN_OTRA_PAGINA:
        return Incidencia(
            FALLO, cita.linea, cita.etiqueta,
            f"Página incorrecta: la cita «{literal}» no está en {paginas_citadas}, "
            f"sino en la página {donde}.",
            f"Corrige la página: debe ser {donde}.",
        )
    if encontrado.resultado == busqueda.PAGINA_INEXISTENTE:
        pista = f" La cita sí aparece en la página {donde}." if donde else ""
        return Incidencia(
            FALLO, cita.linea, cita.etiqueta,
            f"La página {obra_citada.pagina_inicio} no existe en el texto disponible de "
            f"«{obra_citada.clave}».{pista}",
            "Revisa el número de página.",
        )
    if encontrado.resultado == busqueda.PARECIDA:
        parecido = round(encontrado.parecido * 100)
        if texto.calidad == "ocr":
            return Incidencia(
                AVISO, cita.linea, cita.etiqueta,
                f"La cita casi coincide ({parecido} %) con la página {donde}, pero el original "
                f"es un escaneo y puede tener errores. El texto escaneado dice: "
                f"«{recortar(encontrado.pasaje_del_original, 200)}».",
                "Compruébala a mano con el libro o el PDF.",
            )
        return Incidencia(
            FALLO, cita.linea, cita.etiqueta,
            f"La cita está alterada: se parece en un {parecido} % a un pasaje de la página "
            f"{donde}, pero no es idéntica. El original dice: "
            f"«{recortar(encontrado.pasaje_del_original, 200)}».",
            "Copia la cita exactamente como está en el original.",
        )
    pista = (
        f" Lo más parecido está en la página {donde}: «{recortar(encontrado.pasaje_del_original, 200)}»."
        if encontrado.pasaje_del_original else ""
    )
    return Incidencia(
        FALLO, cita.linea, cita.etiqueta,
        f"La cita «{literal}» no aparece en «{obra_citada.clave}».{pista}",
        "Comprueba la cita en el original. Si no está, elimínala o conviértela en paráfrasis.",
    )


def verificar_borrador(texto_borrador: str, carpeta_proyecto: Path) -> ResultadoDeVerificacion:
    """
    Hace todas las comprobaciones de un borrador.

    Recibe: el texto del borrador y la carpeta del proyecto.
    Devuelve: la lista de incidencias y un recuento de citas.
    """
    estanteria = cargar_estanteria(carpeta_proyecto)
    contenido = leer_borrador(texto_borrador)
    incidencias = []
    literales_comprobadas = 0

    for linea, hueco in contenido.fuentes_pendientes:
        incidencias.append(Incidencia(
            FALLO, linea, hueco,
            "Queda una fuente pendiente: el texto necesita una obra que no está en la estantería.",
            "Busca una obra que respalde la afirmación y añádela a la estantería, o reformula la frase.",
        ))

    for cita in contenido.citas:
        obras_validas = []
        for obra_citada in cita.obras:
            problema = comprobar_obra(cita, obra_citada, estanteria)
            if problema:
                incidencias.append(problema)
            else:
                obras_validas.append(obra_citada)

        if cita.texto_literal is None or not obras_validas:
            continue
        literales_comprobadas += 1
        # Si la etiqueta cita varias obras, basta con que la cita esté en una de ellas.
        problemas = [
            comprobar_cita_literal(cita, obra, carpeta_proyecto, estanteria) for obra in obras_validas
        ]
        if all(problemas):
            incidencias.append(problemas[0])

    for sin_cita in contenido.textos_sin_cita:
        incidencias.append(Incidencia(
            AVISO, sin_cita.linea, f"«{recortar(sin_cita.texto, 60)}»",
            "Texto entre comillas sin etiqueta de cita. Si es una cita literal, falta la fuente.",
            "Añade la etiqueta con la página, o quita las comillas si no es una cita.",
        ))

    for linea, clave in contenido.claves_no_reconocidas:
        incidencias.append(Incidencia(
            AVISO, linea, clave,
            "Parece una cita, pero no está escrita entre corchetes, así que no se ha comprobado.",
            f"Escríbela como [{clave}, p. X] para que el verificador pueda revisarla.",
        ))

    incidencias.sort(key=lambda i: (i.linea, i.gravedad != FALLO))
    return ResultadoDeVerificacion(
        incidencias=incidencias,
        total_citas=len(contenido.citas),
        citas_literales_comprobadas=literales_comprobadas,
        citas_sin_literal=sum(1 for c in contenido.citas if c.texto_literal is None),
    )


def redactar_informe(resultado: ResultadoDeVerificacion, nombre_borrador: str) -> str:
    """Escribe el informe de verificación en Markdown, en lenguaje llano."""
    fallos, avisos = resultado.fallos, resultado.avisos
    if fallos:
        veredicto = (f"**NO APTO.** Hay {len(fallos)} fallo(s). El borrador no debe darse por "
                     "terminado hasta corregirlos.")
    elif avisos:
        veredicto = (f"**APTO CON AVISOS.** No hay fallos, pero hay {len(avisos)} aviso(s) que "
                     "conviene revisar.")
    else:
        veredicto = "**APTO.** No se ha encontrado ningún problema en las citas comprobadas."

    lineas = [
        f"# Informe de verificación de citas: {nombre_borrador}",
        "",
        veredicto,
        "",
        "| Qué se ha revisado | Cantidad |",
        "|---|---|",
        f"| Etiquetas de cita | {resultado.total_citas} |",
        f"| Citas literales comprobadas contra el original | {resultado.citas_literales_comprobadas} |",
        f"| Citas sin texto literal (paráfrasis o referencias generales) | {resultado.citas_sin_literal} |",
        f"| Fallos | {len(fallos)} |",
        f"| Avisos | {len(avisos)} |",
        "",
    ]
    for titulo, grupo in (("Fallos (hay que corregirlos)", fallos), ("Avisos (conviene revisarlos)", avisos)):
        if not grupo:
            continue
        lineas += [f"## {titulo}", ""]
        for numero, incidencia in enumerate(grupo, start=1):
            lineas += [
                f"{numero}. **Línea {incidencia.linea}** · `{recortar(incidencia.cita, 120)}`",
                f"   - Problema: {incidencia.problema}",
                f"   - Qué hacer: {incidencia.que_hacer}",
                "",
            ]
    lineas += [
        "## Lo que este informe NO garantiza",
        "",
        f"- Las {resultado.citas_sin_literal} citas sin texto literal solo se han comprobado en cuanto "
        "a que la obra existe. **Nadie ha comprobado todavía que el autor diga lo que se le atribuye**: "
        "revísalas tú (la comprobación asistida de paráfrasis aún no está construida).",
        "- El verificador compara con el texto disponible de cada obra. Si ese texto está incompleto "
        "o mal escaneado, puede haber errores que no detecte.",
        "",
    ]
    return "\n".join(lineas)


def ruta_de_proyecto_por_defecto(borrador: Path) -> Path:
    """Si el borrador está en proyecto/borradores/, la carpeta del proyecto es la de arriba."""
    carpeta = borrador.resolve().parent
    return carpeta.parent if carpeta.name == "borradores" else carpeta


def main(argumentos: list[str] | None = None) -> int:
    lector = argparse.ArgumentParser(
        description="Comprueba las citas de un borrador contra la estantería y los textos originales.",
    )
    lector.add_argument("borrador", type=Path, help="el borrador en Markdown (.md)")
    lector.add_argument("--proyecto", type=Path, help="carpeta del proyecto (si no se indica, se deduce)")
    opciones = lector.parse_args(argumentos)

    borrador = opciones.borrador
    if not borrador.exists():
        print(f"No encuentro el borrador {borrador}. Revisa la ruta.", file=sys.stderr)
        return 2
    carpeta_proyecto = opciones.proyecto or ruta_de_proyecto_por_defecto(borrador)

    try:
        resultado = verificar_borrador(borrador.read_text(encoding="utf-8"), carpeta_proyecto)
    except ErrorDeEstanteria as error:
        print(f"No he podido hacer la comprobación: {error}", file=sys.stderr)
        return 2

    informe = redactar_informe(resultado, borrador.name)
    ruta_informe = borrador.with_name(borrador.stem + ".verificacion.md")
    ruta_informe.write_text(informe, encoding="utf-8")

    print(f"Fallos: {len(resultado.fallos)} · Avisos: {len(resultado.avisos)} · "
          f"Citas: {resultado.total_citas}")
    print(f"Informe completo en: {ruta_informe}")
    return 1 if resultado.fallos else 0


if __name__ == "__main__":
    sys.exit(main())
