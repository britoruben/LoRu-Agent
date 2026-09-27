# 04 · Fuentes: de dónde saca el sistema las publicaciones

> **En pocas palabras:** el sistema busca primero en **catálogos abiertos y gratuitos** de
> publicaciones científicas, que se pueden consultar legalmente desde un programa. Para las
> **bases de datos de pago** de la universidad (Scopus, Web of Science, JSTOR…) todavía hay que
> averiguar cómo se accede; mientras tanto, el plan es no automatizar nada que las licencias
> prohíban.

> **Aviso para quien programe:** las condiciones de uso de estos servicios (límites, necesidad de
> clave) cambian a menudo. Antes de conectar cada uno, hay que comprobar su documentación oficial
> y apuntar la fecha en la columna "Comprobado".

## Catálogos abiertos

Son como el catálogo de una biblioteca, pero de publicaciones de todo el mundo, y ofrecen una
"ventanilla" para programas (una **API**, ver [glosario](glosario.md)).

| Catálogo | Qué contiene | Para qué lo usamos | Comprobado |
|---|---|---|---|
| OpenAlex | Publicaciones de todas las disciplinas; muy amplio | Buscar, contar citas, ver quién cita a quién | — |
| Crossref | Datos oficiales de las publicaciones con DOI | **Comprobar que una obra existe** y que sus datos son correctos | — |
| Semantic Scholar | Todas las disciplinas, fuerte en ciencias e ingeniería | Citas y referencias | — |
| Unpaywall | Dónde está la versión gratuita y legal de un artículo | Conseguir textos legalmente | — |
| PubMed / PubMed Central | Medicina y biología | Buscar y conseguir textos gratuitos | — |
| arXiv | Física, matemáticas, informática | Borradores previos a la publicación (*preprints*) | — |
| CORE | Repositorios de universidades de todo el mundo | Textos completos gratuitos | — |
| DOAJ | Revistas de acceso abierto | Buscar | — |
| Dialnet | Publicaciones en español, fuerte en humanidades y ciencias sociales | Buscar | **Hay que averiguar si permite el acceso desde programas** |
| Google Scholar | Muy amplio | — | **No ofrece ventanilla para programas y prohíbe automatizarlo: no se usará** |

## Qué catálogos usar según la disciplina

Es la configuración que se propondrá por defecto; cada proyecto puede cambiarla.

| Disciplina | Catálogos | Estilo de cita habitual | A tener en cuenta |
|---|---|---|---|
| Humanidades | OpenAlex, Crossref, Dialnet, catálogos de bibliotecas | Chicago, MLA, notas al pie | Muchos libros y capítulos no tienen DOI; citar con página es imprescindible |
| Ciencias sociales | OpenAlex, Crossref, Semantic Scholar, Dialnet | APA 7 | Mezcla de artículos y libros |
| Salud y biomedicina | PubMed, PubMed Central, OpenAlex, Semantic Scholar | Vancouver, AMA | En las revisiones sistemáticas (protocolo PRISMA) todo el proceso debe poder repetirse |
| Ingeniería e informática | OpenAlex, Semantic Scholar, arXiv, Crossref | IEEE, ACM | Muchos *preprints* y actas de congresos |

## Bases de datos de pago — pendiente

Ver las preguntas P-03 y P-04 en [07 · Preguntas abiertas](07-preguntas-abiertas.md). Estas son
las opciones:

| Opción | ¿Se puede automatizar? | ¿Es legal? | Comentario |
|---|---|---|---|
| **Ventanilla oficial para programas (API)** con clave de la institución (p. ej. Scopus, Web of Science) | Sí | Sí, dentro de la licencia | La mejor opción si la universidad la ofrece |
| **Entrar por la web** con el usuario de la universidad | Técnicamente es frágil | Las licencias **suelen prohibir** la descarga automática o masiva | No se automatiza; se usa la opción de descarga guiada |
| **Descarga guiada** | En parte | Sí | El sistema prepara la lista ordenada con enlaces y tú descargas los PDF |
| **Exportar resultados** desde la base de datos (archivo RIS, BibTeX o tabla) | Sí, la parte de leer el archivo | Sí | Muy útil: buscas en la base de datos, exportas la lista y el sistema la procesa |

## Normas de acceso

1. Siempre se prefiere la **versión gratuita y legal**.
2. No se abusa de los catálogos: se limita el número de consultas y se guardan las respuestas para
   no repetirlas.
3. Las claves y contraseñas se guardan solo en tu ordenador, en el archivo `.env`, y nunca se
   publican.
4. El acceso a bases de datos de pago solo funciona **en tu ordenador**, con tu conexión y
   credenciales de la universidad.
