#!/usr/bin/env bash
# Show what changed since the last commit: branch, sync state, and every changed file with +/- lines.
set -euo pipefail
cd "${1:-.}"
git rev-parse --git-dir >/dev/null

base=HEAD
git rev-parse -q --verify HEAD >/dev/null || base=$(git hash-object -t tree /dev/null)  # repo with no commits yet

git status --short --branch | head -1
# Staged and unstaged together, against the last commit.
numstat=$(git diff --numstat --no-renames "$base")

total_add=0 total_del=0 n=0
while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  code=${line:0:2} path=${line:3}
  case "$code" in
    "??") kind=new ;;
    *D*)  kind=deleted ;;
    *A*)  kind=added ;;
    *R*)  kind=renamed ;;
    *)    kind=modified ;;
  esac
  if [[ "$code" == "??" ]]; then
    add=$(wc -l < "$path" | tr -d ' ')
    del=0
  else
    stat=$(awk -F'\t' -v p="${path##* -> }" '$3 == p {print $1" "$2}' <<< "$numstat")
    read -r add del <<< "${stat:-0 0}"
  fi
  [[ "$add" == "-" ]] && add=0 && del=0  # binary file
  printf '  %-9s %-50s %+7d %8s\n' "$kind" "$path" "$add" "-$del"
  total_add=$((total_add + add)) total_del=$((total_del + del)) n=$((n + 1))
done < <(git status --porcelain --untracked-files=all)

if [[ $n -eq 0 ]]; then
  echo "  clean, nothing changed since the last commit"
else
  [[ $n -eq 1 ]] && unit=file || unit=files; echo "  $n $unit, +$total_add -$total_del"
fi
