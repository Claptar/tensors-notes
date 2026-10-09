"""Рис. 4: a linear form on the plane drawn inside V itself — the "stack" of parallel, equally spaced
level lines f = c, and the construction from the lecture: a' and b' both have f = 1, so
v = a' - b' has f(v) = 0 and lies on the line f = 0; a' + v again has f = 1."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _house import arrow, clip_line, dot, line, over_arrow, text, write  # noqa: E402

W, H = 640, 350
SC = 50                       # px per unit
OX, OY = 300, 185             # SVG position of the zero vector
RECT = (-5.6, -3.1, 6.4, 3.3)  # visible region in math coordinates (umin, wmin, umax, wmax)


def X(p):
    return (OX + SC * p[0], OY - SC * p[1])


def f(p):                      # the linear form: f(u, w) = (u - 0.3 w) / 1.5
    return (p[0] - 0.3 * p[1]) / 1.5


D = (0.3, 1.0)                 # direction of the level lines (f(D) = 0)
body = []

# level lines f = c
for c in range(-3, 4):
    seg = clip_line((1.5 * c, 0.0), D, RECT)
    p, q = seg
    body.append(line(X(p), X(q), "ink red" if c == 0 else "thin red"))
    top = X(q if q[1] > p[1] else p)
    lbl = "−" + str(-c) if c < 0 else str(c)
    body.append(text(top[0] + 6, top[1] + 14, lbl, "t lbl-red small"))

# the construction
a1 = (1.5 + 0.3 * 1.4, 1.4)    # a' : f(a') = 1
b1 = (1.5 + 0.3 * 0.2, 0.2)    # b' : f(b') = 1, not collinear with a'
v = (a1[0] - b1[0], a1[1] - b1[1])
av = (a1[0] + v[0], a1[1] + v[1])
for name, p in (("a'", a1), ("b'", b1), ("v", v), ("a'+v", av)):
    print(f"{name:5s} = ({p[0]:.3f}, {p[1]:.3f}),  f = {f(p):.6f}")

O = (0.0, 0.0)
body.append(arrow(X(O), X(a1)))
body.append(arrow(X(O), X(b1)))
body.append(arrow(X(b1), X(a1), color="blue", dash=True))
body.append(arrow(X(O), X(v), color="blue"))
body.append(dot(X(O)))
body.append(dot(X(av), "dot-blue"))

# labels
pa = X(a1)
body.append(text(pa[0] + 8, pa[1] + 2, "a′", "m"))
body.append(over_arrow(pa[0] + 8, pa[1] + 2, 9))
pb = X(b1)
body.append(text(pb[0] + 9, pb[1] + 20, "b′", "m"))
body.append(over_arrow(pb[0] + 9, pb[1] + 20, 9))
pv = X(v)
body.append(text(pv[0] - 26, pv[1] + 6, "v", "m lbl-blue"))
body.append(over_arrow(pv[0] - 26, pv[1] + 6, 9, "blue"))
pav = X(av)
body.append(text(pav[0] + 10, pav[1] + 6, "a′ + v", "m lbl-blue"))
body.append(over_arrow(pav[0] + 10, pav[1] + 6, 9, "blue"))
body.append(over_arrow(pav[0] + 10 + 32, pav[1] + 6, 9, "blue"))
po = X(O)
body.append(text(po[0] - 22, po[1] + 20, "0", "t"))
body.append(over_arrow(po[0] - 22, po[1] + 20, 9))

write("level-lines.svg", W, H, body)
