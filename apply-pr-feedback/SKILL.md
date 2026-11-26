---
name: apply-pr-feedback
description: Apply the review feedback on a pull request — fetch its comments with gh (work account), list every finding with a recommendation, ask only the real decisions, fix each accepted finding in its own atomic commit, run tests/types/build, and push only after confirmation. Use when the user gives a PR URL or number with "ajuste", "implemente", "execute os ajustes", "veja o que foi sugerido no PR", "ajuste com base nos comentários de …", or pastes review findings (🔴/🟡 lists, reviewer notes) to act on. Not for reviewing code (use code-review / review-pr) or for watching a PR until merge (steward).
argument-hint: "[PR URL | PR number | pasted findings]"
model: opus
---

# Apply PR Feedback

Turn a PR's review feedback into fixes: one finding → one decision → one commit.
The user decides what to accept; Claude does the triage, the fixes and the checks.

**IS:** a single pass over the feedback that exists *now*, with the user deciding.
**IS NOT:** a code review (nothing new is hunted for), or a loop that keeps watching the PR.

## Phase 1: Gather the findings

**Objective:** a complete, numbered list of actionable findings, each tied to its source.

**Source A — PR URL or number.** Use the **work account** for every `gh` call, without
switching the globally active account:

```bash
GH_TOKEN=$(gh auth token -u romuloduarte-arco) gh pr view <n> -R <owner/repo> \
  --json number,title,headRefName,baseRefName,url,reviews,comments
GH_TOKEN=$(gh auth token -u romuloduarte-arco) gh api --paginate \
  repos/<owner>/<repo>/pulls/<n>/comments      # inline review comments (path, line, body, id)
```

- No `-R`? Derive owner/repo from the URL, or from `git remote get-url origin`.
- If the token call fails, run `gh auth status` and tell the user which account is missing — never fall back to the personal account silently.
- Make sure the local checkout is on the PR's head branch (`headRefName`) and up to date (`git fetch && git status`). If it isn't, stop and ask before checking out — there may be local work.

**Source B — pasted findings** (🔴/🟡/🟢 lists, a reviewer's message, a bot report):
parse them as given. Fetch nothing unless the user also named the PR.

**Filter:**
- Drop: approvals, "LGTM", praise, bot noise, threads already resolved, comments on lines that no longer exist and whose point is already addressed in the current code.
- If the user named a reviewer ("comentários de @Fulano"), keep only that author's.
- Merge duplicates (same point raised twice) into one finding.

## Phase 2: Triage with recommendations

**Objective:** the user sees every finding and what Claude would do about it, before any edit.

Read the code each finding points at before recommending. Then show one table:

```
| # | Sev | Where | Finding (short) | Recommendation | Why |
|---|-----|-------|-----------------|----------------|-----|
| 1 | 🔴 | api/auth.py:42 | token not validated on refresh | Accept | real bug, 3-line fix |
| 2 | 🟡 | models.py:10 | rename `data` → `payload` | Accept | cheap, clearer |
| 3 | 🟡 | service.py:88 | extract a strategy class | Reject | one caller; YAGNI |
| 4 | 🟢 | README | add diagram | Adapt | add a short list instead |
```

Recommendation is one of: **Accept**, **Adapt** (fix the concern differently — say how),
**Reject** (say why), **Ask** (needs info only the user has). Keep severity from the
source when it has one; otherwise infer 🔴 bug/security, 🟡 design/clarity, 🟢 nit.

## Phase 3: Ask only the real decisions

**Objective:** a final accept/reject per finding with the fewest questions.

- Ask with **one** AskUserQuestion call. The first option is always "Aceito recomendação" (applies the whole table as recommended).
- Ask a separate question only for findings that are **Ask**, or **Reject/Adapt** where the reviewer might reasonably push back (max 4 questions; group the rest under the first one).
- Don't ask about clear-cut Accepts.

## Phase 4: Fix — one finding per commit

**Objective:** each accepted finding lands as an atomic, revertible commit.

For each accepted finding, in severity order (🔴 first):

1. Make the smallest change that resolves the finding — no drive-by refactors.
2. Add or update a test when the finding is about behavior (bug, edge case, validation). Skip tests for renames, docs and comments.
3. Run the fast checks scoped to what changed (the relevant test file, the linter on touched files).
4. Commit with Conventional Commits in the repo's existing style, referencing the finding:
   `fix(auth): validate token on refresh` — body: `Addresses review comment: <link or "#1 from review">`.
   No AI attribution trailer.

If a fix turns out bigger than expected, or reveals the finding was wrong, stop and tell
the user rather than expanding scope.

## Phase 5: Verify

**Objective:** the branch is green as a whole.

Run the project's full checks — discover them from `Makefile`, `package.json`, `pyproject.toml`,
CI config, or CLAUDE.md (typically: test suite, type checker, linter, build). Report failures
with their output; fix only failures introduced by this run (as their own commit), and flag
pre-existing ones without fixing them.

## Phase 6: Report and push (on confirmation)

**Objective:** the user knows exactly what happened to each finding, and nothing leaves the machine without their OK.

Report:

```
| # | Finding | Outcome | Commit |
|---|---------|---------|--------|
| 1 | token not validated on refresh | Fixed + test | a1b2c3d |
| 2 | rename data → payload | Fixed | d4e5f6a |
| 3 | extract strategy class | Rejected — one caller | — |

Checks: tests ✅ · types ✅ · build ✅
```

Then ask: push now? Only on yes:
`git push` (the work account's credentials apply via the remote; if push is denied, show the error — don't switch accounts on your own).

After a successful push, **offer** to reply on each review thread (fixed → commit SHA;
rejected → the one-line reason). Post only after explicit confirmation, via
`GH_TOKEN=$(gh auth token -u romuloduarte-arco) gh api repos/<o>/<r>/pulls/<n>/comments/<id>/replies -f body=…`.

## Examples

**PR URL:**
User: `https://github.com/acme/api/pull/99 ajuste com base nos comentários do @gabriel`
→ fetch #99 inline comments, keep only gabriel's → table of 5 findings (4 Accept, 1 Reject)
→ one question: "Aceito recomendação" / per-item override → 4 commits → checks green →
report → "Push?" → yes → push → "Reply on the 5 threads?"

**Pasted findings:**
User pastes:
```
🔴 SQL built with f-string in repo.py:30
🟡 missing type hints in utils.py
```
→ no fetch; table with 2 Accepts → user accepts → 2 commits (the 🔴 one with a test) →
checks → report → ask to push.

## Key Principles

- Read the code before recommending — a finding can be outdated, already fixed, or wrong.
- One finding, one commit. Never batch fixes; reviewers re-review commit by commit.
- Always use the work account for `gh` via `GH_TOKEN`, never `gh auth switch` (it changes global state for other sessions).
- Push and PR replies are outward-facing: both wait for an explicit yes.
- Rejecting is a valid outcome — say why in one line so the reply to the reviewer writes itself.
