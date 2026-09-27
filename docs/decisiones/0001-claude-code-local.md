# Decisión 0001 · El sistema funciona en tu ordenador con Claude Code

- **Estado:** aceptada
- **Fecha:** 2026-09-27
- **Quién decide:** Rubén

## En pocas palabras

El asistente se usará con **Claude Code en el ordenador de cada persona**, no en la nube, porque
necesita acceder a tus PDF, a tu gestor bibliográfico y, en su caso, a las bases de datos de la
universidad.

## Situación

El sistema tiene que leer documentos que están en tu ordenador, conectarse al gestor bibliográfico
y, quizá, usar las bases de datos de pago de la universidad, que solo funcionan con tu conexión o
tu usuario institucional.

## Decisión

Se usará **Claude Code en el ordenador local** (ver [glosario](../glosario.md)). El proyecto se
prepara como una carpeta que incluye las instrucciones, los ayudantes, los comandos, las
comprobaciones automáticas y los "enchufes" (MCP) necesarios.

## Otras opciones que se valoraron

- **Claude Code en la nube** (desde la web): no tiene acceso a la red de la universidad ni a tus
  archivos. Solo serviría para buscar en catálogos abiertos o para construir el propio proyecto.
- **La aplicación de escritorio de Claude:** admite "enchufes" (MCP), pero no permite organizar el
  trabajo en ayudantes, comandos y comprobaciones automáticas con la misma flexibilidad.

## Consecuencias

- El acceso a bases de datos de pago nunca se hará desde la nube.
- Cada persona guarda sus claves y contraseñas en su propio ordenador (archivo `.env`).
