#!/usr/bin/env python3
"""Check the text of a lecture draft for what the author's reviews keep catching.

    python3 lint_text.py docs/lecture-01/lecture-01.md
    python3 lint_text.py --selftest     # his own lecture 1 must pass every check

Reports, with line numbers:
  NO IDEA       a paragraph (or side remark) without an «Идея» callout right before it.
                Draft convention, see SKILL.md: `> **Идея.** …` before every new paragraph.
  OPEN QUESTION a «Вопрос N» callout, i.e. something the lecturer or the user still has to answer.
  REGISTER      lecture-speak from references/register-patterns.tsv (prose only).
  BEFORE DEF    a term used before the paragraph that defines it (bold term in a definition).
  SHORT         a sentence of three words or fewer — usually a spoken fragment.
  MATH IN CALLOUT  display math split over several "> " lines (renders with a literal ">").
  EDITOR LABEL  «Замечание редактора»: the book has only «Замечание» (author-rulings 29). An error.
  HEADER        «О чём лекция» with parentheses or longer than two short sentences (ruling 26).
  INTRO         more than one paragraph between the header block and § 1 (ruling 27).
  BOLD          bold outside a sentence that defines the term («… называется …») (ruling 28).
  LONG          the median sentence is longer than his (16 words in his lecture 1; author-model §8).

Everything except NO IDEA, OPEN QUESTION and EDITOR LABEL is a *candidate*: look at it, keep it
if it's right in context. The calibration is his own text: `--selftest` converts his lecture 1
(raw/reviews/lecture-01/lecture1_indices.tex) and fails if any candidate fires on it. The idea check applies only to drafts that use Идея callouts at all (a
finalized lecture has had them stripped), and not to a lecture built on the author's own text,
marked by a `<!-- author-text -->` line. Exit code is 0, except for a failed --selftest;
hook_check.py and render_preview.py call lint() directly.
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATTERNS_FILE = HERE.parent / "references" / "register-patterns.tsv"
LECTURE_RE = re.compile(r"docs/lecture-(\d\d)/lecture-\1\.md$")

IDEA_RE = re.compile(r"^\*\*Идея\.?\*\*")
# «**Вопрос 3.**», «**Вопрос 3**», «**Вопрос 9 (для пользователя).**» — any bold label starting «Вопрос».
QUESTION_RE = re.compile(r"^\*\*Вопрос(?:\s+(\d+))?[^*]*\*\*")
ASIDE_RE = re.compile(r"^[*_]{1,2}(Замечание редактора|Замечание|Предупреждение|Забегая вперёд|Забегая вперед)\.[*_]{1,2}")
ABOUT_RE = re.compile(r"Необходимые знания|О ч[её]м лекция")
EDITOR_RE = re.compile(r"Замечание редактора")
AUTHOR_TEXT_RE = re.compile(r"<!--\s*author-text\b")
DEFINES = re.compile(r"называ|будем называть|назовём|назовем", re.I)
HIS_MEDIAN_WORDS = 16          # median sentence length of his lecture 1 (author-model.md §3, §8)
DRAFT_RE = re.compile(r"^\*\*Черновик")
DISPLAY_MATH = re.compile(r"\$\$.*?\$\$", re.S)
INLINE_MATH = re.compile(r"\$[^$\n]+\$")
# "т. е.", "рис. 3" and the like don't end a sentence.
ABBREV = re.compile(r"\b(т\. ?е|т\. ?д|т\. ?п|т\. ?к|рис|см|ср|гл|с|стр|напр|им)\.(\s|$)", re.I)
# Bold words that are labels, not defined terms.
NOT_TERMS = re.compile(r"^(Идея|Вопрос|Предупреждение|Замечание|Доказательство|Черновик|Необходимые знания|О ч[её]м лекция|Важно)")


@dataclass
class Block:
    kind: str          # heading, idea, question, aside, about, draft, quote, math, figure, caption,
                       # table, list, comment, rule, end, para
    line: int          # 1-based line of the first line
    text: str
    continues: bool = False   # a prose block that continues the previous paragraph (after display math)


@dataclass
class Report:
    path: Path
    blocks: list = field(default_factory=list)
    ideas: int = 0
    no_idea: list = field(default_factory=list)        # [(line, excerpt)]
    questions: list = field(default_factory=list)      # [(number, line, excerpt)]
    register: list = field(default_factory=list)       # [(line, category, excerpt, hint)]
    before_def: list = field(default_factory=list)     # [(line, term, def_line)]
    short: list = field(default_factory=list)          # [(line, sentence)]
    old_markers: list = field(default_factory=list)    # [(line, excerpt)] leftover <!-- ПРОВЕРИТЬ … -->
    callout_math: list = field(default_factory=list)   # [line] multi-line $$ inside a blockquote
    editor_label: list = field(default_factory=list)   # [(line, excerpt)] «Замечание редактора»
    header: list = field(default_factory=list)         # [(line, why)]
    intro: list = field(default_factory=list)          # [(line, number of intro paragraphs)]
    bold: list = field(default_factory=list)           # [(line, term)] bold outside a defining sentence
    median_words: float = 0
    author_text: bool = False


def blocks_of(md: str):
    """Split the Markdown into blocks, the way the drafts are written (blank-line separated)."""
    lines = md.splitlines()
    out, i, n = [], 0, len(lines)
    while i < n:
        st = lines[i].strip()
        if not st:
            i += 1
            continue
        start = i
        if st.startswith("<!--"):
            while "-->" not in lines[i] and i + 1 < n:
                i += 1
            out.append(Block("comment", start + 1, "\n".join(lines[start:i + 1])))
            i += 1
            continue
        if st.startswith("$$"):
            if not (st.endswith("$$") and len(st) > 4):
                i += 1
                while i < n and not lines[i].strip().endswith("$$"):
                    i += 1
            out.append(Block("math", start + 1, "\n".join(lines[start:i + 1])))
            i += 1
            continue
        if st.startswith(">"):
            while i < n and lines[i].strip().startswith(">"):
                i += 1
            body = "\n".join(re.sub(r"^\s*>\s?", "", l) for l in lines[start:i]).strip()
            first = body.lstrip()
            kind = ("idea" if IDEA_RE.match(first) else "question" if QUESTION_RE.match(first)
                    else "aside" if ASIDE_RE.match(first) else "about" if ABOUT_RE.search(body)
                    else "draft" if DRAFT_RE.match(first) else "quote")
            out.append(Block(kind, start + 1, body))
            continue
        if st.startswith("#"):
            out.append(Block("heading", start + 1, st))
            i += 1
            continue
        if re.match(r"^!\[[^\]]*\]\([^)]+\)\s*$", st):
            out.append(Block("figure", start + 1, st))
            i += 1
            continue
        if re.match(r"^(---|\*\*\*)\s*$", st):
            out.append(Block("rule", start + 1, st))
            i += 1
            continue
        while i < n and lines[i].strip() and not lines[i].strip().startswith(("$$", ">", "<!--")):
            i += 1
        text = "\n".join(lines[start:i])
        if st.startswith("|"):
            kind = "table"
        elif re.match(r"^\*Рис\.", st):
            kind = "caption"
        elif re.match(r"^\*Конец лекции", st):
            kind = "end"
        elif re.match(r"^([-*+]|\d+[.)])\s+", st):
            kind = "list"
        else:
            kind = "para"
        b = Block(kind, start + 1, text)
        if kind == "para":
            # Prose right after a display formula or a table continues the same paragraph
            # ("где …", "— функция …", or a new sentence on the same point). A new paragraph
            # after a formula gets its own Идея callout, so it isn't mistaken for this.
            b.continues = bool(out) and out[-1].kind in ("math", "table")
        out.append(b)
    return out


def prose(text: str) -> str:
    """Text with math, links' targets, emphasis markers and comments removed, for word checks."""
    t = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    t = DISPLAY_MATH.sub(" ", t)
    t = INLINE_MATH.sub(" X ", t)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\]\([^)]*\)", "]", t)
    t = t.replace("**", "").replace("*", "")
    return t


