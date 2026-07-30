"""Geometry for the diagram scanner: do labels collide with the drawing?

The original scanner only compared text against text. The owner's 2026-07-30
note ("many components overlap") is about labels sitting on top of the drawing
itself, so this module extracts real geometry from the SVG primitives the
diagrams actually use — line, rect, path, circle, polyline, polygon, ellipse —
and tests it against each label's measured bounding box.

Two things are deliberately NOT flagged, because both are intentional design in
this project's diagrams and flagging them would bury the real defects:

  * a label inside a LIGHT filled box (a callout/legend panel). Only a dark or
    saturated fill actually hurts legibility, so fill luminance is the test.
  * a stroke that merely touches the outer edge of a label's box. Text boxes are
    measured generously, so edge contact is normal; the stroke has to cross into
    the inset interior to count.
"""
import math
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from ttfwidth import metrics

# Glyph box relative to the baseline, measured against getBBox() in the browser
# over real labels: the box runs 0.98*size above the baseline and 0.22*size
# below. An earlier 0.78 ascent was 2.4 units short at 12px and let labels sit
# under thick rules while the checker called them clear.
ASCENT = 0.98
DESCENT = 0.22


def text_box(x, y, anchor, size, weight, content):
    w = metrics().width(content, size, weight)
    x0 = x - w / 2 if anchor == "middle" else x - w if anchor == "end" else x
    return (x0, y - size * ASCENT, x0 + w, y + size * DESCENT)


# A stroke has to cross this far inside the text box before it counts. Text
# bounding boxes include leading and side bearing, so the outer few units are
# whitespace the drawing may legitimately touch.
INSET_X = 2.0
INSET_Y = 3.0
# Fills lighter than this are backgrounds/callout panels, not obstructions.
LIGHT_FILL = 0.72


def _num(s, default=0.0):
    try:
        return float(s)
    except (TypeError, ValueError):
        return default


def _attr(tag, name, default=None):
    m = re.search(rf'\b{name}="([^"]*)"', tag)
    return m.group(1) if m else default


def luminance(color):
    """Rough relative luminance of an SVG colour, 0 (black) to 1 (white).
    Returns 1.0 for anything unparseable so unknown fills are treated as light
    and therefore not flagged — this checker errs toward silence."""
    if not color:
        return 1.0
    c = color.strip().lower()
    if c in ("none", "transparent"):
        return 1.0
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6}|[0-9a-f]{8})", c)
    if not m:
        return 1.0
    h = m.group(1)
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    if len(h) == 8:
        # #rrggbbaa — these diagrams shade bands with a low alpha suffix, which
        # is a wash over white, not an opaque block. Composite before judging.
        a = int(h[6:8], 16) / 255
        lum = a * lum + (1.0 - a) * 1.0
    return lum


def _path_points(d):
    """Approximate a path as a list of polylines.

    Curves are reduced to their endpoints and control points, which is enough
    to catch a curve sweeping through a label without pulling in a full bezier
    flattener. Arcs (A) contribute their endpoint only.
    """
    out, cur, x, y, start = [], [], 0.0, 0.0, (0.0, 0.0)
    for m in re.finditer(r"([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)", d):
        cmd, raw = m.group(1), m.group(2)
        nums = [float(v) for v in re.findall(r"-?\d*\.?\d+(?:e-?\d+)?", raw)]
        rel = cmd.islower()
        c = cmd.upper()
        if c == "M":
            for i in range(0, len(nums) - 1, 2):
                nx, ny = nums[i], nums[i + 1]
                x, y = (x + nx, y + ny) if rel else (nx, ny)
                if i == 0:
                    if len(cur) > 1:
                        out.append(cur)
                    cur, start = [(x, y)], (x, y)
                else:
                    cur.append((x, y))
        elif c == "L":
            for i in range(0, len(nums) - 1, 2):
                nx, ny = nums[i], nums[i + 1]
                x, y = (x + nx, y + ny) if rel else (nx, ny)
                cur.append((x, y))
        elif c == "H":
            for nx in nums:
                x = x + nx if rel else nx
                cur.append((x, y))
        elif c == "V":
            for ny in nums:
                y = y + ny if rel else ny
                cur.append((x, y))
        elif c in ("C", "S", "Q", "T"):
            step = {"C": 6, "S": 4, "Q": 4, "T": 2}[c]
            for i in range(0, len(nums) - step + 1, step):
                seg = nums[i:i + step]
                for j in range(0, len(seg) - 1, 2):
                    px, py = seg[j], seg[j + 1]
                    cur.append((x + px, y + py) if rel else (px, py))
                x, y = cur[-1]
        elif c == "A":
            for i in range(0, len(nums) - 6, 7):
                nx, ny = nums[i + 5], nums[i + 6]
                x, y = (x + nx, y + ny) if rel else (nx, ny)
                cur.append((x, y))
        elif c == "Z":
            if cur:
                cur.append(start)
                x, y = start
    if len(cur) > 1:
        out.append(cur)
    return out


