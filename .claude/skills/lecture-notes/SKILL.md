---
name: lecture-notes
description: Writes up lectures of the ТЕНЗОРЫ (tensors) course in this project as finished Russian lecture notes built from the lecture's handwritten notes (raw/handnotes) and its Whisper transcript (raw/transcipts), in the style of the "Лекция 1. Индексы" example. Drafts and revisions happen in Markdown with KaTeX math and SVG illustrations; once approved, the lecture is finalized as LaTeX (.tex) and PDF. Use whenever the user asks to write up, make notes or a конспект for, redo, revise, illustrate or finalize a lecture of this course — by number ("lecture 7", "лекция 4"), by topic ("the tangent space lecture", "Леви-Чивита"), or in bulk ("all lectures that have transcripts") — when they ask for the .tex/.pdf of a lecture, and when a transcript or handnote arrives for a lecture that so far has only a draft. Prefer this over the general study-kb adapt-recordings / adapt-material skills for anything belonging to this tensors course.
---

# Lecture notes for the ТЕНЗОРЫ course

This skill turns one lecture's raw material into a finished written lecture in Russian:

| Input | Where | What it gives you |
|---|---|---|
| Handwritten notes | `raw/handnotes/N <тема>_<YYMMDD_HHMMSS>.pdf` | What was on the board: formulas, diagrams, the order of topics, what the lecturer stressed |
| Transcript | `raw/transcipts/<folder>/` (`.txt`, `.srt`, `.vtt`, `.json`, `.tsv` from Whisper) | What the lecturer *said*: explanations, motivation, analogies, warnings |
| Target style | `raw/examples/Лекция_1__Индексы_*.pdf` | The finished lecture 1 — the standard to match (and to improve on with illustrations) |

The work has two stages: **draft** in Markdown, revised with the user as often as needed, then **final** as .tex and .pdf once the user approves.

```
docs/
  lecture-NN/                one folder per lecture, everything for it inside
    lecture-NN.md            ← draft: written and revised here (the source of truth)
    figures/*.svg            ← figures, each with the .py that computes it (+ .pdf made at finalize)
    lecture-NN.tex           ← final, generated from the .md by scripts/finalize.py
    lecture-NN.pdf           ← final, compiled from the .tex (pdfLaTeX, TeX Live 2026, as on Overleaf)
```

`NN` is two digits: `docs/lecture-04/lecture-04.md`. A lecture folder is also a complete Overleaf project. Nothing for one lecture lives outside its folder, and nothing of another lecture lives inside it.

## Philosophy

These principles come first. The workflow and rules below are applications of them; when a situation isn't covered, reason from here.

**1. The lecturer is the author; we are the editor.** The content, the order of ideas, the emphasis, the analogies and the opinions belong to the lecturer. Our job is to make what was said readable, not to write our own chapter on the topic. This matters because the notes are a record of *this* course: its particular route through the material (indices as functions on a finite set, "nothing here is magic, you can check it by hand") is the point, even where textbooks go another way. When the lecturer insists on a distinction — a function's name versus its argument, the Levi-Civita *symbol* versus the *tensor* — the notes insist on it too.

**2. Faithful in content, free in form.** Speech circles back, repeats itself, starts sentences three times; reading is linear. Reorder freely, merge three attempts at an explanation into the best one, drop logistics, jokes and "поставьте плюсики". Never change what is claimed. A cleaned-up transcript is still hard to read, and a free retelling stops being the lecture; the line between them is content versus form.

**3. Correctness before fluency.** Whisper garbles words ("ландавшица" is Ландау–Лифшиц, "тендеров" is тензоров) and turns formulas into speech ("а и жилька"), and the board never made it into the recording. Every formula, index, sign and term has to be reconstructed *and checked* — against the handnotes, against the mathematics (recompute a small case), against earlier lectures. Readers trust typeset notes more than their own memory, so a fluent wrong formula does more damage than a visible gap.

**4. Be honest about where things come from.** The text says what the lecture said. Anything you add — a figure, a worked example, a fix for a slip of the tongue — must serve what was said, and anything that goes beyond the lecture is identifiable as such. If a passage can't be reconstructed, say so instead of inventing it. Without a transcript, write a draft, not a lecture. The user must always be able to tell the lecturer's content from Claude's.

**5. A picture must show something the formula hides.** Illustrations are where these notes can most improve on the original example. A good figure makes a mechanism visible: a function on a finite set as a table, a linear form as a family of parallel level lines, a change of basis as one vector over two grids, a tangent plane touching a surface. The handnote sketches, and the moments when the lecturer says "смотрите, нарисуем", show where pictures belong. A decorative figure, or one that restates a formula, costs the reader attention and gives nothing back.

**6. Write for the student who missed the lecture.** The reader knows the listed prerequisites and the earlier lectures, but not this one. Every symbol is introduced before it is used, every step done on the board is shown, and nothing depends on "как видно на доске". This sets the level of detail: not a summary for someone who was there, and not a textbook for someone who knows nothing.

**7. One course, one book.** Notation, terms and style stay the same from lecture to lecture, and later lectures refer back to earlier ones. In tensor calculus inconsistent notation does real harm (which index is up, which is down, what a bracket means), so consistency is part of correctness, not polish.

