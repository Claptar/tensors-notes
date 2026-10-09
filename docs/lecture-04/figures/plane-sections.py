"""Рис. 3: the graph of a linear function is a plane through 0; its horizontal sections at heights
1, 2 project onto V as the level lines f = 1, f = 2, and all level lines f = c are parallel
and equally spaced."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _house import (P as P0, arrow, clip_poly_halfplane, dot, line, polygon,  # noqa: E402
                    text, write)

W, H = 640, 340
S, LX, LY = 46, 2.0, 2.8
OX, OY = 320, 175
A, B = -0.2, 0.75         # f(x, y) = A x + B y  (x toward the viewer, y to the right)
LEVELS_V = (-2, -1, 0, 1, 2)
LEVELS_UP = (1, 2)


def P(x, y, z):
    return P0(x, y, z, s=S, ox=OX, oy=OY)


def f(x, y):
    return A * x + B * y


def level_segment(c):
    """Endpoints (x, y) of {A x + B y = c} inside the rectangle |x| <= LX, |y| <= LY."""
    out = []
    for x in (-LX, LX):                    # crossings with the edges x = ±LX
        y = (c - A * x) / B
        if -LY - 1e-9 <= y <= LY + 1e-9:
            out.append((x, y))
    for y in (-LY, LY):                    # crossings with the edges y = ±LY
        x = (c - B * y) / A
        if -LX - 1e-9 <= x <= LX + 1e-9:
            out.append((x, y))
    out = sorted(set((round(x, 9), round(y, 9)) for x, y in out))
    return out[0], out[-1]


body = []
quad = [(LX, -LY), (LX, LY), (-LX, LY), (-LX, -LY)]

# V
body.append(polygon([P(x, y, 0) for x, y in quad], "ink tint-grey"))
cV = P(LX, -LY, 0)
body.append(text(cV[0] - 26, cV[1] + 2, "V", "m"))

# value axis
o = P(0, 0, 0)
body.append(line(o, P(0, 0, -1.2), "thin dash"))

# the plane z = f(x, y): part below V dashed, part above V solid
q3 = [(x, y, f(x, y)) for x, y in quad]
lower = clip_poly_halfplane(q3, lambda p: -p[2])
upper = clip_poly_halfplane(q3, lambda p: p[2])
body.append(polygon([P(*p) for p in lower], "ink red dash"))

# level lines on V, labelled at their front end
for c in LEVELS_V:
    p, q = level_segment(c)
    body.append(line(P(*p, 0), P(*q, 0), "ink red" if c == 0 else "thin red"))
    e = max((p, q), key=lambda e: (e[0], e[1]))          # the end nearer to the viewer / to the right
    pe = P(*e, 0)
    lbl = "−" + str(-c) if c < 0 else str(c)
    if abs(e[0] - LX) < 1e-6:                              # exits through the front edge: label below it
        body.append(text(pe[0], pe[1] + 19, lbl, "t lbl-red small", anchor="middle"))
    else:                                                  # exits through the right edge: label to the right
        body.append(text(pe[0] + 7, pe[1] + 6, lbl, "t lbl-red small"))

body.append(polygon([P(*p) for p in upper], "ink red tint-red"))

# horizontal sections of the plane at heights 1, 2 and their projections onto V
for c in LEVELS_UP:
    p, q = level_segment(c)
    body.append(line(P(*p, c), P(*q, c), "ink red"))
    for e in (p, q):
        body.append(line(P(*e, c), P(*e, 0), "thin dash"))
        body.append(dot(P(*e, c), "dot-red", r=2.5))

body.append(arrow(o, P(0, 0, 3.0)))
top = P(0, 0, 3.0)
body.append(text(top[0] + 9, top[1] + 12, "ℝ", "t"))
body.append(dot(o))

write("plane-sections.svg", W, H, body)
for c in LEVELS_V:
    print(c, level_segment(c))
