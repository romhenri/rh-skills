---
name: md-track
description: Audit a git repo for Markdown documentation that has fallen behind the code, then repair the stale docs against the actual diff. Use this whenever the user asks which docs are out of date, wants documentation checked or refreshed against the codebase, says the README/docs are stale or lying, asks "what docs need updating", wants doc drift tracked, or is preparing a release/handoff and needs the Markdown to match reality. Also use when they mention md-track by name.
---

# md-track

Documentation doesn't announce when it starts lying. `scripts/md-track` finds the
files most likely to be lying, and the rest of this skill is about repairing them
without wrecking the ones that were fine.

## Measure

```bash
<skill-dir>/scripts/md-track
```

Run it from anywhere inside the repo; it locates the root itself. Output:

```
FILE       C_BEHIND  COMMIT   SUBJECT               N_UPDATES
draft.md   NEW       —        never committed       0
api.md     4         d04aa0f  init: api docs + app  1
README.md  1         6db060e  docs: add readme      1
```

- **C_BEHIND** — code commits landed since this doc was last touched. Commits that
  only edit `*.md` are excluded, so writing docs never makes other docs look fresher.
  A `!` suffix means the count blew past 99 and stopped being interesting.
- **COMMIT** — the last commit that touched the doc. This is the number you need: it's
  the exact point the doc's knowledge stops.
- **N_UPDATES** — lifetime edits. A doc with high C_BEHIND *and* N_UPDATES of 1 was
  written once and abandoned, which is the strongest staleness signal in the table.
- **NEW** — never committed. Not stale, just uncommitted. Leave the content alone;
  mention it so the user can commit or delete it.

## C_BEHIND is a suspicion, not a verdict

The number counts commits, and commits aren't claims. A doc can sit 200 commits behind
and still be entirely true, because none of those commits touched anything it talks
about. Editing it anyway is how you introduce errors into a correct file.

So the table only picks the reading order. Nothing gets edited until a specific
sentence has been shown to be false.

**Some files are supposed to drift.** Anything whose purpose is to record a moment —
`CHANGELOG.md`, ADRs under `docs/adr/` or `decisions/`, release notes, post-mortems,
meeting notes, dated design docs — is *correct* precisely because it hasn't changed.
"Updating" an ADR to match current code destroys the record of why the decision was
made. Skip these and say you skipped them; don't silently pass over them, since the
user may disagree about a borderline one.

## Verify before editing

For each candidate, the doc's blind spot is exactly `COMMIT..HEAD`:

```bash
git diff <COMMIT>..HEAD --stat -- . ':(exclude)*.md'
```

Start with `--stat` to see the shape — which areas of the tree moved. If nothing the
doc covers appears in that list, the doc is probably fine; say so and move on.

When the diff is large, don't read it end to end. A document's falsifiable content is
mostly **identifiers**: file paths, command names, flags, env vars, config keys,
function and class names, version numbers, ports, URLs. Pull those out of the doc and
check each one against the working tree:

```bash
git grep -n -- '--output'          # does this flag still exist?
ls src/parser.ts                    # does this path still exist?
git log --oneline <COMMIT>..HEAD -- src/parser.ts
```

This is faster than reading the diff and it produces evidence you can point at, which
is what separates a fix from a rewrite.

Two kinds of drift are worth fixing:

- **Contradiction** — the doc states something now false. A renamed flag, a moved
  path, a changed default, a dependency that's gone, a command that errors. Always fix.
- **Omission** — something exists that this doc's own scope says it should cover. A new
  subcommand missing from the command reference, a required env var absent from setup.
  Fix when it's clearly in scope; a new internal module doesn't belong in a user README.

Anything else — prose you'd word differently, sections you'd organise differently — is
not drift. Leave it.

## Edit narrowly

Every change traces to a specific piece of evidence. If you can't name the commit or
the grep result that makes the current text wrong, don't touch the line.

Keep the doc's voice, heading structure, formatting conventions, and level of detail.
The diff on the Markdown file should be small and boring — the same shape a maintainer
would have produced had they remembered to update it at the time. A doc that comes back
restructured and rewritten is impossible to review, so the user can't tell your correct
fixes from your unrequested ones.

Don't append a "Recent changes" or "Updates" section summarising commits. That's
changelog work; it makes the doc longer without making it truer, and it'll be stale
again next week.

## Report

Lead with the outcome per file, ordered as the table was:

```
docs/api.md    42 behind  →  fixed 3 claims: --out renamed to --output (a31f2c8),
                              redis dependency dropped (7d10b4e), default port 8080→3000
README.md      18 behind  →  no contradictions found, left alone
CHANGELOG.md  120 behind  →  skipped, historical record
draft.md       NEW        →  never committed, not reviewed
```

The "left alone" and "skipped" lines matter as much as the fixes — they tell the user
the file was actually checked, so the next run doesn't re-litigate it.

Stop there. Don't commit unless the user asks; they'll want to read the doc diffs
first, and that's the right instinct.
