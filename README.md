# skills

My authored [Claude Code](https://docs.claude.com/en/docs/claude-code) skills. This repo is the source of truth; `~/.claude/skills/<name>` are symlinks into it, so edits here are live immediately.

## Skills

| Skill | What it does |
|---|---|
| [ascii-architect](ascii-architect/SKILL.md) | Draws a system's architecture as a boxed ASCII diagram — the current repo, or a proposed one. |
| [atomic-commits](atomic-commits/SKILL.md) | Splits a pile of uncommitted changes into clean, atomic commits in a sensible order. |
| [concept-lineage](concept-lineage/SKILL.md) | Maps a concept against its broader categories, sibling concepts and subtypes, each with a one-line definition. |
| [decision-tree](decision-tree/SKILL.md) | Turns a decision or set of options into a boxed ASCII flowchart saved as Markdown. |
| [github-desc](github-desc/SKILL.md) | Generates 5 GitHub "About" descriptions from the repo, applies the pick with `gh repo edit`. |
| [md-track](md-track/SKILL.md) | Finds Markdown docs that have fallen behind the code, then repairs them against the diff. |
| [readme-md](readme-md/SKILL.md) | Writes a repo's README.md from my own template, filled in from what the project contains. |
| [run-md](run-md/SKILL.md) | Writes RUN.md — a ≤30-line copy-pasteable setup/run cheat sheet. |

## Install

```bash
git clone https://github.com/<you>/skills.git ~/Dev/skills
~/Dev/skills/install.sh
```

Symlinks every `*/SKILL.md` directory into `~/.claude/skills/`. Existing real directories are skipped, not clobbered. Override the destination with `CLAUDE_SKILLS_DIR`.

## Adding a skill

```
<name>/
  SKILL.md          # frontmatter: name, description — required
  scripts/          # optional, chmod +x
  assets/           # optional templates
```

The `description` is the only thing Claude sees when deciding whether to load the skill — write it as trigger phrases, not a summary. Run `./install.sh` again to link it.
