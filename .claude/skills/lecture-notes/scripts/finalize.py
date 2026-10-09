#!/usr/bin/env python3
"""Turn an approved lecture draft into the final .tex and .pdf, inside the lecture's own folder.

    python3 finalize.py docs/lecture-04/lecture-04.md                 # -> docs/lecture-04/lecture-04.tex + .pdf
    python3 finalize.py docs/lecture-04/lecture-04.md --tex-only      # convert, don't compile
    python3 finalize.py docs/lecture-04/lecture-04.md --overleaf-zip  # also lecture-04-overleaf.zip for upload
    python3 finalize.py docs/lecture-04/lecture-04.md --force         # overwrite a .tex edited by hand

Each lecture lives in one folder: lecture-NN.md, figures/ (SVG + the .py that draws each),
and, after this script, lecture-NN.tex and lecture-NN.pdf. The folder is an Overleaf-ready
project as it stands.

What it does:
  1. converts every SVG figure the draft uses to a vector PDF next to the SVG (headless
     Chrome), because LaTeX cannot include SVG;
  2. converts the Markdown to LaTeX using assets/lecture-template.tex. It understands the
     Markdown subset described in references/style.md: title, header block, numbered
     sections, paragraphs with $math$, $$display$$, tables, figures with a "*Рис. N. …*"
     caption line, lists, HTML comments (kept as % comments), and the end mark;
  3. compiles exactly as Overleaf does by default: pdfLaTeX via latexmk on TeX Live 2026
     (full scheme), in the official texlive/texlive Docker image pinned by digest.

The .md stays the source of truth. The generated .tex ends with a checksum line; if the .tex
was edited by hand since it was generated, the script stops instead of overwriting it.
Exit code 1 on any error. Warnings (characters pdfLaTeX can't typeset, section numbering)
are printed but do not stop the build; fix them in the .md.
"""

import argparse
import hashlib
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _chrome import run_chrome  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "lecture-template.tex"
CYR = re.compile(r"[А-Яа-яЁё]")

# TeX Live 2026, full scheme: the distribution Overleaf compiles new projects with (Oct 2026).
# Pinned by digest so builds are reproducible; when Overleaf moves to a new TeX Live year,
# pin the new `latest-full` digest from hub.docker.com/r/texlive/texlive.
TEXLIVE_IMAGE = "texlive/texlive@sha256:a7ae4dfa9d521b5db14446872fa488b839021d1f604d0a3c74461784895f2a67"

# What pdfLaTeX with T2A + utf8 can set in running text besides ASCII and Cyrillic: tested in
# the TeX Live image. Greek, ≤ ≥ ≈ ≠ ∈ ∞ ∂ ℝ ′ and the minus sign U+2212 fail and belong in $…$.
TEXT_OK = set("«»„“”‘’‚—–‑‐…№§°×±·•½¼→←©€™‰¬µ\u00a0")

warnings = []


def warn(msg):
    warnings.append(msg)


# ---------------------------------------------------------------- inline conversion

MATH_RE = re.compile(r"\$\$(.+?)\$\$|\$((?:[^\s\\$])|(?:[^\s$][^$]*?[^\s\\$]))\$", re.S)
TEXT_CMDS = re.compile(r"\\(?:text|textbf|textit|textrm|mbox|operatorname\*?|mathrm|mathbf)\s*\{")


def strip_text_groups(tex):
    """Remove \\text{...}-like groups (balanced braces) so we can look for bare Cyrillic."""
    out, i = [], 0
    while True:
        m = TEXT_CMDS.search(tex, i)
        if not m:
            out.append(tex[i:])
            return "".join(out)
        out.append(tex[i:m.start()])
        depth, j = 1, m.end()
        while j < len(tex) and depth:
            depth += {"{": 1, "}": -1}.get(tex[j], 0)
            j += 1
        i = j


def math_problem(tex):
    """Why pdfLaTeX would choke on this formula (KaTeX happily renders it), or None."""
    bare = strip_text_groups(tex)
    if CYR.search(bare):
        return "Cyrillic outside \\text{} in math"
    odd = sorted({c for c in bare if ord(c) > 127})
    if odd:
        return f"Unicode {''.join(odd)} in math (use \\alpha, \\to, \\le, … instead)"
    return None


def text_problem(text):
    """Characters in running text that pdfLaTeX (T2A + utf8) cannot typeset, or None."""
    odd = sorted({c for c in text if ord(c) > 127 and not CYR.match(c) and c not in TEXT_OK})
    return f"{''.join(odd)} in text (put symbols in $…$, e.g. $\\to$, $\\alpha$)" if odd else None


