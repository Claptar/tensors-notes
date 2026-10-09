"""Рис.: кривые через точку p на многообразии и их образы в карте.

Chart coordinates (x, y), p at the origin. Curves gamma_i(t) = a_i t + c_i t^2 in the chart:
gamma_1, gamma_2 share the velocity a = (1, 0.45) (equivalent), gamma_3 has another one.
The left panel shows the same curves on M: M-picture = g(chart), g a smooth bend with
g(0) = 0 and derivative = identity at 0, so tangency at p is preserved.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _house import SVG, polyline, dot, text, arrow, vec_label, f  # noqa: E402

W, H = 640, 290
svg = SVG(W, H)

a = (1.0, 0.45)
curves = [((1.0, 0.45), (0.05, 0.75), "red"),
          ((1.0, 0.45), (-0.15, -0.6), "red"),
          ((0.3, 1.05), (0.55, 0.05), "blue")]
T0, T1 = -1.0, 0.85


def chart_curve(vel, acc, t):
    return (vel[0] * t + acc[0] * t * t, vel[1] * t + acc[1] * t * t)


# ------------------------------------------------------------- right panel: the chart in R^2
CS, CO = 60.0, (492.0, 160.0)          # px per unit, screen position of phi(p)


def C(P):
    return (CO[0] + CS * P[0], CO[1] - CS * P[1])


ax0 = (-1.95, -1.75)
svg.add(arrow(C(ax0), C((2.2, ax0[1]))))
svg.add(arrow(C(ax0), C((ax0[0], 2.0))))
svg.add(text(C((2.2, ax0[1]))[0] - 4, C((2.2, ax0[1]))[1] + 22, "x"))
svg.add(text(C((ax0[0], 2.0))[0] - 18, C((ax0[0], 2.0))[1] + 8, "y"))
svg.add(text(C((2.2, 2.0))[0], C((2.2, 2.0))[1] + 6, 'ℝ<tspan class="sub t" dy="-9">2</tspan>', "t", anchor="end"))

# chart domain phi(U): a rounded square around phi(p)
box = []
for k in range(200):
    s = 2 * math.pi * k / 200
    c, si = math.cos(s), math.sin(s)
    rr = 1.45 / (abs(c) ** 4 + abs(si) ** 4) ** 0.25        # superellipse
    box.append((rr * c, rr * si))
svg.add(polyline([C(P) for P in box], "thin dash tint-grey", closed=True))
svg.add(text(C((1.25, -1.45))[0], C((1.25, -1.45))[1], 'φ<tspan class="t">(</tspan>U<tspan class="t">)</tspan>', "m small"))

ts = [T0 + (T1 - T0) * k / 200 for k in range(201)]
for vel, acc, col in curves:
    svg.add(polyline([C(chart_curve(vel, acc, t)) for t in ts], f"ink {col}"))
# velocities: the columns (x'(0), y'(0))
svg.add(arrow(C((0, 0)), C(a), "red", width=2.2))
svg.add(arrow(C((0, 0)), C(curves[2][0]), "blue", width=2.2))
svg.add(dot(C((0, 0)), "dot", r=4))
svg.add(text(C((0, 0))[0] + 4, C((0, 0))[1] + 24, 'φ<tspan class="t">(</tspan>p<tspan class="t">)</tspan>'))
tip = C(a)
svg.add(vec_label(tip[0] + 6, tip[1] + 6, "v", "red"))
tipb = C(curves[2][0])
svg.add(vec_label(tipb[0] - 26, tipb[1] + 2, "w", "blue"))

# ------------------------------------------------------------- left panel: the manifold
MS, MO = 50.0, (148.0, 152.0)


def g(P):
    """A smooth bend of the plane: identity to first order at 0."""
    x, y = P
    return (x + 0.22 * y * y - 0.08 * x * y, y - 0.18 * x * x + 0.05 * y * y)


def Mp(P):
    q = g(P)
    return (MO[0] + MS * q[0], MO[1] - MS * q[1])


blob = []
for k in range(240):
    s = 2 * math.pi * k / 240
    rr = 2.45 + 0.2 * math.sin(3 * s + 0.6) + 0.1 * math.cos(5 * s)
    blob.append((MO[0] + MS * rr * math.cos(s) * 1.08, MO[1] - MS * rr * math.sin(s) * 0.98))
svg.add(polyline(blob, "ink tint-grey", closed=True))
svg.add(polyline([Mp(P) for P in box], "thin dash", closed=True))
svg.add(text(blob[0][0] - 30, MO[1] + 112, "M"))
ub = Mp((-0.95, 0.95))
svg.add(text(ub[0] - 6, ub[1] + 6, "U", "m small"))

for i, (vel, acc, col) in enumerate(curves):
    svg.add(polyline([Mp(chart_curve(vel, acc, t)) for t in ts], f"ink {col}"))
svg.add(dot(Mp((0, 0)), "dot", r=4))
pp = Mp((0, 0))
svg.add(text(pp[0] + 6, pp[1] + 22, "p"))
for (vel, acc, col), name, dx, dy in zip(curves, ("1", "2", "3"), (6, 6, -26), (-2, 16, -6)):
    e = Mp(chart_curve(vel, acc, T1))
    svg.add(text(e[0] + dx, e[1] + dy, f'γ<tspan class="sub t" dy="5">{name}</tspan>', f"m lbl-{col}"))

# the chart map phi: M -> R^2
s0, s1 = (262.0, 70.0), (370.0, 70.0)
svg.add(f'<path class="ink" d="M{f(s0[0])},{f(s0[1])} Q316,40 {f(s1[0])},{f(s1[1])}" marker-end="url(#arrow)"/>')
svg.add(text(310, 42, "φ"))

svg.save(__file__)
