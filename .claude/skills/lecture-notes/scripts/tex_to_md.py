#!/usr/bin/env python3
"""Convert the lecturer's own LaTeX (his lecture 1, `raw/reviews/lecture-01/lecture1_indices.tex`) to
the draft Markdown of this skill.

    python3 tex_to_md.py raw/reviews/lecture-01/lecture1_indices.tex > lecture-01.md

Used by `lint_text.py --selftest` (his text is the standard, so no check may fire on it) and as the
starting point when a lecture is rebuilt from his text. It handles what his file uses and nothing
more:
- the body between \\begin{document} and \\end{document} (what follows \\end{document} is cut by
  him, and so is every commented-out line);
- his macros \\R, \\N, \\eqdef, \\d;
- the title, the quote blocks of the header, \\section / \\subsection;
- \\[…\\] display math, written on one line;
- tabular → a display `array` (hlines dropped);
- \\textbf, \\emph, and ---/-- as dashes.

Check the result against the PDF by eye: this is a converter for one known file, not general LaTeX.
"""
import re
import sys

MACROS = {r"\R": r"\mathbb{R}", r"\N": r"\mathbb{N}", r"\eqdef": r"\;\equiv\;", r"\d": r"\delta"}


def convert(src: str) -> str:
    body = src.split("\\begin{document}", 1)[1].split("\\end{document}", 1)[0]
    lines = []
    for line in body.splitlines():
        if line.lstrip().startswith("%"):
            continue
        lines.append(re.sub(r"(?<!\\)%.*$", "", line))
    t = "\n".join(lines)

    for k, v in MACROS.items():
        t = re.sub(re.escape(k) + r"(?![A-Za-z])", lambda m, v=v: v, t)

    t = re.sub(r"\\hline", "", t)

    def table(m):
        body = " ".join(m.group(2).replace("$", "").split())
        return "\n\n$$\\begin{array}{" + m.group(1).replace(" ", "") + "}" + body + "\\end{array}$$\n\n"

    t = re.sub(r"\\begin\{tabular\}\{([^}]*)\}(.*?)\\end\{tabular\}", table, t, flags=re.S)
    t = re.sub(r"\\begin\{center\}|\\end\{center\}|\\medskip|\\bigskip|\\noindent|\\hrule|"
               r"\\vspace\{[^}]*\}|\\thispagestyle\{[^}]*\}", "", t)
    t = re.sub(r"\\begin\{quote\}\\small\s*(.*?)\\end\{quote\}", lambda m: "> " + m.group(1).strip(), t, flags=re.S)
    t = re.sub(r"\\textbf\{\s*\\Large\s*([^}]*)\}", lambda m: "# " + m.group(1).strip(), t)

    counter = {"sec": 0, "sub": 0}

    def heading(m):
        if m.group(1) == "section":
            counter["sec"] += 1
            counter["sub"] = 0
            return f"\n## {counter['sec']}. {m.group(2)}\n"
        counter["sub"] += 1
        return f"\n### {counter['sec']}.{counter['sub']}. {m.group(2)}\n"

    t = re.sub(r"\\(section|subsection)\{([^}]*)\}", heading, t)
    t = re.sub(r"\\\[(.*?)\\\]", lambda m: "\n$$" + " ".join(m.group(1).split()) + "$$\n", t, flags=re.S)
    t = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", t)
    t = re.sub(r"\\emph\{([^}]*)\}", r"*\1*", t)
    t = t.replace("---", "—").replace("--", "–")
    t = re.sub(r"\\noindent\\emph\{(Конец лекции[^}]*)\}|\*(Конец лекции[^*]*)\*",
               lambda m: "\n*" + (m.group(1) or m.group(2)) + "*", t)
    # Inline math with a space just inside the dollars ($ a_i$) doesn't render in markdown-it.
    # Trim it: this changes nothing in the text.
    parts = re.split(r"(\$\$.*?\$\$)", t, flags=re.S)
    for k in range(0, len(parts), 2):
        parts[k] = re.sub(r"\$([^$\n]+?)\$", lambda m: "$" + m.group(1).strip() + "$", parts[k])
    t = "".join(parts)
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip() + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.stdout.write(convert(open(sys.argv[1], encoding="utf-8").read()))
