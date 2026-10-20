---
name: lecture-notes
description: Writes the lectures of the ТЕНЗОРЫ (tensors) course in this project as chapters of a Russian book of lectures, the way the lecturer himself wrote lecture 1 (his own text is the standard). Each lecture is built from its handwritten notes (raw/handnotes) and Whisper transcript (raw/transcipts) in book register, not as a record of the spoken lecture. Drafts are Markdown with KaTeX math, SVG illustrations and draft-only callouts that state each paragraph's idea and ask what is unclear. Approved lectures are finalized as LaTeX (.tex) and PDF. Use it whenever the user asks to write up, make notes or a конспект for, redo, revise, illustrate or finalize a lecture of this course — by number ("lecture 7", "лекция 4"), by topic ("the tangent space lecture", "Леви-Чивита") or in bulk ("all lectures that have transcripts"). Also use it when the lecturer's review of a draft arrives (a recording, transcript or list of comments), when the user asks for a lecture's .tex/.pdf, and when a transcript or handnote arrives for a lecture that so far has only a draft. Prefer this skill over the general study-kb adapt-recordings / adapt-material skills for anything belonging to this course.
hooks:
  PostToolUse:
    - matcher: "Write|Edit|MultiEdit"
      hooks:
        - type: command
          command: 'python3 "${CLAUDE_PROJECT_DIR}/.claude/skills/lecture-notes/scripts/hook_check.py" post'
  Stop:
    - hooks:
        - type: command
          command: 'python3 "${CLAUDE_PROJECT_DIR}/.claude/skills/lecture-notes/scripts/hook_check.py" stop'
---

# The ТЕНЗОРЫ book of lectures

This skill turns one lecture's raw material into a chapter of a book. The book keeps the lecture structure: chapters are titled «Лекция N. Тема», like Feynman's lectures. It is written for a reader alone with the book, in the lecturer's voice as an author, not as a record of what was said in the room.

**The lecturer wrote lecture 1 himself, from the same kind of recording and handnotes, and that text is the standard** («референс — это абсолютная правда для нас»). The job is to do for every other lecture what he did for lecture 1. Even a small deviation from how he writes draws a critical review. So the first reference is always `references/author-model.md`, which describes how his text was made from his lecture.

| Input | Where | What it gives you |
|---|---|---|
| **His own lecture 1** | `raw/reviews/lecture-01/lecture1_indices.tex` (PDF: `raw/examples/Лекция_1__Индексы_*.pdf`) | **The standard.** What a finished chapter is: what he keeps, cuts, moves and adds, his voice, his format |
| **The author model** | `references/author-model.md` | How his text was made from his recording, with evidence, and what the blind test showed. Read it first, every time |
| Handwritten notes | `raw/handnotes/N <тема>_<YYMMDD_HHMMSS>.pdf` | What was on the board: formulas, diagrams, the order of topics. Boxed means stressed in the room, not "keep" |
| Transcript | `raw/transcipts/<folder>/` (`.txt`, `.srt`, `.vtt`, `.json`, `.tsv` from Whisper) | What the lecturer *said*: ideas, motivation, analogies, warnings |
| Author's reviews | `raw/reviews/lecture-NN/` | His comments on a draft, often a transcribed call (may be UTF-16) |
| Author's rulings | `references/author-rulings.md` | What he has decided in reviews, each checked against his text |
| Reference books | `raw/examples/Слободянюк т1–т4.pdf`; the others are named in `author-model.md` §6 | How a narrative is built (Slobodyanyuk). Never cited or copied |

The work has two stages. First a **draft** in Markdown, reviewed and revised as often as needed. Then the **final** .tex and .pdf, once the user approves. Only the book register exists for now; the lecturer may later want a conversational mode as well.

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

These principles come first. The workflow and rules below apply them. When a situation isn't covered, reason from here. They were rewritten after the lecturer's second review of lecture 1 (2026-10-19). That review showed two things. His own text had been the model all along. And rules generalized from his comments had come to ban what he himself writes.

