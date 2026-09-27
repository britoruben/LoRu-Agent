# Herramientas

> **En pocas palabras:** aquí están los programas que hacen el trabajo mecánico, siempre del
> mismo modo. Cada archivo empieza con una explicación en lenguaje llano de qué hace y por qué.

| Carpeta / archivo | Qué hace |
|---|---|
| `verificacion/verificar_citas.py` | El verificador: comprueba todas las citas de un borrador y escribe el informe |
| `verificacion/leer_borrador.py` | Encuentra en el borrador las citas, las citas literales y los huecos pendientes |
| `verificacion/buscar_en_texto.py` | Busca una cita en el texto original y comprueba la página |
| `verificacion/normalizar.py` | Quita diferencias tipográficas sin importancia antes de comparar |
| `verificacion/estanteria.py` | Carga la estantería del proyecto y los textos de cada obra |
| `pdf/extraer_texto.py` | Saca el texto de un PDF página a página, con su página impresa, y avisa de escaneos |
| `pdf/paginacion.py` | Averigua la página impresa y quita cabeceras y números de página |
| `fuentes/crossref.py` | Pregunta a Crossref si un DOI existe y compara los datos |
| `fuentes/comprobar_dois.py` | Comprueba todos los DOI de una estantería |

Las pruebas automáticas de estos programas están en la carpeta `tests/`.
