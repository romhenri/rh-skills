---
name: atomic-prs
description: Split a branch (or a pile of local work) that mixes several features into one pull request per feature, each PR holding exactly the commits of that feature, on its own branch, titled in the repo's own style. Use this whenever the user says "atomic PRs", "split this into PRs", "one PR per feature", "this branch does too much", "break up this PR", wants a big branch reviewed in pieces, or is about to open a PR whose commits cover unrelated work. Also use when a single PR would bundle features that could be reviewed, merged or reverted separately. For splitting uncommitted changes into commits, that is atomic-commits; this skill works one level up.
allowed-tools: Bash(git:*), Bash(gh:*)
---

# Atomic PRs

A PR is atomic when it delivers exactly one feature (or one fix) and can be
reviewed, merged and reverted on its own. That is not one commit per PR: a
feature is usually several commits (the model, the endpoint, the UI, its tests),
and they all belong in the same PR. The seam is the feature, not the commit.

The job here is to read the branch, group its commits by feature, and give each
group its own branch and PR.

## 1. Read the work

```bash
git fetch origin
base=$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)
git log --oneline --reverse "origin/$base"..HEAD   # the commits to distribute
git diff --stat "origin/$base"...HEAD
git status                                          # anything not committed yet?
gh pr list --state merged --limit 15                # how this repo titles PRs
```

If there is uncommitted work, it has to become commits first. Use the
atomic-commits approach (or that skill) before going further; PRs are made of
commits, and a commit that mixes two features can't be split between two PRs.

Read `git show` for any commit whose subject doesn't make its feature obvious.
Subjects lie; diffs don't.

## 2. Group commits by feature

Assign every commit to exactly one feature. A useful test: could the PR title
describe the group in one sentence with no "and"? If not, split the group.

- **Support commits** (a test, a docs line, a config key) go with the feature
  they support, not into a "misc" PR.
- **Shared groundwork** (a refactor or helper two features both need) is its own
  PR, and the features that need it are stacked on top of it (see below).
- **Truly unrelated chores** (a dependency bump, a typo fix elsewhere) can share
  one small `chore` PR. That is the only grouping allowed to have an "and".

Then check dependencies: does feature B touch code that only exists after
feature A? `git show` the B commits and look for files or symbols introduced in A.

- Independent features each branch off `origin/$base`.
- A dependent feature branches off the PR it depends on (a stacked PR). Its PR
  targets that branch, not `$base`, and the body says "Depends on #N".

State the plan back to the user before touching anything: one line per PR with
its branch name, base, title and the commits in it. Branches, pushes and PRs are
visible to the whole team, so this is the cheap moment to fix the grouping.

## 3. Build each branch

For each PR, in dependency order:

```bash
git switch -c feat/login-page origin/main       # or the branch it stacks on
git cherry-pick a1b2c3d e4f5a6b 9c8d7e6         # oldest first, as in the original log
```

Keep the commits' original order within a group. If a cherry-pick conflicts,
that is a dependency you missed: abort (`git cherry-pick --abort`), move the
commit or stack the branch, and update the plan. Don't resolve the conflict by
hand-editing code; that creates a version of the commit that never existed.

If the repo has a quick build or test command, run it on each branch. A PR that
only works together with another PR isn't atomic, it's stacked, and should say so.

Name branches the way the repo already does (`git branch -r` shows it). If there
is no pattern, use `<type>/<short-feature-name>`.

## 4. Push and open the PRs

Only with the user's go-ahead on the plan.

```bash
git push -u origin feat/login-page
gh pr create --base main --head feat/login-page \
  --title "feat(auth): add login page with validation" \
  --body "..."
```

- **Title:** the repo's merged-PR style from step 1. With no history, use the
  commit convention the repo uses (often `type(scope): description`).
- **Body:** what the feature does and why, the commits it contains, how to test
  it, and "Depends on #N" for stacked PRs. Check for
  `.github/pull_request_template.md` and fill it in if it exists.
- Open stacked PRs after the PR they depend on, so the number exists to link.

## 5. Verify and clean up

```bash
gh pr list --author @me
git log --oneline "origin/$base"..<original-branch>
```

Every commit from the original branch must appear in exactly one PR. List any
that were left out and why. Never delete the original branch or force-push it;
offer to, once the user has checked the PRs.

Report back with a table: PR number and link, branch, base, title, commit count.

## When not to split

Some branches really are one feature: a migration plus the code that needs it,
a rename across the codebase, a fix and the test that proves it. Splitting those
gives PRs that can't be merged on their own, which is worse than one honest PR.
Say so instead of splitting. Likewise, a branch with one feature and two tiny
unrelated commits may be better as one PR plus a note than three PRs; ask.