**1. It is the author's book, and his text is the measure.** The lecturer is the author. The order of authority is:
- his written text (lecture 1, `author-model.md`);
- what he decided explicitly in a review (`author-rulings.md`);
- the recording.

Our own taste overrides nothing. A review comment means "you drifted from how I write". Resolve it by looking at how his text does it, never by turning it into a general ban. This course has its own route through the material: indices as functions on a finite set, sets with no structure beyond what is defined, everything computable by hand. That route is the point, even where textbooks go another way.

**2. Faithful to his line, not to every word.** He keeps what the lecture builds on:
- definitions;
- the comparison with functions on ℝ;
- warnings that prevent a misreading;
- the computations the reader needs.

He drops logistics, the room, personal stories, textbooks, and **asides that the rest of the lecture doesn't use, even ones he enjoyed saying**: «если какое-то знание не используется в дальнейшем… значит, это знание не фундаментально» (review 2, 03:03). Such material becomes a small «Замечание» or goes; in his own text it goes. One analogy per point. Repeated worked cases become one general argument. The order is logical, not the order of speaking. The result is about a third of the spoken text. Every spoken habit still becomes its written equivalent: a question to the room becomes a question the text answers at once, and a mood becomes the fact behind it. `references/register.md` and `author-model.md` §2 show the transformations, with real pairs.

**3. Every paragraph has a point, and the reader is led.** Decide what a paragraph is for before writing it, and make the paragraph say it. In a draft, the idea sits above the paragraph in an «Идея» callout. Each paragraph starts where the previous one stopped, often with his callbacks («Как уже было сказано», «Вновь…»). Nothing appears without a reason: no question, figure or example arrives unannounced, and motivation comes before a computation. The main line is linear.

**4. Claim exactly what is true.**
- Whisper garbles words and formulas, and the board never made it into the recording. Every formula, index, sign and term is reconstructed *and checked* against the handnotes, the mathematics (recompute a small case) and earlier lectures. Readers trust a typeset book more than their memory.
- An analogy is called an analogy («аналог», «полная аналогия»; never «ту же роль»).
- Nothing is used before it is defined. Reordering is allowed, but every move means re-checking what depends on what.

**5. Honest provenance, kept out of the printed text.** The user must always be able to tell the lecturer's content from ours. Every addition of ours goes into the draft's Идея callout as «(добавление)» and into the report, or becomes a «Вопрос». That covers:
- a caption that says more than the lecture;
- a term we coined;
- a framing sentence;
- a reordering;
- a cleaner example.

The book itself carries no such label: he rejected «Замечание редактора» («просто напишите замечание»). Additions by *him*, such as the progressions in lecture 1, are normal. Additions by *us* need his approval. Without a transcript, write a draft, not a lecture.

**6. Pictures reveal, never add, and stay modest.** Illustrations are where the book improves most on the spoken lectures, and he praised every one. A good figure makes a mechanism visible. But a picture also adds structure (positions, neighbours, a diagonal), and the course insists that a set has none beyond what is defined. So every figure is introduced as one possible visualization («можно изобразить…», «если расположить…, то…»), and the logic never rests on it. No figure takes more than about a third of a page, captions are short, and nothing leaves a gap on the page. `references/figures.md` covers this.

**7. One book, read alone.**
- **The reader has only the book.**
  - «Сегодня — …» opening a chapter, «в этой лекции», «в лекции 3», «позже» are his.
  - «на доске», «в прошлый раз», «я говорил», «вы», «нас сейчас интересует» are not.
- **Notation, terms, register and rulings are the same in every lecture.** A ruling made on lecture 1 applies to lecture 12.
- **Inconsistency is an error, not a matter of polish.** In tensor calculus, inconsistent notation (which index is up, what a bracket means) does real harm.

**8. Ask, don't guess, and ask him little.** When you are unsure what the lecturer meant, or which way the book should go, ask. A visible question costs the author a minute; a confident guess costs a review round, and his trust. But he reviews the *typeset pages*, by page and figure number, and expects us to have done the comparison with his text ourselves. Questions for him are therefore:
- few;
- concrete;
- each answerable in a word;
- sent as one short list next to the typeset preview.

