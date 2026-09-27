# 07 · Preguntas abiertas

> **En pocas palabras:** lista de lo que queda por decidir. Sirve de orden del día para las
> reuniones del equipo. Cuando se responde una pregunta, se escribe una nota de decisión en
> [`decisiones/`](decisiones/) y aquí se marca como cerrada.

## Pendientes

### P-01 · ¿Qué gestor bibliográfico usamos?

Un gestor bibliográfico es un programa que guarda tus referencias y PDF y da formato a las citas.

- **Opciones:** Zotero, Mendeley, EndNote o ninguno (el sistema llevaría su propia lista).
- **Recomendación: Zotero.** Es gratuito, muy usado en universidades y otros programas pueden
  conectarse a él fácilmente. Eso permite que el sistema lea y añada referencias automáticamente.
- **Bloquea:** la fase 1.

### P-03 · ¿Cómo se accede a las bases de datos de pago de la institución?

- **Opciones:** ventanilla oficial para programas (API), entrada por la web con el usuario de la
  universidad, exportar las listas de resultados o descarga guiada (ver
  [04 · Fuentes](04-fuentes-y-acceso.md)).
- **Recomendación:** la ventanilla oficial si existe; si no, exportar resultados y descarga guiada.
- **Quién:** Lola consulta con la biblioteca (ver las preguntas de abajo).
- **Bloquea:** la fase 7.

### P-04 · ¿Qué bases de datos de pago concretas tenemos?

- Por ejemplo: Scopus, Web of Science, JSTOR, EBSCO, ProQuest, Dialnet Plus…
- **Bloquea:** la fase 7.

### P-05 · ¿Cuál es el proyecto piloto y en qué disciplina empezamos?

- Una pregunta de investigación real y acotada con la que probar el sistema.
- **Recomendación:** empezar por la disciplina en la que antes se vaya a usar.
- **Bloquea:** la fase 3. **Es la pregunta más importante**: sin ella no se puede comprobar si el
  sistema es útil.

### P-09 · ¿Cómo se extrae la bibliografía de cada PDF?

- **Opciones:** tomarla de los catálogos (OpenAlex, Crossref) o leerla del propio PDF con una
  herramienta especializada (por ejemplo GROBID).
- **Recomendación:** primero los catálogos; la herramienta especializada solo si faltan muchas
  referencias (probable en humanidades).
- **Bloquea:** la fase 5. Es una decisión técnica: puede tomarla quien programe.

## Preguntas para la biblioteca de la universidad (P-03 y P-04)

1. ¿A qué bases de datos estamos suscritos?
2. ¿Alguna ofrece a los investigadores una **ventanilla para programas (API)** con clave propia?
   Por ejemplo, Elsevier la ofrece para Scopus y Clarivate para Web of Science.
3. ¿Qué dicen las licencias sobre el **análisis automático de textos y la descarga automática**?
   (En inglés se llama *text and data mining*, TDM.)
4. ¿Cómo se entra desde fuera del campus: por VPN, por el portal de la biblioteca o con el usuario
   institucional?
5. ¿Hay un límite de descargas por persona?

## Cerradas

| Pregunta | Decisión | Nota |
|---|---|---|
| P-02 · ¿En qué lenguaje se programan las herramientas? | Python | [Decisión 0005](decisiones/0005-stack-tecnico.md) |
| P-06 · ¿En qué formatos se entrega el artículo? | Word y PDF (el texto de trabajo en Markdown) | [Decisión 0005](decisiones/0005-stack-tecnico.md) |
| P-07 · ¿En qué idiomas se busca y se escribe? | Se busca en español e inglés; se escribe en el idioma de la revista | [Decisión 0005](decisiones/0005-stack-tecnico.md) |
| P-08 · ¿Cómo se paga el uso de Claude? | Suscripción Pro o Max | [Decisión 0005](decisiones/0005-stack-tecnico.md) |
| P-10 · ¿Dónde se guardan los datos? | En una carpeta aparte del programa | [Decisión 0003](decisiones/0003-datos-fuera-del-repo.md) |
