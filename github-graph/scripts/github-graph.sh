#!/usr/bin/env bash
# Draw a GitHub contribution graph (last 26 weeks, about a semester) in ASCII. Usage: github-graph.sh [user]
set -euo pipefail

fields='login contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}'
if [[ $# -gt 0 ]]; then
  json=$(gh api graphql -f query="query(\$u:String!){user(login:\$u){$fields}}" -f u="$1" --jq '.data.user')
else
  json=$(gh api graphql -f query="{viewer{$fields}}" --jq '.data.viewer')
fi

python3 -I -c '
import json, sys
from datetime import date
d = json.loads(sys.argv[1])
cal = d["contributionsCollection"]["contributionCalendar"]
all_days = [x for w in cal["weeks"] for x in w["contributionDays"]]
weeks = cal["weeks"][-26:]  # a semester; each week gets two columns
glyph = {"NONE": "·", "FIRST_QUARTILE": "░", "SECOND_QUARTILE": "▒", "THIRD_QUARTILE": "▓", "FOURTH_QUARTILE": "█"}

# Month labels: put each month name over the first week that starts in it.
months = [" "] * (2 * len(weeks))
last = None
for i, w in enumerate(weeks):
    m = date.fromisoformat(w["contributionDays"][0]["date"]).strftime("%b")
    if m != last and 2 * i + 3 <= len(months):
        months[2 * i:2 * i + 3] = m
        last = m
print("    " + "".join(months).rstrip())

for row, label in enumerate(["   ", "Mon", "   ", "Wed", "   ", "Fri", "   "]):
    # GitHub weeks start on Sunday; the first and last weeks can be partial.
    cells = []
    for w in weeks:
        days = {date.fromisoformat(x["date"]).isoweekday() % 7: x for x in w["contributionDays"]}
        cells.append(glyph[days[row]["contributionLevel"]] if row in days else " ")
    print(label + " " + " ".join(cells).rstrip())

days = [x for w in weeks for x in w["contributionDays"]]
streak = 0
for x in reversed(all_days):
    if x["contributionCount"] == 0:
        if x is all_days[-1]:
            continue  # today with no contributions yet does not break the streak
        break
    streak += 1
best = max(days, key=lambda x: x["contributionCount"])
print()
best_date, best_count = best["date"], best["contributionCount"]
start = days[0]["date"]
login, total = d["login"], sum(x["contributionCount"] for x in days)
active = sum(x["contributionCount"] > 0 for x in days)
print(f"{login}: {total} contributions since {start}, {active} active days, "
      f"current streak {streak}d, best day {best_date} ({best_count})")
print("Less · ░ ▒ ▓ █ More")

# Same grid with the counts instead of shades, three columns per week. "·" is zero.
print()
months = [" "] * (3 * len(weeks))
last = None
for i, w in enumerate(weeks):
    m = date.fromisoformat(w["contributionDays"][0]["date"]).strftime("%b")
    if m != last:
        months[3 * i:3 * i + 3] = m
        last = m
print("    " + "".join(months).rstrip())
for row, label in enumerate(["   ", "Mon", "   ", "Wed", "   ", "Fri", "   "]):
    cells = []
    for w in weeks:
        days = {date.fromisoformat(x["date"]).isoweekday() % 7: x["contributionCount"] for x in w["contributionDays"]}
        cells.append((str(days[row] or "·") if row in days else "").rjust(3))
    print(label + " " + "".join(cells).rstrip())
' "$json"
