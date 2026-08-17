---
name: atomic-commits
description: Split a pile of uncommitted git changes into clean, atomic commits, ordered sensibly and named in the style the repo's own history already uses. Use this whenever the user has accumulated many changes at once and wants them separated into logical commits, says "atomic commits", "split my commits", "organize my changes", "clean up this commit history", "commit these properly", or is about to open a PR and the diff is a mess of unrelated work. Also use when a single `git commit` would bundle changes that have nothing to do with each other.
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
git log --oneline -30   # how this repo writes commit messages
```

Read the actual diff, not just the file names. Two changes in the same file
often belong to different commits, and two changes in different files often
belong to the same one. File boundaries are a hint, not the answer.

## 2. Find the seams

Group hunks by intent, not by location. A useful test: could each group be
described in one sentence with no "and" in it? If not, split further.

Useful intents to sort by: feature, fix, docs, tests, refactor, chore. These are
for your own grouping; whether they appear in the message depends on the repo's
style, covered below.

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

(Those subjects are written in conventional style for the example only. Use
whatever style the log showed you.)

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

The repo already has a house style, and `git log --oneline -30` shows it. Match
what is there. A history that reads consistently is worth more than a history
that switches to a better format halfway down, because the inconsistency is what
people notice, and it makes your commits look like they came from somewhere else.

Read the last 30 subjects and answer four questions:

- **Prefixes?** `feat:` / `fix(scope):` conventional prefixes, a ticket key
  (`PROJ-123:`), an area tag (`[api]`), or nothing at all.
- **Mood?** Imperative (`Add login page`) or past tense (`Added login page`).
- **Case?** `Add login page` or `add login page`.
- **Bodies?** Subject only, or a body explaining the reasoning.

Then write in that style, even if you would have chosen differently. A repo whose
log is thirty lines of `Update readme` is telling you it does not want
conventional commits.

If the log is genuinely mixed, or the repo has almost no history, fall back to
conventional commits, since they encode the grouping you just did:

```
<type>(<scope>): <description>

[optional body explaining why, not what]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`. Imperative
mood, no trailing period, lowercase after the colon.

A `CONTRIBUTING.md`, a `commitlint` config, or a `.gitmessage` template outranks
the log; those are the convention written down on purpose, while the log is only
the convention as practised. Check for them when the log looks inconsistent.

Whichever style you land on, the subject says what changed. A body is only worth
writing when the reason is not obvious from the diff.

## When not to split

Some changes genuinely are one commit: a rename that touches forty files, a
dependency bump plus the call-site updates it forces, a fix and the test that
proves it. Splitting these produces commits that do not build on their own,
which is worse than one honest commit. Prefer more commits when in doubt, but
not at the cost of a broken intermediate state.
