"""Move colliding diagram labels to the nearest clear position.

The scanner (drafts/qa_content.py + svggeom.py) finds labels sitting on top of
the drawing. Fixing ~140 of those by hand would be slow and inconsistent, so
this searches each offending label's neighbourhood for the closest position
that clears the artwork, the other labels and the viewBox, and rewrites its
x/y in place.

Deliberate limits, because a label that has wandered away from the thing it
names is a worse defect than one that overlaps a line:
  * MAX_SHIFT caps how far a label may move; anything needing more is left
    alone and REPORTED for a human, never silently dragged across the figure.
  * candidates are tried nearest-first, so a label moves the least it can.
  * anchored/rotated labels (transform=) are never touched.
  * a move that would create a NEW collision with another label is rejected.

Usage:  python3 drafts/nudge_labels.py --dry     (report only)
        python3 drafts/nudge_labels.py           (apply)
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from ttfwidth import metrics
from svggeom import shapes_in, text_hits_shape, text_box

M = metrics()
MAX_SHIFT = 24.0        # units; beyond this the label has left its referent
STEP = 3.0
MARGIN = 4.0            # keep this clear of the viewBox edge
TEXT_RE = re.compile(r"<text\b([^>]*)>(.*?)</text>", re.S)


def _a(attrs, name, default=None):
    m = re.search(rf'\b{name}="([^"]*)"', attrs)
    return m.group(1) if m else default


def parse_texts(fig):
    out = []
    for m in TEXT_RE.finditer(fig):
        attrs, body = m.group(1), m.group(2)
        content = re.sub(r"<[^>]+>", "", body)
        rotated = bool(re.search(r"transform=", attrs))
        try:
            x = float(_a(attrs, "x", "0"))
            y = float(_a(attrs, "y", "0"))
        except ValueError:
            rotated = True
            x = y = 0.0
        out.append({
            "span": m.span(), "attrs": attrs, "content": content,
            "x": x, "y": y, "rotated": rotated,
            "size": float(_a(attrs, "font-size", "12") or 12),
            "weight": _a(attrs, "font-weight", "400"),
            "anchor": _a(attrs, "text-anchor", "start"),
            "fill": _a(attrs, "fill"),
        })
    return out


def candidates():
    """Offsets ordered by distance, nearest first."""
    n = int(MAX_SHIFT / STEP)
    cand = [(dx * STEP, dy * STEP)
            for dx in range(-n, n + 1) for dy in range(-n, n + 1)]
    cand.sort(key=lambda d: (d[0] * d[0] + d[1] * d[1]))
    return cand


def fix_figure(fig, vbw, vbh):
    texts = parse_texts(fig)
    shapes = list(shapes_in(fig))
    boxes = [text_box(t["x"], t["y"], t["anchor"], t["size"], t["weight"], t["content"])
             if not t["rotated"] else None for t in texts]

    def clear(box, idx):
        if box[0] < MARGIN or box[2] > vbw - MARGIN:
            return False
        if box[1] < 0 or box[3] > vbh:
            return False
        for sh in shapes:
            if text_hits_shape(box, sh, texts[idx]["fill"]):
                return False
        for j, ob in enumerate(boxes):
            if j == idx or ob is None:
                continue
            # true 2D intersection. A row-based test ("same y, overlapping x")
            # misses stacked labels drifting into each other vertically, which
            # is exactly what an unconstrained nudge tends to cause.
            if box[0] < ob[2] and ob[0] < box[2] and box[1] < ob[3] and ob[1] < box[3]:
                return False
        return True

    moved, stuck = [], []
    cands = candidates()
    for i, t in enumerate(texts):
        if t["rotated"] or not t["content"].strip():
            continue
        # Page furniture — the figure title at the top, the caption line at the
        # bottom, anything hard against the left margin — sits at a deliberate
        # position and is not an annotation of a feature. If artwork runs
        # through it, the artwork is what is wrong, so report rather than move.
        b = boxes[i]
        if t["y"] <= 30 or t["y"] >= vbh - 22 or t["x"] <= 20 or len(t["content"]) > 34:
            if not clear(b, i):
                stuck.append(t["content"])
            continue
        if clear(boxes[i], i):
            continue
        placed = False
        for dx, dy in cands:
            if dx == 0 and dy == 0:
                continue
            nb = text_box(t["x"] + dx, t["y"] + dy, t["anchor"],
                          t["size"], t["weight"], t["content"])
            if clear(nb, i):
                t["nx"], t["ny"] = t["x"] + dx, t["y"] + dy
                boxes[i] = nb
                moved.append((t["content"], dx, dy))
                placed = True
                break
        if not placed:
            stuck.append(t["content"])

    if not moved:
        return fig, moved, stuck
    out, last = [], 0
    for t in texts:
        if "nx" not in t:
            continue
        s, e = t["span"]
        seg = fig[s:e]
        seg = re.sub(r'\bx="[^"]*"', f'x="{t["nx"]:g}"', seg, count=1)
        seg = re.sub(r'\by="[^"]*"', f'y="{t["ny"]:g}"', seg, count=1)
        out.append(fig[last:s]); out.append(seg); last = e
    out.append(fig[last:])
    return "".join(out), moved, stuck


def main(argv):
    dry = "--dry" in argv
    total_moved = total_stuck = 0
    stuck_list = []
    big = []
    for path in sorted(pathlib.Path("data/content").glob("*.json")):
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        fmt = next(((i, tl) for i in (1, 2, 4) for tl in ("", "\n")
                    if json.dumps(data, indent=i, ensure_ascii=False) + tl == raw), None)
        assert fmt, f"{path}: unrecognised formatting"
        indent, tail = fmt
        changed = False
        for lid, les in data.items():
            if not isinstance(les, dict):
                continue
            lec = les.get("lecture")
            if not isinstance(lec, str):
                continue
            new_lec, pieces = lec, []
            for fig in re.findall(r"<figure.*?</figure>", lec, re.S):
                vb = re.search(r'viewBox="([^"]+)"', fig)
                if not vb:
                    continue
                parts = vb.group(1).split()
                vbw, vbh = float(parts[2]), float(parts[3])
                nf, moved, stuck = fix_figure(fig, vbw, vbh)
                total_moved += len(moved)
                total_stuck += len(stuck)
                for c, dx, dy in moved:
                    big.append(((dx*dx+dy*dy)**0.5, f"{path.stem} L{lid}", c))
                for c in stuck:
                    stuck_list.append(f"{path.stem} L{lid}: {c!r}")
                if moved:
                    pieces.append((fig, nf))
                    print(f"  {path.stem} L{lid}: moved {len(moved)} label(s)"
                          + (f", {len(stuck)} stuck" if stuck else ""))
            for old, new in pieces:
                new_lec = new_lec.replace(old, new, 1)
                changed = True
            les["lecture"] = new_lec
        if changed and not dry:
            path.write_text(json.dumps(data, indent=indent, ensure_ascii=False) + tail,
                            encoding="utf-8")
    big.sort(key=lambda r: -r[0])
    if big[:12]:
        print("\nLargest displacements (eyeball these):")
        for dist, where, lab in big[:12]:
            print(f"    {dist:5.1f}u  {where}  {lab!r}")
    print(f"\n{'[dry run] ' if dry else ''}moved {total_moved}, "
          f"could not place {total_stuck}")
    if stuck_list:
        print("NEEDS A HUMAN (no clear spot within "
              f"{MAX_SHIFT:g} units):")
        for s in stuck_list:
            print("   ", s)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
