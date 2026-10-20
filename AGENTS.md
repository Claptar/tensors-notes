# ТЕНЗОРЫ — a book of lectures

This project turns a Russian-language course on tensors into a book of lectures: handwritten notes + recording transcripts in, a typeset lecture per session out. The book keeps the «Лекция N» structure, like Feynman's lectures, but is written in book register for a reader learning alone, not as a record of the spoken lecture. The lecturer is the author and reviews every draft.

## Layout

- `raw/` — source material (git-ignored)
  - `handnotes/` — scanned handwritten notes, one PDF per lecture: `N Тема_YYMMDD_HHMMSS.pdf`. `N` is the lecture number; the suffix is the export date, and the lecture date is written on the first page.
  - `transcipts/` (sic) — Whisper output per recording (`.txt`, `.srt`, `.vtt`, `.json`, `.tsv`). `lectureN` / `ТЕНЗОРЫ N` folders are lecture N; `video…` folders have to be matched to a lecture by content.
  - `examples/` — the PDF of «Лекция 1. Индексы», which the lecturer wrote himself, and Slobodyanyuk's «Физика для любознательных» (т1–т4), one of his reference books for how a narrative is built.
  - `reviews/lecture-NN/` — the lecturer's reviews and answers, often transcribed calls (sometimes UTF-16, with a `<name>.utf8.txt` copy next to each), plus what we sent him: typeset previews and lists of changes. `reviews/lecture-01/lecture1_indices.tex` is his own text of lecture 1, **the standard for the whole book**.
  - `sources.md` — map of lecture ↔ handnotes ↔ transcript ↔ output, with status. Maintained by the `lecture-notes` skill.
- `docs/` — the notes
  - one folder per lecture, `docs/lecture-NN/`, holding everything for that lecture:
    - `lecture-NN.md` — draft; the source of truth, revised here. While under review it carries draft-only callouts: `> **Идея.** …` before each paragraph (what it is meant to say, and what is our addition) and `> **Вопрос N.** …` (questions for the lecturer). They show on the website on purpose; they are stripped when the lecture is finalized. A lecture built on the author's own text carries `<!-- author-text -->` under the title and no callouts (lecture 1).
    - `figures/` — SVG figures, each with the `.py` that computes it (+ PDFs made at finalize)
    - `lecture-NN.tex`, `lecture-NN.pdf` — final versions, generated from the `.md`. Lecture 1's current ones are from an earlier draft and are kept until it is finalized again.
  - A lecture folder compiles on Overleaf as is.
  - `README.md` — the list of lectures; it is the website's navigation, so keep it in lecture order.
  - `index.html`, `assets/` — the website: a no-build reader that renders the `.md` files in the browser with vendored markdown-it 14.1.0 + markdown-it-texmath 1.0.0 + KaTeX 0.16.11, the same versions as the skill's `render_preview.py` (keep them in step). `.nojekyll` stops GitHub's Jekyll from touching the files.

## Website

https://claptar.github.io/tensors-notes/ — GitHub Pages from `main:/docs` of `Claptar/tensors-notes`. Pushing to `main` publishes; there is no build step. Preview locally with `python3 -m http.server -d docs 8765`, then open http://127.0.0.1:8765/ (opening `index.html` as a file won't work, because it fetches the `.md` files).

## Working on lectures

Use the `lecture-notes` skill (`.claude/skills/lecture-notes/`) for anything that writes, revises, illustrates or finalizes a lecture, and for processing the lecturer's reviews. Its **Philosophy** section decides judgment calls:
- it is the author's book, and his text is the measure;
- faithful to his line, not to every word: what the rest of the lecture doesn't use goes, or becomes a small «Замечание»;
- every paragraph has a point, and the reader is led;
- claim exactly what is true;
- honest provenance, kept out of the printed text;
- pictures reveal, never add, and stay modest (at most a third of a page);
- one book, read alone;
- **ask, don't guess**, and ask him little.

The order of authority is: his own lecture 1 text, then his decisions from reviews, then the recordings. How his text was made from his lecture is described in `.claude/skills/lecture-notes/references/author-model.md`; his decisions are in `references/author-rulings.md`. Both apply to every lecture. Resolve a review comment by looking at how his text does it, never by turning it into a general ban.

- **When unsure** of what the lecturer meant or which way to go, ask. Ask the user with AskUserQuestion, or ask the lecturer with a visible «Вопрос» callout in the draft. Never settle it silently. The skill's hooks (`scripts/hook_check.py`, registered in SKILL.md's frontmatter) give a checklist after every edit of a lecture draft, and block ending a turn once if a question isn't named in the final message.

- Draft and iterate in Markdown. Produce `.tex`/`.pdf` in the lecture folder only when the user approves a draft (`scripts/finalize.py`).
- The lecturer reviews typeset pages, by page and figure number. For a review, build the preview with `finalize.py` on a scratch copy with the «Вопрос» callouts removed (it refuses to run while one is open), and send his questions as a short separate list.
- Make changes in the `.md`, never directly in the generated `.tex`. `finalize.py` refuses to overwrite a hand-edited `.tex`.
- The lectures are in Russian. Register: `references/register.md`. Format, Markdown/KaTeX rules and callouts: `references/style.md`. Text checks: `scripts/lint_text.py`; its `--selftest` must pass on his own lecture 1 after any change to the checks or patterns.

## Tools on this machine

- **LaTeX runs in Docker**, compiling the way Overleaf does by default: pdfLaTeX via latexmk on TeX Live 2026, full scheme. The image is the official `texlive/texlive`, pinned by digest in `scripts/finalize.py`, ~2.7 GB. `finalize.py` starts Docker Desktop and pulls the image if needed. Each lecture folder is Overleaf-ready; `--overleaf-zip` packs one for upload. There is no local TeX installation.
- **Google Chrome**, headless, renders Markdown previews and converts SVG → PDF. The preview loads KaTeX and markdown-it from jsDelivr, so it also needs network.
- **poppler** (`pdftotext`, `pdftoppm`, from Homebrew): `finalize.py` uses `pdftotext` to report pages that end early; `pdftoppm` renders pages to look at.
- Python standard library only: no pandoc, numpy or matplotlib.
- Homebrew lives in `~/.homebrew` (non-default prefix) and builds many formulae from source, so prefer prebuilt binaries.
- Figures are dark-ink-on-white SVGs; the website's CSS makes them follow light/dark. A dark-mode rule inside an SVG doesn't work reliably in Safari. Check figures as readers see them with `.claude/skills/lecture-notes/scripts/snap_svg.py`, which renders both themes in WebKit, Safari's engine.
