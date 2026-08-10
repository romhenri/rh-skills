---
name: decision-tree
description: Turn a discussion, decision, or set of competing options into a boxed ASCII flowchart saved as a Markdown file named after the topic. Use this whenever the user asks for a decision tree, a flowchart, a "how do I choose between X and Y" breakdown, wants to map out a technical choice (which architecture, which database, which library, which approach), or wants a conversation you've been having about a decision written up as a diagram. Also use when they say "what should I consider", "help me choose", "map this out", or "tree this".
---

# Decision trees

The point is not to draw a diagram. It's to force the decision into a sequence of
questions the user can actually answer today, so a vague "which architecture should I
use" becomes three factual checks and an answer.

## Get the decision

If the conversation has already been circling a choice, map *that* — the options
actually raised, the constraints actually mentioned. Don't restart from a textbook
version of the topic and quietly drop what was said.

If the user just names a topic cold ("decision tree for picking a vector DB"), build
it from the topic. Ask nothing first; a concrete tree they can correct beats an
interview.

## What makes the tree worth reading

**Every internal node is a question with a factual answer.** "Do you have more than
10k labeled examples?" is a real question — the user goes and looks. "Is high accuracy
important?" is not; everyone says yes and the branch carries no information. This is
the single thing that separates a useful tree from a flowchart-shaped restatement of
the options. When a node comes out vague, it usually means the real discriminator is
one level down: find it and hoist it up.

**Order questions by how much they eliminate.** The first question should cut the
option space roughly in half, and it should be the cheapest one to answer. A tree that
asks about deployment latency before asking whether any labeled data exists wastes the
reader's first decision.

**Leaves are the actual options**, named as the user would name them — `LSTM`,
`Postgres + pgvector`, `do nothing for now`. Include "do nothing" or "defer" as a leaf
when it's genuinely live; a tree where every path ends in work is selling, not
deciding.

**The same option may appear at several leaves.** That's fine and often true — don't
contort the questions to keep each option unique.

**Honesty beats symmetry.** If a branch genuinely doesn't resolve — two options tie
until you know the budget — end it in a box saying so rather than inventing a
tiebreaker. A tree that pretends to decide something it can't is worse than one that
names the missing fact.

## Draw it

Don't hand-draw the boxes. Aligning borders, stems and arrows by eye fails silently —
one column off and the whole chart looks broken. Write the tree as JSON and render it:

```bash
python3 <skill-dir>/scripts/render_tree.py tree.json
```

JSON shape — `label` is the box text (`\n` splits lines), `edge` is the branch label
above the connector, any number of children per node:

```json
{"label": "Labeled data > 10k?", "children": [
  {"edge": "no",  "label": "LLM\nfew-shot"},
  {"edge": "yes", "label": "Word order matters?", "children": [
    {"edge": "no",  "label": "CNN"},
    {"edge": "yes", "label": "LSTM"}
  ]}
]}
```

Boxed layout grows sideways fast, so **keep labels short** — questions under ~30
characters, edge labels one or two words, option names bare. The renderer prints
`[width: N columns]` to stderr — trust that number and don't re-measure with `wc -L`
or `awk`, which count bytes and will tell you a 60-column chart is 155 wide, since
every box-drawing character is three bytes. Past ~100 columns it wraps in most editors
and stops being readable. When a tree is
genuinely that big, cut the deepest subtree out, end that branch in a box like
`see: streaming path`, and render it as a second tree under its own heading. Two
readable charts beat one that wraps.

Run `render_tree.py --demo` if you want to see a worked example before building yours.

## The file

Write to `<kebab-case-topic>.md` in the current directory — `sentiment-analysis-architecture.md`,
`vector-db-choice.md`. Name it after the decision, not after the word "decision tree",
so it's findable later.

````markdown
# Sentiment analysis architecture

One line stating what's being decided and what's fixed going in.

## The tree

```
<rendered ASCII>
```

## Endpoints

**CNN** — fast to train, cheap to serve. Ceiling is low on negation ("not bad").

**LSTM** — handles order, slow to train, beaten by transformers on most benchmarks now.

**LLM few-shot** — no training, strongest on small data. Per-call cost, latency, vendor lock-in.
````

The endpoint notes are what stop the tree from being a trap: it walks you to one
answer, and the note tells you what you're signing up for if you take it. Two or three
lines each — when it wins, and what it costs. Cover every distinct leaf; skip the
ones that are self-explanatory rather than padding.

Keep the ASCII in a fenced block so Markdown renderers don't reflow it.
