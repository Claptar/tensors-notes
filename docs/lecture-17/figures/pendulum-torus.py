"""Рис.: двойной маятник и его конфигурационное пространство — тор S^1 x S^1.

Left: the pendulum, angles phi1, phi2 of the two rods from the vertical.
Right: the torus  ((R + r cos v) cos u, (R + r cos v) sin u, r sin v)  with u = phi1 + U0,
v = phi2; the configuration of the left panel is the red dot, a motion is the red curve.
Silhouette: points where the surface normal is perpendicular to the view direction.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _house import (SVG, Ortho, polyline, dot, text, curve_3d, runs, add, mul,  # noqa: E402
                    dotp, f)

W, H = 640, 290
svg = SVG(W, H)

# ---------------------------------------------------------------- pendulum
phi1, phi2 = math.radians(28), math.radians(58)
O = (115.0, 48.0)
L1, L2 = 105.0, 92.0
B1 = (O[0] + L1 * math.sin(phi1), O[1] + L1 * math.cos(phi1))
B2 = (B1[0] + L2 * math.sin(phi2), B1[1] + L2 * math.cos(phi2))

svg.add(polyline([(55, O[1]), (175, O[1])], "ink"))
for k in range(9):
    x = 60 + 13 * k
    svg.add(polyline([(x, O[1]), (x + 9, O[1] - 9)], "thin"))
for P0, length in ((O, 82), (B1, 72)):
    svg.add(polyline([P0, (P0[0], P0[1] + length)], "thin dash"))
svg.add(polyline([O, B1, B2], "ink"))
svg.add(dot(O, r=2.5))
svg.add(dot(B1, r=5))
svg.add(dot(B2, r=5))


def arc(c, rad, a0, a1, n=30):
    """Arc around c from angle a0 to a1 measured from the downward vertical, toward +x."""
    return [(c[0] + rad * math.sin(a0 + (a1 - a0) * k / n), c[1] + rad * math.cos(a0 + (a1 - a0) * k / n))
            for k in range(n + 1)]


svg.add(polyline(arc(O, 52, 0, phi1), "thin"))
svg.add(polyline(arc(B1, 42, 0, phi2), "thin"))
m1 = arc(O, 66, phi1 / 2, phi1 / 2, 1)[0]
m2 = arc(B1, 56, phi2 / 2, phi2 / 2, 1)[0]
svg.add(text(m1[0] - 6, m1[1] + 6, 'φ<tspan class="sub t" dy="5">1</tspan>'))
svg.add(text(m2[0] - 4, m2[1] + 8, 'φ<tspan class="sub t" dy="5">2</tspan>'))

# ---------------------------------------------------------------- torus
R, r = 2.0, 0.72
view = Ortho(az=-90, el=32, s=56, ox=455, oy=150)
U0 = math.radians(-125)          # where phi1 = 0 sits on the torus (chosen so the dot faces us)


def T(u, v):
    return ((R + r * math.cos(v)) * math.cos(u), (R + r * math.cos(v)) * math.sin(u), r * math.sin(v))


def normal(u, v):
    return (math.cos(v) * math.cos(u), math.cos(v) * math.sin(u), math.sin(v))


def inside(Q):
    return (math.hypot(Q[0], Q[1]) - R) ** 2 + Q[2] ** 2 < r * r


# silhouette: both branches of  A cos v + B sin v = 0, visible parts only
el = math.radians(32)
for branch in (0.0, math.pi):
    pts, flags = [], []
    for k in range(721):
        u = 2 * math.pi * k / 720
        A = dotp((math.cos(u), math.sin(u), 0.0), view.d)        # = cos(el) cos(u - az)
        v = math.atan2(-A, math.sin(el)) + branch
        P = add(T(u, v), mul(0.012, normal(u, v)))
        pts.append(view(P))
        flags.append(view.visible(P, inside))
    for a, b, vis in runs(flags):
        if vis and b - a > 2:
            svg.add(polyline(pts[a:b + 1], "ink"))

# coordinate circles: phi2 = 0 (outer equator) and phi1 = const (a meridian of the tube)
eq = [T(2 * math.pi * k / 360, 0.0) for k in range(361)]
for s_ in curve_3d(view, eq, inside, "thin", "thin dash"):
    svg.add(s_)
um = math.radians(-42)               # a meridian on the front-right
mer = [T(um, 2 * math.pi * k / 240) for k in range(241)]
for s_ in curve_3d(view, mer, inside, "thin", "thin dash"):
    svg.add(s_)

# a motion of the pendulum: a curve (phi1(t), phi2(t)) on the torus, through the marked state
ts = [k / 400 for k in range(401)]
traj = [T(U0 + phi1 + 2.2 * (t - 0.5), phi2 + 0.9 * math.sin(5 * (t - 0.5))) for t in ts]
for s_ in curve_3d(view, traj, inside, "ink red", "ink red dash"):
    svg.add(s_)
Pm = T(U0 + phi1, phi2)
assert view.visible(add(Pm, mul(0.01, normal(U0 + phi1, phi2))), inside)
svg.add(dot(view(Pm), "dot-red", r=4.5))

# arrowheads: the direction in which phi1 (along the big circle) and phi2 (around the tube) grow
for pts in ([T(math.radians(a), 0.0) for a in (-122, -116, -110)],
            [T(um, math.radians(a)) for a in (10, 25, 40)]):
    scr = [view(P) for P in pts]
    svg.add(f'<path class="thin" d="M{f(scr[0][0])},{f(scr[0][1])} L{f(scr[1][0])},{f(scr[1][1])} '
            f'L{f(scr[2][0])},{f(scr[2][1])}" marker-end="url(#arrow)"/>')

# labels: phi1 runs along the big circle, phi2 around the tube
lab1 = view(T(math.radians(-112), -math.pi / 2))      # just below the bottom of the front tube
svg.add(text(lab1[0] - 6, lab1[1] + 26, 'φ<tspan class="sub t" dy="5">1</tspan>'))
lab2 = view(T(um, math.radians(5)))
svg.add(text(lab2[0] - 38, lab2[1] - 8, 'φ<tspan class="sub t" dy="5">2</tspan>'))
svg.add(text(625, 40, 'S<tspan class="sub t" dy="-9">1</tspan><tspan class="t" dy="9"> × </tspan>S<tspan class="sub t" dy="-9">1</tspan>',
             "m", anchor="end"))

svg.save(__file__)
