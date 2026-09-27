"""
Averiguar la página impresa de cada página de un PDF y limpiar cabeceras y pies.

Por qué existe: para citar hay que usar la página impresa (la del libro o la revista), no la
del PDF. La página 1 de un PDF puede ser la 45 del libro. Además, cada página suele llevar
una cabecera que se repite (el título del libro, el nombre de la autora) y el número de
página, que no forman parte del texto y estorban al buscar citas.

Cómo averigua la página impresa, por este orden de preferencia:
1. Si la persona usuaria la indica ("la página 1 del PDF es la 45").
2. Si el PDF trae su propia numeración de páginas (muchos PDF de editoriales la traen).
3. Si encuentra números de página en las primeras o últimas líneas y encajan entre sí.
   Cada página se queda con el número que lleva impreso; las que no llevan número se
   completan a partir de sus vecinas (45, 46, sin número, 48 → la tercera es la 47). Si la
   numeración salta (50 → 52), se avisa: puede faltar una página en el PDF.
4. Si nada de lo anterior funciona, usa la numeración del PDF y lo deja anotado como
   "sin determinar", para que las citas de ese documento se revisen a mano.

Limitaciones conocidas:
- No reconoce números romanos (páginas de prólogos o introducciones).
- Si un PDF junta varios documentos, las páginas del documento sin números reciben números
  deducidos de las del otro.
"""

import re
from collections import Counter

# Cuántas líneas del principio y del final de cada página se miran en busca de cabeceras,
# pies y números de página.
LINEAS_A_REVISAR = 2

# Número de página suelto ("45", "- 45 -", "— 45 —") o al principio/final de la cabecera
# ("112   REVISTA...", "...COMPRENSIÓN   113").
NUMERO_SOLO = re.compile(r"^[\s\-–—]*(\d{1,4})[\s\-–—]*$")
NUMERO_AL_PRINCIPIO = re.compile(r"^(\d{1,4})\s+\S")
NUMERO_AL_FINAL = re.compile(r"\S\s+(\d{1,4})$")

# Proporción mínima de páginas en las que debe aparecer una línea para considerarla cabecera.
# Es baja (40 %) porque muchos libros alternan dos cabeceras: autor en las pares y título en
# las impares.
PROPORCION_CABECERA = 0.4

# Distancia máxima entre el número que se espera en una página y el que lleva impreso para
# aceptarlo como su número de página. Evita confundir con el número de página un año, una
# cifra del texto o una marca de imprenta.
DISTANCIA_MAXIMA = 5

ORIGEN_INDICADO = "indicada_a_mano"
ORIGEN_PDF = "numeracion_del_pdf"
ORIGEN_DETECTADO = "numeros_detectados"
ORIGEN_SIN_DETERMINAR = "sin_determinar"


def lineas_de_los_bordes(lineas: list[str]) -> list[str]:
    """Devuelve las primeras y últimas líneas de una página (donde van cabeceras y pies)."""
    if len(lineas) <= 2 * LINEAS_A_REVISAR:
        return lineas
    return lineas[:LINEAS_A_REVISAR] + lineas[-LINEAS_A_REVISAR:]


def numeros_candidatos(linea: str) -> set[int]:
    """Devuelve los números que podrían ser un número de página dentro de una línea."""
    linea = linea.strip()
    candidatos = set()
    for patron in (NUMERO_SOLO, NUMERO_AL_PRINCIPIO, NUMERO_AL_FINAL):
        coincidencia = patron.search(linea)
        if coincidencia:
            candidatos.add(int(coincidencia.group(1)))
    return candidatos


def detectar_desfase(paginas_en_lineas: list[list[str]]) -> int | None:
    """
    Busca la diferencia constante entre la página del PDF y la página impresa.

    Recibe: las líneas de cada página.
    Devuelve: el desfase (página impresa = página del PDF + desfase), o None si no hay
    suficientes números que encajen entre sí.

    Por qué así: un número suelto al principio de una página puede ser un año o una nota.
    Pero si en casi todas las páginas aparece un número que es "página del PDF + 44", eso
    es la numeración del libro.
    """
    votos = Counter()
    paginas_con_texto = 0
    for posicion, lineas in enumerate(paginas_en_lineas, start=1):
        if not lineas:
            continue
        paginas_con_texto += 1
        desfases = {n - posicion for linea in lineas_de_los_bordes(lineas) for n in numeros_candidatos(linea)}
        votos.update(desfases)
    if not votos:
        return None
    desfase, apoyos = votos.most_common(1)[0]
    minimo = 1 if paginas_con_texto == 1 else max(2, paginas_con_texto / 2)
    return desfase if apoyos >= minimo else None


def numero_propio(lineas: list[str], esperado: int) -> int | None:
    """
    Devuelve el número de página impreso en esta página, si hay uno cerca del esperado.

    Si hay varios candidatos, elige el más cercano al esperado.
    """
    candidatos = {n for linea in lineas_de_los_bordes(lineas) for n in numeros_candidatos(linea)}
    cercanos = [n for n in candidatos if abs(n - esperado) <= DISTANCIA_MAXIMA]
    return min(cercanos, key=lambda n: abs(n - esperado)) if cercanos else None


