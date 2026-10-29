---
name: git-track
description: Scan every git repo under ~/Dev, ~/CDev, ~/DDev, ~/GameDev and ~/ADev and report which ones have uncommitted changes or commits that were never pushed. Use this whenever the user asks for the git status of all their projects, "what haven't I committed", "what haven't I pushed", "is everything pushed", "which repos are dirty", wants a sweep before switching machines or wiping a disk, or mentions git-track by name. Also use when they name other folders to scan the same way.
---

# git-track

One sweep, every repo, two questions: is there work not committed, and is there work
not pushed.

## Run

```sh
~/.claude/skills/git-track/scripts/git-track.sh            # default roots
~/.claude/skills/git-track/scripts/git-track.sh ~/Other    # custom roots
```

If the user names folders, pass them as arguments; otherwise use the defaults. Roots
that don't exist are skipped with a note on stderr.

Columns:

- `CHANGES`: lines of `git status --porcelain` (modified, staged and untracked files).
- `UNPUSHED`: commits on the current branch that no remote branch contains, so a
  branch that was never pushed counts too.
- `NOTE`: `ok` when both are zero, `no remote` when the repo has nowhere to push,
  `no commits` for an empty repo.

The scan is local only: no `git fetch`, so it never reports "behind upstream" and
never touches the network. Only the checked-out branch is counted.

## Report

Don't paste the whole table. Reply with:

1. A one-line count: how many repos scanned, how many need attention.
2. The repos that need attention, grouped: **unpushed** first (that work exists on
   one machine only), then **uncommitted**, then **no remote**. Show path, branch
   and the number. Sort each group by size, biggest first.
3. Point out noise when you see it: if a repo's only change is `.DS_Store` or an
   editor folder like `.obsidian/`, say so (check with `git -C <repo> status
   --porcelain`) and suggest the `gitignore` skill rather than a commit.

Clean repos are just the count. List them only if the user asks.

Read-only: never commit, push, stash or clean anything unless the user asks for that
repo specifically.
