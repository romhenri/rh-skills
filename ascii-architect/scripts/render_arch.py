#!/usr/bin/env python3
"""Render a layered architecture diagram as a boxed ASCII chart.

Usage:  python3 render_arch.py arch.json
        cat arch.json | python3 render_arch.py
        python3 render_arch.py --demo

Input JSON:
  {"rows": [["web", "admin"],
            ["api gateway"],
            ["auth", "postgres", "billing\\nservice"]],
   "edges": [["web", "api gateway", "HTTP"],
             ["admin", "api gateway"],
             ["api gateway", "auth"],
             ["api gateway", "billing\\nservice"],
             ["api gateway", "postgres", "SQL"]],
   "sides": [["billing\\nservice", "Stripe", "HTTPS"]]}

`rows` are top-to-bottom layers, each a list of box labels (`\\n` splits lines).
Labels are the box ids, so they must be unique across the whole diagram.
`edges` are [from, to] or [from, to, label] and must join adjacent rows — a
dependency that skips a layer needs a passthrough box, which is usually a sign
the layering is wrong anyway.

`sides` are external systems — the ones you call over the network and can't
point to on disk. Exactly one endpoint names a box in `rows` (the spine box),
the other is the external system. Links are bidirectional by default, drawn
◀───▶, because you send a request to use the response. Add a 4th field
"one-way" for a link where only one direction carries meaning, and the arrow
then points from the first endpoint to the second, so
["billing", "Stripe", "POST", "one-way"] fires out and
["Stripe", "billing", "webhook", "one-way"] arrives. Sidecars hang off the
right of the spine, so the spine box must be last in its row and a row can
carry only one.
"""
import json
import sys

GUTTER = 4     # blank columns between sibling boxes
SIDE_GAP = 9   # blank columns between a spine box and its sidecar

# Connector cells are described by which directions they link to; mapping that
# set to a character is what keeps junctions correct when a source column
# happens to land exactly on a target column.
_CHARS = {
    "lr": "─", "du": "│", "l": "─", "r": "─", "u": "│", "d": "│",
    "dr": "┌", "dl": "┐", "ru": "└", "lu": "┘",
    "dlr": "┬", "lru": "┴", "dru": "├", "dlu": "┤", "dlru": "┼",
}


def _put(line, x, text):
    for i, ch in enumerate(text):
        line[x + i] = ch


def _box_w(label):
    return max(len(s) for s in label.split("\n")) + 4


def _geometry(rows):
    canvas = 0
    for row in rows:
        widths = [_box_w(lab) for lab in row]
        canvas = max(canvas, sum(widths) + GUTTER * (len(row) - 1))
    geo = []
    for row in rows:
        widths = [_box_w(lab) for lab in row]
        x = (canvas - (sum(widths) + GUTTER * (len(row) - 1))) // 2
        pos = {}
        for lab, w in zip(row, widths):
            pos[lab] = (x, w)
            x += w + GUTTER
        geo.append(pos)
    return geo, canvas


def _draw_row(row, pos, canvas):
    inner = max(len(lab.split("\n")) for lab in row)
    lines = [[" "] * canvas for _ in range(inner + 2)]
    for lab in row:
        x, w = pos[lab]
        text = lab.split("\n")
        _put(lines[0], x, "┌" + "─" * (w - 2) + "┐")
        for i in range(inner):
            body = text[i] if i < len(text) else ""
            _put(lines[1 + i], x, "│" + body.center(w - 2) + "│")
        _put(lines[inner + 1], x, "└" + "─" * (w - 2) + "┘")
    return lines


def _center(entry):
    x, w = entry
    return x + w // 2


def _draw_band(edges, up, down, canvas):
    """Connector band between two adjacent rows."""
    if not edges:
        return [[" "] * canvas]

    routed = [(_center(up[a]), _center(down[b]), lab) for a, b, lab in edges]
    if all(sc == tc for sc, tc, _ in routed) and not any(l for _, _, l in routed):
        line = [" "] * canvas
        for _, tc, _ in routed:
            line[tc] = "▼"
        return [line]

    dirs = [[set() for _ in range(canvas)] for _ in range(2)]
    arrow = [" "] * canvas
    for sc, tc, _ in routed:
        dirs[0][sc] |= {"u", "d"}
        if sc == tc:
            dirs[1][sc] |= {"u", "d"}
        else:
            step = "r" if tc > sc else "l"
            back = "l" if tc > sc else "r"
            dirs[1][sc] |= {"u", step}
            dirs[1][tc] |= {"d", back}
            for c in range(min(sc, tc) + 1, max(sc, tc)):
                dirs[1][c] |= {"l", "r"}
        arrow[tc] = "▼"

    band = []
    for grid in dirs:
        band.append([_CHARS["".join(c for c in "dlru" if c in s)] if s else " "
                     for s in grid])
    for _, tc, lab in routed:
        if not lab:
            continue
        at = tc + 2
        if at + len(lab) > canvas:
            at = tc - 1 - len(lab)
        if at < 0 or any(ch != " " for ch in arrow[at:at + len(lab)]):
            print(f"warning: no room for edge label {lab!r}, dropped",
                  file=sys.stderr)
            continue
        _put(arrow, at, lab)
    band.append(arrow)
    return band