Everything his own text already decides is not a question. See "When to ask" below.

## When to ask

**Ask the user now (AskUserQuestion)** when the answer changes what you do next:
- which sources belong to the lecture, if the match isn't clear;
- the scope;
- a conflict between the transcript and the handnotes, between the lecture and a ruling, or **between a review comment and his own text**;
- register or format that neither his text nor a ruling covers;
- whether to drop, move or merge an idea the lecturer developed, when the "used later?" test doesn't settle it;
- anything beyond the lecture: a new example, a new term, a reworded definition, a figure not grounded in the sources. Put these as proposals, not decisions.

**Ask the lecturer through the draft (`> **Вопрос N.** …`)** when only he can know:
- what a garbled passage said;
- which of two readings was meant;
- whether a reconstruction is right;
- whether an addition the lecture only hints at belongs in (for example, a known formula the recording alludes to).

Say what is unclear, give the options, and have the text carry the most defensible version meanwhile.

Settle something silently only when his text, a ruling, the conventions of mathematics or the plain sense of the sources decides it. "It seemed reasonable" is not enough.

**If you can't ask the user directly** (you are a subagent, or in a batch run), don't decide in their place. Write the question into the draft as `> **Вопрос N (для пользователя).** …` and list it in your report.

The skill's hooks back this up. Registered in the frontmatter, they run `scripts/hook_check.py`:
- **After each edit of a lecture draft**, you get a checklist. It lists paragraphs without an Идея, open questions, register candidates, terms used before their definition, «Замечание редактора», header/intro/bold problems and sentence length. It ends with this rule and a reminder to compare the passage with his text.
- **At the end of a turn that edited a draft**, the hook blocks once if an open «Вопрос N» isn't named in your final message, or if a paragraph lacks its Идея.

Hooks can't see doubt; they make sure doubt that was written down reaches a person. They are registered only when the skill is invoked through the Skill tool. If you are following this file some other way, for example as a subagent told to read it, run `lint_text.py` yourself after each larger edit and before you report.

## Workflow

### 1. Find the sources

Keep a source map in `raw/sources.md`, creating it on first use:

```markdown
| № | Тема | Заметки | Расшифровка | Конспект | Статус |
|---|---|---|---|---|---|
| 1 | Индексы | handnotes/1 Индексы_260114_204948.pdf | transcipts/lecture1/ | docs/lecture-01/ | на проверке |
| 4 | Линейные формы | handnotes/4 Линейные формы _260121_235035.pdf | transcipts/video_2026-06-13_11-27-55/ (по содержанию) | docs/lecture-04/ | на проверке |
| 17 | Касательное пространство | handnotes/17_… | — | docs/lecture-17/ | черновик (нет записи) |
```

**Statuses:**
- `черновик (нет записи)`: written from handnotes only;
- `на проверке`: a full draft waiting for the lecturer's review;
- `готово`: finalized to .tex/.pdf.

If the lecture you need is already in the map, use it. Otherwise match it up:
- **Handnotes.** The leading number in the filename is the lecture number. The `_YYMMDD_HHMMSS` suffix is the export date. The real lecture date is written in coloured ink at the top of the first page.
- **Transcripts in `lectureN` / `ТЕНЗОРЫ N` folders** are lecture N. Still confirm the topic from the opening few minutes, where the lecturer usually says what the lecture is about and what was covered last time.
- **Transcripts with uninformative names** (`video…`) have to be matched by content. Read the first ~3000 characters of each candidate and compare them with the handnote headings and key terms, e.g. using `grep -c` counts for the topic words. The download date in the folder name tells you nothing.
- **Record how you matched it** («по содержанию: …»). If two transcripts fit equally well, or none fits but one is close, ask the user.

**Possible cases:**
- notes + transcript: the normal case;
- notes only: a draft, see "Draft mode" below;
- transcript only: a full lecture with formulas reconstructed from speech and mathematics, each reconstruction a «Вопрос».

