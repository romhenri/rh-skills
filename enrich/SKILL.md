---
name: enrich
description: Enriches an existing text — fills gaps with missing context or examples, sharpens weak or vague passages, and explains terms and concepts inline — while keeping the author's structure, order and voice. Use when the user pastes or references a text (inline or a file path) and asks to enriquecer, complementar, expandir, aprofundar, "explica melhor", or make it richer/more complete. Not a rewrite and not a copyedit — for grammar-only fixes use soft-improve.
argument-hint: "[text or file path]"
---

# Enrich

Enriquece um texto que já existe: complementa o que falta, melhora o que está fraco e explica o que o leitor pode não entender. O foco é o que já está escrito — o texto final continua sendo o do autor, só que mais completo.

## Input

The text comes either inline in the prompt or as a file path in `$ARGUMENTS`.
- File path → read the file; return the enriched text in the response. Only write back to the file if the user explicitly asks.
- Inline text → work on it as given.
- Neither → ask for the text.

## The three interventions

| Marker | Tipo | O que fazer | Exemplo |
|--------|------|-------------|---------|
| `[+]` | Complementar | Adicionar o que falta: contexto, exemplo, passo omitido, consequência não dita | "Usamos cache." → + por que e onde |
| `[~]` | Melhorar | Tornar mais preciso/claro o que já está lá: trocar vago por concreto, fechar saltos de raciocínio | "melhora muito a performance" → "reduz a latência de ~800ms para ~50ms" (só se o dado estiver no texto/contexto) |
| `[?]` | Explicar | Definir termo, sigla ou conceito no ponto em que aparece, em uma frase | "idempotente" → "(pode ser repetida sem efeito extra)" |

## Boundaries

**Do:**
- Keep the original section order, headings and paragraph structure. New material goes *inside* the existing structure, next to what it enriches.
- Preserve tone, register (formal/informal), language and person (eu/nós/você).
- Fix grammar along the way when touching a sentence — but don't do a copyedit pass of untouched text.

**Do NOT:**
- Rewrite from scratch or reorganize the text.
- Invent facts, numbers, names or sources. If a complement needs a fact you don't have, insert `[verificar: <o que falta>]` instead of guessing.
- Pad. Every addition must answer a question the reader would actually have. If a passage is already clear and complete, leave it alone.
- Change the author's position or conclusions.

**Proportion:** aim for roughly +20–60% length. Short texts may grow more; a text that's already dense may barely grow. More than doubling usually means you're rewriting — pull back.

## Workflow

1. **Read** — identify the text's purpose, intended reader, tone and language. The reader determines what needs explaining (a dev doc doesn't define "API"; a text for leadership might).
2. **Diagnose** — scan for: vague claims, jumps in reasoning, jargon/acronyms the reader may not know, assertions without example, missing "why", steps skipped.
3. **Enrich** — apply `[+]`, `[~]`, `[?]` where the diagnosis found gaps. Prioritize the gaps that most block understanding.
4. **Check** — reread the result against the original: same structure? same voice? nothing invented? no filler?
5. **Return** — in the format below.

## Output format

```
<texto enriquecido completo, mesma formatação do original (markdown, listas, quebras)>

---
Changes:
- [+] <o que foi complementado e onde>
- [~] <o que foi melhorado e onde>
- [?] <termo explicado>
- [verificar] <pontos que dependem de informação que o autor precisa confirmar>
```

The markers appear only in the Changes list, not in the text itself (except `[verificar: …]`, which stays inline so the author sees it). If the text needed nothing, say so instead of inventing changes.

## Example

**Input:**
> Migramos o serviço de pagamentos para filas. Isso resolveu os problemas de timeout. Agora os jobs são idempotentes.

**Output:**
```
Migramos o serviço de pagamentos para filas: em vez de processar cada pagamento dentro da requisição HTTP, a API agora publica uma mensagem e um worker a consome em segundo plano. Isso resolveu os problemas de timeout, porque a requisição não espera mais o gateway de pagamento responder — ela retorna assim que a mensagem é enfileirada. Agora os jobs são idempotentes, ou seja, se o mesmo pagamento for processado duas vezes (por exemplo, numa nova tentativa após falha), o cliente não é cobrado em dobro. [verificar: qual fila/broker foi usado e como a idempotência é garantida — chave única por pagamento?]

---
Changes:
- [+] explicado o que "migrar para filas" significa na prática (publicação + worker)
- [~] "resolveu os problemas de timeout" → incluído o porquê
- [?] "idempotentes" definido com exemplo concreto (retry sem cobrança dupla)
- [verificar] broker usado e mecanismo de idempotência
```

Note what was kept: the three original sentences in the same order, the same informal-technical tone, and no invented technology names.
