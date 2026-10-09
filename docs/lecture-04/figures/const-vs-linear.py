"""Рис. 2: the two simplest kinds of surfaces over V: a constant function (horizontal plane, left)
and a linear function (a tilted plane through the origin, right)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _house import P as P0, arrow, clip_poly_halfplane, dot, line, polygon, text, write  # noqa: E402

W, H = 640, 240
S, L = 34, 2.2
A, B = -0.35, 0.4         # right panel: f(x, y) = A x + B y  (x toward the viewer, y to the right)
C = 2.0                   # left panel: f = C


def panel(ox, oy):
    def P(x, y, z):
        return P0(x, y, z, s=S, ox=ox, oy=oy)
    return P


def square(P, z):
    return [P(L, -L, z(L, -L)), P(L, L, z(L, L)), P(-L, L, z(-L, L)), P(-L, -L, z(-L, -L))]


body = []

# ---------------- left: constant function
P = panel(165, 135)
body.append(polygon(square(P, lambda x, y: 0), "ink tint-grey"))
o = P(0, 0, 0)
body.append(line(o, P(0, 0, -0.6), "thin dash"))
body.append(arrow(o, P(0, 0, 2.95)))
body.append(polygon(square(P, lambda x, y: C), "ink red tint-red"))
body.append(dot(P(0, 0, C), "dot-red"))
pc = P(0, 0, C)
body.append(text(pc[0] - 18, pc[1] + 6, "c", "m"))
body.append(dot(o))
body.append(text(o[0] - 18, o[1] + 6, "0", "t"))
cV = P(L, -L, 0)
body.append(text(cV[0] - 24, cV[1] + 2, "V", "m"))

# ---------------- right: linear function, a plane through the origin
P = panel(482, 135)
f = lambda x, y: A * x + B * y   # noqa: E731
body.append(polygon(square(P, lambda x, y: 0), "ink tint-grey"))
o = P(0, 0, 0)
body.append(line(o, P(0, 0, -0.6), "thin dash"))
body.append(arrow(o, P(0, 0, 2.95)))

quad = [(L, -L), (L, L), (-L, L), (-L, -L)]
q3 = [(x, y, f(x, y)) for x, y in quad]
upper = clip_poly_halfplane(q3, lambda p: p[2])
lower = clip_poly_halfplane(q3, lambda p: -p[2])
body.append(polygon([P(*p) for p in lower], "ink red dash tint-red"))
body.append(polygon([P(*p) for p in upper], "ink red tint-red"))
# the line where the tilted plane meets V: f = 0
zero = [p for p in upper if abs(p[2]) < 1e-9]
body.append(line(P(*zero[0]), P(*zero[1]), "ink red"))
body.append(dot(o))
body.append(text(o[0] - 18, o[1] + 6, "0", "t"))
cV = P(L, -L, 0)
body.append(text(cV[0] - 24, cV[1] + 2, "V", "m"))

write("const-vs-linear.svg", W, H, body)
print("zero line of f on V:", zero)
