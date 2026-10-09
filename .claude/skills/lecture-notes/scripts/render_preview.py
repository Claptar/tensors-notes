#!/usr/bin/env python3
"""Render a lecture Markdown file to PDF the way VS Code's preview would, and report problems.

Uses markdown-it + KaTeX (via markdown-it-texmath) loaded from jsDelivr, and headless
Google Chrome to run the page and print it. Relative image paths resolve against the
Markdown file's own folder, so figures show up exactly as they will in the editor.

Usage:
    python3 render_preview.py docs/lecture-04/lecture-04.md --pdf <scratch>/lecture-04.pdf
    python3 render_preview.py docs/lecture-04/lecture-04.md               # PDF goes to the temp dir
    python3 render_preview.py docs/lecture-04/lecture-04.md --check-only  # report errors, no PDF

The preview PDF never goes next to the .md, because that's where the final PDF lives.

Prints a report: every formula KaTeX could not parse (with the error and the source),
every image that failed to load, and leftover literal `$` that probably meant broken
math. Exit code is 1 if anything is wrong, 0 if the document is clean.
"""

import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _chrome import run_chrome  # noqa: E402

CDN = "https://cdn.jsdelivr.net/npm"
HEAD_LIBS = f"""
<link rel="stylesheet" href="{CDN}/katex@0.16.11/dist/katex.min.css">
<script src="{CDN}/katex@0.16.11/dist/katex.min.js"></script>
<script src="{CDN}/markdown-it@14.1.0/dist/markdown-it.min.js"></script>
<script src="{CDN}/markdown-it-texmath@1.0.0/texmath.js"></script>
"""

CSS = """
@page { size: A4; margin: 22mm 20mm 20mm 20mm;
  @top-left { content: "ТЕНЗОРЫ"; font: 9pt 'PT Serif', Georgia, serif; }
  @top-right { content: "__RUNNING__"; font: 9pt 'PT Serif', Georgia, serif; }
  @bottom-center { content: counter(page); font: 9pt 'PT Serif', Georgia, serif; }
}
body { font-family: 'PT Serif', Georgia, 'Times New Roman', serif; font-size: 11pt;
  line-height: 1.45; color: #111; background: #fff; max-width: 170mm; margin: 0 auto; }
h1 { text-align: center; font-size: 17pt; margin: 0 0 10pt; }
h2 { font-size: 14pt; margin: 18pt 0 6pt; break-after: avoid; }
h3 { font-size: 12pt; margin: 14pt 0 4pt; break-after: avoid; }
p { margin: 0 0 6pt; text-align: justify; hyphens: auto; }
blockquote { margin: 8pt 10mm 14pt; padding: 0; border: none; font-size: 10pt; }
img { display: block; margin: 10pt auto; max-width: 100%; break-inside: avoid; }
table { border-collapse: collapse; margin: 8pt auto; break-inside: avoid; }
th, td { border: 1px solid #444; padding: 2pt 7pt; text-align: center; }
hr { border: none; border-top: 0.6pt solid #000; margin: 16pt 0 6pt; }
section { margin: 8pt 0; overflow-x: auto; } eqn { display: block; text-align: center; }
.katex-display { margin: 6pt 0; }
.katex-error { background: #ffd6d6; }
"""

PAGE = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<base href="__BASE__">
<link href="https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
__LIBS__
<style>__CSS__</style>
</head><body>
<div id="doc"></div>
<pre id="__report" style="display:none"></pre>
<script>
const SRC = __SRC__;
const report = {katex_errors: [], broken_images: [], stray_dollars: []};
try {
  const md = window.markdownit({html: true, linkify: false, typographer: false})
    .use(texmath, {engine: katex, delimiters: 'dollars',
                   katexOptions: {throwOnError: false, strict: false, errorColor: '#cd0a0b'}});
  document.getElementById('doc').innerHTML = md.render(SRC);
} catch (e) { report.fatal = String(e); }
document.querySelectorAll('.katex-error').forEach(el =>
  report.katex_errors.push({error: el.getAttribute('title') || '', source: el.textContent.slice(0, 200)}));
// Unknown commands don't raise with throwOnError:false; KaTeX paints them in errorColor instead.
document.querySelectorAll('.katex [style*="#cd0a0b"]').forEach(el =>
  report.katex_errors.push({error: 'Unsupported command ' + el.textContent,
                            source: (el.closest('.katex').querySelector('annotation') || el).textContent.slice(0, 200)}));