def check_math(tex):
    why = math_problem(tex)
    if why:
        warn(f"{why}: {tex.strip()[:80]}")


def escape_text(s):
    repl = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "&": r"\&", "%": r"\%",
            "#": r"\#", "_": r"\_", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
            "$": r"\$"}
    return "".join(repl.get(c, c) for c in s)


def inline(s):
    """Markdown inline -> LaTeX. Math is protected first, then text is escaped, then markup."""
    s = s.replace(r"\$", "\x02")
    slots = []

    def keep(latex):
        slots.append(latex)
        return f"\x00{len(slots) - 1}\x00"

    def math(m):
        if m.group(1) is not None:
            check_math(m.group(1))
            return keep(r"\[" + m.group(1).strip() + r"\]")
        check_math(m.group(2))
        return keep("$" + m.group(2) + "$")

    s = MATH_RE.sub(math, s)
    why = text_problem(re.sub(r"\x00\d+\x00", "", s))
    if why:
        warn(f"{why}: {re.sub(chr(0) + r'\d+' + chr(0), '…', s).strip()[:80]}")
    s = re.sub(r"`([^`]+)`", lambda m: keep(r"\texttt{" + escape_text(m.group(1)) + "}"), s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               lambda m: keep(r"\href{" + m.group(2).replace("%", r"\%").replace("#", r"\#") + "}{")
               + m.group(1) + keep("}"), s)
    if re.search(r"<(?!!--)[a-zA-Z/][^>]*>", s):
        warn(f"HTML tag dropped: {s.strip()[:80]}")
        s = re.sub(r"<(?!!--)[a-zA-Z/][^>]*>", "", s)
    s = escape_text(s)
    s = re.sub(r"\*\*\*(.+?)\*\*\*", r"\\textbf{\\emph{\1}}", s, flags=re.S)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s, flags=re.S)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\\emph{\1}", s, flags=re.S)
    s = s.replace("\x02", r"\$")
    while "\x00" in s:
        s = re.sub(r"\x00(\d+)\x00", lambda m: slots[int(m.group(1))], s)
    return s


def split_comments(text):
    """Pull <!-- ... --> out of a block; return (text, [comment lines])."""
    comments = []

    def grab(m):
        comments.extend(line.strip() for line in m.group(1).strip().splitlines())
        return ""

    return re.sub(r"<!--(.*?)-->", grab, text, flags=re.S), comments


def tex_comments(lines):
    return "\n".join("% " + line for line in lines if line)


# ---------------------------------------------------------------- block conversion

BLOCK_START = re.compile(r"^(#{1,6}\s|>|\$\$|\||!\[|---\s*$|\*\*\*\s*$|[-*+]\s|\d+[.)]\s|<!--)")


