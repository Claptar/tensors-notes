"""Рис. 1. Два набора из трёх геометрических векторов в пространстве.

Слева — три попарно перпендикулярных вектора (вдоль x, y, z): ни один не выражается через два других.
Справа — три вектора в одной плоскости: a3 = a1 + a2 (красный), штрихи достраивают параллелограмм.
Фронтальная диметрия (figures.md): y вправо, z вверх, x к зрителю, вниз-влево под 45°, сжатие 1/2.
"""

from _house import P, arrow, dot, fmt, line, polygon, vec, write

W, H = 640, 250
S = 90

# ---- left panel: three mutually perpendicular vectors
OL = dict(s=S, ox=165, oy=160)
o = P(0, 0, 0, **OL)
a1 = P(2.0, 0, 0, **OL)       # toward the viewer
a2 = P(0, 1.35, 0, **OL)      # to the right
a3 = P(0, 0, 1.25, **OL)      # up

body = []
body += [arrow(o, a1), arrow(o, a2), arrow(o, a3), dot(o)]
body.append(vec(a1[0] - 26, a1[1] + 6, "a", "1"))
body.append(vec(a2[0] - 2, a2[1] + 24, "a", "2"))
body.append(vec(a3[0] + 10, a3[1] + 8, "a", "3"))

# ---- right panel: three vectors in one plane; the plane is spanned by u (to the right) and v (up, leaning toward
# the viewer), so that it is seen nearly face-on and the parallelogram stays readable
OR = dict(s=S, ox=400, oy=200)
u = (0.0, 1.0, 0.0)
v = (0.7, 0.0, 1.0)


def plane_pt(p, q):
    """Point p*u + q*v of the plane, projected."""
    return P(p * u[0] + q * v[0], p * u[1] + q * v[1], p * u[2] + q * v[2], **OR)


corners = [plane_pt(-0.35, -0.3), plane_pt(2.15, -0.3), plane_pt(2.15, 1.75), plane_pt(-0.35, 1.75)]
body.append(polygon(corners, "thin tint-grey"))

c1, c2 = (1.35, 0.2), (0.25, 1.15)                  # a1, a2 in plane coordinates
c3 = (c1[0] + c2[0], c1[1] + c2[1])               # a3 = a1 + a2
O2 = plane_pt(0, 0)
A1, A2, A3 = plane_pt(*c1), plane_pt(*c2), plane_pt(*c3)
body += [line(A1, A3, "ink dash"), line(A2, A3, "ink dash")]
body += [arrow(O2, A1), arrow(O2, A2), arrow(O2, A3, color="red"), dot(O2)]
body.append(vec(A1[0] - 4, A1[1] + 24, "a", "1"))
body.append(vec(A2[0] - 32, A2[1] + 2, "a", "2"))
body.append(vec(A3[0] + 8, A3[1] - 4, "a", "3", color="red"))

# sanity check: a3 really is the sum (in projection too, since the projection is linear)
assert abs((A1[0] - O2[0]) + (A2[0] - O2[0]) - (A3[0] - O2[0])) < 1e-6
assert abs((A1[1] - O2[1]) + (A2[1] - O2[1]) - (A3[1] - O2[1])) < 1e-6
for x, y in [a1, a2, a3, *corners, A1, A2, A3]:
    assert 10 < x < W - 10 and 10 < y < H - 10, (fmt(x), fmt(y))

write("three-vectors.svg", W, H, body)
