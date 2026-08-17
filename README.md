# skills

My authored [Claude Code](https://docs.claude.com/en/docs/claude-code) skills. This repo is the source of truth; `~/.claude/skills/<name>` are symlinks into it, so edits here are live immediately.

## Skills

**ASCII**

- [ascii-architect](ascii-architect/SKILL.md): draws a system's architecture as a boxed ASCII diagram, the current repo or a proposed one.
- [decision-tree](decision-tree/SKILL.md): turns a decision or set of options into a boxed ASCII flowchart saved as Markdown.

**Markdown gen**

- [readme-md](readme-md/SKILL.md): writes a repo's README.md from my own template, filled in from what the project contains.
- [run-md](run-md/SKILL.md): writes RUN.md, a ≤20-line copy-pasteable setup/run cheat sheet.
- [md-track](md-track/SKILL.md): finds Markdown docs that have fallen behind the code, then repairs them against the diff.

**Git Ops**

- [atomic-commits](atomic-commits/SKILL.md): splits a pile of uncommitted changes into clean, atomic commits in a sensible order.
- [gitignore](gitignore/SKILL.md): writes a .gitignore from what the repo actually contains, and untracks what slipped in.
- [github-desc](github-desc/SKILL.md): generates 5 GitHub "About" descriptions from the repo, applies the pick with `gh repo edit`.

**Study**

- [concept-lineage](concept-lineage/SKILL.md): maps a concept against its broader categories, sibling concepts and subtypes, each with a one-line definition.

# How to use

`install.sh` symlinks all skills into `~/.claude/skills/`. You can also symlink individual skills into that directory, or copy them there.

`softlink.sh` symlinks all skills into `~/.claude/skills/` but does not overwrite existing ones, so you can keep your own edits in place.

`verify.sh` checks that all skills are symlinked into `~/.claude/skills/` and that they are up to date with this repo.