## Workflow

### 1. Find the sources

Keep a source map in `raw/sources.md`, creating it on first use:

```markdown
| № | Тема | Заметки | Расшифровка | Конспект | Статус |
|---|---|---|---|---|---|
| 1 | Индексы | handnotes/1 Индексы_260114_204948.pdf | transcipts/lecture1/ | docs/lecture-01/ | готово |
| 4 | Линейные формы | handnotes/4 Линейные формы _260121_235035.pdf | transcipts/video_2026-06-13_11-27-55/ (по содержанию) | docs/lecture-04/ | на проверке |
| 17 | Касательное пространство | handnotes/17_… | — | docs/lecture-17/ | черновик (нет записи) |
```

Statuses: `черновик (нет записи)` — written from handnotes only; `на проверке` — full draft waiting for the user's review; `готово` — finalized to .tex/.pdf.

If the lecture you need is already in the map, use it. Otherwise match it up:

- **Handnotes**: the leading number in the filename is the lecture number. The `_YYMMDD_HHMMSS` suffix is the export date. The real lecture date is written in coloured ink at the top of the first page.
- **Transcripts in `lectureN` / `ТЕНЗОРЫ N` folders** are lecture N. Still confirm the topic from the opening few minutes, where the lecturer usually says what today is about and what was covered last time.
- **Transcripts with uninformative names** (`video…`) have to be matched by content. Read the first ~3000 characters of each candidate and compare them with the handnote headings and key terms, e.g. using `grep -c` counts for the topic words. The download date in the folder name tells you nothing.
- Record how you matched it ("по содержанию: …"). If two transcripts fit equally well, or none fits but one is close, ask the user rather than guess, because a wrong match produces confidently wrong notes.

Possible cases: notes + transcript (normal), notes only (→ draft, see below), transcript only (→ full lecture with formulas reconstructed from speech and mathematics; flag the reconstructed ones).

If `docs/lecture-NN/lecture-NN.md` already exists: if it is `черновик (нет записи)` and a transcript has now appeared, rewrite it fully and keep the figures that still fit. Otherwise ask before overwriting, because the user may have edited it by hand.

Several lectures at once: do them one at a time, or hand each lecture to its own subagent following this skill. Only you update `raw/sources.md`, after each lecture, so parallel writers don't clobber it.

### 2. Read everything before writing anything

- **Handnotes, every page.** The PDFs are image scans, so use Read with `pages`. Highlighted or boxed formulas are what the lecturer stressed. Red ink usually marks the key construction. A crossed-out formula is usually a *counterexample the lecturer showed* (e.g. $a_i = b_j$ crossed out = "это бессмыслица"), not a mistake in the notes.
- **The transcript, all of it** (`.txt`, in chunks if long; 60–115k characters is typical). Use `.srt` only to look up timestamps for passages you will flag.
- **The previous lecture's write-up** in `docs/` (and skim the headings of the others) for notation, terms and things to refer back to.
- `references/style.md` — voice, format, Markdown/KaTeX rules, and a worked transcript → text example. Read it every time; it is short.
- `references/figures.md` — before drawing.

### 3. Plan

Before writing, sketch for yourself, not in the deliverable:
- the lecture's **arc**: the sequence of ideas as they should be read, which is often not the order they were spoken;
- sections and subsections;
- figures and where they go;
- what you will drop (logistics, homework admin, digressions) and anything borderline;
- every place where the transcript is garbled and you had to reconstruct, and how sure you are.

### 4. Write `docs/lecture-NN/lecture-NN.md`

Follow the format in `references/style.md`: title `# Лекция N. Тема`, the **Необходимые знания / О чем лекция** block, an introductory paragraph in the lecturer's framing, numbered sections, and `*Конец лекции N.*`.

On length: the finished lecture 1 is about 26k characters of text (roughly 33k as Markdown with formulas) from a 66k-character transcript. About 40% of the spoken text is typical, because speech is redundant, but let the substance decide. Never pad, and never cut an idea the lecturer actually developed.

Homework discussion at the start of a lecture: drop the administrative part. If it contains real mathematics (a solved problem that sharpens an earlier idea), you may add a short closing section "Из разбора домашнего задания". Either way, say in the report what you did with it.

Student questions: when a question led to a useful clarification, fold the clarification into the text as a remark. Don't write it as dialogue.

### 5. Draw the figures

Follow `references/figures.md`: SVG files in `docs/lecture-NN/figures/`, referenced from the `.md` as `figures/<name>.svg`, house style from `assets/figure-template.svg`, coordinates computed rather than eyeballed, and every figure checked visually after it is drawn.

### 6. Verify

1. Run `python3 <skill-dir>/scripts/render_preview.py docs/lecture-NN/lecture-NN.md --pdf <scratch-dir>/lecture-NN.pdf`. It renders the page the way VS Code's preview does (markdown-it + KaTeX), prints every formula KaTeX can't parse, every missing image and every stray `$`, and writes an A4 PDF. Fix everything it reports and run it again until it says OK.
2. Read the PDF pages. Check that the figures sit where they're discussed, labels are legible and nothing overlaps or is clipped.
3. Go through the handnotes page by page. Every boxed or highlighted formula and every definition should appear in the text, unless you dropped it deliberately and can say why.
4. Re-derive anything you computed or reconstructed: signs, index order, small examples.