def convert(md, md_path, fig_pdf):
    lines = md.splitlines()
    out, title, i, n = [], None, 0, len(lines)
    sec = sub = 0

    def para_until(j):
        buf = []
        while j < n and lines[j].strip() and not (buf and BLOCK_START.match(lines[j])):
            buf.append(lines[j].strip())
            j += 1
        return " ".join(buf), j

    while i < n:
        line = lines[i]
        st = line.strip()
        if not st:
            i += 1
            continue

        # HTML comment block
        if st.startswith("<!--"):
            buf = [line]
            while "-->" not in buf[-1] and i + 1 < n:
                i += 1
                buf.append(lines[i])
            rest, comments = split_comments("\n".join(buf))
            out.append(tex_comments(comments))
            if rest.strip():
                out.append(inline(rest.strip()))
            i += 1
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", st)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1 and title is None:
                title = text
            elif level == 2:
                sec, sub = sec + 1, 0
                num = re.match(r"^(\d+)\.?\s+(.*)$", text)
                if num:
                    if int(num.group(1)) != sec:
                        warn(f"Section '{text}' is numbered {num.group(1)} in the .md but will be {sec} in LaTeX")
                    text = num.group(2)
                out.append(r"\section{" + inline(text) + "}")
            elif level == 3:
                sub += 1
                num = re.match(r"^(\d+)\.(\d+)\.?\s+(.*)$", text)
                if num:
                    if (int(num.group(1)), int(num.group(2))) != (sec, sub):
                        warn(f"Subsection '{text}' will be numbered {sec}.{sub} in LaTeX")
                    text = num.group(3)
                out.append(r"\subsection{" + inline(text) + "}")
            else:
                out.append(r"\subsubsection*{" + inline(text) + "}")
            i += 1
            continue

        # blockquote
        if st.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            paras = [p.replace("\n", " ").strip() for p in re.split(r"\n\s*\n", "\n".join(buf)) if p.strip()]
            body = "\n\n".join(inline(p) for p in paras)
            joined = " ".join(paras)
            if "Необходимые знания" in joined or "О чем лекция" in joined or "О чём лекция" in joined:
                out.append("\\begin{lectureabout}\n" + body.replace("\n\n", "\n\n\\smallskip\n") + "\n\\end{lectureabout}")
            elif joined.startswith("**Черновик"):
                out.append("\\begin{draftnote}\n" + body + "\n\\end{draftnote}")
            else:
                out.append("\\begin{quote}\n" + body + "\n\\end{quote}")
            continue

        # display math block
        if st.startswith("$$"):
            buf = [st[2:]]
            if not (st.endswith("$$") and len(st) > 4):
                i += 1
                while i < n and not lines[i].strip().endswith("$$"):
                    buf.append(lines[i])
                    i += 1
                if i < n:
                    buf.append(lines[i].strip()[:-2])
            else:
                buf = [st[2:-2]]
            content = "\n".join(buf).strip()
            check_math(content)
            out.append(("math", "\\[\n" + content + "\n\\]"))
            i += 1
            continue

        # table
        if st.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            cells = [split_row(r) for r in rows if not re.match(r"^\|[\s:|-]+\|?$", r)]
            ncol = max(len(c) for c in cells)
            spec = "|" + "|".join("c" * 1 for _ in range(ncol)) + "|"
            body = " \\\\ \\hline\n".join(" & ".join(inline(c) for c in row + [""] * (ncol - len(row))) for row in cells)
            out.append("\\begin{center}\n\\begin{tabular}{" + spec + "}\n\\hline\n" + body + " \\\\ \\hline\n\\end{tabular}\n\\end{center}")
            continue

        # figure (+ optional caption paragraph)
        m = re.match(r"^!\[([^\]]*)\]\(([^)\s]+)\)\s*$", st)
        if m:
            src = m.group(2)
            pdf_rel, width = fig_pdf(src)
            i += 1
            while i < n and not lines[i].strip():
                i += 1
            caption = ""
            if i < n and re.match(r"^\*Рис\.", lines[i].strip()):
                cap, i = para_until(i)
                caption = inline(cap.strip().strip("*"))
            fig = ["\\begin{figure}[H]", "\\centering",
                   f"\\includegraphics[width={width:.2f}\\textwidth]{{{pdf_rel}}}"]
            if caption:
                fig.append("\\caption*{" + caption + "}")
            fig.append("\\end{figure}")
            out.append("\n".join(fig))
            continue

        # horizontal rule / end mark
        if re.match(r"^(---|\*\*\*)\s*$", st):
            i += 1
            while i < n and not lines[i].strip():
                i += 1
            if i < n and re.match(r"^\*Конец лекции", lines[i].strip()):
                end, i = para_until(i)
                out.append("\\par\\bigskip\\noindent\\rule{\\textwidth}{0.4pt}\\par\\noindent " + inline(end))
            else:
                out.append("\\par\\medskip\\noindent\\rule{\\textwidth}{0.4pt}\\par\\medskip")
            continue

        # lists
        m = re.match(r"^([-*+]|\d+[.)])\s+", st)
        if m:
            ordered = m.group(1)[0].isdigit()
            items = []
            while i < n and lines[i].strip():
                lm = re.match(r"^\s*([-*+]|\d+[.)])\s+(.*)$", lines[i])
                if lm and not lines[i].startswith("    "):
                    items.append(lm.group(2))
                elif items:
                    items[-1] += " " + lines[i].strip()
                i += 1
            env = "enumerate" if ordered else "itemize"
            out.append(f"\\begin{{{env}}}\n" + "\n".join("\\item " + inline(it) for it in items) + f"\n\\end{{{env}}}")
            continue

        # paragraph
        text, i = para_until(i)
        text, comments = split_comments(text)
        if text.strip():
            out.append(("para", inline(text.strip())))
        if comments:
            out.append(tex_comments(comments))

    if title is None:
        warn("No '# Лекция N. Тема' title found")
        title = md_path.stem
    return title, join_blocks(out)


