#!/usr/bin/env python3
"""Claude Code hooks of the lecture-notes skill (registered in SKILL.md's frontmatter).

    hook_check.py post   PostToolUse on Write/Edit: after every edit of a lecture draft
                         (docs/lecture-NN/lecture-NN.md), hand Claude the checklist from
                         lint_text.py plus the ask-don't-guess reminder.
    hook_check.py stop   Stop: before Claude ends a turn in which it edited a lecture draft,
                         make sure every open «Вопрос N» in that draft is named in the final
                         message (asked of the user or listed for the lecturer) and, in a
                         draft that uses Идея callouts, that no paragraph lacks one.

Hooks can't see doubt; they enforce the protocol that turns doubt into questions. The
judgment is SKILL.md's principle 8. Input is the hook JSON on stdin; output follows the
Claude Code hooks contract (additionalContext for post, decision=block for stop). Any
failure here exits 0 silently: a broken check must never block the work.
"""

import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

REMINDER = ("Ask, don't guess (lecture-notes, principle 8): any choice in this edit you weren't sure of — "
            "a reading of the transcript, the statement of an idea, a term, a reordering, a figure or caption "
            "not grounded in the sources, a definition reworded — must become a «Вопрос N» callout for the "
            "lecturer or an AskUserQuestion for the user, not a silent guess.")


def state_file(inp):
    sid = re.sub(r"[^\w-]", "", str(inp.get("session_id") or "nosession"))
    return Path(tempfile.gettempdir()) / f"lecture-notes-hook-{sid}.json"


def load_state(inp):
    try:
        return json.loads(state_file(inp).read_text(encoding="utf-8"))
    except Exception:
        return {"files": []}


def save_state(inp, st):
    try:
        if st.get("files"):
            state_file(inp).write_text(json.dumps(st), encoding="utf-8")
        else:
            state_file(inp).unlink(missing_ok=True)
    except Exception:
        pass


def post(inp):
    from lint_text import LECTURE_RE, lint
    ti = inp.get("tool_input") or {}
    fp = ti.get("file_path") or (inp.get("tool_response") or {}).get("filePath")
    if not fp or not LECTURE_RE.search(fp.replace("\\", "/")) or not Path(fp).exists():
        return
    st = load_state(inp)
    if fp not in st["files"]:
        st["files"].append(fp)
    save_state(inp, st)

    rep = lint(Path(fp))
    out = [f"lecture-notes check of {Path(fp).name} after this edit:"]
    if rep.ideas:
        if rep.no_idea:
            out.append(f"- {len(rep.no_idea)} paragraph(s) without an «Идея» callout: " +
                       "; ".join(f"line {l} «{ex[:40]}…»" for l, ex in rep.no_idea[:6]))
    elif not rep.author_text:
        out.append("- No «Идея» callouts in this draft. A draft under review needs one before every paragraph "
                   "(`> **Идея.** …`); add them when you next revise it.")
    if rep.editor_label:
        out.append("- «Замечание редактора» at line(s) " + ", ".join(str(l) for l, _ in rep.editor_label) +
                   ": the book has only «Замечание» (ruling 29). Note in the Идея callout and the report that it is ours.")
    if rep.header or rep.intro:
        out.append("- Header/intro: " + "; ".join([w for _, w in rep.header] +
                   [f"{n} intro paragraphs, his is one" for _, n in rep.intro]) + ".")
    if rep.bold:
        out.append("- Bold outside a defining sentence: " + ", ".join(f"«{t}» (line {l})" for l, t in rep.bold[:5]) + ".")
    if rep.questions:
        out.append(f"- Open questions: " + ", ".join(f"Вопрос {n} (line {l})" for n, l, _ in rep.questions) +
                   ". Name each one in your final message.")
    if rep.old_markers:
        out.append(f"- {len(rep.old_markers)} old <!-- ПРОВЕРИТЬ --> marker(s): the lecturer can't see these; "
                   "turn them into «Вопрос N» callouts.")
    if rep.callout_math:
        out.append("- Display math split over lines inside a callout (lines " + ", ".join(map(str, rep.callout_math)) +
                   "): put it on one line, `> $$ … $$`, or the site shows a literal '>'.")
    if rep.before_def:
        out.append("- Used before definition: " + "; ".join(f"«{t}» line {l} (defined at {d})" for l, t, d in rep.before_def[:5]))
    if rep.register:
        out.append(f"- {len(rep.register)} register candidate(s), e.g. " +
                   "; ".join(f"line {l} [{c}] …{ex[:40]}…" for l, c, ex, _ in rep.register[:5]) +
                   f". Full list: python3 {Path(__file__).with_name('lint_text.py')} {fp}")
    if rep.short:
        out.append("- Short sentences: " + "; ".join(f"line {l} «{s}»" for l, s in rep.short[:5]))
    if rep.median_words > 18:
        out.append(f"- Median sentence {rep.median_words} words; his lecture 1: 16. Split long explanations.")
    out.append("- Before you report: compare the changed passage with how his own text does it "
               "(references/author-model.md): structure, what is kept, his connectives, questions answered at once.")
    out.append(REMINDER)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                             "additionalContext": "\n".join(out)[:3500]}}, ensure_ascii=False))


