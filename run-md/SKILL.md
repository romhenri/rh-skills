---
name: run-md
description: Read a project and write RUN.md — a ≤30-line cheat sheet of the exact setup and run commands, copy-pasteable, nothing else. Use this whenever the user asks for a RUN.md, a quickstart, "how do I run this", "document the setup commands", "getting started file", onboarding commands for a repo, or wants the run/build/test commands for a project collected in one place. Also use when handing a repo to someone else and they need to get it running fast.
---

# RUN.md

Someone just cloned this repo. They want to get it running in the next two minutes.
They will copy-paste from your file without reading prose. That is the whole job.

## What RUN.md is

A **maximum 30 line** file of shell commands under short headings. No paragraphs,
no architecture notes, no "this project uses X to do Y". If a line doesn't get the
reader closer to a running app, delete it.

Length is a hard ceiling, not a target. 12 lines is better than 30. Most projects
fit in under 20.

## Find the real commands

Never invent commands. Every line must come from something in the repo. Read, in
this order — the first hits are the highest-signal:

- **Task runner first**: `Makefile`, `justfile`, `Taskfile.yml`, `package.json`
  scripts, `pyproject.toml` `[tool.poetry.scripts]` / `[project.scripts]`,
  `composer.json` scripts, `Rakefile`, `mix.exs` aliases.
  If a task runner exists, prefer it — `make dev` beats reconstructing the six
  commands it wraps.
- **Container**: `docker-compose.yml` / `compose.yaml`, `Dockerfile`, `devcontainer.json`.
  If compose brings the whole stack up, that's usually the shortest path and should
  lead.
- **Package manager**: lockfile decides the command, not your habit — `pnpm-lock.yaml`
  → `pnpm`, `yarn.lock` → `yarn`, `bun.lockb` → `bun`, `uv.lock` → `uv sync`,
  `poetry.lock` → `poetry install`, `Cargo.lock` → `cargo`, `go.sum` → `go`.
- **Runtime version**: `.nvmrc`, `.tool-versions`, `.python-version`, `engines` in
  package.json, `go.mod`, `rust-toolchain.toml`. Mention only the version, not how
  to install a version manager.
- **Config/secrets**: `.env.example`, `.env.sample`, `config.example.*`. If one
  exists, copying it is a setup step and belongs in the file. If required vars have
  no sane default (API keys, DB URLs), name them — a reader who runs everything and
  gets a blank-token crash learned nothing.
- **Services**: migrations directory, `schema.sql`, seed scripts — a project that
  needs `db migrate` before it starts will otherwise fail on line 3.
- **Existing README**: mine it for commands, but distrust it. READMEs rot. If the
  README says `npm run serve` and package.json has no `serve` script, the README is
  wrong — trust the manifest.

When a command in the README contradicts the manifest, or a required env var has no
example value, say so in one trailing line rather than guessing.

## Structure

Use whichever of these sections the project actually has. Drop the rest — an empty
"Test" heading is a wasted line.

~~~markdown
# RUN.md

## Setup
```bash
<one-time: install deps, copy env, migrate>
```

## Run
```bash
<the dev command — the one they came for>
```

## Notes
- <only genuinely surprising things: required env var, port, external service>
~~~

Put **Run** as early as makes sense — that's what the reader wants. Setup comes
first only because they can't skip it.

## Writing the commands

- Copy-pasteable as-is: real flags, real paths, no `<placeholders>` unless the value
  is genuinely user-specific (an API key), and then make it obviously fake: `sk-...`.
- One command per line. A reader should be able to run them top to bottom.
- Annotate only where the command lies about itself — `npm run dev  # :3000`. A
  comment restating the command (`npm test  # runs tests`) is noise.
- Multiple entry points (API + worker + web)? Show each with a heading of its own
  name, not a paragraph explaining the topology.
- Monorepo? Give the root-level command that starts everything, plus the per-package
  commands only if there's no root command.

## Before you write it

Check whether `RUN.md` already exists. If it does, verify its commands against the
current manifests and rewrite it rather than appending — a stale RUN.md is worse
than none.

Then count the lines. Over 30 means you're explaining instead of listing: cut the
Notes section first, then merge setup steps onto fewer lines, then drop the least
essential section entirely. Something had to go — say which in your reply to the
user, not in the file.
