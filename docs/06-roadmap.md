# 06 · Roadmap

Principio: **cada fase termina con algo usable y verificable**. No se empieza una fase sin cerrar
las preguntas abiertas que la bloquean.

| Fase | Objetivo | Entregables | Criterio de aceptación | Bloqueada por |
|---|---|---|---|---|
| **0 · Diseño** | Arquitectura documentada | `docs/`, ADRs, preguntas abiertas | Rubén y Lola aprueban la arquitectura | — |
| **1 · Cimientos** | Entorno y biblioteca | Estructura `.claude/`, `herramientas/` Python, plantilla `proyecto.yaml`, integración con gestor bibliográfico | Crear un proyecto e importar 10 referencias verificadas | P-01, P-02 |
| **2 · Verificador** | R4 + mapa de páginas | Verificador de citas, extracción PDF con páginas impresas, tests con casos trampa (DOI falso, cita alterada, página errónea) | Detecta el 100 % de los casos trampa del set de pruebas | Fase 1 |
| **3 · Búsqueda abierta** | B1, B3, B4 (OA) | Clientes OpenAlex/Crossref/S2/Unpaywall, ranking, `candidatos.csv`, skill `/buscar` | Para una pregunta real, lista útil según el investigador | Fase 1 |
| **4 · Lectura y síntesis** | B5, B7 | Subagentes `lector` (2 niveles) y `sintetizador`, skill `/estado-cuestion`; resumen, informe y tablas | Estado de la cuestión trazable en un proyecto piloto | Fase 3 |
| **5 · Snowballing** | B6 | Grafo de citas, rondas acotadas, mapa visual `mapa.html` | Descubre documentos relevantes no hallados en la búsqueda inicial | Fase 4 |
| **6 · Redacción** | R1–R3 | Subagente `redactor` (por secciones), fichas de revista a partir de guías oficiales, Pandoc+CSL, hook de verificación | Borrador de artículo con 0 fallos de verificación | Fase 2, 4 |
| **7 · Bases privadas** | B2 | Cliente(s) API oficial o flujo de descarga manual guiada | Según decisión P-03 | P-03 |
| **8 · Revisor** | — | Subagente `revisor` (peer review simulado) | Sus objeciones coinciden sustancialmente con las de un revisor humano en un caso de prueba | Fase 6 |

Nota: el verificador (fase 2) va **antes** que la búsqueda y la redacción a propósito: es la pieza
que da confianza al resto y se puede probar de forma aislada.

## Proyecto piloto

Se recomienda elegir **una pregunta de investigación real y acotada** (P-05) para validar las
fases 3–6. Probar en varias disciplinas desde el principio multiplica el trabajo; mejor una
disciplina primero y luego generalizar el perfil disciplinar.
