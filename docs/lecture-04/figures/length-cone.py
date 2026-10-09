"""Рис. 1: function "length of a vector" on the plane of geometric vectors — a cone z = |a| over V."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _house import P as P0, arrow, dot, line, over_arrow, polygon, polyline, text, write  # noqa: E402

W, H = 640, 310
S, OX, OY = 52, 330, 245


def P(x, y, z):
    return P0(x, y, z, s=S, ox=OX, oy=OY)


L = 2.7          # half-side of the drawn patch of V
R = 2.2          # the cone is drawn up to height R (radius R)
body = []

# the plane V (patch), grey tint
corners = [P(L, -L, 0), P(L, L, 0), P(-L, L, 0), P(-L, -L, 0)]
body.append(polygon(corners, "ink tint-grey"))
cV = P(-L, L, 0)
body.append(text(cV[0] - 34, cV[1] + 24, "V", "m"))

# value axis (the part below V is hidden: dashed)
apex = P(0, 0, 0)
body.append(line(apex, P(0, 0, -0.75), "thin dash"))
top = P(0, 0, 3.55)
body.append(arrow(apex, top))
body.append(text(top[0] + 9, top[1] + 12, "ℝ", "t"))

# cone: rim ellipse and silhouette generators (tangent lines from the apex to the projected rim)
N = 720
ts = [2 * math.pi * i / N for i in range(N)]
rim = [P(R * math.cos(t), R * math.sin(t), R) for t in ts]
ang = [math.atan2(p[0] - apex[0], apex[1] - p[1]) for p in rim]   # angle from "straight up"
iL = min(range(N), key=lambda i: ang[i])
iR = max(range(N), key=lambda i: ang[i])
# front arc = the arc between the silhouette points that contains the lowest rim point
iLow = max(range(N), key=lambda i: rim[i][1])
arc1 = [rim[(iL + k) % N] for k in range((iR - iL) % N + 1)]
arc2 = [rim[(iR + k) % N] for k in range((iL - iR) % N + 1)]
front = arc1 if rim[iLow] in arc1 else arc2
body.append(polygon(rim, "tint-red"))
body.append(polygon([apex] + front, "tint-red"))

# a vector a in V and its value |a| measured upward to the cone
ax, ay = 1.25, 1.35
r = math.hypot(ax, ay)
t_a = math.atan2(ay, ax)
tip = P(ax, ay, 0)
up = P(ax, ay, r)

# a few rulings on the front surface, one of them through the point (a, |a|)
front_idx = [i % N for i in (range(iL, iL + (iR - iL) % N + 1) if front is arc1 else range(iR, iR + (iL - iR) % N + 1))]
for k in (1, 2, 3):
    i = front_idx[len(front_idx) * k // 4]
    body.append(line(apex, rim[i], "thin red"))
for t in [t_a]:
    body.append(line(apex, P(R * math.cos(t), R * math.sin(t), R), "thin red"))
body.append(line(apex, rim[iL], "ink red"))
body.append(line(apex, rim[iR], "ink red"))
body.append(polyline(rim + [rim[0]], "ink red"))

body.append(arrow(apex, tip))
body.append(line(tip, up, "ink dash"))
body.append(dot(up, "dot-red"))
body.append(dot(apex))
body.append(text(tip[0] - 4, tip[1] + 24, "a", "m"))
body.append(over_arrow(tip[0] - 4, tip[1] + 24, 9))

# label f(a) = |a|, typeset piece by piece so that the arrows sit over the a's
x0, y0 = up[0] + 12, up[1] + 6
pieces = [("f", "m", 0), ("(", "t", 8), ("a", "m", 14), (")", "t", 24), ("=", "t", 35),
          ("|", "t", 52), ("a", "m", 58), ("|", "t", 68)]
for s, cls, dx in pieces:
    body.append(text(x0 + dx, y0, s, cls))
body.append(over_arrow(x0 + 14, y0, 9))
body.append(over_arrow(x0 + 58, y0, 9))
body.append(text(apex[0] - 22, apex[1] + 6, "0", "t"))

write("length-cone.svg", W, H, body)
print("apex", apex, "tip", tip, "value point", up, "|a| =", round(r, 3))
