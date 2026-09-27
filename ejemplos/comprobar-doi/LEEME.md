# Ejemplo: comprobar DOI en Crossref

> **En pocas palabras:** la estantería de esta carpeta tiene cuatro obras sobre IA y filosofía
> de la mente. Dos están bien, una tiene el año equivocado a propósito y otra es inventada. El
> comprobador pregunta a Crossref (el registro oficial de DOI) y debería detectar los dos
> problemas.

| Clave | Obra | Qué debería pasar |
|---|---|---|
| `turing1950` | Turing, "Computing Machinery and Intelligence", *Mind*, 1950 | CONFIRMADA |
| `searle1980` | Searle, "Minds, brains, and programs", *Behavioral and Brain Sciences*, 1980 | CONFIRMADA |
| `lecun2016` | LeCun et al., "Deep learning", *Nature* — con el año cambiado a 2016 (es 2015) | DISCREPANCIAS: año distinto |
| `inventada2023` | Obra y DOI inventados | NO EXISTE |

**Aviso honesto:** este ejemplo **no se ha podido ejecutar todavía contra el Crossref real**,
porque el entorno en la nube donde se construyó no tiene acceso a Crossref. La lógica sí está
probada con respuestas simuladas (pruebas automáticas en `tests/test_crossref.py`). La primera
ejecución real, en tu ordenador, es la prueba de verdad: si algún resultado no coincide con la
tabla, apúntalo.

## Cómo ejecutarlo

En la terminal, dentro de la carpeta `LoRu-Agent`, con conexión a internet:

```
python3 -m tools.sources.check_dois ejemplos/comprobar-doi/biblioteca.json --email tu@correo.org
```

Con `--save`, las obras confirmadas quedan marcadas como comprobadas en `biblioteca.json`
(las que tienen problemas nunca se marcan).
