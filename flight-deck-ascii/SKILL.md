---
name: flight-deck-ascii
description: Render quota-style data (absences vs. limit, budget vs. cap, hours used vs. allowed, any "used / planned / remaining" numbers) as a "Flight Deck" ASCII panel — double-line frame, fixed-width columns, three-tone gauge bars (█ actual, ▒ planned, ░ free) and a short timeline underneath. Hard-capped at 72 columns so it never wraps in a 1/3-width terminal split. Use whenever the user asks for a "flight deck", "painel de bordo", or an ASCII report/simulation of usage against a limit (e.g. SIGAA faltas, "what if I miss these days"), or wants the same look as an earlier flight-deck panel.
---

# Flight Deck ASCII

A boxed panel that answers "how close am I to the limit, and what happens if I do X?"
at a glance. Three gauge tones carry the meaning, because a terminal chat has no color:

| Glyph | Meaning |
|---|---|
| `█` | actual — already happened |
| `▒` | planned / simulated — what-if |
| `░` | free — margin left before the limit |

## Width budget (the rule that matters most)

The user splits the screen into **3 terminals**, so a pane is roughly 80 columns and
anything wider wraps and wrecks the frame.

- **Hard max: 72 columns** for every line of the art. **Target: 64 or fewer.**
- Count the frame itself, the markdown fence indent and any leading spaces.
- **Never widen to fit content.** Truncate labels (abbreviate, or cut with `…`),
  shrink the bar, or drop a column. If it still doesn't fit, stack the panel
  vertically (one card per item) instead of adding width.
- Fixed-width columns: pad every cell to the same width on every row, so the
  `║` and `╦╬╩` characters line up.
- Put the art in a fenced code block, never inside a list or table (indentation
  eats the budget). Keep prose around it short; prose wraps too.
- Single-width glyphs only: box-drawing (`╔═╗║╠╬╣╚╩╦`), blocks (`█▒░`), Latin
  accents, `·`. **No emoji, no `✓ ✗ ⚠`, no CJK** — they render double-width or
  ambiguous and shift the frame.

## Layout

The reference layout is 61 columns: name 20, counter 9, bar 15 plus `[ ]` plus a
4-wide percent.

```
╔═══════════════════════════════════════════════════════════╗
║          SIMULAÇÃO DE FALTAS · VIAGEM 15/10 → 25/10       ║
╠══════════════════════╦═══════════╦════════════════════════╣
║ DISCIPLINA           ║ A+P=TOTAL ║ USO DO LIMITE (máx 15) ║
╠══════════════════════╬═══════════╬════════════════════════╣
║ Big Data             ║ 0+8=8     ║ [▒▒▒▒▒▒▒▒░░░░░░░]  53% ║
║ Cálculo Numérico     ║ 2+4=6     ║ [██▒▒▒▒░░░░░░░░░]  40% ║
║ Teste de Software    ║ 2+4=6     ║ [██▒▒▒▒░░░░░░░░░]  40% ║
╠══════════════════════╬═══════════╬════════════════════════╣
║ TOTAL                ║ 4+16=20   ║ █ atual ▒ plan ░ livre ║
╚══════════════════════╩═══════════╩════════════════════════╝

Aulas perdidas
  Seg 19  Imagens ▒▒ · Teste ▒▒
  Sex 23  Big Data ▒▒▒▒
```

Structure, in order:
1. **Title bar** — what is simulated and the period, centered.
2. **Column header**, then a `╠╬╣` rule.
3. **One row per item** — label, `actual+planned=total`, gauge, percent of limit.
4. **Total row** — doubles as the legend (`█ atual ▒ plan ░ livre`).
5. **Timeline** (optional) — one line per date, each unit of the quota as one `▒`
   (or `█` for past events), items separated by ` · `.
6. **One-line verdict** below the art: the tightest item and its margin, plus any
   assumption the numbers rest on (holidays, time of departure, …).

## Gauge rules

- Bar is **15 cells** wide, scaled to the limit: `cells = round(value / limit * 15)`.
  When the limit is 15 this is 1 cell per unit.
- Fill order left to right: `█` actual, then `▒` planned, then `░` free.
- If actual + planned exceeds the limit, fill all 15 cells and append ` !` after
  the percent (the bar can't show overflow; the percent can, e.g. `113% !`).
- A plain report with no simulation drops the `▒` tone and the `+P` in the counter.
- Percent is right-aligned in 4 columns (`  0%`, ` 53%`, `100%`).

## Verify before sending

Write the art to the scratchpad and measure it — don't eyeball alignment:

```bash
python3 -I -c 'import sys
for i, l in enumerate(sys.stdin, 1):
    w = len(l.rstrip("\n"))
    print(("OVER " if w > 72 else "ok   ") + f"{i:>3} {w:>3}")' < panel.txt
```

Every line must read `ok`, and all rows of the frame must share one width.
If a line is over, fix the content (truncate, shrink the bar) and re-measure.
