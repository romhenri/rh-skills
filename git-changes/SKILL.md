---
name: git-changes
description: Read the diff and return a Markdown table with two columns, File (relative path) and Changes (a short explanation in Brazilian Portuguese of what was changed in that file). Covers uncommitted changes by default, or a commit, branch or range when the user names one. Use this whenever the user asks "o que mudou", "o que foi mexido", "explica as mudanças", "tabela das mudanças", "resume o diff", wants a per-file summary of changes in Portuguese, or invokes git-changes by name. For the raw +/- line counts, that is git-status.
allowed-tools: Bash(git:*)
---

# git-changes

The output is one table: each changed file and, in pt-BR, what was changed in it.
The point is to understand the change without reading the diff, so the explanation
says what the change does, not which lines moved.

## 1. Pick the range

- Nothing named: everything since the last commit, staged and unstaged, plus new
  files. `git status --porcelain --untracked-files=all` lists them, `git diff HEAD`
  shows the tracked ones, and new files are read whole.
- A commit (`abc123`): `git show abc123`.
- A branch or range (`main..feat/x`, "this branch"): `git diff main...HEAD`, with
  the base from `gh repo view --json defaultBranchRef` if the user doesn't say.

Paths in the table are relative to the repo root, as git prints them.

## 2. Read the real diff

Read the diff of every file, not just the names. A file called `utils.py` with
40 changed lines can be a new feature, a bug fix or a rename; only the diff says.
For a new file, read enough of it to say what it is for.

Skip reading, but still list, files where the content says nothing: lockfiles
(`package-lock.json`, `uv.lock`), binaries, images, generated output. Describe
them by what they are ("lockfile atualizado", "imagem nova").

## 3. Write the table

```markdown
| Arquivo | Mudanças |
|---|---|
| `src/auth/login.ts` | Adiciona validação de e-mail antes do envio e mostra o erro abaixo do campo. |
| `src/auth/login.test.ts` | Novo teste cobrindo e-mail inválido e campo vazio. |
| `README.md` | Documenta a variável `AUTH_URL` na seção de setup. |
| `package-lock.json` | Lockfile atualizado pela nova dependência `zod`. |
```

Rules for the Changes column:

- Brazilian Portuguese, one or two short sentences, verb first ("Adiciona",
  "Corrige", "Remove", "Renomeia", "Move").
- Say what changed in behaviour or content and, when it's obvious from the diff,
  why. Name the functions, fields or sections involved in `code`.
- Deleted files: "Arquivo removido" plus what it was. Renames: "Renomeado de
  `old/path`" plus any content change.
- Junk files (`.DS_Store`, `__pycache__/`, `.log`): list them as "Arquivo do
  sistema, provavelmente deveria estar no `.gitignore`".
- Order: the most important change first, then related files together, junk last.

Below the table, at most one line in pt-BR summing up the whole change if the
files together form one feature or fix. No other prose.

Read-only: don't stage, commit or discard anything.
