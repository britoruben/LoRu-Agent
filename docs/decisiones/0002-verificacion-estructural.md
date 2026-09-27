# Decisión 0002 · Las citas se protegen con el diseño del sistema

- **Estado:** aceptada
- **Fecha:** 2026-09-27
- **Quién decide:** Rubén

## En pocas palabras

No basta con pedirle a la IA que no invente citas. El sistema está construido para que **no pueda**
colar una cita falsa: solo cita obras comprobadas, el formato lo pone un programa y otro programa
revisa cada cita antes de terminar.

## Situación

Las IA a veces inventan referencias, dan DOI incorrectos, alteran citas literales o se equivocan
de página. Pedirles en las instrucciones que no lo hagan reduce el problema, pero no lo elimina.

## Decisión

1. La IA solo puede citar obras de la **estantería verificada** del proyecto, mediante etiquetas.
2. El **formato** de las citas lo aplica un programa con el estilo que corresponda (APA,
   Chicago…).
3. Un **verificador** (un programa, no la IA) comprueba que la obra existe, que el DOI es correcto,
   que la cita literal está en el original y que la página es la correcta. Si hay fallos, el texto
   no se puede dar por terminado.

Explicación completa en [05 · Verificación de citas](../05-verificacion-citas.md).

## Otras opciones que se valoraron

- **Solo instrucciones a la IA:** insuficiente.
- **Solo revisión humana:** con decenas de citas es lento y fácil pasar errores por alto.

## Consecuencias

- Hace falta la estantería del proyecto y el texto de cada obra citada.
- Una obra de la que no se tiene el texto no se puede citar literalmente sin comprobarla a mano.
