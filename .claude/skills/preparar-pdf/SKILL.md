---
name: preparar-pdf
description: Extrae el texto de un PDF página a página, con su página impresa, para que el verificador de citas pueda comprobar citas de esa obra. Usar cuando se añada un PDF a un proyecto o se pida preparar, leer o extraer el texto de un PDF.
---

# Preparar el texto de un PDF

1. Averigua: la ruta del PDF, la carpeta del proyecto y la clave de la obra en `biblioteca.json`.
   Si la obra no está en la estantería, dilo: primero hay que añadirla y comprobarla.
2. Ejecuta (con el entorno virtual `.venv` si existe):
   `python -m herramientas.pdf.extraer_texto RUTA.pdf --proyecto CARPETA --clave CLAVE`
3. Explica el resultado en lenguaje llano:
   - cuántas páginas y qué páginas impresas;
   - **cómo se ha averiguado la paginación** (indicada, del PDF, deducida o sin determinar);
   - los avisos, sin suavizarlos. Si el PDF parece escaneado, di claramente que sus citas no se
     podrán comprobar automáticamente.
4. Si la paginación queda "sin determinar", pide a la persona usuaria qué página impresa es la
   primera del PDF y repite con `--primera-pagina N`. No la adivines.
5. Si la obra no tenía `texto_local` en `biblioteca.json`, indica que hay que añadir
   `"texto_local": "texto/CLAVE.json"`, y hazlo solo si te lo piden.
6. Abre el texto extraído y comprueba a simple vista una página: si ves cabeceras repetidas,
   notas al pie mezcladas o texto a dos columnas desordenado, avísalo.
