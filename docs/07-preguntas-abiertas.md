# 07 · Preguntas abiertas

Agenda para la reunión Rubén + Lola. Cada respuesta debe convertirse en un ADR en `docs/decisiones/`.

| ID | Pregunta | Opciones | Recomendación | Bloquea | Estado |
|---|---|---|---|---|---|
| P-01 | ¿Qué gestor bibliográfico? | Zotero · Mendeley · EndNote · ninguno (CSL-JSON propio) | **Zotero** (gratuito, API local, Better BibTeX, integración con Pandoc, servidores MCP comunitarios) | Fase 1 | Abierta |
| P-02 | ¿Lenguaje de las herramientas? | Python · TypeScript | **Python** (ecosistema PDF/bibliometría: PyMuPDF, pandas, networkx, citeproc vía Pandoc) | Fase 1 | **Cerrada → ADR-0005** |
| P-03 | ¿Cómo se accede a las bases privadas? | API oficial · proxy/SSO · exportación RIS/CSV · descarga manual | API oficial si existe; si no, exportación + descarga manual guiada | Fase 7 | Abierta — **Lola consulta con biblioteca** |
| P-04 | ¿Qué bases privadas concretas? | Scopus, WoS, JSTOR, EBSCO, ProQuest, Dialnet Plus... | — | Fase 7 | Abierta |
| P-05 | ¿Proyecto piloto y disciplina inicial? | Una pregunta real y acotada | Elegir la disciplina donde más se vaya a usar primero | Fase 3 | Abierta |
| P-06 | ¿Formato de salida del borrador? | Markdown · .docx · LaTeX | Markdown como fuente → .docx y LaTeX/PDF con Pandoc | Fase 6 | **Cerrada → ADR-0005** |
| P-07 | ¿Idiomas de búsqueda y redacción? | es · en · ambos | Ambos | Fase 3 | **Cerrada → ADR-0005** |
| P-08 | ¿Presupuesto y plan de Claude? | Plan Pro/Max · API con pago por uso | Plan Pro/Max | Fase 4 | **Cerrada → ADR-0005** |
| P-09 | ¿Herramienta de extracción de referencias de PDF? | Metadatos API · GROBID · parser propio | Metadatos API primero; GROBID si falta cobertura | Fase 5 | Abierta |
| P-10 | ¿Dónde se guardan los datos de proyectos? | Dentro del repo (git-ignored) · carpeta externa · repo de datos | Carpeta externa configurable | Fase 1 | **Cerrada → ADR-0003** |

## Preguntas para la biblioteca de la institución (P-03/P-04)

1. ¿Qué bases de datos tenemos suscritas?
2. ¿Alguna ofrece **API** para investigadores (p. ej. clave de Elsevier para Scopus, Clarivate para WoS)?
3. ¿Qué dicen las licencias sobre **minería de texto y descarga automatizada** (TDM)?
4. ¿El acceso es por IP, VPN, proxy (EZproxy) o SSO (Shibboleth/OpenAthens)?
5. ¿Hay límites de descarga por usuario?
