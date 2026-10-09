"""House style for ТЕНЗОРЫ figures (copied from lecture-notes/assets/figure-template.svg).

Each figure script in this folder imports this module, computes its coordinates and calls
`save(name, width, height, body)`, which writes <name>.svg next to the script.
"""

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

DEFS = """  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,1 L10,5 L0,9 z" fill="#1a1a1a"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,1 L10,5 L0,9 z" fill="#c0392b"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,1 L10,5 L0,9 z" fill="#2563a8"/>
    </marker>
  </defs>
  <style>
    .ink  { stroke: #1a1a1a; stroke-width: 1.6; fill: none; stroke-linecap: round; stroke-linejoin: round; }
    .thin { stroke: #1a1a1a; stroke-width: 1; fill: none; }
    .grid { stroke: #1a1a1a; stroke-width: 0.6; stroke-opacity: 0.25; fill: none; }
    .red  { stroke: #c0392b; }
    .blue { stroke: #2563a8; }
    .dash { stroke-dasharray: 5 4; }
    .tint-red  { fill: #c0392b; fill-opacity: 0.10; }
    .tint-blue { fill: #2563a8; fill-opacity: 0.10; }
    .tint-grey { fill: #1a1a1a; fill-opacity: 0.05; }
    .dot  { fill: #1a1a1a; stroke: none; }
    .dot-red { fill: #c0392b; stroke: none; }
    .dot-blue { fill: #2563a8; stroke: none; }
    text { fill: #1a1a1a; font-family: 'Times New Roman', Times, serif; font-size: 19px; }
    .m { font-style: italic; }
    .t { font-style: normal; }
    .small { font-size: 15px; }
    .sub { font-size: 13px; }
    .lbl-red { fill: #c0392b; }
    .lbl-blue { fill: #2563a8; }
    .mid { text-anchor: middle; }
    .end { text-anchor: end; }
  </style>
  <rect width="100%" height="100%" fill="#ffffff"/>
"""


def f(x):
    """Format a coordinate."""
    return f"{x:.1f}".rstrip("0").rstrip(".")


def save(name, width, height, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
           f'width="{width}" height="{height}">\n{DEFS}{body}</svg>\n')
    out = HERE / f"{name}.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"wrote {out.name}")


def smooth_closed(points):
    """Closed Catmull-Rom spline through points, as an SVG path of cubic Beziers."""
    n = len(points)
    d = [f"M{f(points[0][0])},{f(points[0][1])}"]
    for k in range(n):
        p0, p1, p2, p3 = points[k - 1], points[k], points[(k + 1) % n], points[(k + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}")
    return " ".join(d) + " Z"


def blob(cx, cy, rx, ry, phase=0.0, k=12):
    """A hand-drawn-looking closed set outline: a wobbled ellipse."""
    pts = []
    for s in range(k):
        t = 2 * math.pi * s / k
        r = 1 + 0.07 * math.sin(2 * t + phase) + 0.04 * math.cos(3 * t + 2 * phase)
        pts.append((cx + rx * r * math.cos(t), cy + ry * r * math.sin(t)))
    return smooth_closed(pts)
