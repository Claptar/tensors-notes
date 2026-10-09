"""Рис.: полярные координаты на плоскости и базис, который карта задаёт в точках p и q.

The coordinate lines of the chart (r, phi) are circles r = const and rays phi = const.
The basis vectors at a point are the velocities of the coordinate lines through it:
    e_r   = d/dt (r + t, phi)  = (cos phi, sin phi),
    e_phi = d/dt (r, phi + t)  = (-r sin phi, r cos phi)       (Cartesian components).
Drawn at true scale: |e_r| = 1, |e_phi| = r. Blue: the Cartesian basis e_x, e_y, the same at
every point.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _house import SVG, polyline, dot, text, arrow, vec_label  # noqa: E402

W, H = 640, 420
svg = SVG(W, H)
S, O = 47.0, (300.0, 240.0)


def P(x, y):
    return (O[0] + S * x, O[1] - S * y)


def pol(r, a):
    return (r * math.cos(a), r * math.sin(a))


rp, ap = 3.0, 1.0                      # the point p of the lecture: r_p = 3, phi_p = 1
rq, aq = 2.0, 1.0 + math.pi / 2        # a second point q

# coordinate lines: circles and rays (the two through p drawn heavier)
for r in (1, 2, 3):
    pts = [P(*pol(r, 2 * math.pi * k / 240)) for k in range(241)]
    svg.add(polyline(pts, "ink" if r == rp else "thin"))
for k in range(8):
    a = ap + k * math.pi / 4
    svg.add(polyline([P(0, 0), P(*pol(3.55, a))], "ink" if k == 0 else "thin"))

# Cartesian axes
svg.add(arrow(P(-3.7, 0), P(3.9, 0)))
svg.add(arrow(P(0, -3.6), P(0, 4.3)))
svg.add(text(*P(3.82, -0.42), "x"))
svg.add(text(*P(0.14, 4.12), "y"))
for r in (1, 2, 3):
    x, y = P(r, 0)
    svg.add(text(x + 3, y + 17, str(r), "t small"))


def basis(r, a, labels):
    p = pol(r, a)
    er = (math.cos(a), math.sin(a))
    ef = (-r * math.sin(a), r * math.cos(a))
    for v, col in (((1, 0), "blue"), ((0, 1), "blue"), (er, "red"), (ef, "red")):
        svg.add(arrow(P(*p), P(p[0] + v[0], p[1] + v[1]), col, width=2.0))
    svg.add(dot(P(*p), "dot", r=4))
    if labels:
        ex, ey = P(p[0] + er[0], p[1] + er[1])
        svg.add(vec_label(ex + 6, ey + 4, "e", "red", "r"))
        fx, fy = P(p[0] + ef[0], p[1] + ef[1])
        svg.add(vec_label(fx - 2, fy - 8, "e", "red", "φ"))
        bx, by = P(p[0] + 1, p[1])
        svg.add(vec_label(bx + 6, by + 14, "e", "blue", "x"))
        cx, cy = P(p[0], p[1] + 1)
        svg.add(vec_label(cx - 30, cy + 4, "e", "blue", "y"))
    return p


p = basis(rp, ap, True)
q = basis(rq, aq, False)
x, y = P(*p)
svg.add(text(x + 8, y + 22, "p"))
x, y = P(*q)
svg.add(text(x + 6, y + 22, "q"))

svg.save(__file__)
