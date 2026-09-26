---
name: assignment-checker
description: Check a finished piece of work (document, code, essay, project) against the brief that assigned it, and report exactly what's missing before submission. The deliverable is often the current project directory itself (a Python assignment, a coding exercise repo) rather than pasted text — read the working directory's files, don't wait for them to be pasted in. Use this whenever the user pastes an assignment prompt, professor's instructions, client brief, or rubric and asks whether the project/code/document they already built meets the requirements — phrases like "verifica se atendi todos os requisitos", "confere com o que o professor pediu", "bate certidão com o enunciado", "did I cover everything the brief asked for", "check this against the rubric", "am I missing anything before I submit this". Also use when they hand over both a spec/ticket and an implementation and ask if it's complete, even without the word "assignment".
---

# assignment-checker

Two documents come in: a brief (what was asked) and a deliverable (what got made).
The job is to turn the brief into a list of things a grader could point at and say
"yes" or "no" to, then go point at each one in the deliverable. Nothing here is
about whether the work is *good* — only whether it does what it was told to do.

## Get both halves

You need the actual brief text and the actual deliverable. The brief usually gets
pasted in. The deliverable, though, is more often the current project than pasted
text — a Python assignment lives in the working directory, not in the chat. Default
to reading the repo/folder you're already in: look at the file tree first (`ls`,
`find`, whatever's fast) to see its real shape before deciding what's relevant,
then read the files that plausibly answer the brief — source files, README,
config, tests, requirements/dependency manifests. Don't wait for the user to name
files; a folder listing usually makes it obvious which ones matter. Only ask when
the project has no obvious entry point (multiple unrelated subprojects, or nothing
that looks like the assignment at all).

If the deliverable truly isn't available (no repo open, no file pasted, user is
describing it from memory), ask for it rather than guessing. A checklist built from
a paraphrase of the brief just checks the user's memory against itself, which is
circular and worthless.

Read enough to actually cover the brief's scope, not just the top-level files — a
requirement satisfied only in a nested module, a test file, or a config buried a
few directories down is easy to miss on a skim, which is exactly the kind of miss
this skill exists to catch. For a codebase, that often means running the tests or
the program if the brief demands specific behavior ("the script must accept a
--input flag", "output must be valid JSON") — reading the code that claims to do
something is weaker evidence than watching it actually do it.

## Extract requirements

Read the brief once for the whole shape, then again to pull out every checkable
item. A requirement is checkable when a specific piece of the deliverable either
satisfies it or doesn't — no judgment call needed to decide which. Split compound
sentences into separate items; a brief that says "submit a PDF with an
introduction, at least 3 sources, and a conclusion, by Friday" is four requirements,
not one.

Look across these categories, since briefs bury requirements in different places:

- **Format** — file type, page/word count, font, spacing, naming convention.
- **Required content** — sections, topics, questions that must be answered,
  features that must exist.
- **Quantity** — minimum/maximum counts: sources, examples, test cases, slides.
- **Structure/order** — a mandated section sequence, a required template.
- **Standards** — citation style (ABNT, APA, MLA), coding style guide, accessibility
  rules, a schema the output must validate against.
- **Constraints** — things explicitly forbidden ("no external libraries", "max
  500 words", "don't modify the test files").
- **Deadline** — due date/time, and submission method if specified.

Vague brief language ("discuss the topic in depth", "clean code") isn't a
requirement you can check off — note it as context, not as a checklist line. Don't
invent a rubric to make it checkable; that's you grading against your own taste,
not the brief.

## Confront each requirement with the deliverable

Go through the list one item at a time and look for the actual evidence in the
deliverable — the section, the line, the file, the count — rather than judging
from a general impression of the whole. Cite what you found (or didn't) so the
verdict is falsifiable by the user, not just asserted.

Three verdicts:

- **✅ Atendido** — the evidence is there and it satisfies the requirement as
  stated.
- **⚠️ Parcial** — the requirement is addressed but incompletely: fewer sources
  than required, a section that exists but skips part of what it was told to
  cover, a format followed inconsistently.
- **❌ Faltando** — no evidence found, or it contradicts the requirement outright
  (wrong file format, over the forbidden limit, missing section entirely).

## Report

Use this exact structure:

```markdown
# Checklist — <assignment name>

| # | Requisito | Status | Justificativa |
|---|-----------|--------|----------------|
| 1 | <requirement as stated in the brief> | ✅ | <one line: where/how it's satisfied> |
| 2 | ... | ⚠️ | <what's there, what's short> |
| 3 | ... | ❌ | <what's missing> |

## Resumo

<Pronto para entrega, or a short list of exactly what to fix before submitting,
ordered by how much work each fix needs — quick text edits before structural
rework.>
```

Keep the justificativa to one line each — it's a pointer to evidence, not an essay.
The summary is the part the user actually acts on: "pronto para entrega" only when
every row is ✅, otherwise the shortest path to getting there.
