#!/usr/bin/env python3
"""Render figures to PNG in both themes exactly as the website shows them, to look at them.

    python3 snap_svg.py docs/lecture-04/figures/level-lines.svg [more.svg ...] --out <scratch-dir>
    python3 snap_svg.py ... --engine chrome      # Chrome instead of WebKit

Writes <name>.light.png and <name>.dark.png per figure: the figure on the website's page colour,
with the website's figure styling (docs/assets/reader.css: white blended into the paper; in dark
mode, inverted with hues kept). Look at both; nothing may vanish in dark mode.

The default engine is WebKit, the engine Safari uses: it is the strictest about SVG and CSS (a
dark-mode trick that worked in Chrome failed in Safari), so a figure that looks right here looks
right everywhere. webkit_snap.swift is compiled once with swiftc into ~/Library/Caches. Without
swiftc it falls back to headless Chrome. QuickLook isn't used: it follows the Mac's own appearance
and so shows only one theme.
"""

import argparse
import hashlib
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _chrome import run_chrome  # noqa: E402

PAGE = {"light": "#faf8f3", "dark": "#1c1a17"}  # docs/assets/reader.css --bg
# Same figure rules as docs/assets/reader.css (.content img); keep the two in step.
FIGURE_CSS = ("img{display:block;mix-blend-mode:multiply}"
              "@media (prefers-color-scheme: dark){img{filter:invert(1) hue-rotate(180deg);"
              "mix-blend-mode:screen}}")


def size(svg: Path):
    head = re.search(r"<svg\b[^>]*>", svg.read_text(encoding="utf-8")).group(0)
    w, h = re.search(r'\bwidth="([\d.]+)', head), re.search(r'\bheight="([\d.]+)', head)
    if w and h:
        return float(w.group(1)), float(h.group(1))
    vb = re.search(r'viewBox="[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)"', head)
    return (float(vb.group(1)), float(vb.group(2))) if vb else (640.0, 400.0)


def webkit_tool():
    """Path to the compiled WebKit renderer, building it on first use; None if impossible."""
    src = HERE / "webkit_snap.swift"
    if sys.platform != "darwin" or not shutil.which("swiftc") or not src.exists():
        return None
    digest = hashlib.sha1(src.read_bytes()).hexdigest()[:10]
    exe = Path.home() / "Library" / "Caches" / "lecture-notes" / f"webkit_snap-{digest}"
    if not exe.exists():
        exe.parent.mkdir(parents=True, exist_ok=True)
        print("compiling the WebKit renderer (once)…", file=sys.stderr)
        r = subprocess.run(["swiftc", "-O", "-o", str(exe), str(src)], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr[-1500:], file=sys.stderr)
            return None
    return exe


def snap(engine, tool, page: Path, png: Path, scheme, W, H):
    if engine == "webkit":
        r = subprocess.run([str(tool), page.as_uri(), str(png), scheme, str(W), str(H), "0.5"],
                           capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            sys.exit(f"WebKit render failed for {png.name}: {r.stdout.strip()} {r.stderr.strip()}")
    else:
        run_chrome(["--hide-scrollbars", "--virtual-time-budget=3000", f"--window-size={W},{H}",
                    f"--screenshot={png}", page.as_uri()], scheme=scheme)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", nargs="+")
    ap.add_argument("--out", required=True, help="folder for the PNGs (use a scratch folder)")
    ap.add_argument("--engine", choices=["webkit", "chrome"], default="webkit")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    tool = webkit_tool() if a.engine == "webkit" else None
    engine = "webkit" if tool else "chrome"
    if a.engine == "webkit" and not tool:
        print("WebKit renderer unavailable; using Chrome (Safari-specific problems won't show).", file=sys.stderr)
    for name in a.svg:
        svg = Path(name).resolve()
        w, h = size(svg)
        W, H = int(w) + 40, int(h) + 40
        for scheme, bg in PAGE.items():
            page_html = (f"<!doctype html><meta charset='utf-8'><meta name='color-scheme' content='{scheme}'>"
                         f"<style>{FIGURE_CSS}</style><body style='margin:0;padding:20px;background:{bg}'>"
                         f"<img src='{html.escape(svg.as_uri())}' width='{w:g}' height='{h:g}'></body>")
            with tempfile.TemporaryDirectory() as tmp:
                page = Path(tmp) / "snap.html"
                page.write_text(page_html, encoding="utf-8")
                png = out / f"{svg.stem}.{scheme}.png"
                snap(engine, tool, page, png, scheme, W, H)
                print(png)


if __name__ == "__main__":
    main()
