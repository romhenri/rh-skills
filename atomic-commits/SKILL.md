---
name: atomic-commits
description: Split a pile of uncommitted git changes into clean, atomic, conventionally-named commits in a sensible order. Use this whenever the user has accumulated many changes at once and wants them separated into logical commits, says "atomic commits", "split my commits", "organize my changes", "clean up this commit history", "commit these properly", or is about to open a PR and the diff is a mess of unrelated work. Also use when a single `git commit` would bundle changes that have nothing to do with each other.
allowed-tools: Bash(git:*)
---

# Atomic Commits

A commit is atomic when it does exactly one thing and the repo still works
afterwards. That matters because it is what makes `git revert`, `git bisect`
and code review usable later. A commit that mixes a bug fix with a refactor
cannot be reverted without losing the fix, and a reviewer has to hold both in
their head at once.

The job here is to read the working tree, decide where the seams are, and
commit along them.

## 1. Read the changes

```bash
git status
git diff --stat
git diff            # and `git diff --cached` if anything is already staged
```

Read the actual diff, not just the file names. Two changes in the same file
often belong to different commits, and two changes in different files often
belong to the same one. File boundaries are a hint, not the answer.

## 2. Find the seams

Group hunks by intent, not by location. A useful test: could each group be
described in one sentence with no "and" in it? If not, split further.

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

Before committing, state the plan back to the user as a short list of the
commits you intend to make, in order. It is cheap for them to correct the
grouping now and expensive after the commits exist.

## 3. Commit in order

Order commits so that each one leaves the repo in a working state, lowest risk
first:

1. `docs` and `chore` (touch no behaviour)
2. `test` (sets up verification)
3. `fix` (independent corrections)
4. `feat` (the main work)
5. `refactor` (rides on top of everything else)

```bash
git add README.md
git commit -m "docs: document the login flow"

git add tests/login.test.ts
git commit -m "test: cover login validation"

git add src/components/Avatar.tsx
git commit -m "fix: correct avatar scaling on retina displays"

git add src/pages/Login.tsx src/components/LoginForm.tsx
git commit -m "feat(auth): add login page with validation"
```

Never `git add .` or `git add -A` here. It defeats the entire point and will
sweep in unrelated work the user did not mention. Stage explicit paths, and
when one file contains hunks belonging to different commits, split it:

```bash
git add -p path/to/file    # interactive; needs the user to drive it
```

`git add -p` cannot be driven from a non-interactive shell. When a file needs
splitting, either ask the user to run it themselves, or say plainly that those
hunks are going into one commit together and why.

## 4. Verify

```bash
git status              # working tree should be clean, or only hold what was
                        # deliberately left out
git log --oneline -10
```

Confirm nothing was left behind by accident. If files remain uncommitted on
purpose, say which and why.

Push only if the user asked for it. Pushing is the one step here that other
people see, and rewriting it afterwards costs them a force-push.

## Message format

```
<type>(<scope>): <description>

[optional body explaining why, not what]
```

Imperative mood, no trailing period, lowercase after the colon. The subject
line says what changed; the body is only worth writing when the reason is not
obvious from the diff.

## When not to split

Some changes genuinely are one commit: a rename that touches forty files, a
dependency bump plus the call-site updates it forces, a fix and the test that
proves it. Splitting these produces commits that do not build on their own,
which is worse than one honest commit. Prefer more commits when in doubt, but
not at the cost of a broken intermediate state.