// A `$` left in plain text usually means a formula the parser did not recognise as math.
const walker = document.createTreeWalker(document.getElementById('doc'), NodeFilter.SHOW_TEXT);
while (walker.nextNode()) {
  const n = walker.currentNode;
  if (n.parentElement.closest('.katex, code, pre')) continue;
  if (n.nodeValue.includes('$')) report.stray_dollars.push(n.nodeValue.trim().slice(0, 160));
}
function finish() {
  document.querySelectorAll('img').forEach(img => {
    if (!img.complete || img.naturalWidth === 0) report.broken_images.push(img.getAttribute('src'));
  });
  document.getElementById('__report').textContent = JSON.stringify(report);
}
window.addEventListener('load', finish);
</script>
</body></html>
"""


def build_html(md_path: Path) -> str:
    src = md_path.read_text(encoding="utf-8")
    m = re.search(r"^#\s+(.+)$", src, re.M)
    running = (m.group(1).strip() if m else md_path.stem).replace('"', "'")
    src_js = json.dumps(src, ensure_ascii=False).replace("</", "<\\/")
    base = md_path.parent.resolve().as_uri() + "/"
    return (PAGE.replace("__BASE__", html.escape(base))
                .replace("__LIBS__", HEAD_LIBS)
                .replace("__CSS__", CSS.replace("__RUNNING__", running))
                .replace("__SRC__", src_js))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown")
    ap.add_argument("--pdf", help="output PDF path (default: <temp dir>/<name>-preview.pdf)")
    ap.add_argument("--check-only", action="store_true", help="only report errors, do not write a PDF")
    a = ap.parse_args()

    md_path = Path(a.markdown).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "preview.html"
        page.write_text(build_html(md_path), encoding="utf-8")
        url = page.as_uri()

        dom = run_chrome(["--virtual-time-budget=20000", "--run-all-compositor-stages-before-draw",
                          "--dump-dom", url])
        m = re.search(r'<pre id="__report"[^>]*>(.*?)</pre>', dom, re.S)
        if not m or not m.group(1).strip():
            sys.exit("Could not read the render report (no network for the CDN, or Chrome failed).")
        rep = json.loads(html.unescape(m.group(1)))

        if not a.check_only:
            pdf = Path(a.pdf).resolve() if a.pdf else Path(tempfile.gettempdir()) / f"{md_path.stem}-preview.pdf"
            run_chrome(["--virtual-time-budget=20000", "--run-all-compositor-stages-before-draw",
                        "--no-pdf-header-footer", f"--print-to-pdf={pdf}", url])
            print(f"PDF: {pdf}" if pdf.exists() else "PDF was not written.")

    problems = 0
    if rep.get("fatal"):
        print(f"FATAL: {rep['fatal']}"); problems += 1
    seen = set()
    for e in rep["katex_errors"]:
        if (e["error"], e["source"]) in seen:  # nested spans can report the same error twice
            continue
        seen.add((e["error"], e["source"]))
        print(f"MATH ERROR: {e['error']}\n    in: {e['source']}"); problems += 1
    for s in rep["broken_images"]:
        print(f"MISSING OR INVALID IMAGE: {s}  (check the path; check the SVG with xmllint --noout)"); problems += 1
    for s in rep["stray_dollars"]:
        print(f"UNRENDERED $: {s}"); problems += 1
    # KaTeX renders things the final pdfLaTeX build cannot (Cyrillic or Unicode symbols in math,
    # Greek or arrows typed straight into text). Catch them now, not at finalize time.
    from finalize import MATH_RE, math_problem, text_problem
    src = md_path.read_text(encoding="utf-8")
    for m in MATH_RE.finditer(src):
        why = math_problem(m.group(1) if m.group(1) is not None else m.group(2))
        if why:
            print(f"NOT LATEX-SAFE: {why}: {m.group(0).strip()[:80]}"); problems += 1
    plain = re.sub(r"<!--.*?-->|`[^`]*`|!\[[^\]]*\]\([^)]*\)", "", MATH_RE.sub("", src), flags=re.S)
    for no, line in enumerate(plain.splitlines(), 1):
        why = text_problem(line)
        if why:
            print(f"NOT LATEX-SAFE: {why}: {line.strip()[:80]}"); problems += 1
    # Every SVG figure must carry its own light/dark rule (theme_svg.py), or it shows as a white box
    # on a dark page: on the website, on github.com and in VS Code.
    for src in re.findall(r"!\[[^\]]*\]\(([^)\s]+\.svg)\)", src):
        f = md_path.parent / src
        if f.exists() and "lecture-notes:theme" not in f.read_text(encoding="utf-8"):
            print(f"FIGURE NOT THEMED: {src} (run scripts/theme_svg.py on it)"); problems += 1
    print("OK: all math rendered, all images loaded." if not problems else f"{problems} problem(s).")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
