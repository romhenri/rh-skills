#!/usr/bin/env bash
# Report whether each skill in this repo is active in the global skills dir.
repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
fail=0

for skill in "$repo"/*/SKILL.md; do
  name="$(basename "$(dirname "$skill")")"
  target="$dest/$name"

  if [[ -L "$target" && ! -e "$target" ]]; then
    status="BROKEN   dangling link -> $(readlink "$target")"
  elif [[ ! -e "$target" ]]; then
    status="MISSING  not installed"
  elif [[ "$target" -ef "$repo/$name" ]]; then
    status="ACTIVE"
  elif [[ -L "$target" ]]; then
    status="FOREIGN  links elsewhere -> $(readlink "$target")"
  else
    status="SHADOWED real directory, not this repo"
  fi

  [[ "$status" == ACTIVE ]] || fail=1
  printf '%-16s %s\n' "$name" "$status"
done

exit $fail