If `docs/lecture-NN/lecture-NN.md` already exists:
- If it is `черновик (нет записи)` and a transcript has now appeared, rewrite it fully and keep the figures that still fit.
- Otherwise it may contain the author's own edits. Check `git log -p` / `git diff` for changes since the last version Claude wrote. Never rewrite the author's sentences silently; ask if a change of yours would touch them.
- A lecture built on the author's own text (lecture 1) carries a `<!-- author-text -->` line under the title. Its text is his; change it only cosmetically, and list every change.

**Several lectures at once:** do them one at a time, or hand each lecture to its own subagent following this skill. Only you update `raw/sources.md`, after each lecture, so parallel writers don't clobber it.

### 2. Read everything before writing anything

- **`references/author-model.md`, then `author-rulings.md` and `register.md`.** Every time.
- **His lecture 1**, in full, if you haven't read it in this session: the voice to continue.
- **Handnotes, every page.** The PDFs are image scans, so use Read with `pages`.
  - Highlighted or boxed formulas are what the lecturer stressed in the room. They are not automatically what the book keeps: he boxed 2+x=3 in lecture 1 and dropped it.
  - Red ink usually marks the key construction.
  - A crossed-out formula is usually a *counterexample the lecturer showed* (e.g. $a_i = b_j$ crossed out means «это бессмыслица»), not a mistake in the notes.
- **The transcript, all of it** (`.txt`, in chunks if long; 65–170k characters is typical). Use `.srt` to look up the times you will cite in Идея and Вопрос callouts.
- **The previous lecture** in `docs/`, and skim the headings of the others, for notation, terms and things to refer back to.
- **`references/style.md`** (format, Markdown/KaTeX rules, callouts) and **`references/figures.md`** before drawing.

### 3. Plan: the idea skeleton

Write the skeleton into `docs/lecture-NN/lecture-NN.md` before any prose:
- the title and header block;
- the section headings;
- under them, one `> **Идея.** … *(hh:mm:ss)*` callout for every planned paragraph, side remarks included.

The ideas are the lecture's line of argument in the order it should be read, which is often not the order it was spoken.

**Structure as he does it** (`author-model.md` §3, §8):
- the general theory first, in numbered sections;
- the concrete objects of the lecture (named functions, standard constructions, the computations with them) gathered at the end as «Примеры» with subsections, each presented as an example of what the theory introduced;
- each sentence of «О чём лекция» corresponding to one section;
- a computation with its own motivation getting its own subsection.

These rules come from lecture 1; where a lecture's material doesn't fit them, ask.

Read the ideas alone, top to bottom, and check:
- **The argument reads well.** Each idea follows from the ones before it.
- **Definitions come first.** Nothing is used before the idea that defines it.
- **The main line is linear.**
- **The "used later?" test.** For every aside, analogy, side case and forward reference, ask whether later parts *of this lecture* use it. If not, it goes, or becomes a small «Замечание». A forward reference stays only if it prevents a misreading of what is on the page now. Note what you drop, with times, for the report. Anything borderline goes to the user as a question.

Mark doubts as you go: a garbled passage, an unclear intent, two possible readings. Each becomes a «Вопрос N» callout where it arises.

An idea is one sentence saying what the paragraph *establishes*, not a summary of its words. «Сумма значений индексной функции — число; в этом аналогия с определённым интегралом» is an idea. «Обсуждается обозначение суммы» is not.

### 4. Write the paragraphs

Write each paragraph from its idea, in his voice: `author-model.md` §2.4 for real spoken→written pairs, §3 for his habits, §8 for what a writer without that knowledge gets wrong. State the idea in the paragraph, usually first, and lead in from the previous paragraph. Keep the steps the reader needs. Where the lecture computes case after case, write one argument «при фиксированном j …», then the general rule and one example. Keep the lecture's structuring questions as questions answered at once («Что за объект получится?»).

