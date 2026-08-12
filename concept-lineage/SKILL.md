---
name: concept-lineage
description: Gera a "linhagem" de um conceito para fins de estudo, mostrando conceitos mais amplos (acima), conceitos irmãos (mesmo nível) e conceitos mais específicos (abaixo), cada um com uma definição curta. Use esta skill sempre que o usuário digitar "/concept-lineage [conceito]", pedir a "linhagem de um conceito", "concept lineage de X", ou pedir para "aprender X junto com o que está acima, no mesmo nível e abaixo dele" — mesmo que não use exatamente essas palavras, qualquer pedido de mapear um conceito em relação a categorias mais amplas, conceitos irmãos e subconceitos deve acionar esta skill.
---

# Concept Lineage

Um conceito nunca é entendido sozinho — ele fica mais claro quando visto ao lado de: (1) a categoria maior de onde ele vem, (2) os "primos" que vivem na mesma categoria, e (3) os casos específicos que ele engloba. Essa skill gera exatamente essa vizinhança para qualquer conceito que o usuário quiser aprender.

A lógica é de **conjuntos aninhados**, não de causalidade:

- **Acima** = uma categoria mais ampla que **contém** o conceito atual como um caso particular.
- **Mesmo nível** = outros conceitos que também são casos particulares da mesma categoria acima, mas diferentes do atual (irmãos/co-hipônimos).
- **Atual** = o conceito que o usuário quer aprender.
- **Abaixo** = subconjuntos, instâncias, ou casos específicos que estão **contidos** no conceito atual.

## Regra mais importante: sempre múltiplos itens por nível

O objetivo é dar material de estudo, não uma árvore de um único ramo. **Nunca entregue apenas 1 conceito em "Acima", "Mesmo nível" ou "Abaixo".** A meta é:

- **Acima**: 2 a 3 conceitos (categorias que contêm o atual — se só existir uma categoria óbvia, suba mais um nível de abstração para achar uma segunda opção, ou ofereça duas lentes diferentes de categorização)
- **Mesmo nível**: 3 a 5 conceitos (quanto mais opções de comparação, melhor para o usuário fixar o conceito por contraste)
- **Abaixo**: 3 a 5 conceitos (instâncias/subtipos/consequências concretas)

Se genuinamente não existirem tantos, é aceitável entregar menos, mas primeiro tente de verdade — na maioria dos domínios (ciência, tecnologia, economia, biologia, filosofia) dá pra achar de 3 a 5 sem forçar.

## Teste de validação de nível

Antes de finalizar, verifique cada item com este teste de frase:

- Para cada item em **Abaixo**: a frase "[item] é um tipo/caso de [conceito atual]" precisa fazer sentido.
- Para o **conceito atual**: a frase "[conceito atual] é um tipo/caso de [item de Acima]" precisa fazer sentido.
- Para cada item em **Mesmo nível**: ele precisa caber na mesma frase que o conceito atual usa com o "Acima" escolhido, mas não pode ser sinônimo nem estar contido no conceito atual.

Se a frase não fecha, o item está no nível errado — suba, desça, ou mova para "mesmo nível".

## Formato de saída (sempre use este template)

```markdown
# Concept Lineage: [Nome do Conceito]

## Acima (categorias mais amplas)
1. **[Conceito]** — [definição em 1 frase, direta]
2. **[Conceito]** — [definição em 1 frase]
3. **[Conceito]** — [definição em 1 frase, se aplicável]

## Mesmo nível (conceitos irmãos)
1. **[Conceito]** — [definição em 1 frase]
2. **[Conceito]** — [definição em 1 frase]
3. **[Conceito]** — [definição em 1 frase]
4. **[Conceito]** — [definição em 1 frase, se aplicável]

## [Nome do Conceito] — conceito atual
[Explicação de 2 a 4 frases: o que é, do que é composto, ou para que serve. Direta, sem enrolação, priorizando entendimento rápido sobre exaustividade.]

## Abaixo (subconjuntos, instâncias ou casos específicos)
1. **[Conceito]** — [definição em 1 frase]
2. **[Conceito]** — [definição em 1 frase]
3. **[Conceito]** — [definição em 1 frase]
4. **[Conceito]** — [definição em 1 frase, se aplicável]
```

Cada definição deve ter no máximo uma frase — o objetivo é dar o suficiente para reconhecer o conceito depois, não um ensaio. Se o usuário quiser aprofundar em algum item específico da lista, ele vai perguntar depois; não antecipe isso preenchendo demais.

## Exemplo preenchido (referência de calibração)

```markdown
# Concept Lineage: Inteligência Artificial (IA)

## Acima (categorias mais amplas)
1. **Ciência da computação** — área que estuda como processar e transformar informação por meio de algoritmos.
2. **Dados** — informação bruta que pode ser coletada, organizada e explorada para gerar conhecimento ou automação.

## Mesmo nível (conceitos irmãos)
1. **Ciência de dados** — extração de insights e padrões a partir de grandes volumes de dados.
2. **Segurança da informação** — proteção de dados e sistemas contra acesso ou uso não autorizado.
3. **Computação em nuvem** — entrega de poder computacional e armazenamento sob demanda pela internet.
4. **Robótica** — projeto de sistemas físicos capazes de agir no mundo real, muitas vezes usando IA.

## Inteligência Artificial (IA) — conceito atual
Campo que desenvolve sistemas capazes de realizar tarefas que normalmente exigiriam inteligência humana, como reconhecer padrões, tomar decisões ou gerar conteúdo. Grande parte da IA moderna aprende esses comportamentos a partir de dados, em vez de seguir regras escritas manualmente.

## Abaixo (subconjuntos, instâncias ou casos específicos)
1. **Aprendizado de máquina (Machine Learning)** — subcampo da IA em que sistemas aprendem padrões a partir de dados.
2. **Aprendizado por reforço (RL)** — modelo de IA que aprende por tentativa e erro, recebendo recompensas.
3. **Redes neurais profundas (Deep Learning)** — modelos de IA inspirados em redes de neurônios, usados para padrões complexos.
4. **Processamento de linguagem natural (PLN)** — modelos de IA especializados em entender e gerar linguagem humana.
```

## Quando o conceito não tem hierarquia natural clara

Conceitos técnicos, científicos ou de domínios estruturados (tecnologia, biologia, economia, direito) quase sempre têm uma hierarquia de generalidade óbvia. Conceitos mais abstratos ou subjetivos (emoções, valores, experiências pessoais) podem não ter um "acima"/"abaixo" tão natural. Nesses casos:

- Ainda tente — geralmente existe uma categoria mais ampla razoável (ex: "acima" de "ansiedade" pode ser "emoções relacionadas a ameaça percebida").
- Se a hierarquia ficar forçada, diga isso ao usuário em uma frase antes da tabela, em vez de inventar categorias artificiais só para preencher o template.

## Depois de gerar a linhagem

Pergunte ao usuário (ou apenas ofereça, sem bloquear a resposta) se ele quer:
- Aprofundar em algum item específico das listas.
- Gerar o concept-lineage de um dos itens acima/abaixo/mesmo-nível (efetivamente "andando" pela árvore de conceitos).
- Um diagrama visual da estrutura, se a interface suportar geração de imagens/diagramas inline.

Não gere esses extras de forma proativa por padrão — a entrega principal é o template preenchido.
