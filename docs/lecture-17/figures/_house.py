"""House style helpers for the lecture-17 figures (standard library only).

Each figure script imports this module, computes its geometry and writes <name>.svg
next to itself:  python3 <name>.py
"""

import math
from pathlib import Path

INK, RED, BLUE = "#1a1a1a", "#c0392b", "#2563a8"

_DEFS = """  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,1 L10,5 L0,9 z" fill="#1a1a1a"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,1 L10,5 L0,9 z" fill="#c0392b"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,1 L10,5 L0,9 z" fill="#2563a8"/>
    </marker>
{extra}  </defs>
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
    .white {{ fill: #ffffff; }}
    .dot  {{ fill: #1a1a1a; stroke: none; }}
    .dot-red {{ fill: #c0392b; stroke: none; }}
    .dot-blue {{ fill: #2563a8; stroke: none; }}
    text {{ fill: #1a1a1a; font-family: 'Times New Roman', Times, serif; font-size: 19px; }}
    .m {{ font-style: italic; }}
    .t {{ font-style: normal; }}
    .small {{ font-size: 15px; }}
    .sub {{ font-size: 13px; }}
    .lbl-red {{ fill: #c0392b; }}
    .lbl-blue {{ fill: #2563a8; }}
  </style>
  <rect width="100%" height="100%" fill="#ffffff"/>
"""


class SVG:
    def __init__(self, w, h, extra_defs=""):
        self.w, self.h = w, h
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
                      _DEFS.format(extra=extra_defs)]

    def add(self, s):
        self.parts.append("  " + s)

    def save(self, script_file):
        out = Path(script_file).with_suffix(".svg")
        out.write_text("\n".join(self.parts + ["</svg>", ""]), encoding="utf-8")
        print(f"wrote {out}")


def f(v):
    return f"{v:.1f}"


def d_path(pts, closed=False):
    s = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts)
    return s + (" Z" if closed else "")


def polyline(pts, cls="ink", closed=False, attrs=""):
    return f'<path class="{cls}" d="{d_path(pts, closed)}"{attrs}/>'


def arrow(p, q, color="", width=None):
    """Straight arrow p -> q. color: '' (ink), 'red' or 'blue'."""
    cls = "ink" + (f" {color}" if color else "")
    mk = {"": "arrow", "red": "arrow-red", "blue": "arrow-blue"}[color]
    sw = f' style="stroke-width:{width}"' if width else ""
    return (f'<line class="{cls}" x1="{f(p[0])}" y1="{f(p[1])}" x2="{f(q[0])}" y2="{f(q[1])}"'
            f' marker-end="url(#{mk})"{sw}/>')


def dot(p, cls="dot", r=3.5):
    return f'<circle class="{cls}" cx="{f(p[0])}" cy="{f(p[1])}" r="{r}"/>'


def text(x, y, body, cls="m", anchor=None):
    a = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text class="{cls}" x="{f(x)}" y="{f(y)}"{a}>{body}</text>'


def sub(s, back=True):
    """Subscript tspan; returns to the baseline afterwards if back=True."""
    return f'<tspan class="sub" dy="5">{s}</tspan>' + ('<tspan dy="-5"></tspan>' if back else "")


# ------------------------------------------------------------------ 3D (orthographic)

class Ortho:
    """Orthographic view from azimuth `az` and elevation `el` (degrees).
    World: z up. Screen: scale `s` px per unit, origin of world at (ox, oy)."""

    def __init__(self, az, el, s, ox, oy):
        a, e = math.radians(az), math.radians(el)
        self.d = (math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))  # toward viewer
        self.r = (-math.sin(a), math.cos(a), 0.0)
        self.u = (-math.sin(e) * math.cos(a), -math.sin(e) * math.sin(a), math.cos(e))
        self.s, self.ox, self.oy = s, ox, oy

    def __call__(self, P):
        X = sum(P[i] * self.r[i] for i in range(3))
        Y = sum(P[i] * self.u[i] for i in range(3))
        return (self.ox + self.s * X, self.oy - self.s * Y)

    def visible(self, P, inside, step=0.01, far=12.0):
        """True if the ray from P toward the viewer does not pass through the solid `inside`."""
        t = step * 3
        while t < far:
            Q = (P[0] + t * self.d[0], P[1] + t * self.d[1], P[2] + t * self.d[2])
            if inside(Q):
                return False
            t += step
        return True


def runs(flags):
    """Split a list of booleans into (start, end, value) runs (end inclusive)."""
    out, start = [], 0
    for i in range(1, len(flags) + 1):
        if i == len(flags) or flags[i] != flags[start]:
            out.append((start, i - 1, flags[start]))
            start = i
    return out


def curve_3d(view, pts3, inside, cls_vis="ink", cls_hid="ink dash", draw_hidden=True):
    """Polyline in 3D: visible runs solid, hidden runs dashed (or omitted)."""
    flags = [view.visible(P, inside) for P in pts3]
    scr = [view(P) for P in pts3]
    out = []
    for a, b, vis in runs(flags):
        seg = scr[max(a - 1, 0):b + 1] if vis else scr[a:b + 2]
        if len(seg) < 2:
            continue
        if vis:
            out.append(polyline(seg, cls_vis))
        elif draw_hidden:
            out.append(polyline(seg, cls_hid))
    return out


def add(u, v):
    return tuple(a + b for a, b in zip(u, v))


def subv(u, v):
    return tuple(a - b for a, b in zip(u, v))


def mul(k, u):
    return tuple(k * a for a in u)


def dotp(u, v):
    return sum(a * b for a, b in zip(u, v))


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def norm(u):
    n = math.sqrt(dotp(u, u))
    return tuple(a / n for a in u)


def vec_label(x, y, letter, color="", sub_text=None):
    """Italic letter with a small arrow over it (a vector name like v with an arrow), at baseline (x, y)."""
    cls = "m" + (f" lbl-{color}" if color else "")
    stroke = "thin" + (f" {color}" if color else "")
    mk = {"": "arrow", "red": "arrow-red", "blue": "arrow-blue"}[color]
    body = letter + (f'<tspan class="sub" dy="5">{sub_text}</tspan>' if sub_text else "")
    return (f'<text class="{cls}" x="{f(x)}" y="{f(y)}">{body}</text>'
            f'<path class="{stroke}" d="M{f(x + 1)},{f(y - 15)} l9,0" marker-end="url(#{mk})"/>')
