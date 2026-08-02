"""Diagram + verification helpers for authoring lesson content.

WHY THIS LIVES IN THE REPO. Two earlier versions of this file (kdmlib.py,
mfglib.py) were written in the session scratchpad and wiped mid-session with no
warning, costing a rewritten lesson. Anything reusable belongs here, tracked,
not in the scratchpad. Per-lesson scripts are still throwaway — commit each
lesson the moment its gate passes.

WHAT IT BUYS. The house diagram style is a 560-wide SVG with a plot box, and
the recurring defect across 24 authored courses has been labels landing on the
artwork. `Fig.verify()` runs the SAME geometry the pre-build scanner uses
(drafts/svggeom.py + drafts/ttfwidth.py, real glyph advances) BEFORE the JSON
is written, so a bad label fails at authoring time with a message naming the
label — instead of after the build, when the fix costs a round trip.

Usage sketch:

    from lessonlib import Fig, INK, BLUE, close

    f = Fig(560, 300, title="What the figure shows")
    f.axes(x=(0, 10, "load (kN)"), y=(0, 50, "stress (MPa)"))
    f.curve(lambda x: 4.2 * x, colour=BLUE, width=2.2)
    f.label("worked point", 6.0, 25.2, colour=BLUE, dy=-14)
    svg = f.render()          # verify() runs inside render() and raises on a hit
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svggeom import shapes_in, text_hits_shape, text_box   # noqa: E402
from ttfwidth import metrics                                # noqa: E402

# Current house palette — the convention the two newest courses converged on
# (mfg-processes-3, metrology, both 2026-07-31). machine-design-1 used an older
# variant (#07785C/#8A5A0F/#28527a); do not mix the two inside one course.
INK = "#14181F"     # headings, primary rules, axis lines
GREY = "#5B6672"    # ticks, secondary annotation, construction lines
BLUE = "#3a6ea5"    # first data series
GREEN = "#1f7a5c"   # second data series / "good" region
AMBER = "#c2820f"   # third series / the worked point
RED = "#9c2f2f"     # limits, boundaries, failure
BG = "#ffffff"
PALE = "#eef1f5"    # light panel fill

FONT = 'ui-sans-serif,system-ui,sans-serif'


def close(a, b, rel=5e-6):
    """Relative comparison for asserts.

    Hand-rounding a constant into an assert and missing the tolerance cost
    roughly one extra round trip per lesson over 18 lessons. Use this instead
    of writing the printed value back as an exact literal.
    """
    return abs(a - b) <= rel * max(1.0, abs(a), abs(b))


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


class Fig:
    """A 560-unit-wide lesson diagram with author-time collision checking."""

    def __init__(self, w=560, h=300, title=None, aria="",
                 box=(90, 62, 490, 244)):
        self.w, self.h, self.aria = w, h, aria
        self.px0, self.py0, self.px1, self.py1 = box     # plot rectangle
        self.parts = []
        self.texts = []          # (x, y, anchor, size, weight, content, fill)
        self.xr = self.yr = None
        self.parts.append(
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="{BG}"/>')
        if title:
            self.text(16, 22, title, size=12, weight="700", colour=INK)

    # ---------- raw emitters ----------
    def raw(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=11, weight="400", colour=INK, anchor="start"):
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        wt = f' font-weight="{weight}"' if weight != "400" else ""
        self.parts.append(
            f'<text x="{x}" y="{y}"{a} fill="{colour}" '
            f'font-size="{size}"{wt}>{_esc(s)}</text>')
        self.texts.append((float(x), float(y), anchor, float(size),
                           weight, str(s), colour))

    def line(self, x1, y1, x2, y2, colour=INK, width=1.3, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{colour}" stroke-width="{width}"{d}/>')

    def rect(self, x, y, w, h, fill="none", stroke=None, width=1.4,
             opacity=None):
        s = f' stroke="{stroke}" stroke-width="{width}"' if stroke else ""
        o = f' fill-opacity="{opacity}"' if opacity is not None else ""
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
            f'height="{h:.1f}" fill="{fill}"{o}{s}/>')

    def circle(self, x, y, r, fill=INK, stroke=None, width=1.4):
        s = f' stroke="{stroke}" stroke-width="{width}"' if stroke else ""
        self.parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{s}/>')

    def polyline(self, pts, colour=BLUE, width=2.2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.parts.append(
            f'<polyline points="{p}" fill="none" stroke="{colour}" '
            f'stroke-width="{width}"{d}/>')

    # ---------- data-space mapping ----------
    def axes(self, x, y, xticks=None, yticks=None):
        """x, y are (lo, hi, caption). Sets the data->screen mapping."""
        self.xr, self.yr = (x[0], x[1]), (y[0], y[1])
        self.line(self.px0, self.py1, self.px1, self.py1, INK, 1.5)
        self.line(self.px0, self.py1, self.px0, self.py0, INK, 1.5)
        self.text((self.px0 + self.px1) / 2, self.py1 + 32, x[2], size=12,
                  anchor="middle")
        self.parts.append(
            f'<text x="26" y="{(self.py0+self.py1)/2:.0f}" font-size="12" '
            f'fill="{INK}" transform="rotate(-90 26 '
            f'{(self.py0+self.py1)/2:.0f})" text-anchor="middle">'
            f'{_esc(y[2])}</text>')
        for v in (xticks or []):
            sx = self.sx(v)
            self.line(sx, self.py1, sx, self.py1 + 4, GREY, 1)
            self.text(sx, self.py1 + 16, _fmt(v), size=11, colour=GREY,
                      anchor="middle")
        for v in (yticks or []):
            sy = self.sy(v)
            self.line(self.px0 - 4, sy, self.px0, sy, GREY, 1)
            self.text(self.px0 - 8, sy + 4, _fmt(v), size=11, colour=GREY,
                      anchor="end")

    def sx(self, v):
        lo, hi = self.xr
        return self.px0 + (v - lo) / (hi - lo) * (self.px1 - self.px0)

    def sy(self, v):
        lo, hi = self.yr
        return self.py1 - (v - lo) / (hi - lo) * (self.py1 - self.py0)

    def curve(self, fn, lo=None, hi=None, n=120, colour=BLUE, width=2.2,
              dash=None):
        lo = self.xr[0] if lo is None else lo
        hi = self.xr[1] if hi is None else hi
        pts = []
        for i in range(n + 1):
            v = lo + (hi - lo) * i / n
            pts.append((self.sx(v), self.sy(fn(v))))
        self.polyline(pts, colour, width, dash)
        return pts

    def point(self, xv, yv, colour=AMBER, r=4.5):
        self.circle(self.sx(xv), self.sy(yv), r, fill=colour)

    def label(self, s, xv=None, yv=None, at=None, colour=INK, size=11,
              weight="400", anchor="start", dx=0, dy=0):
        """Place a label either in data space (xv, yv) or screen space (at)."""
        if at is not None:
            x, y = at
        else:
            x, y = self.sx(xv), self.sy(yv)
        self.text(x + dx, y + dy, s, size=size, weight=weight, colour=colour,
                  anchor=anchor)

    # ---------- the gate ----------
    def verify(self):
        """Raise if any label lands on the artwork or leaves the viewBox.

        Runs the same geometry as drafts/qa_content.py, so passing here means
        passing there — the point being to fail now, with the label named,
        rather than after a build.
        """
        body = "".join(self.parts)
        fig = f'<figure><svg viewBox="0 0 {self.w} {self.h}">{body}</svg></figure>'
        shapes = list(shapes_in(fig))
        m = metrics()
        problems = []
        for x, y, anchor, size, weight, content, fill in self.texts:
            if not content.strip():
                continue
            wdt = m.width(content, size, weight)
            x0 = (x - wdt / 2 if anchor == "middle"
                  else x - wdt if anchor == "end" else x)
            if x0 < 0 or x0 + wdt > self.w:
                problems.append(
                    f"overflows viewBox [{x0:.0f},{x0+wdt:.0f}] — {content!r}")
                continue
            tb = text_box(x, y, anchor, size, weight, content)
            for sh in shapes:
                if text_hits_shape(tb, sh, fill):
                    problems.append(
                        f"lands on <{sh['name']}> {sh['kind']} — {content!r}")
                    break
        for i in range(len(self.texts)):
            for j in range(i + 1, len(self.texts)):
                a, b = self.texts[i], self.texts[j]
                ba = text_box(a[0], a[1], a[2], a[3], a[4], a[5])
                bb = text_box(b[0], b[1], b[2], b[3], b[4], b[5])
                if (ba[0] < bb[2] and bb[0] < ba[2]
                        and ba[1] < bb[3] and bb[1] < ba[3]):
                    problems.append(
                        f"collides — {a[5]!r} vs {b[5]!r}")
        if problems:
            raise AssertionError(
                "figure has %d label problem(s):\n  " % len(problems)
                + "\n  ".join(problems))

    def render(self, check=True):
        if check:
            self.verify()
        body = "".join(self.parts)
        return (f'<svg viewBox="0 0 {self.w} {self.h}" '
                f'xmlns="http://www.w3.org/2000/svg" font-family="{FONT}" '
                f'role="img" aria-label="{_esc(self.aria)}">{body}</svg>')

    def figure(self, caption):
        return (f'<figure class="lesson-diagram">{self.render()}'
                f'<figcaption>{caption}</figcaption></figure>')


def _fmt(v):
    return f"{v:g}"


def quiz_check(quiz):
    """The 3-solve + 8-MC contract. Counting these before running was the
    single commonest failure across 18 lessons — 9 MC slips through the eye."""
    solves = [q for q in quiz if q["type"] == "solve"]
    mcs = [q for q in quiz if q["type"] == "mc"]
    assert len(solves) == 3, f"need 3 solve, have {len(solves)}"
    assert len(mcs) == 8, f"need 8 mc, have {len(mcs)}"
    for i, q in enumerate(mcs):
        assert len(q["choices"]) == 4, f"mc[{i}] has {len(q['choices'])} choices"
        assert isinstance(q["answer"], int) and 0 <= q["answer"] < 4, \
            f"mc[{i}] answer out of range"
    return True


def write_lesson(path, lid, lesson):
    """Merge one lesson into a content JSON, creating the file if needed."""
    import json
    p = pathlib.Path(path)
    data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    for k in ("lecture", "foundations", "quiz", "kuwait", "recap"):
        assert k in lesson, f"lesson missing {k!r}"
    quiz_check(lesson["quiz"])
    data[str(lid)] = lesson
    p.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n",
                 encoding="utf-8")
    return len(data)


# ---------------------------------------------------------------------------
# Mechanics primitives (added 2026-08-02 for STA 103's figures).
#
# A statics diagram is mostly ARROWS and SUPPORTS, and Fig had neither — every
# course was about to hand-roll them. They live here rather than in a per-course
# scratchpad module for the reason at the top of this file: scratchpad libraries
# have been wiped twice. All of them are built from primitives Fig already
# records, so Fig.verify() still sees every label they place.
# ---------------------------------------------------------------------------

def arrow(f, x1, y1, x2, y2, colour=BLUE, width=2.2, head=9.0, dash=None):
    """A force arrow from (x1,y1) to (x2,y2), head at the far end."""
    f.line(x1, y1, x2, y2, colour, width, dash)
    ang = math.atan2(y2 - y1, x2 - x1)
    for s in (+1, -1):
        a = ang + s * math.radians(155)
        f.line(x2, y2, x2 + head * math.cos(a), y2 + head * math.sin(a),
               colour, width)


def arrow_polar(f, x, y, mag, deg, colour=BLUE, width=2.2, head=9.0):
    """Arrow from (x,y), `deg` anticlockwise from +x. Screen y runs DOWN, so
    the sine is negated and the angle reads the way a student draws it.
    Returns the tip, so a label can be hung off it."""
    a = math.radians(deg)
    x2, y2 = x + mag * math.cos(a), y - mag * math.sin(a)
    arrow(f, x, y, x2, y2, colour, width, head)
    return x2, y2


def ground(f, x0, x1, y, n=9, colour=GREY):
    """Hatched ground line."""
    f.line(x0, y, x1, y, INK, 1.6)
    step = (x1 - x0) / float(n)
    for i in range(n):
        gx = x0 + i * step
        f.line(gx, y + 1, gx - 7, y + 9, colour, 1.0)


def pin_support(f, x, y, size=15, colour=INK):
    """Pin: apex on the body, two reaction components."""
    f.raw(f'<polygon points="{x:.1f},{y:.1f} {x-size:.1f},{y+size*1.5:.1f} '
          f'{x+size:.1f},{y+size*1.5:.1f}" fill="none" stroke="{colour}" '
          f'stroke-width="1.6"/>')
    ground(f, x - size - 8, x + size + 8, y + size * 1.5, 7)


def roller_support(f, x, y, size=13, colour=INK):
    """Roller: one reaction, normal to the surface."""
    f.raw(f'<polygon points="{x:.1f},{y:.1f} {x-size:.1f},{y+size*1.4:.1f} '
          f'{x+size:.1f},{y+size*1.4:.1f}" fill="none" stroke="{colour}" '
          f'stroke-width="1.6"/>')
    for dx in (-size * 0.55, size * 0.55):
        f.circle(x + dx, y + size * 1.4 + 4, 4, fill="none", stroke=colour,
                 width=1.4)
    ground(f, x - size - 8, x + size + 8, y + size * 1.4 + 8, 7)


def fixed_support(f, x, y, h=34, colour=INK, side="left"):
    """Wall: two components plus a moment."""
    f.line(x, y - h / 2, x, y + h / 2, colour, 2.2)
    s = -1 if side == "left" else 1
    for i in range(6):
        gy = y - h / 2 + i * (h / 5.0)
        f.line(x, gy, x + s * 9, gy + 8, GREY, 1.0)


def dim(f, x1, y1, x2, label, colour=GREY, size=11, off=13):
    """Horizontal dimension line with end ticks and a centred label."""
    f.line(x1, y1, x2, y1, colour, 1.0)
    for px in (x1, x2):
        f.line(px, y1 - 4, px, y1 + 4, colour, 1.0)
    f.text((x1 + x2) / 2.0, y1 - off, label, size=size, colour=colour,
           anchor="middle")
