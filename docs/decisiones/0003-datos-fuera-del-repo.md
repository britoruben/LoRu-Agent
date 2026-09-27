# Decisión 0003 · Los datos de investigación se guardan aparte del programa

- **Estado:** aceptada
- **Fecha:** 2026-09-27
- **Quién decide:** Rubén

## En pocas palabras

El programa está en una carpeta y tus investigaciones en otra (por defecto, `Investigacion`, dentro
de tu carpeta personal). Así no se pierde trabajo al actualizar el programa y los PDF con derechos
de autor nunca se publican por error.

## Situación

Cada investigación genera PDF (con derechos de autor), textos extraídos, fichas de lectura y
borradores. El programa, en cambio, se guarda y se comparte en GitHub. Hay que mantenerlos
separados.

## Decisión

Los datos de cada investigación se guardan en una **carpeta aparte**, con una subcarpeta por
proyecto. La ubicación se puede cambiar en el archivo `.env` (en la línea `LORU_DATOS`).

## Otras opciones que se valoraron

- **Dentro de la carpeta del programa**, excluida de GitHub: más sencillo, pero mezcla programa y
  datos, y si se borra el programa se pierde el trabajo.
- **Una carpeta en GitHub por cada investigación** (sin los PDF): guarda el historial de cambios de
  fichas y borradores, pero es más complicado. Se puede añadir más adelante sin cambiar nada del
  diseño.

## Consecuencias

- Todas las herramientas buscan los datos en la carpeta indicada en `LORU_DATOS`.
- La carpeta se puede sincronizar (Drive, OneDrive…) para trabajar en equipo.
- Por seguridad, la carpeta del programa está configurada para no publicar nunca archivos PDF, aunque
  alguien los copie en ella por error (archivo `.gitignore`).
