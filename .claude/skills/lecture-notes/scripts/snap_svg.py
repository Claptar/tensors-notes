#!/usr/bin/env python3
"""Render figures to PNG in both themes, on the website's own page colours, to look at them.

    python3 snap_svg.py docs/lecture-04/figures/level-lines.svg [more.svg ...] --out <scratch-dir>

Writes <name>.light.png and <name>.dark.png per figure. Look at both: the light one is what the
PDF gets, the dark one is what readers with a dark system theme see on the website, on github.com
and in VS Code (see theme_svg.py). Use this rather than QuickLook, which follows the Mac's own
appearance and so shows only one of the two.
"""

import argparse
import html
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _chrome import run_chrome  # noqa: E402

PAGE = {"light": "#faf8f3", "dark": "#1c1a17"}  # docs/assets/reader.css --bg


def size(svg: Path):
    head = re.search(r"<svg\b[^>]*>", svg.read_text(encoding="utf-8")).group(0)
    w, h = re.search(r'\bwidth="([\d.]+)', head), re.search(r'\bheight="([\d.]+)', head)
    if w and h:
        return float(w.group(1)), float(h.group(1))
    vb = re.search(r'viewBox="[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)"', head)
    return (float(vb.group(1)), float(vb.group(2))) if vb else (640.0, 400.0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", nargs="+")
    ap.add_argument("--out", required=True, help="folder for the PNGs (use a scratch folder)")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name in a.svg:
        svg = Path(name).resolve()
        w, h = size(svg)
        W, H = int(w) + 40, int(h) + 40
        for scheme, bg in PAGE.items():
            page = (f"<!doctype html><meta charset='utf-8'><meta name='color-scheme' content='{scheme}'>"
                    f"<body style='margin:0;padding:20px;background:{bg}'>"
                    f"<img src='{html.escape(svg.as_uri())}' width='{w:g}' height='{h:g}'></body>")
            with tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp) / "snap.html"
                p.write_text(page, encoding="utf-8")
                png = out / f"{svg.stem}.{scheme}.png"
                run_chrome(["--hide-scrollbars", "--virtual-time-budget=3000", f"--window-size={W},{H}",
                            f"--screenshot={png}", p.as_uri()], scheme=scheme)
                print(png)


if __name__ == "__main__":
    main()
