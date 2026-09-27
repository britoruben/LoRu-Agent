# 00 · Visión

## Problema

La revisión bibliográfica y la redacción académica consumen la mayor parte del tiempo en tareas
mecánicas (buscar, cribar, descargar, extraer, comprobar citas) y son vulnerables a un riesgo grave
cuando se usan LLM: **referencias inventadas, DOIs erróneos y citas literales falsas**.

## Objetivo

Un repositorio que, clonado en local y abierto con Claude Code, proporcione agentes, comandos y
herramientas para:

- **Flujo B (bibliográfico):** de una pregunta de investigación a un *estado de la cuestión* trazable,
  con identificación de disputas, errores y vacíos.
- **Flujo R (redacción):** de ese estado de la cuestión + documentos propios a un borrador de artículo
  adaptado a una revista concreta, con **todas las citas verificadas**.

## Alcance multidisciplinar

El sistema debe servir para humanidades, ciencias sociales, salud/biomedicina, ingeniería e
informática. Esto implica que fuentes, estilo de cita y criterios de relevancia **no pueden estar
fijados en el código**: se configuran por proyecto mediante un *perfil disciplinar*
(ver `01-arquitectura.md`).

## No-objetivos (explícitos)

- **No** producir artículos publicables sin revisión humana. El sistema es un asistente; la autoría
  y las decisiones intelectuales son del investigador.
- **No** eludir licencias: nada de descargas masivas desde plataformas de suscripción, ni fuentes
  piratas.
- **No** ejecución desatendida en la nube con acceso institucional (el acceso privado depende de la
  red/credenciales del usuario en local).

## Principios de diseño

1. **Determinista donde se pueda, LLM donde aporte.** APIs, extracción de PDF, formateo de citas y
   verificación son código. El LLM lee, clasifica, sintetiza y redacta.
2. **Verificación estructural, no por prompt.** Pedir al modelo "no inventes" no basta; el sistema
   debe impedir que llegue al texto final una cita no verificada.
3. **Trazabilidad total.** Cada afirmación → documento → página.
4. **Humano en el bucle** en los puntos de decisión: selección final del corpus, interpretación de
   disputas, versión final del texto.
5. **Límites explícitos** de profundidad, número de documentos y coste en cada ejecución.
