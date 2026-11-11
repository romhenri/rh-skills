---
name: fill
description: Finds the instructions and placeholders written inside square brackets in a text — e.g. "[fale como a startup é boa]", "[nome do cliente]" — and replaces each one with the requested content, woven into the sentence. Use when the user pastes or references a text (inline or a file path) containing [...] requests and asks to preencher, completar os colchetes, or fill it in. Touches only the bracketed parts; for enriching the whole text use enrich.
argument-hint: "[text or file path]"
---

# Fill

Procura pedidos ou placeholders entre `[...]` no texto e cumpre cada um: o colchete some e, no lugar dele, entra o conteúdo pedido, encaixado na frase. O resto do texto não muda.

## Input

The text comes either inline in the prompt or as a file path in `$ARGUMENTS`.
- File path → read the file; return the filled text in the response. Only write back to the file if the user explicitly asks.
- Inline text → work on it as given.
- Neither → ask for the text.

## What counts as a request

**Fill** any `[...]` that is a request or placeholder:
- Instruction — `[fale como é a capital de tech e AI]`, `[explique o porquê]`, `[dê um exemplo]` → write the content it asks for.
- Placeholder — `[nome do cliente]`, `[data]`, `[valor]` → fill it from the text or conversation context.

**Ignore** brackets that are Markdown/syntax, not requests:
- Links `[texto](url)` and reference links `[texto][ref]`
- Checkboxes `- [ ]` / `- [x]`
- Footnotes `[^1]`
- Anything inside inline code or code blocks
- Citation-style numbers `[1]`, `[2]`

## Hard rule: no brackets in the output

The output never contains a new `[...]` — no `[verificar: …]`, no `[TODO]`, no leftover placeholder. Every request is either fully filled or resolved by asking the user.

When a request needs information you don't have and can't safely infer (a specific fact, name, number, date, or something about a company/person you don't know), **ask the user before producing the output** — use AskUserQuestion (or a direct question) listing every missing item at once, each tied to its bracket. Then fill with the answers.

Do not invent facts to avoid asking. A general, true statement built from what the text already says is fine (e.g. "uma startup que paga bem" when the text says so); a specific invented claim ("que levantou US$ 50M") is not.

## Workflow

1. **Read** — identify the text's tone, register and language.
2. **Locate** — list every bracket that is a request (skip the ignore list above).
3. **Triage** — for each request: can it be filled from general knowledge or the text's own context? If not, collect it as a question.
4. **Ask** — if any questions were collected, ask them all in one go and wait for the answers.
5. **Fill** — replace each bracket with its content:
   - It must read naturally in the sentence: adjust punctuation (commas, dashes), agreement and connectors around the insertion.
   - Match the length to the request and its position: a request mid-sentence becomes a clause or short sentence, not a paragraph — unless the request explicitly asks for more.
   - Same tone and language as the surrounding text.
6. **Check** — no `[...]` requests remain, no new brackets were introduced, and text outside the brackets is unchanged except for punctuation needed to fit the insertion.
7. **Return** — in the format below.

## Output format

```
<texto completo com os colchetes preenchidos, mesma formatação do original>

---
Filled:
- [<pedido original>] → <resumo do que entrou>
- [<pedido original>] → <resumo do que entrou>
```

## Example

**Input:**
> Vou para San Francisco [fale como é a capital de tech e AI] e vou ganhar bem na Sable [fale como a startup é boa]

The second request needs facts about Sable that aren't in the text → ask first:
> Para preencher "[fale como a startup é boa]": o que torna a Sable boa? (ex.: área de atuação, produto, tamanho, investimento, cultura)

User answers: "é de IA para saúde, cresceu 3x no último ano"

**Output:**
```
Vou para San Francisco, o principal polo de tecnologia e IA do mundo, onde estão OpenAI, Anthropic e boa parte das startups que definem o setor, e vou ganhar bem na Sable, uma startup de IA para saúde que triplicou de tamanho no último ano.

---
Filled:
- [fale como é a capital de tech e AI] → SF como polo de tech/IA, com exemplos de empresas
- [fale como a startup é boa] → IA para saúde, crescimento de 3x (informado pelo usuário)
```

Note: the first request was filled from general knowledge without asking; the second needed specifics, so it was asked instead of invented — and no brackets remain.
