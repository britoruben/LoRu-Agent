"""
Leer un borrador y localizar todas sus citas.

Por qué existe: para comprobar las citas, primero hay que encontrarlas. Este módulo lee un
borrador escrito en Markdown y apunta:

- cada cita con etiqueta, por ejemplo [@arendt1958, p. 45] o [@a, pp. 3-4; @b];
- las citas literales: el texto entre comillas («...», “...” o "...") o en un bloque de
  cita (líneas que empiezan por >) que va seguido de una etiqueta;
- los huecos [FUENTE PENDIENTE: ...] que dejó el redactor;
- los textos entre comillas largos que no llevan etiqueta;
- las @etiquetas escritas en un formato que este programa no reconoce.

Sobre este último punto: si una cita estuviera escrita de una forma que el programa no
entiende, se escaparía de la comprobación sin que nadie se diera cuenta. Por eso, en lugar
de ignorarla, se avisa.

Formato de las etiquetas: es el de Pandoc, el programa que después dará formato a las citas.
"""

import re
from dataclasses import dataclass, field

# Una etiqueta de cita entre corchetes que contiene al menos una @clave.
PATRON_CITA = re.compile(r"\[([^\[\]]*@[^\[\]]*)\]")

# La clave de una obra dentro de la etiqueta: @arendt1958
PATRON_CLAVE = re.compile(r"@([A-Za-z0-9_][\w:.\-/]*)")

# La página: p. 45 · pp. 45-46 · pág. 45 · págs. 45-46 · p. xii
PATRON_PAGINA = re.compile(
    r"\b(?:p|pp|pág|págs|pag|pags)\.\s*([0-9]+|[ivxlcdm]+)"
    r"(?:\s*[-–]\s*([0-9]+|[ivxlcdm]+))?",
    re.IGNORECASE,
)

PATRON_FUENTE_PENDIENTE = re.compile(r"\[FUENTE PENDIENTE[^\]]*\]", re.IGNORECASE)

# Texto entre comillas: «...», “...” o "..."
PATRON_COMILLAS = re.compile(r"«([^»]+)»|“([^”]+)”|\"([^\"]+)\"")

# Un bloque de cita: una o más líneas seguidas que empiezan por >
PATRON_BLOQUE_DE_CITA = re.compile(r"(?:^>.*(?:\n|$))+", re.MULTILINE)

# Una @clave suelta, fuera de corchetes. No confunde correos electrónicos (nombre@dominio).
PATRON_CLAVE_SUELTA = re.compile(r"(?<![\w.])@([A-Za-z][\w:.\-]*)")

# Entre el cierre de comillas y la etiqueta solo puede haber espacios o un signo de puntuación.
SEPARACION_MAXIMA = re.compile(r"^\s*[,.;:]?\s*$")

PALABRAS_MINIMAS_PARA_AVISAR = 5


@dataclass
class ObraCitada:
    """Una obra mencionada dentro de una etiqueta, con la página si se indica."""
    clave: str
    pagina_inicio: str | None = None
    pagina_fin: str | None = None

    def describir_paginas(self) -> str:
        """Devuelve las páginas tal como se escribirían en una cita: 'p. 45' o 'pp. 45-46'."""
        if self.pagina_inicio is None:
            return "sin página"
        if self.pagina_fin:
            return f"pp. {self.pagina_inicio}-{self.pagina_fin}"
        return f"p. {self.pagina_inicio}"


@dataclass
class Cita:
    """Una etiqueta de cita del borrador y, si la acompaña, la cita literal."""
    etiqueta: str                      # el texto tal cual, p. ej. "[@arendt1958, p. 45]"
    linea: int
    obras: list[ObraCitada] = field(default_factory=list)
    texto_literal: str | None = None   # lo que va entre comillas, si es una cita literal


@dataclass
class TextoSinCita:
    """Un texto entre comillas, suficientemente largo, que no lleva etiqueta."""
    texto: str
    linea: int


@dataclass
class ContenidoDelBorrador:
    """Todo lo que el verificador necesita saber de un borrador."""
    citas: list[Cita]
    fuentes_pendientes: list[tuple[int, str]]
    textos_sin_cita: list[TextoSinCita]
    claves_no_reconocidas: list[tuple[int, str]]


def numero_de_linea(texto: str, posicion: int) -> int:
    """Devuelve en qué línea del texto (empezando por 1) está una posición."""
    return texto.count("\n", 0, posicion) + 1


