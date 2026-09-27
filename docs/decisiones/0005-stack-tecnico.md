# ADR-0005 · Stack técnico, formatos, idiomas y modelo de uso

- **Estado:** aceptada
- **Fecha:** 2026-09-27
- **Decisores:** Rubén
- **Cierra:** P-02, P-06, P-07, P-08

## Decisión

| Tema | Decisión |
|---|---|
| Lenguaje de herramientas (P-02) | **Python** (PDF, OCR, bibliometría, redes, embeddings) |
| Formatos de salida (P-06) | **Markdown** como fuente; exportación con Pandoc a **.docx** y **LaTeX/PDF** |
| Idiomas (P-07) | Búsqueda bilingüe **español + inglés**; redacción en el idioma de la revista |
| Uso de Claude (P-08) | **Claude Code con plan Pro/Max** (coste fijo) |

## Alternativas consideradas

- TypeScript: bueno para servidores MCP, pero ecosistema científico más pobre.
- API por uso: más control por proyecto, pero coste variable y más configuración.

## Consecuencias

- Dependencias externas: Python 3.11+, Pandoc; más adelante OCR (p. ej. Tesseract) y un modelo de
  embeddings para la verificación asistida (a elegir en fase 2).
- **Los planes Pro/Max tienen límites de uso por ventana de tiempo.** Por eso los flujos largos
  (lectura de 40+ documentos) deben ser **reanudables**: el estado se guarda en disco tras cada
  documento y un comando puede continuar donde se quedó.
- La plantilla `proyecto.yaml` incluye `idiomas: [es, en]` por defecto.
