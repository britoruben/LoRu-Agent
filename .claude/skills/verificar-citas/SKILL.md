---
name: verificar-citas
description: Verifica las citas de un borrador académico (obras existentes, citas literales exactas, páginas correctas, fuentes pendientes) con el verificador de LoRu-Agent y explica el resultado en lenguaje llano. Usar cuando se pida verificar, comprobar o revisar las citas de un borrador.
---

# Verificar las citas de un borrador

1. Averigua qué borrador hay que verificar. Si no lo indican, busca archivos `.md` en carpetas
   `borradores/` y pregunta cuál. Para una demostración, usa
   `ejemplos/proyecto-demo/borradores/borrador-con-errores.md`.
2. Encarga la verificación al ayudante `verificador` (subagente), indicándole la ruta del
   borrador.
3. Presenta a la persona usuaria el resultado que devuelva, sin adornos y en este orden:
   1. **Veredicto** en una línea.
   2. **Fallos**, numerados: línea, qué pasa, qué hacer.
   3. **Avisos**, agrupados.
   4. **Qué no se ha comprobado** (paráfrasis, obras sin texto disponible).
   5. Dónde está el informe completo.
4. No corrijas el borrador salvo que te lo pidan expresamente. Si te lo piden, corrige solo
   lo que el informe permite corregir con seguridad (por ejemplo, una página que el informe
   indica), vuelve a verificar y enseña el nuevo resultado.