Follow the format in `references/style.md`:
- the title `# Лекция N. Тема`;
- the **Необходимые знания / О чём лекция** block: a comma list, then two short sentences, no parentheses;
- **one** introductory paragraph;
- numbered sections;
- bold only for the term being defined;
- `*Конец лекции N.*` at the end, with no summary before it.

**Length** is measured in characters, as Python's `len` counts them; `wc -c` counts bytes, about twice as many for Cyrillic. His lecture 1 has 22.6k characters of prose (formulas excluded) from a 66.5k-character transcript, about a third. Sentences have a median of about 16 words. Treat both as targets, not limits: a lecture dense with computation may run longer.

**Homework discussion at the start of a lecture.** Drop the administrative part. If it contains real mathematics (a solved problem that sharpens an earlier idea), you may add a short closing section «Из разбора домашнего задания»; ask first, since his lecture 1 has none. Either way, say in the report what you did with it.

**Student questions.** When a question led to a useful clarification, fold the clarification into the text. Don't write it as dialogue.

### 5. Draw the figures

Follow `references/figures.md`:
- SVG files go in `docs/lecture-NN/figures/` and are referenced from the `.md` as `figures/<name>.svg`.
- Use the house style from `assets/figure-template.svg`.
- Compute coordinates; don't eyeball them.
- Introduce each figure in the text before it appears, framed as a visualization.
- Keep it small: at most a third of the page, with a caption of one or two lines.
- Keep the white background; the website handles light and dark.

Check every figure in both themes with `scripts/snap_svg.py`.

### 6. Verify: five passes

1. **Rendering.** Run `python3 <skill-dir>/scripts/render_preview.py docs/lecture-NN/lecture-NN.md --pdf <scratch-dir>/lecture-NN.pdf`. It renders the page with markdown-it + KaTeX, styling callouts as the website does. It prints:
   - every formula KaTeX can't parse;
   - every missing image;
   - every stray `$`;
   - everything pdfLaTeX can't typeset;
   - a summary of the text checks.

   Fix and rerun until it says OK. Then read the PDF: the figures sit where they are discussed, and nothing overlaps or is clipped.
2. **Fidelity.** Go through the handnotes page by page and the transcript section by section. Every definition and every idea the lecture builds on is in the text. Everything you dropped, you dropped by the "used later?" test and can name with its time. Re-derive what you computed or reconstructed: signs, index order, small examples.
3. **Logic and order.** Run `python3 <skill-dir>/scripts/lint_text.py docs/lecture-NN/lecture-NN.md`.
   - Every paragraph needs its Идея, and each paragraph must deliver the idea above it.
   - Look at every «BEFORE DEF» candidate.
   - Check that every question, figure and example has a lead-in.
4. **Register and additions.**
   - Look at every REGISTER, SHORT, BOLD, HEADER, INTRO and LONG candidate from `lint_text.py`. The patterns are calibrated so that none fires on his own text (`lint_text.py --selftest`), so a hit is worth a look.
   - Then read the text once more for our own additions: captions and coined terms, framing sentences and reorderings, cleaner examples, claims stronger than what was said. Each is traceable to the sources, or is marked «(добавление)» and listed, or becomes a «Вопрос».
5. **Against his text.** Put a section of your draft next to a section of his lecture 1 and go through `author-model.md` §8 point by point:
   - structure and «Примеры»;
   - one analogy per point;
   - compressed cases;
   - questions kept as questions;
   - motivation first, forward references last;
   - bold;
   - his callbacks;
   - sentence length;
   - notation (ℓ, «+1»).

   Every difference is either justified by this lecture's material or fixed.

### 7. Update the map and report

Update `raw/sources.md`: paths, how the transcript was matched, and the status (`на проверке`, or `черновик (нет записи)` in draft mode).

Add or update the lecture's line in `docs/README.md`, the website's navigation: `N. [Лекция N. Тема](lecture-NN/lecture-NN.md)`, in lecture order, with « — черновик, без записи лекции» after a draft-mode lecture. The site at https://claptar.github.io/tensors-notes/ renders `docs/` as it is, so pushing to `main` publishes, Идея and Вопрос callouts included. Don't push unless the user asks.

