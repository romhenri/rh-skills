#!/usr/bin/env bash
# Interactive picker: arrows/j/k move, space toggles, enter applies, q aborts.
# Selected skills get linked into the global skills dir; deselected ones get unlinked.
set -uo pipefail
repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

names=()
for s in "$repo"/*/SKILL.md; do names+=("$(basename "$(dirname "$s")")"); done
[ ${#names[@]} -gt 0 ] || { echo "no skills found in $repo" >&2; exit 1; }
[ -t 0 ] || { echo "not a terminal; use install.sh instead" >&2; exit 1; }

# Preselect whatever is already linked, so the picker shows current state.
sel=()
for n in "${names[@]}"; do
  if [[ "$dest/$n" -ef "$repo/$n" ]]; then sel+=(1); else sel+=(0); fi
done

cur=0
cleanup() { printf '\033[?25h'; }   # always restore the cursor
trap cleanup EXIT INT TERM
printf '\033[?25l'
echo "space = toggle   enter = apply   q = cancel"

draw() {
  local i mark
  for i in "${!names[@]}"; do
    if [ "${sel[$i]}" -eq 1 ]; then mark="x"; else mark=" "; fi
    if [ "$i" -eq "$cur" ]; then
      printf '\033[7m> [%s] %s\033[0m\033[K\n' "$mark" "${names[$i]}"
    else
      printf '  [%s] %s\033[K\n' "$mark" "${names[$i]}"
    fi
  done
}

draw
while true; do
  IFS= read -rsn1 key || key=""
  if [ "$key" = $'\033' ]; then
    read -rsn2 -t 1 rest || rest=""
    key="$key$rest"
  fi
  case "$key" in
    $'\033[A'|k) [ "$cur" -gt 0 ] && cur=$((cur - 1)) ;;
    $'\033[B'|j) [ "$cur" -lt $((${#names[@]} - 1)) ] && cur=$((cur + 1)) ;;
    " ")         if [ "${sel[$cur]}" -eq 1 ]; then sel[$cur]=0; else sel[$cur]=1; fi ;;
    "")          break ;;                        # enter
    q|$'\033')   echo "cancelled"; exit 0 ;;
  esac
  printf '\033[%dA' "${#names[@]}"               # rewind to the top of the list
  draw
done

cleanup
for i in "${!names[@]}"; do
  name="${names[$i]}"
  target="$dest/$name"
  if [ "${sel[$i]}" -eq 1 ]; then
    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "skip    $name (real directory already at $target)" >&2
    else
      mkdir -p "$dest"
      ln -sfn "$repo/$name" "$target"
      echo "linked  $name"
    fi
  elif [[ "$target" -ef "$repo/$name" ]] && [ -L "$target" ]; then
    rm "$target"                                  # only ever removes our own link
    echo "removed $name"
  fi
done
