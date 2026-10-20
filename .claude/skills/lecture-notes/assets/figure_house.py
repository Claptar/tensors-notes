"""House style and drawing helpers for ТЕНЗОРЫ figures (lecture-notes skill, assets/).

Copy this file into a lecture's figures folder as `_house.py`; each figure script there
imports it, computes its coordinates (standard library only) and writes one SVG with
`save(name, w, h, body_str)` or `write("name.svg", w, h, body_lines)`. The style is the
one in assets/figure-template.svg: dark ink on white (the website themes it), red for the
main object, blue for a contrasting one. Merged from the helpers of lectures 1 and 4.
"""

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

HEAD = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
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
    .ink  {{ stroke: #1a1a1a; stroke-width: 1.6; fill: none; stroke-linecap: round; stroke-linejoin: round; }}
    .thin {{ stroke: #1a1a1a; stroke-width: 1; fill: none; }}
    .grid {{ stroke: #1a1a1a; stroke-width: 0.6; stroke-opacity: 0.25; fill: none; }}
    .red  {{ stroke: #c0392b; }}
    .blue {{ stroke: #2563a8; }}
    .dash {{ stroke-dasharray: 5 4; }}
    .tint-red  {{ fill: #c0392b; fill-opacity: 0.10; }}
    .tint-blue {{ fill: #2563a8; fill-opacity: 0.10; }}
    .tint-grey {{ fill: #1a1a1a; fill-opacity: 0.05; }}
    .dot  {{ fill: #1a1a1a; stroke: none; }}
    .dot-red {{ fill: #c0392b; stroke: none; }}
    .dot-blue {{ fill: #2563a8; stroke: none; }}
    .deco {{ stroke: #1a1a1a; stroke-width: 1.1; fill: none; stroke-linecap: round; stroke-linejoin: round; }}
    text {{ fill: #1a1a1a; font-family: 'Times New Roman', Times, serif; font-size: 19px; }}
    .m {{ font-style: italic; }}
    .t {{ font-style: normal; }}
    .small {{ font-size: 15px; }}
    .sub {{ font-size: 13px; }}
    .lbl-red {{ fill: #c0392b; }}
    .lbl-blue {{ fill: #2563a8; }}
    .mid {{ text-anchor: middle; }}
    .end {{ text-anchor: end; }}
  </style>
  <rect width="100%" height="100%" fill="#ffffff"/>
"""


def fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else str(int(round(v)))


def pts(points):
    return " ".join(f"{fmt(x)},{fmt(y)}" for x, y in points)


def line(p, q, cls="ink"):
    return f'<line class="{cls}" x1="{fmt(p[0])}" y1="{fmt(p[1])}" x2="{fmt(q[0])}" y2="{fmt(q[1])}"/>'


def arrow(p, q, color="", dash=False, width=None):
    marker = {"": "arrow", "red": "arrow-red", "blue": "arrow-blue"}[color]
    cls = "ink" + (f" {color}" if color else "") + (" dash" if dash else "")
    style = f' style="stroke-width:{width}"' if width else ""
    return (f'<path class="{cls}"{style} d="M{fmt(p[0])},{fmt(p[1])} L{fmt(q[0])},{fmt(q[1])}" '
            f'marker-end="url(#{marker})"/>')


def polygon(points, cls):
    return f'<polygon class="{cls}" points="{pts(points)}"/>'


def polyline(points, cls):
    return f'<polyline class="{cls}" points="{pts(points)}"/>'


def dot(p, cls="dot", r=3.5):
    return f'<circle class="{cls}" cx="{fmt(p[0])}" cy="{fmt(p[1])}" r="{r}"/>'


def text(x, y, content, cls="m", anchor=None):
    a = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text class="{cls}" x="{fmt(x)}" y="{fmt(y)}"{a}>{content}</text>'


def sub(s):
    """Subscript; digits are set upright, letter indices italic (as in the formulas)."""
    cls = "sub t" if s.isdigit() else "sub"
    return f'<tspan class="{cls}" dy="5">{s}</tspan><tspan dy="-5"> </tspan>'


def over_arrow(x, y, w=10, color=""):
    """Small arrow above a letter whose baseline-left corner is (x, y): the course writes vectors as a⃗."""
    cls = "deco" + (f" {color}" if color else "")
    yy = y - 15
    return (f'<path class="{cls}" d="M{fmt(x + 1)},{fmt(yy)} h{fmt(w)} '
            f'm-3,-2.5 l3,2.5 l-3,2.5"/>')


def over_tilde(x, y, w=11, color=""):
    """Small tilde above a letter: the course writes linear forms as ω̃, f̃."""
    cls = "deco" + (f" {color}" if color else "")
    yy = y - 15
    q = w / 4
    return (f'<path class="{cls}" d="M{fmt(x + 1)},{fmt(yy + 1)} q{fmt(q)},-3.5 {fmt(2 * q)},0 '
            f't{fmt(2 * q)},0"/>')


def vec(x, y, letter, subscript=None, color="", prime=False, w=10, extra=""):
    """Vector label a⃗ (optionally with subscript and prime) at baseline-left (x, y)."""
    lbl = {"": "", "red": " lbl-red", "blue": " lbl-blue"}[color]
    body = letter + ("′" if prime else "") + (sub(subscript) if subscript else "") + extra
    return text(x, y, body, "m" + lbl) + over_arrow(x, y, w, color)


def form(x, y, letter, subscript=None, color="", w=11, extra=""):
    """Linear-form label ω̃ with optional subscript at baseline-left (x, y)."""
    lbl = {"": "", "red": " lbl-red", "blue": " lbl-blue"}[color]
    body = letter + (sub(subscript) if subscript else "") + extra
    return text(x, y, body, "m" + lbl) + over_tilde(x, y, w, color)


def write(name, w, h, body):
    svg = HEAD.format(w=w, h=h) + "\n".join("  " + b for b in body) + "\n</svg>\n"
    (HERE / name).write_text(svg, encoding="utf-8")
    print(f"wrote {HERE / name}")


# ---------------------------------------------------------------- 3D: frontal dimetric projection

def P(x, y, z, s=60, ox=320, oy=230, k=0.5, a=math.radians(45)):
    """3D point -> SVG coordinates (SVG y grows downward). y to the right, z up, x toward the viewer."""
    return (ox + s * (y - k * x * math.cos(a)), oy - s * (z - k * x * math.sin(a)))


# ---------------------------------------------------------------- 2D helpers

def clip_line(p0, d, rect):
    """Segment of the line p0 + t d inside rect = (xmin, ymin, xmax, ymax) (math coordinates)."""
    xmin, ymin, xmax, ymax = rect
    t0, t1 = -1e9, 1e9
    for p, dd, lo, hi in ((p0[0], d[0], xmin, xmax), (p0[1], d[1], ymin, ymax)):
        if abs(dd) < 1e-12:
            if not (lo <= p <= hi):
                return None
            continue
        ta, tb = (lo - p) / dd, (hi - p) / dd
        t0, t1 = max(t0, min(ta, tb)), min(t1, max(ta, tb))
    if t0 > t1:
        return None
    return (p0[0] + t0 * d[0], p0[1] + t0 * d[1]), (p0[0] + t1 * d[0], p0[1] + t1 * d[1])


def clip_poly_halfplane(poly, g):
    """Sutherland–Hodgman: keep the part of a polygon where g(point) >= 0 (g affine)."""
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        ga, gb = g(a), g(b)
        if ga >= 0:
            out.append(a)
        if (ga >= 0) != (gb >= 0):
            t = ga / (ga - gb)
            out.append(tuple(a[j] + t * (b[j] - a[j]) for j in range(len(a))))
    return out


# ---------------------------------------------------------------- string-body API (lecture 1 style)

def f(x):
    """Format a coordinate (same as fmt, kept for scripts written against lecture 1's helper)."""
    return f"{x:.1f}".rstrip("0").rstrip(".")


def save(name, width, height, body):
    """Write <name>.svg next to the script; body is one string of SVG elements."""
    svg = HEAD.format(w=width, h=height) + body + "</svg>\n"
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
    """A hand-drawn-looking closed set outline (a wobbled ellipse), for pictures of sets and maps."""
    pts_ = []
    for s in range(k):
        t = 2 * math.pi * s / k
        r = 1 + 0.07 * math.sin(2 * t + phase) + 0.04 * math.cos(3 * t + 2 * phase)
        pts_.append((cx + rx * r * math.cos(t), cy + ry * r * math.sin(t)))
    return smooth_closed(pts_)

def column(x, y, entries, cls="t", color="", h_line=22, w=34):
    """A column of numbers in parentheses, centred at x; y is the vertical centre (a column of
    components, an element of S_n). Returns a list of SVG lines."""
    n = len(entries)
    top, bot = y - n * h_line / 2, y + n * h_line / 2
    stroke = {"": "", "red": " red", "blue": " blue"}[color]
    lbl = {"": "", "red": " lbl-red", "blue": " lbl-blue"}[color]
    out = []
    for side in (-1, 1):
        xe = x + side * w / 2
        xc = xe + side * 7
        out.append(f'<path class="deco{stroke}" d="M{fmt(xe)},{fmt(top)} Q{fmt(xc)},{fmt(y)} {fmt(xe)},{fmt(bot)}"/>')
    for i, e in enumerate(entries):
        yy = top + (i + 0.5) * h_line + 6
        out.append(f'<text class="{cls}{lbl}" x="{fmt(x)}" y="{fmt(yy)}" text-anchor="middle">{e}</text>')
    return out