def _parse_sides(entries, row_of):
    """Map row index -> (spine label, sidecar label, edge label, mode).

    Mode is "both" (request/response, the default), or "out"/"in" for a
    one-way link, taken from the order the endpoints were written in.
    """
    by_row = {}
    for entry in entries:
        a, b, lab, flag = tuple(entry) + ("",) * (4 - len(entry))
        if flag not in ("", "one-way"):
            raise ValueError(
                f"sidecar {a!r} <-> {b!r}: 4th field must be \"one-way\" if "
                f"present, got {flag!r}")
        anchored = [n for n in (a, b) if n in row_of]
        if len(anchored) != 1:
            raise ValueError(
                f"sidecar {a!r} <-> {b!r}: exactly one endpoint must be a box "
                "in `rows`; the other is the external system")
        spine = anchored[0]
        i = row_of[spine]
        if i in by_row:
            raise ValueError(
                f"row {i} already has sidecar {by_row[i][1]!r}; sidecars hang "
                "off the right, so a row can only carry one")
        mode = "both" if not flag else ("out" if spine == a else "in")
        by_row[i] = (spine, b if spine == a else a, lab, mode)
    return by_row


def _draw_connector(block, spine, car, lab, mode):
    """Overlay the horizontal spine<->sidecar link onto a drawn row block."""
    sx, sw = spine
    gap_x = sx + sw                      # first blank column past the box edge
    gap = car[0] - gap_x
    mid = 1 + (len(block) - 3) // 2      # middle body line of the row
    a, z = gap_x + 1, car[0] - 2         # connector span, inclusive
    _put(block[mid], a, "─" * (z - a + 1))
    if mode != "in":
        block[mid][z] = "▶"
    if mode != "out":
        block[mid][a] = "◀"
    if lab:
        _put(block[mid - 1], gap_x + (gap - len(lab)) // 2, lab)


def render(spec):
    rows = spec["rows"]
    edges = [tuple(e) + ("",) * (3 - len(e)) for e in spec.get("edges", [])]

    seen = [lab for row in rows for lab in row]
    dupes = {lab for lab in seen if seen.count(lab) > 1}
    if dupes:
        raise ValueError(f"box labels must be unique, repeated: {sorted(dupes)}")

    geo, canvas = _geometry(rows)
    row_of = {lab: i for i, row in enumerate(rows) for lab in row}

    # Sidecars are placed after `rows` is laid out and extend the canvas to the
    # right, so adding one can never shift the vertical spine.
    sides = _parse_sides(spec.get("sides", []), row_of)
    for i, (spine, car, lab, _mode) in sides.items():
        if rows[i][-1] != spine:
            raise ValueError(
                f"sidecar {car!r} hangs off {spine!r}, which must be the last "
                f"box in its row so the connector has clear space to cross; "
                f"reorder row {i}")
        sx, sw = geo[i][spine]
        x = sx + sw + max(SIDE_GAP, len(lab) + 4)
        geo[i][car] = (x, _box_w(car))
        canvas = max(canvas, x + _box_w(car))

    bands = [[] for _ in rows]
    for a, b, lab in edges:
        for end in (a, b):
            if end not in row_of:
                raise ValueError(f"edge references unknown box: {end!r}")
        if row_of[b] != row_of[a] + 1:
            raise ValueError(
                f"edge {a!r} -> {b!r} skips or reverses a layer; "
                "edges must join adjacent rows")
        bands[row_of[a]].append((a, b, lab))

    out = []
    for i, row in enumerate(rows):
        spine, car, lab, mode = sides.get(i, (None,) * 4)
        block = _draw_row(row + ([car] if car else []), geo[i], canvas)
        if car:
            _draw_connector(block, geo[i][spine], geo[i][car], lab, mode)
        out += block
        if i + 1 < len(rows):
            out += _draw_band(bands[i], geo[i], geo[i + 1], canvas)
    return [("".join(line)).rstrip() for line in out], canvas


DEMO = {
    "rows": [["web app", "admin ui"],
             ["api gateway"],
             ["auth", "postgres", "billing\nservice"]],
    "edges": [["web app", "api gateway", "HTTP"],
              ["admin ui", "api gateway"],
              ["api gateway", "auth"],
              ["api gateway", "billing\nservice"],
              ["api gateway", "postgres", "SQL"]],
    "sides": [["billing\nservice", "Stripe", "HTTPS"]],
}


def _demo():
    lines, width = render(DEMO)
    assert all(len(l) <= width for l in lines), "a line overflowed the canvas"
    targets = {e[1] for e in DEMO["edges"]}  # fan-in shares one arrowhead
    assert sum(l.count("▼") for l in lines) == len(targets), "lost an arrow"
    straight, _ = render({"rows": [["a"], ["b"]], "edges": [["a", "b"]]})
    assert straight[3].strip() == "▼", straight
    both, _ = render({"rows": [["a"]], "sides": [["a", "ext", "HTTPS"]]})
    assert both[1] == "│ a │ ◀─────▶ │ ext │", both
    assert both[0] == "┌───┐  HTTPS  ┌─────┐", both
    one = {"rows": [["a"]], "sides": [["a", "ext", "", "one-way"]]}
    assert render(one)[0][1] == "│ a │ ──────▶ │ ext │", render(one)[0]
    one["sides"] = [["ext", "a", "", "one-way"]]
    assert render(one)[0][1] == "│ a │ ◀────── │ ext │", render(one)[0]
    print("\n".join(lines))
    print(f"[width: {width} columns]", file=sys.stderr)


def main():
    if "--demo" in sys.argv[1:]:
        return _demo()
    src = open(sys.argv[1]) if sys.argv[1:] else sys.stdin
    with src:
        spec = json.load(src)
    lines, width = render(spec)
    print("\n".join(lines))
    print(f"[width: {width} columns]", file=sys.stderr)


if __name__ == "__main__":
    main()
