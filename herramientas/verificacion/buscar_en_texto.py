"""
Buscar una cita literal en el texto original.

Por qué existe: es el corazón del verificador. Dada una cita y la página que se indica,
responde a tres preguntas:

1. ¿Está la cita, tal cual, en esa página?
2. Si no, ¿está en otra página? (entonces la página de la cita es incorrecta)
3. Si no está tal cual en ninguna parte, ¿hay un pasaje muy parecido? (entonces la cita
   está alterada, o el texto del original tiene errores de escaneo)

Cómo compara: primero normaliza los dos textos (ver normalizar.py). Si la cita tiene
omisiones ([...]), comprueba que cada trozo aparece en el original y en el mismo orden.
"""

from dataclasses import dataclass
from difflib import SequenceMatcher

from .estanteria import Pagina, TextoDeObra
from .normalizar import dividir_en_fragmentos, normalizar_texto

# A partir de qué parecido (de 0 a 1) se considera que un pasaje "casi coincide".
PARECIDO_MINIMO = 0.85
# A partir de qué parecido se muestra el pasaje más cercano como pista.
PARECIDO_PARA_PISTA = 0.6

SIGNOS_DE_PUNTUACION = ".,;:!?¡¿\"'()"

# Resultados posibles de la búsqueda.
EN_SU_PAGINA = "en_su_pagina"
CRUZA_DE_PAGINA = "cruza_de_pagina"
EN_OTRA_PAGINA = "en_otra_pagina"
PARECIDA = "parecida"
NO_ENCONTRADA = "no_encontrada"
PAGINA_INEXISTENTE = "pagina_inexistente"


@dataclass
class ResultadoDeBusqueda:
    """Qué se encontró al buscar una cita en el original."""
    resultado: str
    paginas_encontradas: list[str]
    pasaje_del_original: str = ""
    parecido: float = 0.0


def es_numero(pagina: str | None) -> bool:
    return pagina is not None and pagina.isdigit()


def posiciones_de_paginas(texto: TextoDeObra, inicio: str, fin: str | None) -> list[int]:
    """
    Devuelve las posiciones (0, 1, 2...) de las páginas citadas dentro del documento.

    Si la cita dice "pp. 45-47", devuelve las posiciones de las páginas 45, 46 y 47.
    Devuelve una lista vacía si la página no existe en el texto disponible.
    """
    if fin and es_numero(inicio) and es_numero(fin):
        rango = range(int(inicio), int(fin) + 1)
        return [i for i, p in enumerate(texto.paginas) if es_numero(p.impresa) and int(p.impresa) in rango]
    return [i for i, p in enumerate(texto.paginas) if p.impresa.casefold() == inicio.casefold()]


def unir_paginas(paginas: list[Pagina]) -> str:
    """Une varias páginas en un solo texto normalizado (respeta las palabras partidas)."""
    return normalizar_texto("\n".join(p.texto for p in paginas))


def contiene_en_orden(texto: str, fragmentos: list[str]) -> bool:
    """Comprueba que todos los trozos aparecen en el texto, uno detrás de otro."""
    posicion = 0
    for fragmento in fragmentos:
        encontrado = texto.find(fragmento, posicion)
        if encontrado == -1:
            return False
        posicion = encontrado + len(fragmento)
    return True


def quitar_puntuacion(palabras: list[str]) -> str:
    """Une las palabras sin los signos de puntuación pegados a ellas."""
    return " ".join(palabra.strip(SIGNOS_DE_PUNTUACION) for palabra in palabras)


def pasaje_mas_parecido(cita: str, texto: str) -> tuple[str, float]:
    """
    Busca en el texto el pasaje que más se parece a la cita.

    Devuelve: el pasaje y su parecido, de 0 (nada que ver) a 1 (idéntico).

    Cómo lo hace: recorre el texto con una "ventana" del mismo número de palabras que la
    cita y compara letra a letra, sin puntuación. Se compara letra a letra (y no palabra a
    palabra) para que un error de escaneo como "prornete" en lugar de "promete" cuente como
    una diferencia pequeña y no como una palabra entera distinta.
    """
    palabras_cita = cita.split()
    palabras_texto = texto.split()
    tamano = len(palabras_cita)
    if tamano == 0 or not palabras_texto:
        return "", 0.0
    cita_sin_puntuacion = quitar_puntuacion(palabras_cita)
    mejor_pasaje, mejor_parecido = "", 0.0
    for inicio in range(max(1, len(palabras_texto) - tamano + 1)):
        ventana = palabras_texto[inicio: inicio + tamano]
        comparador = SequenceMatcher(None, cita_sin_puntuacion, quitar_puntuacion(ventana))
        if comparador.quick_ratio() <= mejor_parecido:
            continue
        parecido = comparador.ratio()
        if parecido > mejor_parecido:
            mejor_pasaje, mejor_parecido = " ".join(ventana), parecido
    return mejor_pasaje, mejor_parecido


