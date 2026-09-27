# Próximos pasos (nota de traspaso entre sesiones)

> **En pocas palabras:** qué está hecho, qué falta y en qué orden. Una sesión nueva de Claude
> debe leer este archivo primero para no tener que repasar conversaciones anteriores.

## Estado (27-09-2026)

- Diseño documentado (`docs/`), decisiones 0001–0008.
- Prototipo funcionando: verificador de citas, extractor de PDF (pypdf), comprobador de DOI
  (sin probar contra Crossref real), comandos `/verificar-citas` y `/preparar-pdf`.
- Pruebas mínimas (`docs/politica-de-pruebas.md`), solo Windows, trabajo en la nube.

## Siguiente, en orden

1. **Aplicar la decisión 0008** (núcleo en inglés). Una sola pasada, sin ampliar pruebas.
2. **Probar con un PDF académico real y corto** (acceso abierto, pocas páginas), una vez.
3. **Crossref real**, cuando la red del entorno permita `api.crossref.org`.
4. **Revisión del código** y petición de cambios (PR) a `main`.

## Restricciones del equipo

- Solo nube (sin ordenador local por ahora); ambos usan Windows.
- Ahorrar tokens: sesiones cortas, pruebas mínimas, nada de documentos largos.
- Pendiente de la reunión con Lola: preguntas P-01, P-03, P-04, P-05, P-09.
