---
name: verify-citations
description: Verifies the citations of an academic draft (existing works, exact literal quotes, correct pages, pending sources) with LoRu-Agent's verifier and explains the result in plain language. Use when asked to verify, check or review the citations of a draft (verificar, comprobar o revisar las citas).
---

# Verify the citations of a draft

Talk to the person in Spanish.

1. Find out which draft to verify. If not given, look for `.md` files in `borradores/`
   folders and ask which one. For a demonstration, use
   `ejemplos/proyecto-demo/borradores/borrador-con-errores.md`.
2. Hand the verification to the `verifier` helper (subagent), giving it the draft path.
3. Present the result it returns to the person, without embellishment and in this order:
   1. **Verdict** in one line.
   2. **Failures**, numbered: line, what is wrong, what to do.
   3. **Warnings**, grouped.
   4. **What was not checked** (paraphrases, works without available text).
   5. Where the full report is.
4. Do not correct the draft unless explicitly asked. If asked, correct only what the report
   allows to be corrected safely (for example, a page the report gives), verify again and
   show the new result.
