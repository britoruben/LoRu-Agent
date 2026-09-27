# Decisión 0007 · Usar pypdf (y no MarkItDown) para leer los PDF

- **Estado:** aceptada
- **Fecha:** 2026-09-27
- **Quién decide:** Rubén

## En pocas palabras

Para sacar el texto de los PDF se usa **pypdf**, porque lee la numeración de páginas que
traen muchos PDF y permite trabajar página a página. Se valoró **MarkItDown** (de Microsoft),
pero en las pruebas no sabía qué número de página impresa tiene cada página y, con un PDF
escaneado, devolvía un documento vacío sin avisar.

## Situación

El verificador de citas necesita el texto de cada obra **página a página** y con su **página
impresa**. Hacía falta elegir la herramienta que lee los PDF.

## Qué se probó (27-09-2026, MarkItDown 0.1.8 y pypdf 6.19)

Con PDF de prueba creados para la ocasión:

| Prueba | MarkItDown | pypdf |
|---|---|---|
| Texto de un PDF normal | Correcto | Correcto |
| Separar las páginas | Sí, con un carácter invisible, pero es un efecto de la librería interna que usa y no está documentado | Sí, página a página |
| Leer la numeración propia del PDF (pdf 1 = "45") | No | Sí (aunque, si el PDF no la trae, se inventa "1, 2, 3…": hay que comprobarlo antes) |
| PDF escaneado (solo imagen) | Devuelve un documento vacío **sin avisar** | Devuelve páginas vacías; nuestro programa lo detecta y avisa |
| Paquetes adicionales que instala | 6 (y más con el módulo para PDF) | Ninguno |

En los dos casos hacía falta un programa propio para averiguar la página impresa, quitar
cabeceras y avisar de los escaneos: MarkItDown no ahorraba ese trabajo.

## Decisión

- **pypdf** para los PDF, con el programa `herramientas/pdf/extraer_texto.py`.
- **MarkItDown** queda como candidato para otros formatos (Word, EPUB, páginas web), útil para
  los documentos propios de la persona usuaria, en los que no hay páginas impresas que citar.

## Consecuencias

- Hay que instalar un paquete: `pypdf` (ver `docs/instalacion.md`).
- Los PDF escaneados siguen sin poder leerse: harán falta herramientas de reconocimiento de
  texto (OCR), a decidir más adelante.
