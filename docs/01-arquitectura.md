# 01 · Arquitectura: cómo encajan las piezas

> **En pocas palabras:** el sistema tiene cinco piezas. Unas **instrucciones generales**, unos
> **comandos** que pones en marcha tú, un **equipo de ayudantes** (subagentes), cada uno con una
> sola tarea, unas **herramientas** que hacen el trabajo mecánico y siempre igual (buscar en
> catálogos, extraer texto de un PDF, comprobar citas) y una **carpeta de datos** en tu ordenador
> donde queda todo el trabajo. La IA se usa para leer, resumir y escribir; lo que se puede
> comprobar lo hacen programas.

Si no conoces alguna palabra, consulta el [glosario](glosario.md).

## Esquema general

```
                    Tú (investigadora / investigador)
                                │
                  escribes un comando, p. ej. /estado-cuestion
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │   Claude Code (coordinador)  │  sigue las instrucciones generales
                 └──────────────┬───────────────┘
                                │ reparte el trabajo
          ┌─────────────────────┴───────────────────────┐
          ▼                                             ▼
  Ayudantes de la revisión                    Ayudantes de la escritura
  bibliográfica                               (redactor, verificador,
  (buscador, bibliotecario, lector,            revisor)
   rastreador, sintetizador)
          │                                             │
          └──────────────────┬──────────────────────────┘
                             ▼
        Herramientas (programas que hacen tareas mecánicas)
                             │
     ┌──────────────┬────────┴─────────┬─────────────────────┐
     ▼              ▼                  ▼                     ▼
 Catálogos      Bases de datos     "Estantería"          Tu carpeta
 abiertos       privadas           del proyecto          de datos
 (gratuitos)    (pendiente)        (obras verificadas)   (PDF, fichas,
                                                          borradores)
```

El verificador revisa el borrador antes de darlo por terminado: si encuentra un fallo, el
borrador vuelve al redactor.

## Las cinco piezas

| Pieza | Qué es, en palabras sencillas | Dónde está (detalle técnico) |
|---|---|---|
| **Instrucciones generales** | Las normas que Claude debe cumplir siempre en este proyecto (por ejemplo, "nunca inventes una cita") | Archivo `CLAUDE.md` |
| **Comandos** | Procesos ya preparados que pones en marcha escribiendo `/nombre` | Carpeta `.claude/skills/` |
| **Ayudantes (subagentes)** | Copias de Claude con una sola tarea e instrucciones propias | Carpeta `.claude/agents/` |
| **Herramientas** | Programas que hacen tareas mecánicas siempre del mismo modo, y "enchufes" para conectar con otros servicios | Carpeta `herramientas/` (programas en Python) y archivo `.mcp.json` (enchufes MCP) |
| **Comprobaciones automáticas** | Controles que saltan solos en ciertos momentos, por ejemplo verificar las citas antes de exportar | Archivo `.claude/settings.json` (*hooks*) |

Tus datos de investigación (PDF, fichas, borradores) **no** están en la carpeta del programa,
sino en una carpeta aparte de tu ordenador (ver más abajo).

### ¿Por qué un equipo de ayudantes y no una sola IA?

Claude, como cualquier IA, solo puede "tener en la cabeza" una cantidad limitada de texto a la vez
(lo que se llama su **contexto**). Si leyera 40 artículos seguidos, olvidaría los primeros. Por eso
cada artículo lo lee un ayudante distinto, que entrega una **ficha de lectura** breve. El
coordinador trabaja con las fichas, no con los artículos completos. Además, varios ayudantes
pueden trabajar a la vez.

### ¿Por qué programas además de la IA?

Porque la IA puede responder distinto cada vez y a veces se equivoca, mientras que un programa
hace siempre lo mismo y su resultado se puede comprobar. Por eso buscar en catálogos, quitar
duplicados, calcular la importancia de una obra, extraer el texto de un PDF y verificar citas son
tareas de **programas**. La IA se reserva para leer, interpretar, resumir y redactar.

## El equipo de ayudantes

| Ayudante | Nombre técnico | Qué recibe | Qué entrega |
|---|---|---|---|
| Buscador | `buscador` | Tu pregunta y la ficha del proyecto | Lista de obras ordenadas por importancia |
| Bibliotecario | `recuperador` | Las obras que has elegido | Los PDF que se pueden conseguir legalmente y una lista de los que no |
| Lector | `lector` | Un documento | Su ficha de lectura |
| Rastreador | `rastreador` | Las fichas y sus bibliografías | Obras nuevas que conviene añadir (bola de nieve) |
| Sintetizador | `sintetizador` | Todas las fichas | El estado de la cuestión |
| Redactor | `redactor` | Estado de la cuestión, tus objetivos y las normas de la revista | El borrador del artículo |
| Verificador | `verificador` | El borrador | Un informe de citas correctas y erróneas. **No puede modificar el borrador**, solo señalar |
| Revisor *(fase 8)* | `revisor` | El borrador y las normas de la revista | Un informe como el de un revisor de revista. **Solo lee** |

Decisión: se mantienen estos siete ayudantes más el revisor, para poder probar cada uno por
separado.

## La ficha de cada proyecto (perfil disciplinar)

