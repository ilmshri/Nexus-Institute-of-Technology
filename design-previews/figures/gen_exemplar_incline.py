#!/usr/bin/env python3
"""Exemplar pictorial pair: crate held on a rough incline + its free-body
diagram. Spec: FIGURES.md. Every coordinate is trig-computed from THETA; the
figlib check() gates labels before the SVG is written.

Conventions exercised (studied 2026-08-03 — NASA BGA secondlaw/forces, MIT
OCW 8.01SC week2ps1; see FIGURES.md "Studied sources"): pale-fill pictorial
incline with hatched ground, body symbol on the body, gravity arrow at the
panel edge, angle arc at the real geometry; FBD isolates the body, forces
from their application points, tilted unit-vector axes, θ re-marked where it
enters the decomposition. Original artwork — nothing copied or traced.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from figlib import Figure, TOKENS  # noqa: E402

THETA = math.radians(28)
W, H = 1280, 620
PANEL_W = 590
GAP = W - 2 * PANEL_W  # 100

f = Figure(W, H)

# ---------------------------------------------------------------- panel titles
f.label("PHYSICAL SITUATION", PANEL_W / 2, 40, size=15, italic=False,
        caps=True, fill="muted")
f.label("FREE-BODY DIAGRAM", PANEL_W + GAP + PANEL_W / 2, 40, size=15,
        italic=False, caps=True, fill="muted")

# ================================================================ SKETCH panel
# Incline: horizontal base, hypotenuse rising right->left (high side left),
# angle arc at the RIGHT base corner (OCW orientation).
bx0, bx1, by = 60, 540, 520          # base extent and ground line
apex_x = bx0
apex_y = by - (bx1 - bx0) * math.tan(THETA)
f.poly([(bx0, by), (bx1, by), (apex_x, apex_y)], fill="sunken", stroke="ink", sw=2)
f.hatch(bx0 - 10, by, bx1 + 10)

# Angle arc + theta at the right corner, between base and hypotenuse.
f.arc(bx1, by, 64, math.pi, math.pi + THETA, stroke="gold", sw=2.5)
f.label("θ", bx1 - 88, by - 16, size=17, fill="soft")

# Crate: square sitting on the hypotenuse, mid-slope. Slope dir (downhill,
# left->right along surface): u = (cosT, sinT) in SVG y-down coords.
ct, st = math.cos(THETA), math.sin(THETA)
# point on surface 45% down from apex
sx = apex_x + (bx1 - apex_x) * 0.45
sy = apex_y + (by - apex_y) * 0.45
side = 86
# crate corners: along-slope u=(ct,st), surface normal n=(st,-ct)
u, n = (ct, st), (st, -ct)
c0 = (sx - side / 2 * u[0], sy - side / 2 * u[1])
c1 = (sx + side / 2 * u[0], sy + side / 2 * u[1])
c2 = (c1[0] + side * n[0], c1[1] + side * n[1])
c3 = (c0[0] + side * n[0], c0[1] + side * n[1])
f.poly([c0, c1, c2, c3], fill="paper", stroke="ink", sw=2.5)
ccx, ccy = sx + side / 2 * n[0], sy + side / 2 * n[1]  # crate centre
f.label("m", ccx, ccy + 6, size=17)

# Motion tendency cue: speed-lines trailing up-slope of the crate (it tends
# to slide DOWN-slope), drawn just above the surface beside the crate.
tail_x = c0[0] - 26 * u[0] + 16 * n[0]
tail_y = c0[1] - 26 * u[1] + 16 * n[1]
f.speed_lines(tail_x, tail_y, math.atan2(u[1], u[0]), n=3, ln=18, gap=9)

# Gravity arrow at panel edge.
f.arrow(70, 120, 70, 200, stroke="soft", sw=2.5)
f.label("g", 70, 110, size=15, fill="soft")

# ==================================================================== FBD panel
ox = PANEL_W + GAP + 285   # FBD body centre
oy = 300
bs = 74                    # body half-size drawn as a tilted square
u, n = (ct, st), (st, -ct)
p = [(ox - bs * u[0] - 0 * n[0], oy - bs * u[1]),
     (ox + bs * u[0], oy + bs * u[1])]
q0 = (ox - bs * u[0] - bs * 0.5 * n[0], oy - bs * u[1] - bs * 0.5 * n[1])
q1 = (ox + bs * u[0] - bs * 0.5 * n[0], oy + bs * u[1] - bs * 0.5 * n[1])
q2 = (ox + bs * u[0] + bs * 0.5 * n[0], oy + bs * u[1] + bs * 0.5 * n[1])
q3 = (ox - bs * u[0] + bs * 0.5 * n[0], oy - bs * u[1] + bs * 0.5 * n[1])
f.poly([q0, q1, q2, q3], fill="paper", stroke="ink", sw=2.5)
# dashed construction line showing the (removed) incline surface
f.line(ox - 190 * u[0] - bs * 0.5 * n[0], oy - 190 * u[1] - bs * 0.5 * n[1],
       ox + 190 * u[0] - bs * 0.5 * n[0], oy + 190 * u[1] - bs * 0.5 * n[1],
       stroke="line", sw=1.5, dash="6 6")

# Forces — concurrent particle-FBD register (8.01 style): every force vector
# radiates from the body centre; lengths give magnitude feel, not scale.
L = 132
# N: along +n (away from the removed surface)
f.arrow(ox, oy, ox + L * n[0], oy + L * n[1], stroke="accent")
f.label("N", ox + (L + 24) * n[0], oy + (L + 24) * n[1] + 5, size=16, fill="accent")
# W = mg: straight down
f.arrow(ox, oy, ox, oy + L + 18, stroke="accent")
f.label("mg", ox, oy + L + 44, size=16, fill="accent")
# friction f_s: up-slope (opposes the sliding tendency)
f.arrow(ox, oy, ox - 0.85 * L * u[0], oy - 0.85 * L * u[1], stroke="accent")
f.label("f", ox - 0.85 * L * u[0] - 26 * u[0], oy - 0.85 * L * u[1] - 26 * u[1] - 6,
        size=16, fill="accent")
f.label("s", ox - 0.85 * L * u[0] - 26 * u[0] + 11,
        oy - 0.85 * L * u[1] - 26 * u[1], size=11, fill="accent")

# theta re-marked between mg and the inward surface normal (-n direction):
# angle from +y (down) to -n is THETA.
a_down = math.pi / 2
a_negn = math.atan2(-n[1], -n[0])
f.arc(ox, oy, 66, a_down, a_negn, stroke="gold", sw=2.5)
f.label("θ", ox + 30, oy + 96, size=15, fill="soft")

# tilted unit axes in the panel's top-right free corner
ax, ay = PANEL_W + GAP + 500, 120
f.arrow(ax, ay, ax + 56 * u[0], ay + 56 * u[1], stroke="soft", sw=2)
f.arrow(ax, ay, ax + 56 * n[0], ay + 56 * n[1], stroke="soft", sw=2)
f.label("x̂", ax + 76 * u[0], ay + 76 * u[1] + 5, size=13, fill="soft")
f.label("ŷ", ax + 78 * n[0], ay + 78 * n[1] + 5, size=13, fill="soft")

out = Path(__file__).parent / "exemplar-incline-pair.svg"
f.write(out, title="Crate on a rough incline — physical sketch and free-body diagram")
print(f"wrote {out} — labels: {len(f.labels)}, check passed")