def load_patterns():
    pats = []
    if PATTERNS_FILE.exists():
        for raw in PATTERNS_FILE.read_text(encoding="utf-8").splitlines():
            if not raw.strip() or raw.startswith("#"):
                continue
            parts = raw.split("\t")
            if len(parts) >= 2:
                try:
                    pats.append((re.compile(parts[0], re.I), parts[1], parts[2] if len(parts) > 2 else ""))
                except re.error as e:
                    print(f"bad pattern in {PATTERNS_FILE.name}: {parts[0]!r}: {e}", file=sys.stderr)
    return pats


def stem_pattern(term: str):
    words = re.findall(r"[А-Яа-яЁёA-Za-z-]+", term)
    if not words:
        return None
    stems = [w[:max(4, len(w) - 3)] for w in words]
    return re.compile(r"(?<![\w-])" + r"\w*[\s-]+".join(re.escape(s) for s in stems) + r"\w*", re.I)


def lint(path: Path) -> Report:
    md = path.read_text(encoding="utf-8")
    rep = Report(path)
    rep.blocks = blocks_of(md)
    patterns = load_patterns()

    rep.ideas = sum(b.kind == "idea" for b in rep.blocks)
    rep.author_text = bool(AUTHOR_TEXT_RE.search(md))

    for b in rep.blocks:
        if b.kind in ("aside", "quote", "para") and EDITOR_RE.search(b.text):
            rep.editor_label.append((b.line, b.text.replace("\n", " ")[:90]))
        if b.kind == "about":
            m = re.search(r"О ч[её]м лекция:?\**:?\s*(.*)", b.text, re.S)
            if m:
                about = prose(m.group(1)).strip()
                if "(" in about:
                    rep.header.append((b.line, "parentheses in «О чём лекция»: list the topics, no glosses"))
                if len(about) > 220:
                    rep.header.append((b.line, f"«О чём лекция» is {len(about)} characters; his is two short sentences (~150)"))

    first_sec = next((b.line for b in rep.blocks if b.kind == "heading" and b.text.startswith("## ")), None)
    last_about = max((b.line for b in rep.blocks if b.kind == "about"), default=None)
    if first_sec and last_about:
        intro = [b for b in rep.blocks if last_about < b.line < first_sec and b.kind == "para" and not b.continues]
        if len(intro) > 1:
            rep.intro.append((intro[0].line, len(intro)))
    prev = None                                  # last block that isn't a comment or a question
    for b in rep.blocks:
        if b.kind == "question":
            m = QUESTION_RE.match(b.text)
            rep.questions.append((int(m.group(1) or 0), b.line, b.text.replace("\n", " ")[:160]))
        if b.kind == "comment" and "ПРОВЕРИТЬ" in b.text:
            rep.old_markers.append((b.line, b.text.replace("\n", " ")[:160]))
        needs_idea = (b.kind == "para" and not b.continues) or b.kind == "aside"
        if needs_idea and not (prev and prev.kind == "idea"):
            rep.no_idea.append((b.line, prose(b.text).strip().replace("\n", " ")[:70]))
        if b.kind not in ("comment", "question"):
            prev = b

    # A $$ block split over several "> " lines renders with literal ">" on the website
    # (markdown-it-texmath reads the raw lines); inside a callout, display math goes on one line.
    for no, line in enumerate(md.splitlines(), 1):
        if re.match(r"^\s*>\s*\$\$\s*$", line):
            rep.callout_math.append(no)

    # Word checks run on the book text: paragraphs, lists, side remarks, captions.
    book = [b for b in rep.blocks if b.kind in ("para", "list", "aside", "caption", "quote")]
    for b in book:
        for k, line in enumerate(b.text.splitlines()):
            plain = prose(line)
            for rx, cat, hint in patterns:
                for m in rx.finditer(plain):
                    lo = max(0, m.start() - 30)
                    rep.register.append((b.line + k, cat, plain[lo:m.end() + 30].strip(), hint))
        flat = ABBREV.sub(lambda m: m.group(0).replace(". ", ".\u00a0").replace(".", "\u2024"), prose(b.text).replace("\n", " "))
        prev_s = ""
        for s in re.split(r"(?<=[.?!])\s+", flat):
            s = s.strip().replace("\u2024", ".")
            words = re.findall(r"[\wА-Яа-яЁё-]+", s)
            after_question, prev_s = prev_s.endswith("?"), s
            # Short, math-free, starting a sentence of its own: «Вот и всё.», «Обычно пишут самую короткую.»
            # A short answer right after a question is his («Имеет ли смысл писать a = b? Да.»).
            if (s.endswith(".") and 0 < len(words) <= 3 and "X" not in words and not after_question
                    and re.match(r"^[А-ЯЁA-Z«]", s) and not re.match(r"^(Рис|Замечание|Предупреждение|Доказательство|Забегая|Идея|Вопрос)", s)):
                rep.short.append((b.line, s))

    # Bold outside the sentence that defines the term, and the median sentence length. A paragraph
    # that continues after a display formula is the same sentence, so it is joined to the one before.
    texts = []
    for b in rep.blocks:
        if b.kind in ("para", "aside", "list"):
            if b.kind == "para" and b.continues and texts:
                texts[-1] = (texts[-1][0], texts[-1][1] + " X " + b.text.replace("\n", " "))
            else:
                texts.append((b.line, b.text.replace("\n", " ")))
    lengths = []
    for line, text in texts:
        flat = ABBREV.sub(lambda m: m.group(0).replace(".", "\u2024"), text)
        for s in re.split(r"(?<=[.?!])\s+", flat):
            words = re.findall(r"[\wА-Яа-яЁё-]+", prose(s))
            if len(words) > 1:
                lengths.append(len(words))
            for term in re.findall(r"\*\*([^*]+)\*\*", s):
                if not NOT_TERMS.match(term) and not DEFINES.search(s):
                    rep.bold.append((line, term))
    if lengths:
        lengths.sort()
        rep.median_words = lengths[len(lengths) // 2]

    # Terms used before the paragraph that defines them.
    for b in rep.blocks:
        if b.kind not in ("para", "aside"):
            continue
        for term in re.findall(r"\*\*([^*]+)\*\*", b.text):
            if NOT_TERMS.match(term):
                continue
            rx = stem_pattern(term)
            if not rx:
                continue
            for e in rep.blocks:
                if e.line >= b.line:
                    break
                if e.kind in ("para", "aside", "list", "caption") and rx.search(prose(e.text)):
                    rep.before_def.append((e.line, term, b.line))
                    break
    return rep


def candidates(rep):
    """Every candidate line of a report, as printed (EDITOR LABEL included; ideas/questions not)."""
    out = [f"{line}: EDITOR LABEL: «Замечание редактора» is not used in the book; write «Замечание», and record "
           f"that it is ours in the draft's Идея callout and the report (ruling 29): {ex}" for line, ex in rep.editor_label]
    out += [f"{line}: HEADER: {why}" for line, why in rep.header]
    out += [f"{line}: INTRO: {n} paragraphs before § 1; his introduction is one paragraph (ruling 27)" for line, n in rep.intro]
    out += [f"{line}: BEFORE DEF: «{term}» is defined at line {d}" for line, term, d in rep.before_def]
    out += [f"{line}: REGISTER [{cat}]: …{ex}… → {hint}" for line, cat, ex, hint in rep.register]
    out += [f"{line}: BOLD: «{term}» is bold outside a defining sentence; bold is only for the term being defined (ruling 28)"
            for line, term in rep.bold]
    out += [f"{line}: SHORT: {s}" for line, s in rep.short]
    if rep.median_words > HIS_MEDIAN_WORDS + 2:
        out.append(f"LONG: median sentence {rep.median_words} words; his lecture 1: {HIS_MEDIAN_WORDS}. "
                   "Split long explanations; lead into formulas with short sentences («Тогда:», «Реализуем его:»).")
    return out


def selftest():
    """His own lecture 1 is the standard: every candidate check must stay silent on it."""
    from tex_to_md import convert
    root = next((d for d in HERE.parents if (d / "raw").is_dir()), None)
    tex = root / "raw/reviews/lecture-01/lecture1_indices.tex" if root else None
    if not tex or not tex.exists():
        sys.exit("selftest: raw/reviews/lecture-01/lecture1_indices.tex not found (raw/ is not in git)")
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        md = Path(d) / "lecture-01.md"
        md.write_text(convert(tex.read_text(encoding="utf-8")), encoding="utf-8")
        found = candidates(lint(md))
    if found:
        print(f"selftest FAILED: {len(found)} check(s) fire on his own text, so they ban what he writes. "
              "Narrow them (register-patterns.tsv, lint_text.py):")
        print("\n".join("  " + f for f in found))
        sys.exit(1)
    print(f"selftest OK: no check fires on his lecture 1 ({tex.name}).")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--selftest":
        return selftest()
    for name in sys.argv[1:]:
        rep = lint(Path(name))
        print(f"== {name}")
        if rep.ideas:
            for line, ex in rep.no_idea:
                print(f"{line}: NO IDEA: {ex}…")
        elif rep.author_text:
            print("(built on the author's own text: no Идея callouts needed)")
        else:
            print("(no Идея callouts: fine for a finalized lecture; a draft under review needs them)")
        for num, line, ex in rep.questions:
            print(f"{line}: OPEN QUESTION {num}: {ex}")
        for line in rep.callout_math:
            print(f"{line}: MATH IN CALLOUT: write it on one line, `> $$ … $$` (split over lines it shows a literal '>' on the site)")
        for line, ex in rep.old_markers:
            print(f"{line}: OLD MARKER (turn into a Вопрос callout): {ex}")
        for c in candidates(rep):
            print(c)
        print(f"Summary: {rep.ideas} ideas, {len(rep.no_idea) if rep.ideas else '-'} paragraphs without one, "
              f"{len(rep.questions)} open questions, {len(rep.register)} register candidates, "
              f"{len(rep.before_def)} before-definition, {len(rep.short)} short sentences, "
              f"{len(rep.bold)} bold, median sentence {rep.median_words} words (his: {HIS_MEDIAN_WORDS})"
              + (f", {len(rep.editor_label)} EDITOR LABEL" if rep.editor_label else "") + ".")


if __name__ == "__main__":
    main()
