---
name: soft-improve
description: Light copyedit pass for a piece of text — fixes grammar, spelling, punctuation and agreement errors, plus at most trivial wording tweaks, then returns the text. Use when the user pastes or references a text and asks to correct, revisar, corrigir, or lightly polish it. Never rewrites, reorders, or restructures — if the fix isn't a clear correction, leave the original wording alone.
argument-hint: "[text or file path]"
---

# Soft Improve

Corrige um texto: erros de gramática, ortografia, pontuação e concordância, além de, no máximo, pequenos ajustes de redação. Devolve o texto — nunca reescreve nem muda a estrutura.

## Scope — what counts as "soft"

**Fix:**
- Ortografia e erros de digitação
- Concordância verbal/nominal, regência, crase
- Pontuação incorreta ou ausente (vírgulas, ponto final, acentuação)
- Espaçamento duplo, capitalização óbvia, erros mecânicos
- Repetição acidental de palavra ("o o carro")
- Pequenas trocas de palavra quando a original está claramente errada (ex.: "mas" por "mais" no contexto errado)

**Do NOT:**
- Reescrever frases "para soarem melhor"
- Trocar a ordem de frases, parágrafos ou ideias
- Mudar o tom, o registro (formal/informal) ou o vocabulário por preferência estilística
- Adicionar ou remover conteúdo, exemplos, explicações
- Quebrar ou fundir parágrafos
- "Melhorar" algo que já está gramaticalmente correto

If in doubt whether a change is a correction or a rewrite, don't make it — preserve the author's original phrasing.

## Workflow

1. Read the input text (inline in the prompt, or from the file path given).
2. Pass 1 — mechanical correctness: fix grammar, spelling, punctuation, agreement, obvious typos.
3. Pass 2 — minimal polish: only changes covered by "Scope" above. Skip anything borderline.
4. Return the corrected text in full, preserving original formatting (line breaks, paragraphs, markdown, lists).
5. Below the text, add a short "Changes:" bullet list naming what was fixed (e.g. "concordância verbal em '...'", "vírgula antes de..."). If nothing needed fixing, say so instead of inventing changes.

## Output format

```
<corrected text, unchanged in structure>

---
Changes:
- <change 1>
- <change 2>
(or: "Nenhuma correção necessária.")
```

## Example

**Input:**
> Os time chegaram atrasado na reunião e ninguem avisou ele sobre o horario novo.

**Output:**
```
Os times chegaram atrasados na reunião e ninguém avisou eles sobre o horário novo.

---
Changes:
- "Os time" → "Os times" (concordância nominal)
- "chegaram atrasado" → "chegaram atrasados" (concordância)
- "ninguem" → "ninguém" (acentuação)
- "horario" → "horário" (acentuação)
```

Note what was *not* touched: sentence order, word choice ("avisou ele"/"avisou eles" kept colloquial), and no rephrasing for style.