Then tell the user briefly:
- what was written, with file paths;
- which sources were used, and how the transcript was matched if it wasn't obvious;
- the figures, saying which ones are our additions;
- **every open question as «Вопрос N — …»**, with its time in the recording (the stop hook checks this);
- what was dropped by the "used later?" test, with times, so they can ask for it back;
- our additions.

**What the lecturer gets** (when the user decides to send it):
- the typeset preview, built with `finalize.py` on a scratch copy without the callouts;
- a one-page list of the open questions in Russian: what each is, his own words if a review touched it, and the choice in a word («оставить / убрать»).

Not the draft full of callouts, and not a long response document.

Then stop. Finalize only when the user says so.

### Revising after an author review

Reviews usually arrive as a transcribed call in `raw/reviews/lecture-NN/`. These can be UTF-16; decode them with Python (`b.decode('utf-16')`) and save the copy as `<original name>.utf8.txt` next to it.

1. **Map** every comment to its place in the draft: section, page, figure or quoted phrase. He refers to the typeset pages, and the transcription garbles terms («левечевита» is Леви-Чивита), so match by meaning.
2. **Read each comment against his text first.** A comment that points at a passage usually means "this differs from how I write". Look up how his text does it before deciding what the comment asks for.
3. **Classify** each comment:
   - **form**: register, order, wording, layout. Apply it.
   - **an author's decision about content**: apply it, and add it to the rulings if it is general. Check that the general version doesn't ban anything his text does (`lint_text.py --selftest`).
   - **a request for options**: two versions, several layouts. Produce them; don't choose for the author.
   - **"I'll decide myself"**: leave it, and note it under "Open" in the rulings.
   - **praise**: record it under "What to keep doing".
   - **a conflict with his text or an earlier review**: don't pick a side. Put it to the user, or to him in the short question list.
   - **unclear what the author wants**: ask.
4. **Generalize carefully.** Write every general point into `references/author-rulings.md` with its time, new lecture-speak into `references/register-patterns.tsv`, and new evidence about how he writes into `author-model.md`. Run `lint_text.py --selftest` after changing patterns. Apply each ruling to the whole lecture, not just the spot pointed at, and list which other lectures it affects.
5. **Rewrite from the ideas.** A corrected Идея means the paragraph is rewritten from the corrected idea, not patched. An answered Вопрос is applied to the text and the callout deleted.
6. **Respond briefly.** Write `raw/reviews/lecture-NN/response-YYYY-MM-DD.md`: one page, a table of comment, time and what changed, plus the open questions. Summarise it for the user.

**When a later lecture corrects an earlier one.** Sometimes the lecturer says that something in a previous lecture was wrong or imprecise (e.g. lecture 2, 00:03:32: a formula for a function on a finite set always exists). That is the author's later view, so it wins (principle 1).
- Fix the earlier lecture's text.
- Put a «Вопрос» there citing the lecture and the time, so the lecturer can confirm the wording.
- Tell the user.
- If the correction is general, add it to the rulings.
- If the earlier lecture is already final, ask the user before touching it.

For small comments from the user in the session ("раздел 3 слишком сжат", "добавь рисунок"), the same applies on a smaller scale. Edit the `.md` and figures, rerun step 6, and report what changed. When a comment is about the lecture's content, go back to the transcript rather than relying on memory.

### 8. Finalize: .tex and .pdf

Only when the user approves the draft ("finalize", "готово, собери pdf", "make the tex").

```bash
python3 <skill-dir>/scripts/finalize.py docs/lecture-NN/lecture-NN.md --strip-ideas
```

