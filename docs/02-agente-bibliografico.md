# 02 · Flujo B — Gestión bibliográfica

Numeración: B1–B7 corresponden a las tareas 1–7 de la idea original.

| # | Tarea | Tipo | Estado de diseño |
|---|---|---|---|
| B1 | Acceso a repositorios públicos | Determinista (APIs) | Definido |
| B2 | Acceso a bases de datos privadas | Determinista (API oficial) | **ABIERTO** — ver P-03 |
| B3 | Búsqueda temática y selección de los más relevantes | Mixto | Definido (pesos por validar) |
| B4 | Descarga de documentos | Determinista | Parcial (depende de B2) |
| B5 | Análisis de contenido | LLM | Definido |
| B6 | Análisis de referencias y bucle | Mixto | Definido |
| B7 | Estado de la cuestión, disputas, errores, vacíos | LLM | Definido |

---

## B1 · Repositorios públicos

- **Entrada:** `proyecto.yaml` (pregunta, disciplina, periodo, idiomas).
- **Proceso:** traducir la pregunta a consultas por fuente (el LLM propone términos y sinónimos,
  el usuario valida); ejecutar contra las fuentes del perfil; normalizar a un esquema común;
  deduplicar por DOI → PMID → título normalizado + año.
- **Salida:** `candidatos.csv` (id, título, autores, año, tipo, DOI, fuente(s), citas, OA sí/no, URL).
- **Fuentes:** ver `04-fuentes-y-acceso.md`.

## B2 · Bases privadas

**Pendiente de la reunión con Lola** (P-03). Diseño condicionado:
- Si hay API oficial (Scopus, WoS…): cliente en `herramientas/fuentes/` igual que B1.
- Si solo hay acceso web institucional: **no se automatiza el login/descarga**. El agente genera
  una lista priorizada con enlaces y el usuario descarga manualmente en `pdf/`.

## B3 · Selección por relevancia

"Más citado" solo no es un buen criterio (sesgo a lo antiguo, cobertura desigual, varía según la
fuente). Puntuación compuesta configurable:

| Señal | Qué mide | Nota |
|---|---|---|
| Citas totales | Impacto acumulado | Tomar máximo entre fuentes, registrar cuál |
| Citas / año desde publicación | Impacto normalizado por edad | Evita enterrar lo reciente |
| Centralidad en la red del corpus | Cuánto lo citan *los demás documentos del tema* | Disponible tras B6; la más fiable temáticamente |
| Similitud semántica con la pregunta | Pertinencia | Juicio del LLM sobre título+resumen, con justificación |
| Recencia | Estado actual del debate | Peso bajo |

**Punto de control humano:** el usuario revisa `candidatos.csv` y produce `seleccion.csv`.

## B4 · Recuperación de documentos

Orden de intento: 1) Unpaywall / versión OA del editor; 2) repositorios (arXiv, PMC, CORE,
repositorios institucionales); 3) acceso privado según B2; 4) lista de "no disponibles" para
gestión manual (préstamo interbibliotecario, contacto con autor).

Registrar siempre la procedencia y la versión (preprint / aceptada / publicada): **para citar con
página hay que usar la versión publicada**.

## B5 · Análisis de contenido

Un subagente `lector` por documento. Produce una ficha estructurada:

```yaml
id: doi:10.xxxx/yyyy
tesis_principal: "..."
preguntas: [...]
metodologia: "..."
datos_o_corpus: "..."
hallazgos: [{afirmacion: "...", pagina: 12}]
conceptos_clave: [...]
posiciona_contra: [{id: ..., en_que: "..."}]
posiciona_a_favor: [{id: ..., en_que: "..."}]
limitaciones_declaradas: [...]
limitaciones_detectadas: [...]
citas_textuales_relevantes: [{texto: "...", pagina_impresa: 45}]
calidad_extraccion: ok | ocr | parcial
```

Toda `pagina` se valida contra el texto extraído (ver `05`).

## B6 · Referencias y snowballing

- Extraer referencias (preferente: metadatos de OpenAlex/Crossref; alternativa: parser de
  referencias sobre el PDF, p. ej. GROBID — **a evaluar**).
- Construir `grafo.json` (documentos del corpus + referencias).
- Detectar referencias muy citadas dentro del corpus que no están en él → nuevos candidatos.
- **Hacia atrás** (lo que citan) y **hacia delante** (quién los cita).
- **Criterio de parada:** profundidad máxima, máximo de nuevos candidatos por ronda, o
  saturación (una ronda aporta < N documentos nuevos relevantes).
- Cada ronda vuelve a pasar por el control humano de B3.

## B7 · Estado de la cuestión

Salida `estado-cuestion.md` con:
1. Mapa del campo (líneas / escuelas / enfoques) con documentos de referencia.
2. Consensos.
3. **Disputas:** posiciones enfrentadas, quién sostiene qué, con cita y página.
4. **Errores:** afirmaciones refutadas o mal citadas en la literatura (con evidencia).
5. **Vacíos:** preguntas no abordadas, poblaciones/periodos/métodos ausentes.
6. Tabla de trazabilidad: afirmación → documento → página.

Advertencia: la detección de "errores" y "vacíos" por un LLM es una **hipótesis a revisar**, no
un hallazgo. El documento lo debe indicar.
