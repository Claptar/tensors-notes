"""Рис.: стереографическая проекция — карта на сфере без северного полюса.

Unit sphere centred at C = (0,0,1) resting on the plane z = 0; N = (0,0,2) is the north pole.
A point P of the sphere goes to P' = the point where the line NP meets the plane:
    P' = N + s (P - N),  s = 2 / (2 - P_z).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _house import SVG, Ortho, polyline, dot, text, curve_3d, add, subv, mul  # noqa: E402

C, N = (0.0, 0.0, 1.0), (0.0, 0.0, 2.0)
view = Ortho(az=25, el=20, s=78, ox=0, oy=0)
X0, X1, Y0, Y1 = -1.5, 2.8, -2.0, 2.2      # the plane z = 0 drawn as this rectangle
_corners = [(X0, Y0, 0), (X1, Y0, 0), (X1, Y1, 0), (X0, Y1, 0)]
_xs = [view(c)[0] for c in _corners]
_ys = [view(c)[1] for c in _corners] + [view(N)[1] - 40]
W, H = 640, int(max(_ys) - min(_ys) + 20)
view.ox = (W - (max(_xs) + min(_xs))) / 2
view.oy = 10 - min(_ys)


def inside_sphere(Q):
    return (Q[0] - C[0]) ** 2 + (Q[1] - C[1]) ** 2 + (Q[2] - C[2]) ** 2 < 1.0


def on_sphere(z, beta_deg):
    rho = math.sqrt(1 - (z - 1) ** 2)
    b = math.radians(beta_deg)
    return (rho * math.cos(b), rho * math.sin(b), z)


def project(P):
    s = 2 / (2 - P[2])
    return add(N, mul(s, subv(P, N)))


P = on_sphere(0.45, 62)       # lower hemisphere -> lands close to the sphere
Q = on_sphere(1.2, -14)      # upper hemisphere -> lands far away
Pp, Qp = project(P), project(Q)
for name, A, B in (("P", P, Pp), ("Q", Q, Qp)):
    assert abs(B[2]) < 1e-12
    # P, N, P' collinear: cross product of (P-N) and (P'-N) vanishes
    u, v = subv(A, N), subv(B, N)
    cr = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    assert max(abs(c) for c in cr) < 1e-12
    print(name, [round(c, 3) for c in A], "->", [round(c, 3) for c in B])

svg = SVG(W, H)

# plane z = 0
svg.add(polyline([view(c) for c in _corners], "ink tint-grey", closed=True))

# sphere: opaque disc (hides the plane behind it), outline, equator
cx, cy = view(C)
R = view.s
svg.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}" class="ink white"/>')
svg.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}" class="ink tint-grey"/>')
eq = [(math.cos(t), math.sin(t), 1.0) for t in [2 * math.pi * k / 240 for k in range(241)]]
for s_ in curve_3d(view, [(e[0] * 0.999, e[1] * 0.999, e[2]) for e in eq], inside_sphere,
                   cls_vis="thin", cls_hid="thin dash"):
    svg.add(s_)

# rays N -> P -> P' (red) and N -> Q -> Q' (blue); the chord inside the sphere is hidden
for A, B, col in ((Q, Qp, "blue"), (P, Pp, "red")):
    seg = [add(N, mul(k / 200, subv(B, N))) for k in range(201)]
    for s_ in curve_3d(view, seg, inside_sphere, cls_vis=f"ink {col}", cls_hid=f"ink {col} dash"):
        svg.add(s_)

for A, cls in ((N, "dot"), (P, "dot-red"), (Pp, "dot-red"), (Q, "dot-blue"), (Qp, "dot-blue")):
    svg.add(dot(view(A), cls))

nx, ny = view(N)
svg.add(text(nx - 6, ny - 10, "N"))
px, py = view(P)
svg.add(text(px + 10, py + 8, "P", "m lbl-red"))
ppx, ppy = view(Pp)
svg.add(text(ppx + 9, ppy + 18, "P′", "m lbl-red"))
qx, qy = view(Q)
svg.add(text(qx + 9, qy + 21, "Q", "m lbl-blue"))
qpx, qpy = view(Qp)
svg.add(text(qpx + 10, qpy + 16, "Q′", "m lbl-blue"))

svg.save(__file__)
