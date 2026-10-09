"""Рис.: кривая на сфере, «разность» двух её точек и касательная плоскость.

Unit sphere at the origin. gamma(t) = cos(k t) p + sin(k t) w is a great circle through
p = gamma(0) with velocity k w at p (w is a unit tangent vector at p). The chord from
gamma(0) to gamma(dt) runs inside the ball; the velocity lies in the tangent plane at p.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _house import (SVG, Ortho, polyline, dot, text, runs, add, subv, mul, dotp,  # noqa: E402
                    cross, norm, f, vec_label)

view = Ortho(az=15, el=18, s=110, ox=300, oy=178)
svg = SVG(640, 310)

lat, lon = math.radians(45), math.radians(15 - 25)
p = (math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat))
# unit tangent at p chosen so that the great circle is seen open (its plane faces the viewer),
# tilted a little so the curve climbs to the left
w0 = norm(cross(view.d, p))
w = mul(-1, norm(add(w0, mul(-0.2, cross(p, w0)))))
e2 = cross(p, w)
k, dt = 0.8, 1.3


def gamma(t):
    return add(mul(math.cos(k * t), p), mul(math.sin(k * t), w))


q = gamma(dt)
v = mul(k, w)                 # the velocity gamma'(0) = k w
print("n.d at p =", round(dotp(p, view.d), 3), " |q-p| =", round(math.dist(p, q), 3))

# tangent plane at p: parallelogram p +- a w +- b e2
a, b = 0.88, 0.5
plane = [add(p, add(mul(sa * a, w), mul(sb * b, e2))) for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def hidden_by_plane(Q):
    den = dotp(view.d, p)
    t = dotp(subv(p, Q), p) / den
    if t <= 1e-6:
        return False
    H = add(Q, mul(t, view.d))
    rel = subv(H, p)
    return abs(dotp(rel, w)) <= a and abs(dotp(rel, e2)) <= b


def hidden_by_ball(Q):
    """Does the ray Q + t d (t > 0) pass through the open unit ball?"""
    bq = dotp(Q, view.d)
    disc = bq * bq - (dotp(Q, Q) - 1)
    return disc > 0 and -bq + math.sqrt(disc) > 1e-3


def visible(Q, plane_too=False):
    # the tangent plane is drawn translucent: only the ball hides things
    return not hidden_by_ball(Q) and not (plane_too and hidden_by_plane(Q))


def draw(pts3, cls_vis, cls_hid, plane_too=False, offset=0.0):
    flags = [visible(mul(1 + offset, P), plane_too) for P in pts3]
    scr = [view(P) for P in pts3]
    for i0, i1, vis in runs(flags):
        seg = scr[max(i0 - 1, 0):i1 + 1] if vis else scr[i0:i1 + 2]
        if len(seg) > 1:
            svg.add(polyline(seg, cls_vis if vis else cls_hid))


# sphere outline (silhouette circle) and equator
sil = [add(mul(math.cos(s), view.r), mul(math.sin(s), view.u)) for s in [2 * math.pi * i / 360 for i in range(361)]]
svg.add(f'<circle cx="{f(view.ox)}" cy="{f(view.oy)}" r="{f(view.s)}" class="tint-grey"/>')
draw([mul(1.0005, P) for P in sil], "ink", "ink dash")
eq = [(math.cos(s), math.sin(s), 0.0) for s in [2 * math.pi * i / 360 for i in range(361)]]
draw(eq, "thin", "thin dash", offset=0.003)

# tangent plane
svg.add(polyline([view(P) for P in plane], "ink red tint-red", closed=True))

# the curve gamma on the sphere
ts = [-1.6 + (dt + 0.06 + 1.6) * i / 400 for i in range(401)]   # stop just past gamma(dt)
draw([gamma(t) for t in ts], "ink red", "ink red dash", offset=0.003)

# chord gamma(t) -> gamma(t + dt): inside the ball, hence dashed
chord = [add(p, mul(i / 100, subv(q, p))) for i in range(101)]
draw(chord, "ink", "ink dash", plane_too=False)
P1, Q1 = view(p), view(q)

# velocity at p, lying in the tangent plane
V1 = view(add(p, v))
svg.add(f'<line class="ink red" x1="{f(P1[0])}" y1="{f(P1[1])}" x2="{f(V1[0])}" y2="{f(V1[1])}" '
        f'marker-end="url(#arrow-red)" style="stroke-width:2.2"/>')
svg.add(dot(P1, "dot-red", r=4))
svg.add(dot(Q1, "dot", r=3.5))

# labels
svg.add(text(view.ox - 0.78 * view.s, view.oy + 0.86 * view.s, "M"))
svg.add(text(P1[0] - 40, P1[1] - 8, 'γ<tspan class="t">(</tspan>t<tspan class="t">)</tspan>', "m lbl-red"))
svg.add(text(Q1[0] + 27, Q1[1] + 6, 'γ<tspan class="t">(</tspan>t<tspan class="t"> + Δ</tspan>t<tspan class="t">)</tspan>', "m"))
svg.add(vec_label(V1[0] - 34, V1[1] - 2, "v", "red"))
G = view(gamma(ts[0]))
svg.add(text(G[0] - 6, G[1] + 34, 'γ', "m lbl-red"))

svg.save(__file__)
