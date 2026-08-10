#!/usr/bin/env python3
"""Render a decision tree as a boxed ASCII flowchart.

Usage:  python3 render_tree.py tree.json
        cat tree.json | python3 render_tree.py

Input JSON:
  {"label": "Labeled data > 10k?", "children": [
     {"edge": "no",  "label": "LLM\\nfew-shot"},
     {"edge": "yes", "label": "Word order matters?", "children": [...]}
  ]}

`label` may contain newlines for a multi-line box. `edge` is the branch label
printed above the connector. Any number of children per node.
"""
import json
import sys

GUTTER = 3  # blank columns between sibling subtrees

# A connector cell is described by which directions it links to; this maps that
# set to the box-drawing character. Doing it by direction set rather than by
# case analysis is what keeps junctions correct when a parent's stem happens to
# land exactly on a child's column.
_CHARS = {
    "lr": "─", "ud": "│", "l": "─", "r": "─", "u": "│", "d": "│",
    "dr": "┌", "dl": "┐", "ru": "└", "lu": "┘",
    "dlr": "┬", "lru": "┴", "dru": "├", "dlu": "┤", "dlru": "┼",
}


def _box(text):
    lines = str(text).split("\n")
    w = max(len(line) for line in lines)
    return (["┌" + "─" * (w + 2) + "┐"]
            + ["│ " + line.center(w) + " │" for line in lines]
            + ["└" + "─" * (w + 2) + "┘"])


def _place(row, col, text):
    col = max(0, col - len(text) // 2)
    for i, ch in enumerate(text):
        if col + i < len(row):
            row[col + i] = ch


def render(node):
    """Return (lines, width, anchor_column) for this node's whole subtree."""
    parent = _box(node["label"])
    bw = len(parent[0])
    kids = node.get("children") or []
    if not kids:
        return parent, bw, bw // 2

    blocks = []
    for kid in kids:
        lines, w, anchor = render(kid)
        label = str(kid.get("edge", ""))
        # Widen the child's block so its edge label fits centred on the anchor,
        # rather than bleeding into a sibling.
        pad_l = max(0, len(label) // 2 - anchor)
        pad_r = max(0, anchor + len(label) - len(label) // 2 - w)
        if pad_l or pad_r:
            w += pad_l + pad_r
            lines = [" " * pad_l + line.ljust(w - pad_l) for line in lines]
            anchor += pad_l
        blocks.append((lines, w, anchor, label))

    offs, x = [], 0
    for _, w, _, _ in blocks:
        offs.append(x)
        x += w + GUTTER
    kids_w = x - GUTTER

    anchors = [offs[i] + blocks[i][2] for i in range(len(blocks))]
    left = (anchors[0] + anchors[-1]) // 2 - bw // 2
    shift = max(0, -left)  # parent sticks out to the left: push the kids right
    left += shift
    offs = [o + shift for o in offs]
    anchors = [a + shift for a in anchors]
    total = max(left + bw, kids_w + shift)
    stem = left + bw // 2

    out = [" " * left + line for line in parent]
    out[-1] = out[-1][:stem] + "┬" + out[-1][stem + 1:]  # exit the parent box

    label_row = [" "] * total
    for anchor, (_, _, _, label) in zip(anchors, blocks):
        if label:
            _place(label_row, anchor, label)
    if label_row[stem] == " ":
        label_row[stem] = "│"
    out.append("".join(label_row))

    dirs = {}
    for col in range(anchors[0], anchors[-1] + 1):
        d = dirs.setdefault(col, set())
        if col > anchors[0]:
            d.add("l")
        if col < anchors[-1]:
            d.add("r")
    for anchor in anchors:
        dirs.setdefault(anchor, set()).add("d")
    dirs.setdefault(stem, set()).add("u")
    bar = [" "] * total
    for col, d in dirs.items():
        bar[col] = _CHARS["".join(sorted(d))]
    out.append("".join(bar))

    arrows = [" "] * total
    for anchor in anchors:
        arrows[anchor] = "▼"
    out.append("".join(arrows))

    height = max(len(b[0]) for b in blocks)
    for r in range(height):
        row = ""
        for i, (lines, w, _, _) in enumerate(blocks):
            row = row.ljust(offs[i])
            row += lines[r] if r < len(lines) else " " * w
        out.append(row)

    return [line.ljust(total) for line in out], total, stem


def demo():
    """Self-check: the drawing has to actually line up."""
    tree = {"label": "Labeled data > 10k?", "children": [
        {"edge": "no", "label": "LLM\nfew-shot"},
        {"edge": "yes", "label": "Word order matters?", "children": [
            {"edge": "no", "label": "CNN"},
            {"edge": "yes", "label": "LSTM"},
            {"edge": "long docs", "label": "Transformer"},
        ]},
    ]}
    lines, width, _ = render(tree)
    assert len({len(line) for line in lines}) == 1, "rows are ragged"
    assert len(lines[0]) == width
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == "▼":
                below = lines[r + 1][c]
                assert below == "─", f"arrow at {r},{c} misses its box (found {below!r})"
    assert "┬" in lines[2], "parent box has no exit stem"
    print("\n".join(line.rstrip() for line in lines))
    print("\nok")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--demo"]:
        demo()
    else:
        src = open(sys.argv[1]) if sys.argv[1:] else sys.stdin
        lines, width, _ = render(json.load(src))
        print("\n".join(line.rstrip() for line in lines))
        # Reported here because measuring it downstream with wc/awk counts bytes,
        # and every box-drawing character is three of them.
        print(f"[width: {width} columns]", file=sys.stderr)