def last_message(inp):
    msg = inp.get("last_assistant_message")
    if msg:
        return msg
    try:  # older builds: read the transcript (may lag the current turn)
        for raw in reversed(Path(inp["transcript_path"]).read_text(encoding="utf-8").splitlines()):
            ev = json.loads(raw)
            if ev.get("type") == "assistant":
                parts = ev.get("message", {}).get("content", [])
                text = "".join(p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text")
                if text:
                    return text
    except Exception:
        pass
    return None


def stop(inp):
    from lint_text import lint
    st = load_state(inp)
    if not st["files"]:
        return
    if inp.get("stop_hook_active"):
        save_state(inp, {"files": []})     # nudged once already this turn; don't loop
        return
    msg = last_message(inp)
    problems = []
    for fp in st["files"]:
        p = Path(fp)
        if not p.exists():
            continue
        rep = lint(p)
        if msg is not None:
            unnamed = [n for n, _, _ in rep.questions
                       if n and not re.search(rf"Вопрос\w*\s*№?\s*{n}(?!\d)", msg)]
            if any(n == 0 for n, _, _ in rep.questions):
                problems.append(f"{p.name}: a «Вопрос» callout has no number; number them (Вопрос 1, 2, …) and name each.")
            if unnamed:
                problems.append(f"{p.name}: open question(s) not named in your final message: " +
                                ", ".join(f"Вопрос {n}" for n in unnamed) +
                                ". For each, either ask the user now (AskUserQuestion) if they can decide it, or list it "
                                "as «Вопрос N — …» for the lecturer.")
        if rep.ideas and rep.no_idea:
            problems.append(f"{p.name}: {len(rep.no_idea)} paragraph(s) still without an «Идея» callout (lines " +
                            ", ".join(str(l) for l, _ in rep.no_idea[:10]) + ").")
        if rep.old_markers:
            problems.append(f"{p.name}: {len(rep.old_markers)} <!-- ПРОВЕРИТЬ --> marker(s) the lecturer can't see; "
                            "turn them into «Вопрос N» callouts and name them.")
    if problems:
        print(json.dumps({"decision": "block",
                          "reason": "lecture-notes: before finishing —\n" + "\n".join(problems)}, ensure_ascii=False))
    else:
        save_state(inp, {"files": []})


def main():
    try:
        mode = sys.argv[1] if len(sys.argv) > 1 else ""
        inp = json.loads(sys.stdin.read() or "{}")
        {"post": post, "stop": stop}.get(mode, lambda _: None)(inp)
    except Exception as e:  # never block work because the checker broke
        print(f"lecture-notes hook_check: {e}", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
