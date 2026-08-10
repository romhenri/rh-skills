#!/usr/bin/env bash
# Symlink every skill in this repo into ~/.claude/skills/
set -euo pipefail
repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$dest"

for skill in "$repo"/*/SKILL.md; do
  name="$(basename "$(dirname "$skill")")"
  target="$dest/$name"
  if [[ -e "$target" && ! -L "$target" ]]; then
    echo "skip $name (real directory already at $target)" >&2
    continue
  fi
  ln -sfn "$repo/$name" "$target"
  echo "linked $name"
done
