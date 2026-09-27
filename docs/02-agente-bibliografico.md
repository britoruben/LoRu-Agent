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
- **Proceso:** traducir la pregunta a consultas por fuente, **en español e inglés** (el LLM propone
  términos, sinónimos y traducciones; el usuario valida en PC-1); ejecutar contra las fuentes del perfil; normalizar a un esquema común;
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

Cada candidato lleva en `candidatos.csv` su puntuación desglosada por señal y una columna
`motivo` con **una frase de justificación** (p. ej. "Muy citado dentro del corpus (12/40) y aborda
directamente la variable X"). Sin justificación, la puntuación no se muestra.

Pesos por defecto (a calibrar en el proyecto piloto): citas 0,2 · citas/año 0,25 ·
centralidad 0,25 · pertinencia 0,25 · recencia 0,05. En la primera búsqueda, sin red aún, el peso
de centralidad se redistribuye entre los demás.

**Punto de control PC-2:** el usuario revisa `candidatos.csv` y produce `seleccion.csv`.

## B4 · Recuperación de documentos

Orden de intento: 1) Unpaywall / versión OA del editor; 2) repositorios (arXiv, PMC, CORE,
repositorios institucionales); 3) acceso privado según B2; 4) lista de "no disponibles" para
gestión manual (préstamo interbibliotecario, contacto con autor).

Registrar siempre la procedencia y la versión (preprint / aceptada / publicada): **para citar con
página hay que usar la versión publicada**.

## B5 · Análisis de contenido

Un subagente `lector` por documento, en **dos niveles**:

| Nivel | A quién se aplica | Qué lee | Ficha |
|---|---|---|---|
| **Ligero** | Todo el corpus seleccionado | Resumen, introducción, conclusiones | `nivel: ligero` — tesis, método, hallazgos principales, conceptos, posición |
| **Completo** | Los `max_lectura_completa` mejor puntuados (+ los que el usuario marque) | Texto completo | `nivel: completo` — todos los campos, incluidas citas textuales con página |

Un documento puede promocionarse de ligero a completo si el `sintetizador` detecta que es central
en una disputa. Esquema de la ficha completa:

```yaml
id: doi:10.xxxx/yyyy
nivel: completo
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
- **Criterio de parada (por defecto, "moderado"):** máximo **2 rondas**, máximo **30 candidatos
  nuevos por ronda**, y parada anticipada si una ronda aporta **menos de 3** documentos que superen
  el umbral de relevancia (saturación).
- Perfiles alternativos en `proyecto.yaml`: `ligero` (1 ronda, solo hacia atrás) y `exhaustivo`
  (hasta 5 rondas o saturación; para revisiones sistemáticas).
- Cada ronda vuelve a pasar por el punto de control PC-2.

## B7 · Estado de la cuestión

Cuatro productos, todos generados a partir de las mismas fichas (una sola fuente de verdad):

| Producto | Archivo | Contenido | Fase |
|---|---|---|---|
| Ficha breve | `resumen-ejecutivo.md` | 1 página: estado del debate, 5 obras clave, principales disputas y vacíos, recomendación | 4 |
| Informe en prosa | `estado-cuestion.md` (+ `.docx` vía Pandoc) | Estructura detallada abajo | 4 |
| Tablas de síntesis | `tablas/*.csv` + incrustadas en el informe | Matriz documento × posición/método/hallazgo; tabla de disputas; tabla de vacíos | 4 |
| Mapa visual | `mapa.html` | Red de citas interactiva coloreada por escuela/posición | 5 (requiere el grafo de B6) |

Estructura del informe en prosa:
1. Mapa del campo (líneas / escuelas / enfoques) con documentos de referencia.
2. Consensos.
3. **Disputas:** posiciones enfrentadas, quién sostiene qué, con cita y página.
4. **Errores:** afirmaciones refutadas o mal citadas en la literatura (con evidencia).
5. **Vacíos:** preguntas no abordadas, poblaciones/periodos/métodos ausentes.
6. Tabla de trazabilidad: afirmación → documento → página.

Advertencia: la detección de "errores" y "vacíos" por un LLM es una **hipótesis a revisar**, no
un hallazgo. El documento lo debe indicar.
