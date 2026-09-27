# Informe de verificación de citas: borrador-con-errores.md

**NO APTO.** Hay 8 fallo(s). El borrador no debe darse por terminado hasta corregirlos.

| Qué se ha revisado | Cantidad |
|---|---|
| Etiquetas de cita | 9 |
| Citas literales comprobadas contra el original | 7 |
| Citas sin texto literal (paráfrasis o referencias generales) | 1 |
| Fallos | 8 |
| Avisos | 4 |

## Fallos (hay que corregirlos)

1. **Línea 4** · `[@ficticia2021, p. 45]`
   - Problema: La cita está alterada: se parece en un 94 % a un pasaje de la página 45, pero no es idéntica. El original dice: «un sistema es opaco cuando sus resultados son verificables pero sus razones no lo son.».
   - Qué hacer: Copia la cita exactamente como está en el original.

2. **Línea 5** · `[@ficticia2021, p. 45]`
   - Problema: Página incorrecta: la cita «exigir una explicación no es un capricho epistemológico» no está en p. 45, sino en la página 46.
   - Qué hacer: Corrige la página: debe ser 46.

3. **Línea 7** · `[@inventado2020, p. 3]`
   - Problema: La obra «inventado2020» no está en la estantería del proyecto. Puede ser una referencia inventada o una clave mal escrita.
   - Qué hacer: Comprueba la clave. Si la obra existe, añádela a biblioteca.json y verifícala; si no, elimina la cita.

4. **Línea 11** · `[@ejemplar2019]`
   - Problema: Cita literal sin página: «podemos ser responsables de lo que no comprendemos».
   - Qué hacer: Añade la página impresa donde aparece, por ejemplo [@clave, p. 45].

5. **Línea 12** · `[@ejemplar2019, p. 113]`
   - Problema: La cita «la inteligencia artificial carece de intencionalidad genuina» no aparece en «ejemplar2019».
   - Qué hacer: Comprueba la cita en el original. Si no está, elimínala o conviértela en paráfrasis.

6. **Línea 13** · `[@ejemplar2019, p. 200]`
   - Problema: La página 200 no existe en el texto disponible de «ejemplar2019». La cita sí aparece en la página 113.
   - Qué hacer: Revisa el número de página.

7. **Línea 15** · `[@sincomprobar2023]`
   - Problema: La obra «sincomprobar2023» está en la estantería, pero nadie ha comprobado que exista (su campo "verificacion" no es doi, isbn ni manual).
   - Qué hacer: Compruébala con el comprobador de DOI o a mano, y anótalo en biblioteca.json.

8. **Línea 19** · `[FUENTE PENDIENTE: datos sobre el uso de sistemas opacos en la administración pública]`
   - Problema: Queda una fuente pendiente: el texto necesita una obra que no está en la estantería.
   - Qué hacer: Busca una obra que respalde la afirmación y añádela a la estantería, o reformula la frase.

## Avisos (conviene revisarlos)

1. **Línea 9** · `[@ficticia2021, p. 46]`
   - Problema: La cita es correcta, pero ocupa más de una página (pp. 46-47).
   - Qué hacer: Cambia «p. 46» por «pp. 46-47».

2. **Línea 17** · `[@escaneo1975, p. 9]`
   - Problema: La cita casi coincide (97 %) con la página 9, pero el original es un escaneo y puede tener errores. El texto escaneado dice: «toda técnica prornete descargarnos de una tarea;».
   - Qué hacer: Compruébala a mano con el libro o el PDF.

3. **Línea 22** · `«la transparencia total es imposible en los sistemas complej…»`
   - Problema: Texto entre comillas sin etiqueta de cita. Si es una cita literal, falta la fuente.
   - Qué hacer: Añade la etiqueta con la página, o quita las comillas si no es una cita.

4. **Línea 25** · `@ejemplar2019`
   - Problema: Parece una cita, pero no está escrita entre corchetes, así que no se ha comprobado.
   - Qué hacer: Escríbela como [@ejemplar2019, p. X] para que el verificador pueda revisarla.

## Lo que este informe NO garantiza

- Las 1 citas sin texto literal solo se han comprobado en cuanto a que la obra existe. **Nadie ha comprobado todavía que el autor diga lo que se le atribuye**: revísalas tú (la comprobación asistida de paráfrasis aún no está construida).
- El verificador compara con el texto disponible de cada obra. Si ese texto está incompleto o mal escaneado, puede haber errores que no detecte.
