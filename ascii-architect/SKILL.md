---
name: ascii-architect
description: Draw a system's architecture as a boxed ASCII diagram — the current repo when no target is given, or a proposed/imagined system when one is. Picks one of three framings: app (boxes are services or workspace packages), folder (boxes are directories), script (boxes are individual files). Use this whenever the user asks to diagram, visualize, sketch, chart or "map out" an architecture, structure, layout, module graph, data flow or pipeline; asks "how is this repo structured", "what does this project look like", "draw the architecture", "show me the modules"; wants an ARCHITECTURE.md; or is proposing a system and wants to see the shape of it before building. Also use when explaining code where a picture of the layout would land better than prose.
---

# ASCII architect

A good architecture diagram answers one question fast: *what talks to what?* It is
worth drawing only if a reader can point at a box and find that thing on disk, and
point at an arrow and find the import, HTTP call or queue that makes it real. Boxes
that name concepts rather than artifacts ("business logic", "the domain layer") are
where these diagrams go to die — they look authoritative and teach nothing.

## What am I drawing?

**No target named** ("diagram this repo", "draw the architecture") — read the current
repo and draw what is actually there. Not what it should be; drift between the two is
the diagram's whole value.

**A target named** — an idea, a proposal, a design under discussion, a system from
elsewhere — draw that instead, and don't quietly swap in the current repo's shape.
If the conversation has been circling a design, map *that* one: the components
actually raised, the constraints actually said out loud.

## Pick the framing

Three framings, one per diagram. Mixing them ("here's a folder, here's a service,
here's a file") is the most common way these end up unreadable, because the reader
can't tell what a box *is*.

| Framing | A box is | Reach for it when |
|---|---|---|
| **app** | a deployable service or workspace package | a monorepo, or anything with several independently-running pieces |
| **folder** | a directory | one app, where the structure lives in the directory layout |
| **script** | a single file | a small project — a handful of scripts, a pipeline, a CLI |

For a repo, the evidence is cheap to gather:

```bash
ls
cat package.json pnpm-workspace.yaml docker-compose.yml Cargo.toml go.mod 2>/dev/null | head -60
git ls-files | wc -l
git ls-files | sed 's|/.*||' | sort | uniq -c | sort -rn | head
```

Workspaces, `apps/` + `packages/`, several compose services or several `go.mod` →
**app**. One package with a structured `src/` → **folder**. Under roughly fifteen
source files, no framework → **script**. Pick one, say which in a single line, move
on — asking the user to choose costs more than being wrong and corrected.

## What earns a box

Aim for five to nine boxes. Past that the diagram becomes a directory listing with
extra steps, and the reader stops seeing the shape.

Cut ruthlessly: config, CI, tests, docs, build output and lockfiles are not
architecture. Fold the thin stuff into its neighbour rather than giving it its own
box. If something genuinely has too many parts, draw the top level and give one
crowded box its own second diagram under its own heading — two readable charts beat
one that wraps.

Arrows are dependencies with a direction: who calls, imports, reads or publishes to
whom. Verify them; don't infer a call graph from the folder names. `grep` the imports,
read the routes, look at what the compose file links. An arrow you couldn't defend
with a file and line number should not be drawn.

Layer top-to-bottom by who depends on whom — entry points and user-facing pieces at
the top, storage and shared primitives at the bottom. That way the arrows all point
one direction and the reader can stop tracing them individually.

## Draw it

Don't hand-draw boxes. Aligning borders, stems and arrowheads by eye fails silently —
one column off and the whole chart looks broken. Write the layers as JSON and render:

```bash
python3 <skill-dir>/scripts/render_arch.py arch.json
```

```json
{"rows": [["install.sh", "soft-install.sh", "verify.sh"],
          ["~/.claude/skills"],
          ["decision-tree", "readme-md", "run-md", "md-track"]],
 "edges": [["install.sh", "~/.claude/skills", "symlink"],
           ["soft-install.sh", "~/.claude/skills"],
           ["verify.sh", "~/.claude/skills"],
           ["~/.claude/skills", "decision-tree"],
           ["~/.claude/skills", "readme-md"],
           ["~/.claude/skills", "run-md"],
           ["~/.claude/skills", "md-track"]]}
```

renders as:

```
     ┌────────────┐    ┌─────────────────┐    ┌───────────┐
     │ install.sh │    │ soft-install.sh │    │ verify.sh │
     └────────────┘    └─────────────────┘    └───────────┘
            │                   │                   │
            └───────────────────┼───────────────────┘
                                ▼ symlink
                      ┌──────────────────┐
                      │ ~/.claude/skills │
                      └──────────────────┘
                                │
        ┌──────────────────┬────┴──────────┬──────────────┐
        ▼                  ▼               ▼              ▼
┌───────────────┐    ┌───────────┐    ┌────────┐    ┌──────────┐
│ decision-tree │    │ readme-md │    │ run-md │    │ md-track │
└───────────────┘    └───────────┘    └────────┘    └──────────┘
```

`rows` are layers top to bottom. Labels are the box ids, so keep them unique and
short — a name plus maybe a `\n` and one qualifier. Edges are `[from, to]` or
`[from, to, label]`, and must join adjacent rows; the renderer rejects an edge that
skips a layer, which nearly always means the layering is wrong rather than the edge.
Edge labels are optional and best kept under ~10 characters — use them for the
*mechanism* (`HTTP`, `SQL`, `imports`, `SNS`), not for narration.

The renderer prints `[width: N columns]` to stderr. Trust that number rather than
re-measuring with `wc -L` or `awk`, which count bytes and will call a 60-column chart
155 wide — every box-drawing character is three bytes. Past ~100 columns it wraps in
most editors; split the diagram instead.

Run `render_arch.py --demo` to see a worked example before building yours.

## The output

Default to writing `ARCHITECTURE.md` in the repo root for repo diagrams, and
`<kebab-case-topic>-architecture.md` for a proposed system. If the user asked for the
diagram inline — in a comment, in a README section, in the chat — just give it to them
there; don't create a file nobody asked for.

````markdown
# Architecture

One line: what this system is, and which framing the diagram uses.

```
<rendered ASCII>
```

## The boxes

**api gateway** — `apps/gateway`. Terminates HTTP, validates the session cookie,
fans out to the services below. Every external request enters here.

**billing service** — `apps/billing`. Owns subscriptions and Stripe webhooks. The
only writer to the `invoices` tables.
````

Keep the ASCII fenced so Markdown renderers don't reflow it. The box notes are what
turn a picture into a document: one or two lines each, naming the path on disk and
what the thing is responsible for. Skip the boxes that are self-explanatory rather
than padding — `postgres` needs no paragraph.

If drawing it surfaced something worth saying — a cycle, a box everything depends on,
a service that turned out to be dead — say it in a short line under the diagram. That
observation is usually the most valuable output of the whole exercise, and it's lost
if you only ship the picture.