- **It refuses while a «Вопрос», an old `<!-- ПРОВЕРИТЬ -->` marker or a «Замечание редактора» is left.** The final version must not carry a guess or our label. Ask the user, apply the answers, delete the callouts.
- **`--strip-ideas`** removes the Идея callouts from the `.md` (git keeps them) once the user has approved the lecture. Without it, they are only left out of the .tex/.pdf.
- **Side-remark callouts become the `aside` environment,** set like a figure caption (the style he approved).
- **It generates `lecture-NN.tex`** in the lecture folder and converts each figure to PDF next to its SVG. The preamble is `assets/lecture-template.tex`, set up like his lecture 1: Computer Modern with cm-super, 1in margins, and the running header «ТЕНЗОРЫ | Лекция N. Тема».
- **Tables and figures.**
  - Tables are set without inner vertical rules.
  - A table of more than 12 rows is split into blocks side by side.
  - Figures are capped at a third of the page height.
- **It compiles `lecture-NN.pdf` the way Overleaf does by default:** pdfLaTeX via latexmk on TeX Live 2026 (full scheme), in the official `texlive/texlive` Docker image pinned by digest. The script starts Docker Desktop if needed and pulls the image on first use (~2.7 GB, once).
- **It then checks the pages:** every page except the last that ends early, typically a table or figure pushed to the next page, is reported as `LAYOUT`.
- **The lecture folder is a self-contained Overleaf project.** If the user wants the lecture on Overleaf, add `--overleaf-zip` and give them `docs/lecture-NN/lecture-NN-overleaf.zip` (the .tex and the figure PDFs) for New Project → Upload Project.
- **Fix every `WARNING` and `LAYOUT` line in the `.md`,** not in the `.tex`, and run it again. `Overfull \hbox` lines point at formulas or tables too wide for the page; break the formula (`aligned`) or shrink the table.
- **Look at every page:**
  - figures next to their text and no larger than needed;
  - side remarks set apart;
  - no table half a page down after a gap;
  - nothing cut off;
  - the header block and «Конец лекции» in place.
- **The `.md` stays the source of truth.** For a change after finalizing, change the `.md` and finalize again. The script refuses to overwrite a `.tex` that was edited by hand; then ask the user whether to carry those edits back into the `.md` (preferred) or to overwrite with `--force`.

Set the status in `raw/sources.md` to `готово`. If the lecture's line in `docs/README.md` carried «черновик», remove that note.

## Draft mode: handnotes but no transcript

Write the same header block and the sections, definitions, formulas and figures that the notes support, joined by short connecting sentences. Give each paragraph its Идея: here the ideas are your reading of the notes, which is exactly what the lecturer should check. Do not invent the lecturer's motivation, analogies or remarks, since that is what the missing transcript would have provided. Put a banner directly under the title:

```markdown
> **Черновик.** Расшифровки этой лекции пока нет; текст восстановлен по рукописным заметкам и содержит только то, что в них есть. Будет переписан, когда появится запись.
```

Mark it `черновик (нет записи)` in `raw/sources.md`. Don't finalize a draft written without a transcript unless the user explicitly asks.

## Callouts and provenance at a glance

| What | How | Where it shows |
|---|---|---|
| The idea of the next paragraph | `> **Идея.** … *(hh:mm:ss)*` | Drafts only (site, preview); stripped at the end |
| Our own addition (a framing sentence, a cleaner example, a remark he didn't make, a coined term) | «(добавление)» in that paragraph's Идея callout, and listed in the report | Drafts only |
| Something unsure, for the lecturer | `> **Вопрос N.** (hh:mm:ss) … Варианты: …` | Drafts only; finalize refuses while one remains |
| A side remark | `> *Замечание.* …`, `> *Предупреждение.* …`, `> *Забегая вперёд.* …` | Everywhere, set smaller and lighter. Use rarely: his lecture 1 has none |
| A fix for an obvious slip of the tongue | No label | |
| A fix for a substantive mathematical error | A «Вопрос», or plain text once the lecturer has confirmed it | |
| A passage that can't be reconstructed | Don't invent it. Write what can be supported, plus a «Вопрос» naming what's missing | |

«Замечание редактора» is no longer used. `lint_text.py` flags it, and `finalize.py` refuses it.

Callout syntax and rendering are in `references/style.md` §5.