def join_blocks(blocks):
    """Blank line between blocks, except around display math inside a sentence: the formula
    stays in the paragraph before it, and text after it that starts in lower case (or with
    punctuation) continues that paragraph instead of starting a new, indented one."""
    parts, prev = [], None
    for b in blocks:
        kind, text = b if isinstance(b, tuple) else ("other", b)
        if not text:
            continue
        glue = (kind == "math" and prev == "para") or \
               (kind == "para" and prev == "math" and re.match(r"^[a-zа-яё,.;:)\-—]", text))
        parts.append(("\n" if glue else "\n\n") + text if parts else text)
        prev = kind
    return "".join(parts)


def split_row(row):
    row = row.strip().strip("|")
    cells, cur, in_math = [], "", False
    for ch in row:  # a | inside $...$ is not a column separator
        if ch == "$":
            in_math = not in_math
        if ch == "|" and not in_math:
            cells.append(cur.strip())
            cur = ""
        else:
            cur += ch
    cells.append(cur.strip())
    return cells


# ---------------------------------------------------------------- figures

def svg_size(svg_text):
    w = re.search(r'<svg[^>]*\bwidth="([\d.]+)', svg_text)
    h = re.search(r'<svg[^>]*\bheight="([\d.]+)', svg_text)
    if w and h:
        return float(w.group(1)), float(h.group(1))
    vb = re.search(r'viewBox="[\d.\-]+\s+[\d.\-]+\s+([\d.]+)\s+([\d.]+)"', svg_text)
    if vb:
        return float(vb.group(1)), float(vb.group(2))
    return 640.0, 400.0


