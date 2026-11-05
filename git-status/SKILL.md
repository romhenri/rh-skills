---
name: git-status
description: Show what changed in the current repo since the last commit, one line per file with its kind (modified, new, deleted) and +/- line counts, plus branch and sync state, and mark which of those files Claude edited in this conversation. Use this whenever the user asks "what did you change", "what changed", "git status", "show me the changes", "what's pending here", wants to review Claude's edits before committing, or invokes git-status by name.
allowed-tools: Bash(git:*)
---

# git-status

## Run

```sh
~/.claude/skills/git-status/scripts/git-status.sh          # current repo
~/.claude/skills/git-status/scripts/git-status.sh <path>   # another repo
```

Output: the branch line from `git status --short --branch` (shows `[ahead N]` /
`[behind N]`), then each changed file with its kind and `+added -deleted` lines,
then a total. Staged and unstaged changes are counted together against the last
commit. New files count all their lines as added. Read-only: it changes nothing.

## Report

Paste the script output inside a code block, as-is.

Git can't tell who changed a file, so add the attribution yourself from this
conversation: after the block, list which of those files you created or edited
with your own tools (Write, Edit, or a shell command that wrote to them), and
which changed files you didn't touch, so they're the user's or another
process's. If the conversation has no edits of yours, say so in one line.

Point out anything risky in one line: deleted files, a very large deletion, or
junk like `.DS_Store`, `__pycache__/`, `.log` showing up as new.

Don't commit, stage or discard anything. Offer atomic-commits if the user wants
to commit.
