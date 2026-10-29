#!/usr/bin/env bash
# Print the git state of every repo under the given roots (default: ~/Dev, ~/CDev, ~/DDev, ~/GameDev, ~/ADev).
# Local only: no fetch, so "behind upstream" is not reported.
set -uo pipefail

roots=("$@")
[[ ${#roots[@]} -eq 0 ]] && roots=("$HOME/Dev" "$HOME/CDev" "$HOME/DDev" "$HOME/GameDev" "$HOME/ADev")

printf '%-45s %-22s %-8s %-9s %s\n' REPO BRANCH CHANGES UNPUSHED NOTE
for root in "${roots[@]}"; do
  [[ -d "$root" ]] || { echo "skip $root (not found)" >&2; continue; }
  find "$root" -name node_modules -prune -o -type d -name .git -print -prune 2>/dev/null
done | sort | while IFS= read -r gitdir; do
  repo="${gitdir%/.git}"
  branch=$(git -C "$repo" symbolic-ref --short -q HEAD || echo "(detached)")
  changes=$(git -C "$repo" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  # Commits on HEAD that no remote branch has, so it also counts branches never pushed.
  unpushed=$(git -C "$repo" rev-list --count HEAD --not --remotes 2>/dev/null || echo 0)
  note=""
  [[ -z "$(git -C "$repo" remote)" ]] && note="no remote"
  git -C "$repo" rev-parse -q --verify HEAD >/dev/null || note="no commits"
  [[ "$changes" -eq 0 && "$unpushed" -eq 0 && -z "$note" ]] && note="ok"
  printf '%-45s %-22s %-8s %-9s %s\n' "${repo/#$HOME/~}" "${branch:0:22}" "$changes" "$unpushed" "$note"
done