def svg_to_pdf(svg: Path, pdf: Path):
    w, h = svg_size(svg.read_text(encoding="utf-8"))
    page = (f"<!doctype html><html><head><meta charset='utf-8'><style>"
            f"@page{{size:{w}px {h}px;margin:0}}html,body{{margin:0;padding:0;overflow:hidden;"
            f"width:{w}px;height:{h}px}}img{{display:block;width:{w}px;height:{h}px}}</style></head>"
            f"<body><img src='{html.escape(svg.resolve().as_uri())}'></body></html>")
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "fig.html"
        p.write_text(page, encoding="utf-8")
        run_chrome(["--virtual-time-budget=5000", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", p.as_uri()])
    if not pdf.exists():
        raise RuntimeError(f"could not convert {svg}")
    pages = re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes())
    if len(pages) > 1:
        warn(f"{svg.name}: converted to {len(pages)} PDF pages (figure overflowed its size?)")
    return w


# ---------------------------------------------------------------- build

def docker_ok():
    return subprocess.run(["docker", "info"], capture_output=True, check=False).returncode == 0


def ensure_texlive():
    """Docker running and the pinned TeX Live image present (pulled once, ~2.7 GB)."""
    if not shutil.which("docker"):
        sys.exit("ERROR: docker not found; the final PDF is built in the TeX Live Docker image.")
    if not docker_ok() and sys.platform == "darwin":
        print("Starting Docker Desktop…")
        subprocess.run(["open", "-a", "Docker"], check=False)
        for _ in range(60):
            time.sleep(2)
            if docker_ok():
                break
    if not docker_ok():
        sys.exit("ERROR: Docker is not running. Start Docker Desktop and run finalize.py again.")
    if subprocess.run(["docker", "image", "inspect", TEXLIVE_IMAGE], capture_output=True,
                      check=False).returncode != 0:
        print("Pulling TeX Live 2026 (one-time download, ~2.7 GB)…")
        if subprocess.run(["docker", "pull", TEXLIVE_IMAGE], check=False).returncode != 0:
            sys.exit("ERROR: could not pull the TeX Live image.")


def compile_pdf(tex_path: Path, pdf_dir: Path):
    """pdfLaTeX via latexmk inside the TeX Live image, as Overleaf compiles by default."""
    ensure_texlive()
    build = tex_path.parent / ".build"
    res = subprocess.run(["docker", "run", "--rm", "-v", f"{tex_path.parent}:/work", "-w", "/work",
                          TEXLIVE_IMAGE, "latexmk", "-pdf", "-interaction=nonstopmode",
                          "-halt-on-error", "-file-line-error", "-outdir=.build", tex_path.name],
                         capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    log_file = build / (tex_path.stem + ".log")
    log = log_file.read_text(encoding="utf-8", errors="replace") if log_file.exists() else ""
    for line in re.findall(r"^Overfull \\hbox.*$", log, re.M):
        print(f"LAYOUT: {line.strip()}")
    pdf = build / (tex_path.stem + ".pdf")
    if res.returncode != 0 or not pdf.exists():
        errs = re.findall(r"^(?:\S+\.tex:\d+:.*|! .*)$(?:\n.*){0,2}", log, re.M)
        print("\n".join(errs[:10]) or (res.stdout + res.stderr)[-3000:])
        sys.exit(f"ERROR: LaTeX compilation failed (full log: {log_file}).")
    out = pdf_dir / pdf.name
    shutil.move(str(pdf), str(out))
    shutil.rmtree(build, ignore_errors=True)
    return out


def overleaf_zip(tex_path: Path, figures: list, zip_path: Path):
    """The .tex plus its figure PDFs, ready for Overleaf's New Project → Upload Project."""
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(tex_path, tex_path.name)
        for f in figures:
            z.write(tex_path.parent / f, f)
    return zip_path


def checksum(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown")
    ap.add_argument("--tex-dir", help="default: the lecture folder (where the .md is)")
    ap.add_argument("--pdf-dir", help="default: the lecture folder (where the .md is)")
    ap.add_argument("--tex-only", action="store_true")
    ap.add_argument("--overleaf-zip", action="store_true", help="also write lecture-NN-overleaf.zip in the lecture folder")
    ap.add_argument("--force", action="store_true", help="overwrite a hand-edited .tex")
    a = ap.parse_args()

    md_path = Path(a.markdown).resolve()
    tex_dir = Path(a.tex_dir).resolve() if a.tex_dir else md_path.parent
    pdf_dir = Path(a.pdf_dir).resolve() if a.pdf_dir else md_path.parent
    tex_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    tex_path = tex_dir / (md_path.stem + ".tex")

    used_figures = []

    def fig_pdf(src):
        """The figure as a PDF at the same relative path under tex_dir (by default: next to the SVG)."""
        svg = (md_path.parent / src).resolve()
        if not svg.exists():
            raise SystemExit(f"ERROR: figure not found: {src}")
        if not svg.is_relative_to(md_path.parent):
            raise SystemExit(f"ERROR: figure outside the lecture folder: {src} (keep figures in figures/)")
        rel = svg.relative_to(md_path.parent).with_suffix(".pdf")
        dest = tex_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if svg.suffix.lower() != ".svg":
            rel = rel.with_suffix(svg.suffix)
            if (tex_dir / rel).resolve() != svg:
                shutil.copy(svg, tex_dir / rel)
            used_figures.append(rel.as_posix())
            return rel.as_posix(), 0.8
        if not dest.exists() or dest.stat().st_mtime < svg.stat().st_mtime:
            svg_to_pdf(svg, dest)
        used_figures.append(rel.as_posix())
        w, _ = svg_size(svg.read_text(encoding="utf-8"))
        return rel.as_posix(), min(1.0, w / 760.0)

    title, body = convert(md_path.read_text(encoding="utf-8"), md_path, fig_pdf)
    running = re.sub(r"\s+", " ", title)
    tex = (TEMPLATE.read_text(encoding="utf-8")
           .replace("%%TITLE%%", inline(title))
           .replace("%%RUNNING%%", inline(running))
           .replace("%%BODY%%", body))
    header = (f"% Сгенерировано из {md_path.name} скриптом lecture-notes/scripts/finalize.py.\n"
              f"% Правки вносите в .md и запускайте finalize.py заново.\n")
    tex = header + tex

    if tex_path.exists() and not a.force:
        old = tex_path.read_text(encoding="utf-8")
        m = re.search(r"\n% checksum: ([0-9a-f]{40})\n?$", old)
        if not m or checksum(old[:m.start() + 1]) != m.group(1):
            sys.exit(f"ERROR: {tex_path} was edited by hand since it was generated. "
                     "Move those edits into the .md, or rerun with --force to overwrite them.")
    tex_path.write_text(tex + f"% checksum: {checksum(tex)}\n", encoding="utf-8")
    print(f"TeX: {tex_path}")

    for w in warnings:
        print(f"WARNING: {w}")

    if a.overleaf_zip:
        z = overleaf_zip(tex_path, used_figures, md_path.parent / (md_path.stem + "-overleaf.zip"))
        print(f"Overleaf zip: {z}")
    if a.tex_only:
        return
    print(f"PDF: {compile_pdf(tex_path, pdf_dir)}")


if __name__ == "__main__":
    main()