Cada investigación tiene una ficha de configuración. Así el mismo sistema sirve para filosofía,
sociología, medicina o ingeniería: lo que cambia es la ficha. Recoge:

- la pregunta de investigación, la disciplina, los idiomas y el periodo;
- dónde buscar (qué catálogos);
- cómo decidir qué obras son más importantes;
- cuántas obras se leen a fondo y cuántas rondas de bola de nieve se hacen;
- qué productos quieres al final;
- el estilo de cita y la revista a la que va dirigido el artículo.

### Detalle técnico: formato de la ficha (`proyecto.yaml`)

```yaml
nombre: ejemplo-proyecto
pregunta: "¿...?"
disciplina: humanidades           # humanidades | sociales | salud | ingenieria | mixta
idiomas: [es, en]
periodo: {desde: 2000, hasta: 2026}
fuentes: [openalex, crossref, semantic_scholar, pubmed]   # según disciplina
relevancia:
  pesos: {citas: 0.2, citas_por_anio: 0.25, centralidad_red: 0.25, pertinencia: 0.25, recencia: 0.05}
limites:
  max_candidatos: 200
  max_lectura_completa: 40        # el resto recibe lectura ligera
snowballing: moderado             # ligero | moderado | exhaustivo
salidas_b7: [resumen, informe, tablas, mapa]
estilo_cita: apa-7th-edition      # identificador del estilo en el catálogo CSL
revista_objetivo: null
```

## Dónde se guarda el trabajo: tu carpeta de datos

La carpeta del programa y la de tus investigaciones están **separadas**:

- Si borras o actualizas el programa, **no pierdes tu trabajo**.
- La carpeta de datos se puede sincronizar (Drive, OneDrive, Nextcloud…) y compartir con el equipo.
- Los PDF, que tienen derechos de autor, nunca se mezclan con el programa, que se publica en
  GitHub.

Por defecto la carpeta es `Investigacion`, dentro de tu carpeta personal, con una subcarpeta por
proyecto:

```
Investigacion/
└── nombre-del-proyecto/
    ├── proyecto.yaml         la ficha del proyecto
    ├── candidatos.csv        obras encontradas, con su puntuación y el motivo (tabla)
    ├── seleccion.csv         las obras que has aprobado (tabla)
    ├── pdf/                  los documentos conseguidos
    ├── texto/                el texto extraído de cada PDF, con sus páginas
    ├── fichas/               una ficha de lectura por documento
    ├── grafo.json            la red de citas (quién cita a quién)
    ├── biblioteca.json       la "estantería": las únicas obras que se pueden citar
    ├── resumen-ejecutivo.md  estado de la cuestión en una página
    ├── estado-cuestion.md    estado de la cuestión completo (también en Word)
    ├── tablas/               tablas de síntesis
    ├── mapa.html             mapa visual de la red de citas (se abre en el navegador)
    └── borradores/           borradores del artículo e informes de verificación
```

Los archivos `.md` son texto con formato sencillo (*Markdown*) y se pueden abrir con cualquier
editor de texto; el sistema genera también versiones en Word.

## Riesgos y cómo se evitan

| Riesgo | Qué significa | Cómo se evita |
|---|---|---|
| Demasiados documentos a la vez | La IA "olvida" si le damos demasiado texto, y el uso tiene un coste | Ayudantes con fichas breves y límites en la ficha del proyecto |
| Se agota el cupo de uso a medio proceso | Las suscripciones de Claude tienen un límite de uso cada pocas horas | El trabajo se guarda después de cada documento y se puede **retomar donde se quedó** (decisión 0005) |
| La página del PDF no es la del libro | La página 1 del PDF puede ser la 45 impresa | El sistema calcula la correspondencia (ver [05](05-verificacion-citas.md)) |
| Libros escaneados | El PDF es una foto y hay que "leerla" (OCR), con posibles errores | Se marca la calidad y esas citas se revisan a mano |
| Obras que no aparecen en los catálogos | Frecuente con libros y en humanidades | Varios catálogos y posibilidad de añadir obras a mano |
| Los catálogos limitan cuántas consultas se les hacen | Si se abusa, bloquean el acceso temporalmente | Guardar las respuestas para no repetir preguntas e identificarse con un correo |

## Detalle técnico: estructura de la carpeta del programa

```
LoRu-Agent/
├── CLAUDE.md                   instrucciones generales
├── README.md                   presentación
├── .mcp.json                   enchufes MCP del proyecto            (fase 1+)
├── .claude/
│   ├── settings.json           permisos y comprobaciones automáticas (fase 1+)
│   ├── agents/                 ayudantes (subagentes)                (fase 1+)
│   └── skills/                 comandos /estado-cuestion, /redactar… (fase 1+)
├── herramientas/               programas en Python                   (fase 1+)
│   ├── fuentes/                conexión con cada catálogo
│   ├── pdf/                    extracción de texto y páginas
│   ├── relevancia/             cálculo de importancia y red de citas
│   └── verificacion/           verificador de citas
├── estilos/                    estilos de cita y fichas de revistas
├── plantillas/                 modelos de ficha de proyecto y de lectura
├── .env.ejemplo                modelo del archivo de claves y de la ruta de datos (fase 1+)
├── tests/                      pruebas automáticas de los programas
└── docs/                       esta documentación
```
