#!/usr/bin/env python3
"""figlib — design-side library for pictorial figure PAIRS (sketch + abstraction).

Spec: design-previews/figures/FIGURES.md. Computed diagrams stay content-side
(drafts/lessonlib.py); this library exists so every design-side figure is
geometry-computed, palette-token-true, and label-collision-checked BEFORE it
ever reaches a page — the same authoring-time discipline lessonlib gives the
content session.

Label-width honesty: widths are estimated from per-class character advances
(serif italic ~0.50em average, wider caps) with a deliberate +15% safety
margin, NOT measured from font files. That is conservative enough for the
few short labels a figure carries; anything estimate-tight must be widened,
not argued with. The browser remains the final visual check.
"""
from pathlib import Path

# Palette tokens — MUST mirror :root in assets/nx/nexus.css (never invent).
TOKENS = {
    "ink":    "#20325A",
    "soft":   "#44506B",
    "muted":  "#6E7688",
    "line":   "#DBD7CF",
    "sunken": "#F6F4F1",
    "accent": "#2D5397",
    "gold":   "#CBA85F",
    "bad":    "#B3382C",
    "paper":  "#FDFCFB",
}

SERIF = "'Source Serif 4',Georgia,serif"
SANS = "'Source Sans 3',Arial,sans-serif"


def _est_width(text, size, caps=False):
    """Conservative width estimate: 0.50em/char serif, 0.62em for caps/sans,
    +15% safety. Honest limitation documented in the module docstring."""
    per = 0.62 if caps else 0.50
    return len(text) * size * per * 1.15


class Figure:
    """One SVG figure. Collects elements + label boxes, then check() + svg()."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.parts = []
        self.labels = []          # (name, x0, y0, x1, y1)

    # ---------------------------------------------------------------- parts
    def raw(self, s):
        self.parts.append(s)

    def poly(self, pts, fill="none", stroke="ink", sw=2, close=True, dash=None):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + ("Z" if close else "")
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<path d="{d}" fill="{TOKENS.get(fill, fill)}" '
            f'stroke="{TOKENS.get(stroke, stroke)}" stroke-width="{sw}" '
            f'stroke-linejoin="round"{dd}/>')

    def line(self, x1, y1, x2, y2, stroke="ink", sw=1.5, dash=None):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{TOKENS.get(stroke, stroke)}" stroke-width="{sw}" '
            f'stroke-linecap="round"{dd}/>')

    def arrow(self, x1, y1, x2, y2, stroke="accent", sw=2.5, head=11):
        """Shaft + filled triangular head, all math here — no marker defs, so
        every arrow renders identically in every consumer."""
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
        self.line(x1, y1, bx, by, stroke=stroke, sw=sw)
        s = head * 0.42
        p1 = (x2, y2)
        p2 = (bx - s * math.sin(ang), by + s * math.cos(ang))
        p3 = (bx + s * math.sin(ang), by - s * math.cos(ang))
        self.poly([p1, p2, p3], fill=stroke, stroke=stroke, sw=1)

    def arc(self, cx, cy, r, a0, a1, stroke="gold", sw=2):
        """Circular arc from angle a0 to a1 (radians, SVG y-down)."""
        import math
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1_, y1_ = cx + r * math.cos(a1), cy + r * math.sin(a1)
        large = 1 if abs(a1 - a0) > 3.14159 else 0
        sweep = 1 if a1 > a0 else 0
        self.parts.append(
            f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} '
            f'{x1_:.1f},{y1_:.1f}" fill="none" '
            f'stroke="{TOKENS.get(stroke, stroke)}" stroke-width="{sw}"/>')

    def hatch(self, x0, y, x1, n=None, drop=9, stroke="muted", sw=1.2):
        """Ground/anchor hatching: short 45° ticks under the line y."""
        n = n or max(3, int((x1 - x0) / 14))
        step = (x1 - x0) / n
        for i in range(n + 1):
            x = x0 + i * step
            self.line(x, y, x - drop * 0.7, y + drop, stroke=stroke, sw=sw)

    def speed_lines(self, x, y, ang, n=3, ln=16, gap=7, stroke="muted", sw=1.5):
        """Motion cue: n short parallel lines trailing the body at angle ang."""
        import math
        dx, dy = math.cos(ang), math.sin(ang)
        px, py = -dy, dx
        for i in range(n):
            ox, oy = x + px * gap * (i - (n - 1) / 2), y + py * gap * (i - (n - 1) / 2)
            self.line(ox, oy, ox - ln * dx, oy - ln * dy, stroke=stroke, sw=sw)

    def label(self, text, x, y, size=13, fill="ink", anchor="middle",
              italic=True, caps=False, font=None):
        """Text + recorded bbox for collision checking. y = baseline."""
        fam = font or (SERIF if italic else SANS)
        style = "font-style:italic;" if italic else ""
        tt = ("letter-spacing:.14em;text-transform:uppercase;font-weight:600;"
              if caps else "")
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
            f'style="font-family:{fam};font-size:{size}px;{style}{tt}" '
            f'fill="{TOKENS.get(fill, fill)}">{text}</text>')
        w = _est_width(text, size, caps=caps)
        x0 = x - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
        self.labels.append((text, x0, y - size, x0 + w, y + size * 0.25))

    # ---------------------------------------------------------------- gates
    def check(self):
        """Assert every label inside the viewBox and no label-pair overlap."""
        errs = []
        for t, x0, y0, x1, y1 in self.labels:
            if x0 < 0 or y0 < 0 or x1 > self.w or y1 > self.h:
                errs.append(f"label {t!r} outside viewBox "
                            f"({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")
        for i in range(len(self.labels)):
            for j in range(i + 1, len(self.labels)):
                a, b = self.labels[i], self.labels[j]
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    errs.append(f"labels {a[0]!r} and {b[0]!r} collide")
        if errs:
            raise AssertionError("figlib check failed:\n  " + "\n  ".join(errs))
        return True

    def svg(self, title=""):
        self.check()
        t = f"<title>{title}</title>" if title else ""
        return (f'<svg viewBox="0 0 {self.w} {self.h}" '
                f'xmlns="http://www.w3.org/2000/svg" role="img">{t}'
                + "".join(self.parts) + "</svg>")

    def write(self, path, title=""):
        Path(path).write_text(self.svg(title), encoding="utf-8")
        return path


def _selftest():
    f = Figure(400, 200)
    f.poly([(20, 180), (380, 180), (380, 160)], fill="sunken")
    f.arrow(200, 60, 200, 140)
    f.arc(60, 180, 30, -1.0, 0.0)
    f.hatch(20, 180, 380)
    f.speed_lines(300, 60, 0.5)
    f.label("m", 200, 50)
    f.label("θ", 95, 172)
    assert f.check()
    assert "<svg" in f.svg()
    # collision must be caught
    g = Figure(100, 50)
    g.label("aaa", 50, 25)
    g.label("bbb", 52, 27)
    try:
        g.check()
    except AssertionError:
        print("figlib selftest OK")
        return
    raise SystemExit("collision not caught")


if __name__ == "__main__":
    _selftest()
