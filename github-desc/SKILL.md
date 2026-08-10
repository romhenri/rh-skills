---
name: github-desc
description: Read the current repo and generate 5 GitHub "About" description ideas, each pitched at a different angle, then optionally apply the chosen one with `gh repo edit`. Use this whenever the user asks for a GitHub description, a repo description, an About box, a one-liner or tagline for a project, wants to describe what a repo does in one sentence, or is publishing/renaming a repo and needs it summarized. Also use when they say the current description is bad, generic, or empty.
---

# GitHub descriptions

The About box is the one sentence someone reads before deciding whether to click.
It sits directly under the repo name in search results and on the profile page.
It gets one shot.

## The style

Read `~/.claude/github-desc.txt` (or `~/.claude/gihub-desc.txt` — the older typo'd
name) if either exists. That file is the user's own collection of descriptions they
liked, and it's the ground truth for their voice. It grows over time, so read it
fresh rather than assuming what's in it.

The pattern those examples share:

> **Visual demonstration of an A\*-based shooting trajectory algorithm for RoboCup autonomous agents.**
> `[qualifier] [artifact] [of what / how] [for whom or in what domain]`

- **Starts with the thing, not a subject.** "Automated Bash audit tool to…" — never
  "This project is…", "A tool that lets you…", "Repository containing…". The
  grammatical subject is wasted characters; the reader already knows it's a repo.
- **Names concrete nouns.** A\*, Bash, HTML, git, Markdown, RoboCup, Competitive
  Programming. Every example commits to specific technology and a specific domain.
  This is the single biggest quality difference — "a tool for analyzing data" and
  "Bash audit tool to track git commit drift in Markdown documentation" describe the
  same class of thing, but only one tells you whether to click.
- **12–18 words**, sentence case, ends with a period. Fragments, not sentences.
- **Narrows at the end.** The last clause scopes it: *for RoboCup agents*, *in
  Markdown documentation*, *through visual HTML lessons*.
- **No marketing.** No "powerful", "blazing fast", "seamless", "modern", "robust",
  no emoji, no exclamation. The examples earn interest by being specific, which is
  the only thing that actually works on developers.

Two more rules that come from where the text is displayed, not from the examples:

- **Don't repeat the repo name.** GitHub renders it immediately above. `pg-schema-diff
  — A tool to diff Postgres schemas` burns a third of the line on a word already on
  screen.
- **Front-load.** GitHub truncates the About box in some views, and search results
  clip it. The distinguishing words belong in the first eight.

## Read the repo first

This skill is about *this* project, so the descriptions have to come from what's
actually in it. Guessing from the directory name produces exactly the generic output
the skill exists to avoid. Look at:

- **README** — the title and opening paragraph, which is usually someone's best
  existing attempt at this same sentence.
- **Manifests** — `package.json`, `pyproject.toml`, `Cargo.toml`, `composer.json`.
  Their `description` field is a direct prior attempt; the dependency list tells you
  the real stack far more honestly than the README does.
- **Entry point and source** — enough to know what the thing *does*, not just what
  it's built with. If the README says "utilities" but the code is one A\* implementation,
  the code wins.
- **Directory names** — `migrations/`, `benchmarks/`, `lessons/`, `agents/` each
  imply a shape.
- **Existing description** — `gh repo view --json description -q .description`. If
  there's one already, the job is beating it, and it's worth saying how.

If there's no project here to read — no repo, no manifests, empty directory — say so
and ask what the project is, rather than inventing five descriptions of nothing.

## The five angles

Five rewordings of one idea is a fake choice. Five *angles* make the user decide what
their repo is actually about, and that decision is worth more than the sentence:

1. **Mechanism** — what it does, technically. The default, closest to the examples.
2. **Use case** — the problem it solves, in the user's language rather than the
   implementation's.
3. **Stack** — leads on languages and libraries. Right when the stack *is* the draw
   (a Rust rewrite, a zero-dependency implementation).
4. **Audience** — who it's for and why they'd want it: a teaching aid, a reference
   implementation, a research artifact.
5. **Terse** — the shortest line that still identifies it, 5–8 words. Often the best
   one, and it's the honesty check on the other four.

When an angle genuinely doesn't apply — a repo with no interesting stack, a library
with no single audience — write the best alternative rather than forcing a weak line
into the slot. A limp option is worse than an unusual one, because it looks like
filler.

## Output

Label each with its angle, so the choice is legible — the point is picking a framing,
not picking a phrasing:

```
1. **Mechanism** — Visual demonstration of an A*-based shooting trajectory algorithm for RoboCup autonomous agents.
2. **Use case** — Simulator for testing goal-shot decisions in autonomous robot soccer.
3. **Stack** — Python and Pygame visualization of pathfinding applied to robot ball trajectories.
4. **Audience** — Teaching aid for understanding A* search through a RoboCup shooting problem.
5. **Terse** — A* shot trajectory visualizer for RoboCup.
```

No preamble explaining what you read, no closing paragraph on which is best unless
asked. Five lines and the offer below.

Then offer to apply it:

> Say a number to set it with `gh repo edit --description`.

Wait for the pick, then run `gh repo edit --description "<chosen>"` in the repo.
Confirm nothing beyond their number — that *is* the confirmation — but never write to
GitHub before they've named one, since it overwrites a live field and there's no undo
in the UI. If `gh` isn't authenticated, print the command for them to run instead of
troubleshooting auth uninvited.
