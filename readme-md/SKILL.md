---
name: readme-md
description: Write a repo's README.md using the user's own README template, filled in from what the project actually contains. Use this whenever the user asks for a README, wants one written, rewritten, restructured or "made proper", says the README is missing/empty/embarrassing, is publishing a repo and needs it presentable, or asks to apply their readme template to a project. Distinct from RUN.md — this produces the full front-page document, not the commands cheat sheet.
---

# README.md

The README is the project's front page: someone who has never seen the repo decides
here whether it's worth their afternoon. The user has a template they like; the job is
to fill it with things that are true about *this* project.

## The template

Read `~/Dev/readme-template/README.md` — that's the user's live template and it's the
one they maintain. If it's not there, fall back to `assets/README.template.md` in this
skill, which is a copy of it.

Current shape: title with a one-line GitHub description, an opening statement, a header
image, then **Installation**, **Usage example**, **Development setup**. Read it fresh
each time rather than assuming — when the user changes their template, the change
should show up in the next README without editing this skill.

## The template is a skeleton, not the output

Its section text is placeholder — `npm install my-crazy-module`, "A few motivating and
useful examples", `edit autoexec.bat`. Shipping any of that is worse than shipping
nothing, because it advertises that nobody looked at the project.

The bar for every section: **filled with something specific to this repo, or removed.**
A missing section costs a reader nothing. A section reading "Describe how to install
all development dependencies" costs them their trust in the whole document.

## Fill it from the repo

Read before writing. The generic README is what you get when you infer from the
directory name:

- **Manifests** — `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`,
  `composer.json`. The real package name for the install line, the real scripts for the
  dev setup, the dependency list for what the thing is actually built on.
- **Lockfile picks the package manager** — `pnpm-lock.yaml` → `pnpm`, `uv.lock` →
  `uv`, `Cargo.lock` → `cargo`. Don't write `npm install` into a pnpm project.
- **Entry point and source** — enough to describe what it does and to write a usage
  example that would actually run. An invented example is the most damaging thing in a
  README, because readers copy it.
- **Existing README, RUN.md, docs/** — prior attempts at these same sentences. Mine
  them, but verify the commands still exist in the manifests; READMEs rot.
- **`gh repo view --json description -q .description`** — fills the template's
  `> Github desc:` line. If it's empty, write one, and mention it can be set with
  `gh repo edit`.
- **`git log --oneline | head -20`** and the test suite — tells you what the project
  is really about versus what it once aspired to be.

## Section by section

**Title and description line.** The repo's real name. The blockquote is the one-liner —
concrete, no marketing.

**Opening statement.** One or two paragraphs answering: what problem, for whom, why
this instead of the obvious alternative. This is the part readers actually read; it
deserves more thought than the command blocks. If the project has a genuine design
decision behind it, say it here — that's what makes a README worth reading rather than
scanning.

**Header image.** The template points at `header.png`. Only keep that line if the repo
has its own banner. Don't copy the template's placeholder image in — a broken image at
the top of a README looks worse than no image, and a stock placeholder looks worse
still. Drop the line silently when there's nothing to show.

**Installation.** Real commands from the manifests. The template splits OS X & Linux
from Windows — keep that split only if the project genuinely differs across them. A
Bash tool that will never run on Windows should say so in one line instead of carrying
an empty Windows block.

**Usage example.** Show the tool doing its actual job, with real flags and real output
where you can get it. Running the thing and pasting genuine output beats inventing
plausible output — and if it can't run here, prefer a smaller example you're sure of.

**Development setup.** Install dev deps, run the tests. If the repo has a `test.sh`, a
`Makefile` target or a `scripts.test`, that's the answer. If there's no test suite,
drop the sentence about running tests rather than implying one exists.

If the repo already has a `RUN.md`, keep Installation short here and point at it —
duplicated commands drift apart, and the reader only needs one canonical copy.

## When a README already exists

Don't overwrite it wholesale. Someone wrote that prose, and it's usually the most
accurate description of intent in the repo — often better than anything you'd infer
from code. Restructure into the template's order, keep the existing wording where it's
still true, fix what the manifests contradict, and fill the gaps.

Say what you changed afterwards — moved, kept, rewrote, dropped — so the user can check
the parts where you overrode them. A README that comes back unrecognisable can't be
reviewed, only accepted or reverted.

Write to `README.md` at the repo root, and don't commit unless asked.
