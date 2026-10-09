#!/usr/bin/env python3
"""Make figure SVGs follow the viewer's light/dark theme, wherever they are shown.

    python3 theme_svg.py docs/lecture-04/figures/*.svg

For each file it
  1. drops the full-canvas white background rectangle, so the figure sits on whatever page shows it;
  2. wraps the drawing in a group and adds, inside the SVG, a `prefers-color-scheme: dark` rule
     that runs the drawing through a colour matrix equal to CSS `invert(1) hue-rotate(180deg)`:
     dark ink turns light, while red stays red and blue stays blue.

Because the rule lives in the SVG itself, the figure adapts on the website, on github.com and in
VS Code's Markdown preview, with no CSS on the page. Light mode looks exactly as drawn.

Run it after every (re)generation of a figure: the figure scripts write plain SVGs. Already-themed
files are left alone, so running it twice is harmless. render_preview.py flags unthemed figures.
"""

import re
import sys
from pathlib import Path

MARK = "lecture-notes:theme"
# invert(1) then hue-rotate(180deg), folded into one matrix (rows R, G, B, A; columns R G B A offset).
MATRIX = ("0.574 -1.430 -0.144 0 1  "
          "-0.426 -0.430 -0.144 0 1  "
          "-0.426 -1.430 0.856 0 1  "
          "0 0 0 1 0")
BG_RECT = re.compile(r'\s*<rect\s+(?:x="0"\s+y="0"\s+)?width="(?:100%|[\d.]+)"\s+height="(?:100%|[\d.]+)"'
                     r'\s+fill="(?:#fff|#ffffff|white)"\s*/>', re.I)


def theme(svg: str) -> str:
    if MARK in svg:
        return svg
    open_tag = re.search(r"<svg\b[^>]*>", svg)
    close_at = svg.rfind("</svg>")
    if not open_tag or close_at < 0:
        raise ValueError("not an SVG document")
    head, inner, tail = svg[:open_tag.end()], svg[open_tag.end():close_at], svg[close_at:]

    vb = re.search(r'viewBox="([-\d.]+)\s+([-\d.]+)\s+([\d.]+)\s+([\d.]+)"', open_tag.group(0))
    x, y, w, h = vb.groups() if vb else ("0", "0", "100%", "100%")
    # Only a background rect that covers the whole canvas goes; other white shapes (e.g. a sphere
    # that hides what is behind it) stay.
    m = BG_RECT.search(inner)
    if m:
        dims = re.findall(r'(?:width|height)="([^"]+)"', m.group(0))
        if all(d == "100%" for d in dims) or (vb and dims == [w, h]):
            inner = inner[:m.start()] + inner[m.end():]

    block = (f"\n  <!-- {MARK}: follows light/dark; see .claude/skills/lecture-notes/scripts/theme_svg.py -->\n"
             f'  <defs><filter id="ln-dark" filterUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}"'
             f' color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="{MATRIX}"/></filter></defs>\n'
             f"  <style>@media (prefers-color-scheme: dark) {{ .ln-theme {{ filter: url(#ln-dark); }} }}</style>\n"
             f'  <g class="ln-theme">')
    return head + block + inner.rstrip() + "\n  </g>\n" + tail


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for name in sys.argv[1:]:
        p = Path(name)
        src = p.read_text(encoding="utf-8")
        out = theme(src)
        if out == src:
            print(f"already themed: {p}")
        else:
            p.write_text(out, encoding="utf-8")
            print(f"themed: {p}")


if __name__ == "__main__":
    main()
