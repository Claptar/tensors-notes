"""Рис.: две карты с перекрывающимися областями и функция перехода psi o phi^{-1}.

U and V are two regions of M; phi maps U to the left copy of R^n, psi maps V to the right one.
Each chart is drawn as a concrete smooth map of the picture plane (scale + rotation + a mild
bend), applied to the boundaries of U and V; the hatched sets are the images of U and V
intersected (SVG clip paths), so phi(U n V) and psi(U n V) really are images of the same set.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _house import SVG, polyline, text, d_path, f  # noqa: E402

HATCH = """    <pattern id="hatch" patternUnits="userSpaceOnUse" width="7" height="7" patternTransform="rotate(40)">
      <line x1="0" y1="0" x2="0" y2="7" stroke="#1a1a1a" stroke-width="1" stroke-opacity="0.55"/>
    </pattern>
"""
W, H = 640, 330
svg = SVG(W, H, extra_defs=HATCH)


def closed(cx, cy, rx, ry, wob, ph, n=200):
    pts = []
    for k in range(n):
        s = 2 * math.pi * k / n
        r = 1 + wob * math.sin(3 * s + ph)
        pts.append((cx + rx * r * math.cos(s), cy + ry * r * math.sin(s)))
    return pts


# ---- the manifold and the two chart domains (picture coordinates, px)
M = closed(320, 92, 150, 72, 0.06, 0.4)
U = closed(278, 92, 72, 50, 0.05, 1.0)
V = closed(366, 96, 70, 48, 0.05, 2.2)


def chart_map(P, centre, target, scale, rot, bend):
    x, y = P[0] - centre[0], P[1] - centre[1]
    c, s = math.cos(rot), math.sin(rot)
    x, y = c * x - s * y, s * x + c * y
    x, y = x + bend * y * y / 60, y - bend * x * x / 80
    return (target[0] + scale * x, target[1] + scale * y)


def phi(P):
    return chart_map(P, (278, 92), (145, 254), 0.85, -0.25, 0.25)


def psi(P):
    return chart_map(P, (366, 96), (488, 254), 0.85, 0.3, -0.25)


svg.add(polyline(M, "ink tint-grey", closed=True))

# hatched U n V on M, phi(U n V), psi(U n V)
for name, T in (("m", lambda P: P), ("l", phi), ("r", psi)):
    svg.add(f'<clipPath id="clip-{name}"><path d="{d_path([T(P) for P in U], True)}"/></clipPath>')
    svg.add(f'<g clip-path="url(#clip-{name})"><path d="{d_path([T(P) for P in V], True)}" fill="url(#hatch)"/></g>')

svg.add(polyline(U, "ink red", closed=True))
svg.add(polyline(V, "ink blue", closed=True))
# in each chart, the boundary of the overlap: image of the other domain's edge, clipped
svg.add(f'<g clip-path="url(#clip-l)"><path class="thin blue" d="{d_path([phi(P) for P in V], True)}"/></g>')
svg.add(f'<clipPath id="clip-rv"><path d="{d_path([psi(P) for P in V], True)}"/></clipPath>')
svg.add(f'<g clip-path="url(#clip-rv)"><path class="thin red" d="{d_path([psi(P) for P in U], True)}"/></g>')
svg.add(text(190, 68, "U", "m lbl-red"))
svg.add(text(448, 90, "V", "m lbl-blue"))
svg.add(text(452, 40, "M"))

# ---- the two copies of R^n
for x0 in (40, 380):
    svg.add(f'<rect class="thin" x="{x0}" y="190" width="220" height="132" fill="none"/>')
    svg.add(text(x0 + 214, 212, 'ℝ<tspan class="sub m" dy="-9">n</tspan>', "t", anchor="end"))
svg.add(polyline([phi(P) for P in U], "ink red", closed=True))
svg.add(polyline([psi(P) for P in V], "ink blue", closed=True))
svg.add(text(50, 312, 'φ<tspan class="t">(</tspan>U<tspan class="t">)</tspan>', "m lbl-red"))
svg.add(text(590, 312, 'ψ<tspan class="t">(</tspan>V<tspan class="t">)</tspan>', "m lbl-blue", anchor="end"))

# ---- arrows: the charts and the transition map
svg.add('<path class="ink" d="M232,132 Q190,160 168,196" marker-end="url(#arrow)"/>')
svg.add(text(178, 158, "φ"))
svg.add('<path class="ink" d="M410,134 Q452,162 470,196" marker-end="url(#arrow)"/>')
svg.add(text(455, 160, "ψ"))
a0, a1 = phi((322, 94)), psi((322, 94))
svg.add(f'<path class="ink" d="M{f(a0[0] + 8)},{f(a0[1])} Q{f((a0[0] + a1[0]) / 2)},{f(a0[1] + 52)} {f(a1[0] - 10)},{f(a1[1] + 4)}" marker-end="url(#arrow)"/>')
svg.add(text(320, 316, 'ψ<tspan class="t"> ∘ </tspan>φ<tspan class="sub t" dy="-9">−1</tspan>', "m", anchor="middle"))

svg.save(__file__)
