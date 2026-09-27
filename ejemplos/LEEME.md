# Ejemplos: qué se puede probar ya

> **En pocas palabras:** ya funciona un primer prototipo del **verificador de citas** y del
> **extractor de texto de PDF**. Hay un proyecto de ejemplo con un PDF y dos borradores: uno
> correcto y otro con 12 errores puestos a propósito.
> Puedes ver los informes que produce sin instalar nada, o ejecutarlo tú misma/o con Claude Code.
> Todas las obras del ejemplo son **ficticias**, inventadas solo para probar.

## 1. Ver el resultado sin instalar nada

Abre estos archivos (en GitHub se ven con formato):

| Archivo | Qué es |
|---|---|
| [`proyecto-demo/borradores/borrador-con-errores.md`](proyecto-demo/borradores/borrador-con-errores.md) | Un breve texto sobre opacidad y responsabilidad, con errores a propósito |
| [`proyecto-demo/borradores/borrador-con-errores.verificacion.md`](proyecto-demo/borradores/borrador-con-errores.verificacion.md) | **El informe del verificador**: 8 fallos y 4 avisos |
| [`proyecto-demo/borradores/borrador-correcto.md`](proyecto-demo/borradores/borrador-correcto.md) | El mismo tema, con las citas bien hechas |
| [`proyecto-demo/borradores/borrador-correcto.verificacion.md`](proyecto-demo/borradores/borrador-correcto.verificacion.md) | Su informe: APTO |

## 2. Las 12 trampas del borrador con errores

| # | Trampa | Qué dice el verificador |
|---|---|---|
| 1 | Una palabra cambiada en una cita ("motivos" en vez de "razones") | FALLO: cita alterada, y muestra el original |
| 2 | Cita correcta con la página equivocada | FALLO: página incorrecta, y dice cuál es la buena |
| 3 | Obra inventada (`inventado2020`) | FALLO: la obra no está en la estantería |
| 4 | Cita que empieza en una página y acaba en la siguiente, citada con una sola página | AVISO: propone "pp. 46-47" |
| 5 | Cita literal sin página | FALLO |
| 6 | Cita literal inventada, atribuida a una obra real del proyecto | FALLO: no aparece en la obra |
| 7 | Página que no existe (p. 200 de un artículo de 3 páginas) | FALLO, y dice en qué página sí está la cita |
| 8 | Obra añadida a la estantería pero nunca comprobada | FALLO |
| 9 | Cita de un libro escaneado con errores de reconocimiento ("prornete" por "promete") | AVISO: casi coincide; comprobar a mano |
| 10 | Hueco `[FUENTE PENDIENTE]` | FALLO: bloquea la versión final |
| 11 | Texto largo entre comillas sin fuente | AVISO |
| 12 | Cita escrita en un formato que el verificador no reconoce | AVISO: no se ha podido comprobar |

## 3. Del PDF al texto con páginas

El texto de la obra ficticia `ficticia2021` que usa el verificador **se ha sacado de un PDF**:
[`proyecto-demo/pdf/ficticia2021.pdf`](proyecto-demo/pdf/ficticia2021.pdf). Ese PDF imita un
libro: su página 1 es la página 45 impresa, lleva cabeceras que alternan autora y título, una
página sin número (inicio de capítulo) y una palabra partida al final de una línea.

El extractor ha averiguado solo las páginas impresas (45 a 48), ha quitado cabeceras y números
y ha guardado el resultado en
[`proyecto-demo/texto/ficticia2021.json`](proyecto-demo/texto/ficticia2021.json). Con ese texto,
el verificador da exactamente los mismos resultados que se ven arriba.

Para repetirlo (ver apartado 5 para los requisitos):

```
python -m herramientas.pdf.extraer_texto ejemplos/proyecto-demo/pdf/ficticia2021.pdf --proyecto ejemplos/proyecto-demo --clave ficticia2021
```

O, en Claude Code: `/preparar-pdf ejemplos/proyecto-demo/pdf/ficticia2021.pdf` (clave `ficticia2021`).

## 4. Probarlo con Claude Code

Requisitos: haber seguido la [guía de instalación](../docs/instalacion.md).

1. Abre la terminal en la carpeta `LoRu-Agent` y escribe `claude`.
2. Escribe: `/verificar-citas ejemplos/proyecto-demo/borradores/borrador-con-errores.md`
3. Claude encarga la tarea al ayudante verificador y te explica los resultados.

Prueba también a pedirle, en lenguaje normal: *"Corrige las páginas que el informe permite
corregir y vuelve a verificar"*. Observa que no inventa correcciones: solo corrige lo que el
informe respalda.

## 5. Probarlo sin Claude (solo el programa)

En la terminal, dentro de la carpeta `LoRu-Agent` y con el entorno virtual activo (ver la
[guía de instalación](../docs/instalacion.md)):

```
python -m herramientas.verificacion.verificar_citas ejemplos/proyecto-demo/borradores/borrador-con-errores.md
```

Para comprobar que todo el programa funciona, ejecuta las **pruebas automáticas** (más de 50
casos con respuesta conocida):

```
python -m unittest -v
```

## 6. Comprobar DOI reales contra Crossref

Ver [`comprobar-doi/LEEME.md`](comprobar-doi/LEEME.md). Necesita conexión a internet.

## Qué NO hace todavía (con honestidad)

- **No comprueba paráfrasis.** Si el borrador atribuye una idea a un autor sin citarlo
  literalmente, solo se comprueba que la obra existe, no que el autor diga eso. El informe lo
  recuerda siempre.
- **El extractor de PDF solo se ha probado con PDF creados para las pruebas.** Los PDF reales de
  editoriales traen dos columnas, notas al pie, guiones de todo tipo... Habrá sorpresas.
- **No lee PDF escaneados.** Los detecta y avisa, pero no puede sacar su texto (hace falta OCR).
- **No reconoce páginas con números romanos** (prólogos, introducciones).
- **No distingue mayúsculas de minúsculas** al comparar, porque al citar a mitad de frase es
  normal cambiar la inicial. Un cambio de mayúsculas deliberado no se detectaría.
- **Descarta trozos de una sola letra** entre omisiones (`[...] y [...]`), porque no sirven para
  comprobar nada.
- Es un **prototipo**: solo se ha probado con estos ejemplos. Hará falta probarlo con textos
  reales del proyecto piloto.
