"""Рис. 6: the reciprocal (dual) basis on the plane. The level lines of ω̃1 (red) are parallel to e2 and
pass through 0, e1, 2e1, ...; those of ω̃2 (blue) are parallel to e1. So ω̃1(e1) = 1, ω̃1(e2) = 0,
ω̃2(e1) = 0, ω̃2(e2) = 1, and for a = 2e1 + e2 the forms read off its components: ω̃1(a) = 2, ω̃2(a) = 1."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _house import arrow, clip_line, dot, line, over_arrow, over_tilde, sub, text, write  # noqa: E402

W, H = 640, 370
SC = 70
OX, OY = 190, 255
RECT = (-2.5, -1.6, 5.15, 3.35)          # visible region (math units, y up)
e1 = (1.3, 0.25)
e2 = (0.45, 1.1)
a = (2 * e1[0] + e2[0], 2 * e1[1] + e2[1])


def X(p):
    return (OX + SC * p[0], OY - SC * p[1])


def coords(p):
    """Components of p in the basis e1, e2 (solve 2x2)."""
    det = e1[0] * e2[1] - e1[1] * e2[0]
    return ((p[0] * e2[1] - p[1] * e2[0]) / det, (e1[0] * p[1] - e1[1] * p[0]) / det)


body = []
# level lines of ω1 (red): {k e1 + t e2}; label at the top end
for k in range(-1, 4):
    seg = clip_line((k * e1[0], k * e1[1]), e2, RECT)
    if not seg:
        continue
    p, q = seg
    body.append(line(X(p), X(q), "ink red" if k == 0 else "thin red"))
    top = X(q if q[1] > p[1] else p)
    if k == 0:
        body.append(text(top[0] + 6, top[1] + 16, "ω" + sub("1") + '<tspan class="t">= 0</tspan>', "m lbl-red small"))
        body.append(over_tilde(top[0] + 6, top[1] + 16, 9, "red"))
    else:
        body.append(text(top[0] + 4, top[1] + 16, str(k).replace("-", "−"), "t lbl-red small"))
# level lines of ω2 (blue): {k e2 + t e1}; label at the right end
for k in range(-1, 3):
    seg = clip_line((k * e2[0], k * e2[1]), e1, RECT)
    if not seg:
        continue
    p, q = seg
    body.append(line(X(p), X(q), "ink blue" if k == 0 else "thin blue"))
    right = X(q if q[0] > p[0] else p)
    if k == 0:
        body.append(text(right[0] + 6, right[1] + 5, "ω" + sub("2") + '<tspan class="t">= 0</tspan>', "m lbl-blue small"))
        body.append(over_tilde(right[0] + 6, right[1] + 5, 9, "blue"))
    else:
        body.append(text(right[0] + 6, right[1] + 5, str(k).replace("-", "−"), "t lbl-blue small"))

O = (0.0, 0.0)
body.append(arrow(X(O), X(e1), width=2.2))
body.append(arrow(X(O), X(e2), width=2.2))
body.append(arrow(X(O), X(a)))
body.append(dot(X(O)))
body.append(dot(X(a)))



def B(c1, c2):
    """SVG point with components (c1, c2) in the basis e1, e2: used to put labels inside grid cells."""
    return X((c1 * e1[0] + c2 * e2[0], c1 * e1[1] + c2 * e2[1]))


for name, (c1, c2), dx in (("1", (0.72, -0.42), -6), ("2", (-0.42, 0.78), -10)):
    pl = B(c1, c2)
    body.append(text(pl[0] + dx, pl[1] + 6, "e" + sub(name), "m"))
    body.append(over_arrow(pl[0] + dx, pl[1] + 6, 9))
pl = B(1.62, 1.5)
body.append(text(pl[0] - 5, pl[1] + 6, "a", "m"))
body.append(over_arrow(pl[0] - 5, pl[1] + 6, 9))
po = X(O)
body.append(text(po[0] - 24, po[1] + 22, "0", "t"))
body.append(over_arrow(po[0] - 24, po[1] + 22, 9))

write("dual-basis.svg", W, H, body)
print("components of a:", coords(a), " e1:", coords(e1), " e2:", coords(e2))
