---
name: english
description: Translates a text into natural English and returns only the translation. Use when the user pastes or references a text (usually Portuguese) and asks to translate it, "traduz", "passa pro inglês", or "em inglês".
argument-hint: "[text or file path]"
---

# English

Traduz o texto recebido para o inglês e devolve a tradução.

## Rules

- Translate faithfully: keep meaning, tone, register (formal/informal) and structure — same paragraphs, lists, line breaks and markdown.
- Write natural English, not word-for-word: use the idiom an English speaker would use.
- Fix obvious typos in the source silently when the intent is clear (e.g. "gignte" → "giant"); don't flag them.
- Keep untouched: proper nouns, brand/org names and acronyms (e.g. "AIL"), code, URLs and numeric values (notation may adapt to English, e.g. "+30k" → "30k+").
- If a term is genuinely ambiguous, pick the most likely reading and add one short note below the translation.
- If the text is already in English, say so and return it unchanged.

## Output format

Return only the translation — no preamble, no "Here is the translation".

```
<translated text>
```

Only if needed:

```
---
Note: <ambiguity and the reading chosen>
```

## Example

**Input:**
> Como presidente da AIL, tive impacto gigante com +30k alunos atingidos.

**Output:**
```
As president of AIL, I had a huge impact, reaching 30k+ students.
```
