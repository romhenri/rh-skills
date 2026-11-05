---
name: github-graph
description: Draw the GitHub contribution graph (the green squares, last 26 weeks, about a semester) as ASCII in the terminal, plus a matrix with the daily contribution counts, with total, active days, current streak and best day. Use this whenever the user asks to see their GitHub contributions, contribution graph, "gráfico do github", "meus quadradinhos", how active they've been on GitHub, their streak, or wants to check it without opening github.com. Also use for another user's graph when they name a GitHub login.
---

# github-graph

## Run

```sh
~/.claude/skills/github-graph/scripts/github-graph.sh          # the logged-in gh user
~/.claude/skills/github-graph/scripts/github-graph.sh <login>  # someone else
```

Needs `gh` logged in (`gh auth status`) and `python3`. Data comes from the GitHub
GraphQL `contributionCalendar`, the same source as the profile page, so the levels
match GitHub's colors: `·` none, `░ ▒ ▓ █` the four green shades.

The output has two parts: the shaded grid, then the same grid with each day's count
in place of the shade (`·` is zero). The numbers are contributions
(commits, PRs, issues, reviews), the same count GitHub shows on hover.

## Report

Paste the whole script output, grid and matrix, as-is inside a code block, so both stay aligned. Don't
redraw it, recolor it or summarize it away. After the block, at most one line if
something stands out (a long gap, a record week). If `gh` isn't logged in, tell the
user to run `! gh auth login`.