def interpretar_etiqueta(interior: str) -> list[ObraCitada]:
    """
    Lee el interior de una etiqueta y devuelve las obras citadas.

    Ejemplo: "véase @a, pp. 3-4; @b" -> [ObraCitada("a", "3", "4"), ObraCitada("b")]
    """
    obras = []
    for parte in interior.split(";"):
        clave = PATRON_CLAVE.search(parte)
        if not clave:
            continue
        pagina = PATRON_PAGINA.search(parte)
        obras.append(ObraCitada(
            clave=clave.group(1).rstrip(".:"),
            pagina_inicio=pagina.group(1) if pagina else None,
            pagina_fin=pagina.group(2) if pagina else None,
        ))
    return obras


def buscar_citas_literales(texto: str) -> list[tuple[int, int, str]]:
    """
    Encuentra los textos entre comillas y los bloques de cita.

    Devuelve: una lista de (inicio, fin, texto citado). Si unas comillas están dentro de
    otras («... “x” ...»), solo se conservan las de fuera.
    """
    encontrados = []
    for coincidencia in PATRON_COMILLAS.finditer(texto):
        contenido = next(g for g in coincidencia.groups() if g is not None)
        if "\n\n" in contenido:  # unas comillas no cruzan de un párrafo a otro
            continue
        encontrados.append((coincidencia.start(), coincidencia.end(), contenido))

    for bloque in PATRON_BLOQUE_DE_CITA.finditer(texto):
        lineas = [re.sub(r"^>\s?", "", linea) for linea in bloque.group(0).splitlines()]
        contenido = " ".join(lineas).strip()
        # En un bloque de cita la etiqueta suele ir al final, dentro del propio bloque.
        etiqueta_final = re.search(r"\s*\[[^\[\]]*@[^\[\]]*\]\s*$", contenido)
        if etiqueta_final:
            contenido = contenido[: etiqueta_final.start()]
            fin = bloque.start() + bloque.group(0).rfind("[")
        else:
            fin = bloque.end()
        encontrados.append((bloque.start(), fin, contenido))

    encontrados.sort()
    sin_anidados = []
    for inicio, fin, contenido in encontrados:
        if sin_anidados and inicio < sin_anidados[-1][1]:
            continue
        sin_anidados.append((inicio, fin, contenido))
    return sin_anidados


def leer_borrador(texto: str) -> ContenidoDelBorrador:
    """
    Analiza un borrador completo.

    Recibe: el texto del borrador (Markdown).
    Devuelve: sus citas, citas literales, huecos pendientes y avisos de formato.
    """
    citas_por_posicion = {}
    for coincidencia in PATRON_CITA.finditer(texto):
        citas_por_posicion[coincidencia.start()] = Cita(
            etiqueta=coincidencia.group(0),
            linea=numero_de_linea(texto, coincidencia.start()),
            obras=interpretar_etiqueta(coincidencia.group(1)),
        )

    textos_sin_cita = []
    for inicio, fin, contenido in buscar_citas_literales(texto):
        cita_siguiente = next(
            (posicion for posicion in sorted(citas_por_posicion) if posicion >= fin), None
        )
        separa = texto[fin:cita_siguiente] if cita_siguiente is not None else "x"
        if cita_siguiente is not None and SEPARACION_MAXIMA.match(separa):
            citas_por_posicion[cita_siguiente].texto_literal = contenido
        elif len(contenido.split()) >= PALABRAS_MINIMAS_PARA_AVISAR:
            textos_sin_cita.append(TextoSinCita(contenido, numero_de_linea(texto, inicio)))

    fuentes_pendientes = [
        (numero_de_linea(texto, c.start()), c.group(0))
        for c in PATRON_FUENTE_PENDIENTE.finditer(texto)
    ]

    # Se tapan las etiquetas ya reconocidas y se buscan @claves sueltas en lo que queda.
    resto = PATRON_CITA.sub(lambda c: " " * len(c.group(0)), texto)
    claves_no_reconocidas = [
        (numero_de_linea(texto, c.start()), c.group(0))
        for c in PATRON_CLAVE_SUELTA.finditer(resto)
    ]

    return ContenidoDelBorrador(
        citas=[citas_por_posicion[p] for p in sorted(citas_por_posicion)],
        fuentes_pendientes=fuentes_pendientes,
        textos_sin_cita=textos_sin_cita,
        claves_no_reconocidas=claves_no_reconocidas,
    )