def buscar_en_una_pagina(texto: TextoDeObra, fragmentos: list[str]) -> list[str] | None:
    """Busca la cita entera dentro de una sola página. Devuelve esa página o None."""
    for pagina in texto.paginas:
        if contiene_en_orden(unir_paginas([pagina]), fragmentos):
            return [pagina.impresa]
    return None


def buscar_entre_dos_paginas(texto: TextoDeObra, fragmentos: list[str]) -> list[str] | None:
    """Busca la cita repartida entre dos páginas seguidas. Devuelve ambas o None."""
    for i in range(len(texto.paginas) - 1):
        pareja = texto.paginas[i: i + 2]
        if contiene_en_orden(unir_paginas(pareja), fragmentos):
            return [p.impresa for p in pareja]
    return None


def buscar_cita(cita: str, texto: TextoDeObra, inicio: str, fin: str | None = None) -> ResultadoDeBusqueda:
    """
    Busca una cita literal en el original y dice si la página es correcta.

    Recibe: la cita, el texto de la obra y la página (o páginas) que indica el borrador.
    Devuelve: un ResultadoDeBusqueda con lo encontrado.
    """
    fragmentos = dividir_en_fragmentos(cita)
    posiciones = posiciones_de_paginas(texto, inicio, fin)

    if posiciones:
        citadas = [texto.paginas[i] for i in posiciones]
        if contiene_en_orden(unir_paginas(citadas), fragmentos):
            return ResultadoDeBusqueda(EN_SU_PAGINA, [p.impresa for p in citadas])

    # Si está entera en otra página, la página citada es incorrecta.
    en_otra = buscar_en_una_pagina(texto, fragmentos)
    if en_otra:
        return ResultadoDeBusqueda(EN_OTRA_PAGINA if posiciones else PAGINA_INEXISTENTE, en_otra)

    if posiciones:
        # ¿Empieza en la página citada y sigue en la siguiente (o empieza en la anterior)?
        primera, ultima = posiciones[0], posiciones[-1]
        for desde, hasta in ((primera, ultima + 1), (primera - 1, ultima)):
            if 0 <= desde and hasta < len(texto.paginas):
                ampliadas = texto.paginas[desde: hasta + 1]
                if contiene_en_orden(unir_paginas(ampliadas), fragmentos):
                    return ResultadoDeBusqueda(CRUZA_DE_PAGINA, [p.impresa for p in ampliadas])

    entre_dos = buscar_entre_dos_paginas(texto, fragmentos)
    if entre_dos:
        return ResultadoDeBusqueda(EN_OTRA_PAGINA if posiciones else PAGINA_INEXISTENTE, entre_dos)

    # No está tal cual: se busca el pasaje más parecido, primero en las páginas citadas.
    cita_completa = " ".join(fragmentos)
    zonas = [[texto.paginas[i] for i in posiciones]] if posiciones else []
    zonas.append(texto.paginas)
    mejor = ("", 0.0, [])
    for zona in zonas:
        for pagina in zona:
            pasaje, parecido = pasaje_mas_parecido(cita_completa, unir_paginas([pagina]))
            if parecido > mejor[1]:
                mejor = (pasaje, parecido, [pagina.impresa])
        if mejor[1] >= PARECIDO_MINIMO:
            break

    pasaje, parecido, paginas = mejor
    if parecido >= PARECIDO_MINIMO:
        return ResultadoDeBusqueda(PARECIDA, paginas, pasaje, parecido)
    if not posiciones:
        return ResultadoDeBusqueda(PAGINA_INEXISTENTE, [], pasaje if parecido >= PARECIDO_PARA_PISTA else "", parecido)
    pista = pasaje if parecido >= PARECIDO_PARA_PISTA else ""
    return ResultadoDeBusqueda(NO_ENCONTRADA, paginas if pista else [], pista, parecido)