### 7. Update the map and report

Update `raw/sources.md` (paths, how matched, status `на проверке`, or `черновик (нет записи)` in draft mode). Add or update the lecture's line in `docs/README.md`, the website's navigation: `N. [Лекция N. Тема](lecture-NN/lecture-NN.md)`, kept in lecture order, with « — черновик, без записи лекции» after a draft-mode lecture. The site at https://claptar.github.io/tensors-notes/ renders `docs/` as it is, so pushing to `main` publishes. Don't push unless the user asks. Then tell the user briefly:
- what was written, with file paths;
- which sources were used, and how the transcript was matched if it wasn't obvious;
- the figures you added;
- **places to check**: each uncertain reconstruction with the `.srt` timestamp, so they can listen to the recording at that moment;
- what was left out (logistics, homework, digressions) so they can ask for it back.

Then stop. The draft goes to the user for review; finalize only when they say so.

### Revising a draft

When the user comments on a draft ("раздел 3 слишком сжат", "добавь рисунок к замене базиса", "здесь он говорил другое"), edit the `.md` and figures, re-run the checks in step 6, and report what changed. When a comment is about the lecture's content, go back to the transcript rather than relying on memory, because the user may be remembering the lecture better than the draft does. If a comment reveals a general preference ("always show the computation in full", "fewer figures with 3D"), apply it to the whole lecture, not just the spot pointed at.

### 8. Finalize: .tex and .pdf

Only when the user approves the draft ("finalize", "готово, собери pdf", "make the tex"). First `grep -n ПРОВЕРИТЬ docs/lecture-NN/lecture-NN.md`. If markers remain, list them and ask whether they are resolved, because the final version shouldn't carry unchecked reconstructions silently.

```bash
python3 <skill-dir>/scripts/finalize.py docs/lecture-NN/lecture-NN.md
```

It generates `lecture-NN.tex` in the lecture folder from the Markdown and converts each figure to PDF next to its SVG. The preamble is `assets/lecture-template.tex`: Computer Modern with cm-super, and the running header «ТЕНЗОРЫ | Лекция N. Тема», as in the example. It then compiles `lecture-NN.pdf`, also in the lecture folder, **the way Overleaf does by default**: pdfLaTeX via latexmk on TeX Live 2026 (full scheme), in the official `texlive/texlive` Docker image pinned by digest. The script starts Docker Desktop if needed and pulls the image on first use (~2.7 GB, once).

The lecture folder is a self-contained Overleaf project. If the user wants the lecture on Overleaf, add `--overleaf-zip` and give them `docs/lecture-NN/lecture-NN-overleaf.zip` (just the .tex and the figure PDFs) for New Project → Upload Project. It compiles there with default settings.
- Fix every `WARNING` in the `.md`, not in the `.tex`, and run it again.
- `LAYOUT: Overfull \hbox` lines point at formulas or tables too wide for the page. Break the formula (`aligned`) or shrink the table in the `.md`.
- Look at the final PDF pages: figures next to their text, nothing cut off, the header block and «Конец лекции» in place.
- The `.md` stays the source of truth. If the user wants a change after finalizing, change the `.md` and finalize again. The script refuses to overwrite a `.tex` that was edited by hand. In that case ask the user whether to carry those edits back into the `.md` (preferred) or to overwrite with `--force`.

Set the status in `raw/sources.md` to `готово`. If the lecture's line in `docs/README.md` carried «черновик», remove that note.

## Draft mode: handnotes but no transcript

Write the same header block and the sections, definitions, formulas and figures that the notes support, joined by short connecting sentences. Do not invent the lecturer's motivation, analogies or remarks, since that is exactly what the missing transcript would have provided. Put a banner directly under the title:

```markdown
> **Черновик.** Расшифровки этой лекции пока нет; текст восстановлен по рукописным заметкам и содержит только то, что в них есть. Будет переписан, когда появится запись.
```

Mark it `черновик (нет записи)` in `raw/sources.md`. Don't finalize a draft written without a transcript unless the user explicitly asks.

## Marking uncertainty in the text

- Confident after checking: no marker.
- Plausible but unconfirmed (a garbled term, a formula pieced together from speech): write it, and leave an HTML comment the user can grep for, e.g. `<!-- ПРОВЕРИТЬ 00:41:12: в записи «...», восстановлено как ... -->`. Also list it in the report.
- Can't be reconstructed: don't invent it. Write what can be supported and add a visible note, e.g. *(фрагмент записи неразборчив: здесь разбирался пример с …)*.
- Your own additions beyond the lecture (an extra worked example, a remark the lecturer didn't make) go in a clearly labelled remark: `*Замечание редактора.* …`. Figures that illustrate what was said need no label. A fix for an obvious slip of the tongue needs no label either; a fix for a substantive mathematical error gets an editor's remark.
