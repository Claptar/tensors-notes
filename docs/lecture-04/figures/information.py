"""Рис. 5: how much information a vector and a linear form carry on the plane: a vector has a length
and a direction (angle φ); a linear form has the spacing d of its level lines and their tilt ψ.
Two numbers in both cases."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _house import arrow, clip_line, dot, line, over_arrow, text, write  # noqa: E402

W, H = 640, 230
body = []


def arc(cx, cy, r, a0, a1, cls="thin"):
    """Arc of radius r around (cx, cy) from angle a0 to a1 (degrees, counter-clockwise, math orientation)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1)))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path class="{cls}" d="M{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 {large} 0 {p1[0]:.1f},{p1[1]:.1f}"/>')


# ---------------- left: a vector — length and direction
O = (80, 180)
phi, ell = 33, 165
tip = (O[0] + ell * math.cos(math.radians(phi)), O[1] - ell * math.sin(math.radians(phi)))
body.append(line(O, (O[0] + 200, O[1]), "thin dash"))
body.append(arc(*O, 48, 0, phi))
body.append(text(O[0] + 56, O[1] - 10, "φ", "m"))
body.append(arrow(O, tip))
body.append(dot(O))
body.append(text(tip[0] + 6, tip[1] - 4, "a", "m"))
body.append(over_arrow(tip[0] + 6, tip[1] - 4, 9))
mid = ((O[0] + tip[0]) / 2, (O[1] + tip[1]) / 2)
body.append(text(mid[0] - 30, mid[1] - 10, "|", "t"))
body.append(text(mid[0] - 24, mid[1] - 10, "a", "m"))
body.append(over_arrow(mid[0] - 24, mid[1] - 10, 9))
body.append(text(mid[0] - 14, mid[1] - 10, "|", "t"))

# ---------------- right: a linear form — spacing and tilt of the level lines
theta = 62                                   # tilt of the level lines (degrees from the horizontal)
u = (math.cos(math.radians(theta)), math.sin(math.radians(theta)))        # along the lines (math, y up)
n = (math.cos(math.radians(theta - 90)), math.sin(math.radians(theta - 90)))  # normal, towards growing f
d = 46                                       # spacing in px
B0 = (385, 200)                              # SVG point on the line f = 0
RECT = (-30, -10, 232, 180)                  # visible region relative to B0, math orientation (px)


def S(p):                                    # math px (y up) relative to B0 -> SVG
    return (B0[0] + p[0], B0[1] - p[1])


for c in range(0, 4):
    seg = clip_line((c * d * n[0], c * d * n[1]), u, RECT)
    if not seg:
        continue
    p, q = seg
    body.append(line(S(p), S(q), "ink red" if c == 0 else "thin red"))
    top = S(q if q[1] > p[1] else p)
    body.append(text(top[0] + 5, top[1] + 14, str(c), "t lbl-red small"))

# tilt ψ: angle between a horizontal reference and the line f = 0
body.append(line(S((0, 0)), S((44, 0)), "thin dash"))
body.append(arc(*S((0, 0)), 26, 0, theta))
body.append(text(S((0, 0))[0] + 26, S((0, 0))[1] - 8, "ψ", "m"))

# spacing d between the lines f = 1 and f = 2, measured along the normal
t0 = 95
p1 = (1 * d * n[0] + t0 * u[0], 1 * d * n[1] + t0 * u[1])
p2 = (2 * d * n[0] + t0 * u[0], 2 * d * n[1] + t0 * u[1])
a, b = S(p1), S(p2)
body.append(f'<path class="ink" d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" '
            f'marker-start="url(#arrow)" marker-end="url(#arrow)"/>')
body.append(text((a[0] + b[0]) / 2 - 4, (a[1] + b[1]) / 2 - 8, "d", "m"))

write("information.svg", W, H, body)
