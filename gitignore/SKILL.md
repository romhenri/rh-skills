---
name: gitignore
description: Write or repair a project's .gitignore by reading what the repo actually contains — its languages, package managers, build tools and directory layout — and cross-checking against files git is already tracking by mistake. Use this whenever the user asks for a .gitignore, says theirs is missing, wrong, bloated or "let's clean this up", complains that build output/node_modules/venv/.env keeps showing up in `git status` or in a diff, is starting a new repo, or has just committed something that should never have been committed. Also use when they ask what a project should ignore, or mention gitignore.io, or a gitignore template.
---

# .gitignore

A .gitignore is not a template you paste in. It is a claim about what this
specific repo produces and what it needs. A generic 200-line dump from
gitignore.io technically works, but nobody can tell later which lines are load
bearing and which are cargo, so nobody ever dares delete one. Write the short
file that matches this project.

Two failure modes to avoid, in order of cost:

- **Ignoring something that must be committed** (a lockfile, `.env.example`, a
  wrapper jar) silently breaks other people's clones. This is the expensive one.
- **Failing to ignore junk** just makes `git status` noisy. Annoying, cheap to fix.

Bias toward the smaller file when unsure. Missing a pattern costs one line later;
a wrong pattern costs someone an afternoon.

## 1. Read the repo, do not guess the stack

Every line you write has to trace back to something you saw. Start here:

```bash
ls -a
git status --short
git ls-files | head -50          # what is already tracked
du -sh */ 2>/dev/null | sort -h  # the fat directories are the candidates
```

Then map evidence to patterns. Lockfiles and manifests are the strongest signal
because they name the toolchain exactly:

| Evidence | Ignore |
|---|---|
| `package.json` | `node_modules/`, `.npm`, `*.tsbuildinfo` |
| `next.config.*` / `vite.config.*` / `astro.config.*` | `.next/`, `dist/`, `.astro/`, `.vite/` |
| `pyproject.toml`, `requirements.txt` | `__pycache__/`, `*.py[cod]`, `.venv/`, `.pytest_cache/`, `.ruff_cache/`, `*.egg-info/` |
| `Cargo.toml` | `/target/` |
| `go.mod` | the compiled binary by name, `vendor/` only if not committed |
| `pom.xml` / `build.gradle` | `target/`, `build/`, `.gradle/` |
| `Gemfile` | `.bundle/`, `vendor/bundle/`, `log/`, `tmp/` |
| `*.csproj` / `*.sln` | `bin/`, `obj/` |
| `Dockerfile`, `compose.yaml` | usually nothing new, but check for bind-mounted data dirs |
| `terraform/`, `*.tf` | `.terraform/`, `*.tfstate`, `*.tfstate.*`, `.terraform.lock.hcl` stays tracked |
| `.env.example` present | `.env`, `.env.*.local` (never the example itself) |
| SQLite/data files in the tree | that path specifically, not `*.db` blanket |

If a framework has a documented ignore list, prefer it over memory. If you are
unsure whether a tool writes a cache directory, look for it in `ls -a` rather
than adding it speculatively.

**Monorepos**: prefer root-level patterns that match at any depth (`node_modules/`
matches nested ones already) over one entry per package. Add a package-local
.gitignore only when one workspace has a genuinely unique output directory.

## 2. Find what is already tracked by mistake

This is the step that gets skipped, and it is where the real value is. Adding a
pattern does nothing to a file git already tracks, so the user adds
`node_modules/`, sees it still in every diff, and concludes gitignore is broken.

After drafting the patterns, check:

```bash
git ls-files --cached | git check-ignore --stdin --verbose --no-index
```

Anything it prints is tracked *and* matched by your new rules. `--no-index` is
required here and not optional: without it check-ignore consults the index,
decides a tracked file cannot be ignored, and prints nothing at all, which is
exactly the wrong answer for this question. For each one,
decide with the user, then untrack without deleting their copy:

```bash
git rm -r --cached node_modules .env
```

Flag secrets loudly. If a `.env`, a key, or a credentials file is already in
history, untracking it does not remove it from past commits and the secret must
be treated as leaked and rotated. Say that plainly rather than implying the
`git rm --cached` fixed it.

## 3. Write the file

Group by why, with a comment per group, ordered most-project-specific first.
Someone reading this in a year should be able to tell which lines are theirs:

```gitignore
# Dependencies
node_modules/

# Build output
dist/
.next/

# Environment
.env
.env.*.local
!.env.example

# Local data
storage/*.sqlite
```

Conventions worth following because they change behaviour, not just style:

- Trailing slash (`build/`) means "directory only". Without it you also match a
  file named `build`, which is rarely intended.
- A leading slash (`/target`) anchors to the repo root. Use it when the name is
  common enough to appear in nested source dirs; skip it when you want every
  depth.
- Negation (`!.env.example`) must come after the rule it carves out of, and
  cannot resurrect a file whose parent directory is ignored. `secrets/` plus
  `!secrets/README.md` does not work; ignore `secrets/*` instead.
- No leading-blank-line clutter or duplicate entries. If you find yourself
  writing the same pattern twice under two headings, pick one heading.

## What does not belong in this file

The .gitignore is shared with everyone who clones the repo, so it should
describe the *project*, not your machine or your editor. Personal noise belongs
in a global ignore file:

```bash
git config --global core.excludesFile ~/.gitignore_global   # .DS_Store, .idea/, *.swp
```

Mention this once if you see editor or OS entries creeping in, then respect the
user's call. Many teams do keep `.DS_Store` and `.vscode/` in the repo file for
convenience, and that is a defensible choice, not an error worth arguing about.
If the repo already has such entries, leave them.

**Never ignore** without the user explicitly asking: lockfiles (`package-lock.json`,
`pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock`, `go.sum`), `.env.example`,
`gradle/wrapper/*.jar`, migration files, or anything under a `src/` tree. These
look like generated output but a clone breaks without them.

## 4. Verify before you hand it over

An existing .gitignore is prior knowledge, not an obstacle. Read it first and
merge into it; a line you do not recognise probably solved a real problem for
someone. Rewrite from scratch only if the user asks.

Then confirm it does what you claimed:

```bash
git status --short           # should be quiet, only real changes
git check-ignore -v dist/    # confirms which rule matched, and why
```

Tell the user in a couple of lines what you ignored and, more importantly,
anything you untracked or any secret that needs rotating. That second part is
the one they actually need to act on.