def asignar_paginas_impresas(paginas_en_lineas: list[list[str]]) -> tuple[list[str], list[str]] | None:
    """
    Asigna a cada página del PDF su página impresa a partir de los números que lleva.

    Recibe: las líneas de cada página.
    Devuelve: (páginas impresas, avisos), o None si no hay números de página fiables.

    Cómo: primero comprueba que el documento tiene numeración (detectar_desfase). Después,
    cada página se queda con su propio número; las páginas sin número se completan
    contando desde la anterior (o hacia atrás desde la primera numerada).
    """
    desfase = detectar_desfase(paginas_en_lineas)
    if desfase is None:
        return None

    propios = []
    anterior = None
    for posicion, lineas in enumerate(paginas_en_lineas, start=1):
        esperado = anterior + 1 if anterior is not None else posicion + desfase
        numero = numero_propio(lineas, esperado) if lineas else None
        propios.append(numero)
        anterior = numero if numero is not None else esperado

    impresas = []
    primera_con_numero = next(i for i, n in enumerate(propios) if n is not None)
    for posicion, numero in enumerate(propios):
        if numero is not None:
            impresas.append(numero)
        elif posicion < primera_con_numero:
            impresas.append(propios[primera_con_numero] - (primera_con_numero - posicion))
        else:
            impresas.append(impresas[-1] + 1)

    avisos = avisos_de_numeracion(impresas)
    deducidas = [f"{posicion} (→ {impresas[posicion - 1]})"
                 for posicion, numero in enumerate(propios, start=1)
                 if numero is None and paginas_en_lineas[posicion - 1]]
    if deducidas:
        avisos.append("Páginas del PDF sin número impreso, numeradas por deducción: "
                      f"{', '.join(deducidas)}. Si citas alguna, comprueba la página.")
    return [str(n) for n in impresas], avisos


def avisos_de_numeracion(impresas: list[int]) -> list[str]:
    """Señala los saltos y las repeticiones en la numeración de páginas."""
    avisos = []
    for posicion in range(1, len(impresas)):
        anterior, actual = impresas[posicion - 1], impresas[posicion]
        donde = f"(páginas {posicion} y {posicion + 1} del PDF)"
        if actual > anterior + 1:
            avisos.append(f"La numeración salta de la página {anterior} a la {actual} {donde}: "
                          "puede faltar alguna página en el PDF.")
        elif actual <= anterior:
            avisos.append(f"La numeración se repite o retrocede, de la página {anterior} a la {actual} "
                          f"{donde}: puede haber páginas de otro documento intercaladas.")
    return avisos


def quitar_numero_de_pagina(lineas: list[str], impresa: str) -> list[str]:
    """
    Quita de las líneas de cabecera o pie la que lleva el número de página impresa.

    Se quita la línea entera, también cuando el número va junto a un texto
    ("112   REVISTA DE FILOSOFÍA"): una línea así es casi siempre una cabecera.
    """
    if not impresa.isdigit():
        return lineas
    bordes = set(range(LINEAS_A_REVISAR)) | set(range(len(lineas) - LINEAS_A_REVISAR, len(lineas)))
    return [linea for indice, linea in enumerate(lineas)
            if not (indice in bordes and int(impresa) in numeros_candidatos(linea))]


def forma_de_cabecera(linea: str) -> str:
    """Simplifica una línea para reconocer cabeceras repetidas (sin números ni mayúsculas)."""
    return re.sub(r"\d+", "", linea).strip(" -–—").casefold()


def quitar_cabeceras_repetidas(paginas_en_lineas: list[list[str]]) -> list[list[str]]:
    """
    Quita las líneas de cabecera o pie que se repiten en muchas páginas.

    Solo actúa si el documento tiene al menos 3 páginas: con menos, no se puede distinguir
    una cabecera de una frase que casualmente se repite.
    """
    con_texto = [lineas for lineas in paginas_en_lineas if lineas]
    if len(con_texto) < 3:
        return paginas_en_lineas
    apariciones = Counter()
    for lineas in con_texto:
        apariciones.update({forma_de_cabecera(l) for l in lineas_de_los_bordes(lineas) if forma_de_cabecera(l)})
    cabeceras = {forma for forma, veces in apariciones.items()
                 if veces >= 2 and veces >= PROPORCION_CABECERA * len(con_texto)}

    limpias = []
    for lineas in paginas_en_lineas:
        bordes = set(range(LINEAS_A_REVISAR)) | set(range(len(lineas) - LINEAS_A_REVISAR, len(lineas)))
        limpias.append([l for i, l in enumerate(lineas)
                        if not (i in bordes and forma_de_cabecera(l) in cabeceras)])
    return limpias