def shapes_in(fig):
    """Yield dicts describing every drawable primitive in one <figure>.

    kind is 'stroke' (a line the eye follows) or 'fill' (a solid area).
    A shape with both a fill and a stroke yields both.
    """
    for tag in re.findall(r"<(?:line|rect|circle|ellipse|polyline|polygon|path)\b[^>]*>", fig):
        name = re.match(r"<(\w+)", tag).group(1)
        fill = _attr(tag, "fill")
        stroke = _attr(tag, "stroke")
        sw = _num(_attr(tag, "stroke-width", "1"), 1.0)
        polys = []
        box = None
        if name == "line":
            polys = [[(_num(_attr(tag, "x1")), _num(_attr(tag, "y1"))),
                      (_num(_attr(tag, "x2")), _num(_attr(tag, "y2")))]]
        elif name == "rect":
            x, y = _num(_attr(tag, "x")), _num(_attr(tag, "y"))
            w, h = _num(_attr(tag, "width")), _num(_attr(tag, "height"))
            box = (x, y, x + w, y + h)
            polys = [[(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]]
        elif name in ("circle", "ellipse"):
            cx, cy = _num(_attr(tag, "cx")), _num(_attr(tag, "cy"))
            rx = _num(_attr(tag, "r")) or _num(_attr(tag, "rx"))
            ry = _num(_attr(tag, "r")) or _num(_attr(tag, "ry"))
            box = (cx - rx, cy - ry, cx + rx, cy + ry)
            polys = [[(cx + rx * math.cos(t), cy + ry * math.sin(t))
                      for t in [i * math.pi / 12 for i in range(25)]]]
        elif name in ("polyline", "polygon"):
            nums = [float(v) for v in re.findall(r"-?\d*\.?\d+", _attr(tag, "points", ""))]
            pts = list(zip(nums[0::2], nums[1::2]))
            if name == "polygon" and pts:
                pts.append(pts[0])
            polys = [pts] if len(pts) > 1 else []
        elif name == "path":
            polys = _path_points(_attr(tag, "d", ""))
        if not polys:
            continue
        if box is None:
            xs = [p[0] for pl in polys for p in pl]
            ys = [p[1] for pl in polys for p in pl]
            box = (min(xs), min(ys), max(xs), max(ys))
        if stroke and stroke != "none":
            yield {"kind": "stroke", "name": name, "polys": polys,
                   "box": box, "w": sw}
        if fill and fill != "none":
            # fill-opacity matters as much as the colour: these diagrams tint
            # panels at 0.15-0.2 over a near-white page, which reads as a pale
            # wash, not a solid block. Composite over white before judging.
            a = _num(_attr(tag, "fill-opacity", "1"), 1.0)
            a *= _num(_attr(tag, "opacity", "1"), 1.0)
            lum = a * luminance(fill) + (1.0 - a) * 1.0
            yield {"kind": "fill", "name": name, "polys": polys,
                   "box": box, "lum": lum}


def _seg_hits_box(p, q, box):
    """Does segment p-q intersect the axis-aligned box (interior included)?"""
    x0, y0, x1, y1 = box
    (ax, ay), (bx, by) = p, q
    if max(ax, bx) < x0 or min(ax, bx) > x1 or max(ay, by) < y0 or min(ay, by) > y1:
        return False
    if x0 <= ax <= x1 and y0 <= ay <= y1:
        return True
    if x0 <= bx <= x1 and y0 <= by <= y1:
        return True
    dx, dy = bx - ax, by - ay
    t0, t1 = 0.0, 1.0
    for pnum, qnum in ((-dx, ax - x0), (dx, x1 - ax), (-dy, ay - y0), (dy, y1 - ay)):
        if pnum == 0:
            if qnum < 0:
                return False
            continue
        r = qnum / pnum
        if pnum < 0:
            if r > t1:
                return False
            t0 = max(t0, r)
        else:
            if r < t0:
                return False
            t1 = min(t1, r)
    return t0 <= t1


def text_hits_shape(tbox, shape, text_fill=None):
    """Does a label's box collide with this shape in a way that hurts?

    text_fill lets the caller rule out the deliberate inverse badge — light
    text set on a dark filled shape is a design choice, not a collision.
    """
    x0, y0, x1, y1 = tbox
    inner = (x0 + INSET_X, y0 + INSET_Y, x1 - INSET_X, y1 - INSET_Y)
    if inner[0] >= inner[2] or inner[1] >= inner[3]:
        return False
    sx0, sy0, sx1, sy1 = shape["box"]
    if sx1 < inner[0] or sx0 > inner[2] or sy1 < inner[1] or sy0 > inner[3]:
        return False
    if shape["kind"] == "fill":
        # only a dark/saturated panel makes a label unreadable; light callout
        # boxes deliberately sit behind text throughout these diagrams
        if shape.get("lum", 1.0) > LIGHT_FILL:
            return False
        if text_fill is not None and luminance(text_fill) > LIGHT_FILL:
            return False   # light text on a dark panel: intentional contrast
        return not (sx1 < x0 or sx0 > x1 or sy1 < y0 or sy0 > y1)
    # A stroke is not a centreline: a 6-unit-wide bar reaches 3 units either
    # side of its path, so the test box is inflated by half the stroke width.
    # Missing this let a label sit visibly under a thick rule and pass.
    half = max(shape.get("w", 1.0), 1.0) / 2.0
    grown = (inner[0] - half, inner[1] - half, inner[2] + half, inner[3] + half)
    for pl in shape["polys"]:
        for i in range(len(pl) - 1):
            if _seg_hits_box(pl[i], pl[i + 1], grown):
                return True
    return False
