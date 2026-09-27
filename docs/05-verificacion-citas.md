# 05 · Verificación de citas (anti-alucinación)

Este es el componente que hace el sistema **fiable**. Si solo se implementa bien una cosa, que sea esta.

## Principio

El modelo **no genera referencias**. Solo usa **claves** de una biblioteca verificada. El formato
lo aplica CSL. Un verificador determinista revisa el borrador y bloquea lo que no cuadra.

## 1. Biblioteca verificada (`biblioteca.json`, CSL-JSON)

Una entrada solo entra en la biblioteca si:
- Tiene DOI y ese DOI **resuelve** en Crossref (o DataCite), y título/año/primer autor coinciden
  con tolerancia; **o**
- No tiene DOI (libros, capítulos, fuentes antiguas) y se valida con ISBN / catálogo, o la
  introduce manualmente el usuario (marcada `verificacion: manual`).

Campos adicionales: `verificacion` (doi | isbn | manual), `fecha_verificacion`, `pdf_local`,
`texto_local`, `version` (preprint | aceptada | publicada).

## 2. Mapa de páginas

Al extraer el texto de un PDF se genera `texto/<id>.json`:

```json
{"paginas": [{"pdf": 1, "impresa": "45", "texto": "..."}, ...], "calidad": "ok|ocr"}
```

La página impresa se obtiene de: 1) metadatos de etiquetas de página del PDF; 2) detección del
número en cabecera/pie; 3) desfase declarado por el usuario (p. ej. "pdf 1 = p. 45"). Si no se
puede determinar, las citas de ese documento requieren revisión manual.

## 3. Verificador (`herramientas/verificacion/`)

Sobre un borrador comprueba:

| Comprobación | Resultado si falla |
|---|---|
| Cada `[@clave]` existe en `biblioteca.json` | FALLO: referencia inexistente |
| Cada DOI de la biblioteca sigue resolviendo | AVISO |
| Cada cita textual entre comillas con `[@clave, p. X]` aparece en el texto de `clave` | FALLO: cita no encontrada |
| La cita aparece en la página X impresa | FALLO: página incorrecta (sugiere la correcta) |
| Afirmaciones atribuidas (paráfrasis) | **Verificación asistida:** se localiza el pasaje más probable (búsqueda semántica en el texto de la fuente) y se muestra junto a la paráfrasis para confirmación humana. Sin pasaje localizable → AVISO destacado |
| `[FUENTE PENDIENTE]` restantes | BLOQUEA versión final |

Salida: `borradores/<nombre>.verificacion.md` con la lista de incidencias.

## 4. Integración como guardarraíl

- El subagente `verificador` no puede editar el borrador (solo lee y reporta).
- Un **hook** de Claude Code ejecuta el verificador al generar la versión final; con FALLOS, se
  bloquea la exportación.

## Límites honestos

- La verificación de **paráfrasis** (que un autor realmente sostiene X) no es 100 % automatizable;
  se ofrece como apoyo, con revisión humana.
- Con OCR de baja calidad, la coincidencia literal puede fallar con citas correctas.
