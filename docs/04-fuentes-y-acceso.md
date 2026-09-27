# 04 · Fuentes y acceso

> Las condiciones de uso, límites y necesidad de clave de API cambian con frecuencia.
> **Antes de implementar cada cliente, verificar la documentación oficial vigente** y anotar
> la fecha de verificación en esta tabla.

## Fuentes abiertas (flujo B1)

| Fuente | Cobertura | Uso principal | Acceso | Verificado |
|---|---|---|---|---|
| OpenAlex | Multidisciplinar, muy amplia | Búsqueda, citas, grafo de referencias | API REST | — |
| Crossref | Metadatos con DOI | Validar DOI y metadatos (R4) | API REST (identificarse con email) | — |
| Semantic Scholar | Multidisciplinar, fuerte en STEM/biomed | Citas, referencias, "influential citations" | API REST (clave opcional) | — |
| Unpaywall | Localización de versiones OA | Descarga legal (B4) | API REST (email) | — |
| PubMed / PMC | Biomedicina | Búsqueda y texto completo OA | NCBI E-utilities | — |
| arXiv | Física, matemáticas, informática | Preprints | API | — |
| CORE | Repositorios institucionales | Texto completo OA | API (clave) | — |
| DOAJ | Revistas OA | Búsqueda | API | — |
| Dialnet | Hispánico, humanidades y sociales | Búsqueda | **Verificar qué acceso programático existe** | — |
| Google Scholar | Amplia | — | **No tiene API oficial; no automatizar** | — |

## Fuentes por disciplina (perfil por defecto propuesto)

| Disciplina | Fuentes base | Estilo de cita habitual | Particularidades |
|---|---|---|---|
| Humanidades | OpenAlex, Crossref, Dialnet, catálogos de bibliotecas | Chicago, MLA, notas al pie | Muchos libros y capítulos sin DOI; cita con página imprescindible |
| Ciencias sociales | OpenAlex, Crossref, Semantic Scholar, Dialnet | APA 7 | Mezcla de artículos y libros |
| Salud / biomedicina | PubMed, PMC, OpenAlex, Semantic Scholar | Vancouver, AMA | Revisiones sistemáticas (PRISMA): el proceso debe ser reproducible |
| Ingeniería / informática | OpenAlex, Semantic Scholar, arXiv, Crossref | IEEE, ACM | Preprints y actas de congresos |

## Bases privadas (flujo B2) — PENDIENTE

Ver P-03 en `07-preguntas-abiertas.md`. Opciones a evaluar:

| Opción | Automatizable | Legalidad | Comentario |
|---|---|---|---|
| API oficial (p. ej. Scopus, Web of Science) con clave institucional | Sí | Sí, según licencia | Opción preferente si la institución la ofrece |
| Portal web con proxy/SSO institucional | Técnicamente frágil | Normalmente **prohíbe descarga automatizada/masiva** | No automatizar; usar descarga manual guiada |
| Descarga manual guiada por el agente | Semiautomático | Sí | El agente prioriza y enlaza; el usuario descarga a `pdf/` |
| Exportación desde la base (RIS/BibTeX/CSV) | Sí (importación) | Sí | Muy útil: el usuario exporta resultados y el agente los procesa |

## Principios de acceso

1. Preferir siempre la versión OA legal.
2. Respetar límites de peticiones y cachear respuestas.
3. Credenciales en `.env` (nunca en git).
4. El acceso privado solo funciona **en local**, en la red/credenciales del usuario.
