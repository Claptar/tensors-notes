# Style and format

Contents: 1. Voice · 2. Document skeleton · 3. Markdown and math rules · 4. Russian typography · 5. Callouts in drafts · 6. The model: the opening of his lecture 1

## 1. Voice

The voice is his: read `author-model.md` (how he writes, with evidence), `register.md` (what to transform) and `author-rulings.md` (what he decided) every time. The typographic conventions that go with it, all as in his lecture 1:

- **Bold only for the lecture's central defined terms**, in the sentence that defines them: «**Индексной функцией** называется любое отображение $a\colon I \to \mathbb{R}$». In his lecture 1 that is two terms in the whole text. Other named objects are defined in plain type («Символом Кронекера по определению называется отображение…»). Course terms go in quotes («немой», «свободные»). Use *italics* for a stressed word, sparingly (*новая функция*, *концептуально просто*).
- Proofs stay in prose: «Доказательство просто и проводится вручную…», «…что и завершает доказательство.»
- A warning or a forward reference can sit in the main text, as in his: «Предупреждение: позже, в контексте тензоров, появится…», «Забегая вперёд скажем, что…». Side-remark callouts (§5) are for material that isn't needed later but is worth keeping. Use them rarely: his lecture 1 has none.
- Questions the text has prepared for, answered at once: «Имеет ли смысл писать $a = b$? Да.»
- Prose, not bullet points. A list is fine for a genuine enumeration (three properties, four cases); it is not a substitute for an explanation.

## 2. Document skeleton

```markdown
# Лекция 4. Линейные формы

> **Необходимые знания:** линейное пространство, базис, разложение вектора по базису (лекции 2–3).
>
> **О чем лекция:** функции на линейном пространстве; линейные формы и их геометрический смысл; компоненты линейной формы в базисе.

Один вводный абзац: что это за лекция, зачем она и чему в ней предстоит научиться — в той рамке, которую задал сам лектор в начале записи.

## 1. Название раздела

Текст…

### 1.1. Подраздел

Текст…

## 2. …

## N. Примеры

### N.1. …

---

*Конец лекции 4.*
```

- **Необходимые знания**: what the lecture actually relies on, both general mathematics and earlier lectures (name them), as a comma list.
- **О чем лекция**: the topics as noun phrases, two short sentences, **no parentheses or glosses** (his: «понятие индексной и многоиндексной функции, операции над ними. Суммы и перестановочность сумм. Символы Кронекера и Леви-Чивиты.»). Each sentence corresponds to a section.
- **One introductory paragraph.** It may open «Сегодня — …», as his does.
- **The concrete objects** (named functions, standard constructions, the computations with them) come at the end, in «Примеры», as subsections.
- **No summary before «Конец лекции»**: he cut his own.
- Sections are numbered `## 1.`, `## 2.`, … and subsections `### 2.1.` in sequence. The LaTeX build renumbers automatically and warns if your numbers disagree.
- For a draft written without a transcript, the banner goes right under the title (see SKILL.md).
- In every draft under review, each paragraph is preceded by its «Идея» callout (§5).

## 3. Markdown and math rules

The draft is read in VS Code's preview (markdown-it + KaTeX) and later converted to LaTeX by `scripts/finalize.py`. Everything below keeps both working.

**Math**
- Inline: `$a_i$`, with no space just inside the dollars (`$ a_i $` does not render).
- Display: `$$` on its own line, the formula, `$$` on its own line, with a blank line before and after. In LaTeX the formula still stays inside the sentence: text after it that starts in lower case continues the paragraph.
- Cyrillic inside formulas only within `\text{…}`: `\underbrace{(1,2,3)}_{\text{чётные}}`. Other symbols as commands, never as Unicode: `\alpha`, `\varepsilon`, `\to`, `\le`, `\in`, `\infty`. The final build is pdfLaTeX, as on Overleaf. KaTeX renders `ε` or `→` happily and pdfLaTeX stops on them, and the same holds for Greek letters or arrows typed into running text: put them in `$…$`. `render_preview.py` flags all of these as `NOT LATEX-SAFE`.
- Inside a callout (a blockquote: side remark, Идея, Вопрос), display math goes on **one line**: `> $$\int_\tau^t \frac{dt'}{t'}.$$`. Split over several `>` lines, the website and VS Code show a literal `>` in the formula (markdown-it-texmath reads the raw lines); `render_preview.py` and `lint_text.py` flag it as MATH IN CALLOUT.
- Allowed inside `$$`: `aligned`, `gathered`, `cases`, `array`, `matrix` / `pmatrix` / `bmatrix` / `vmatrix`. Don't use `\begin{equation}`, `align`, `\label`, `\eqref` or `\newcommand`. To refer to a formula, add `\tag{3}` inside it and write «(3)» in the text.
- `\colon` for maps (`f\colon X \to Y`), `\varepsilon`, `\ell`, `\mathbb{R}`, `\dots` / `\cdots`, `\equiv` for "по определению" as in the example.
- Vectors and indices: follow the handnotes and the previous lectures (e.g. $\vec a$, $\vec e_i$ if that is what the lecturer writes). Once the course uses upper and lower indices, keep their placement exactly; it carries meaning.
- Index tables (values of a function of two indices) go in a display `array`:

  ```
  $$
  \begin{array}{c|cccc}
   & j=1 & j=2 & j=3 & j=4 \\ \hline
  i=1 & 3 & 5 & 7 & 9 \\
  i=2 & 8 & 12 & 16 & 20
  \end{array}
  $$
  ```

**Text**
- Bold `**…**` and italic `*…*` only (no underscores for emphasis).
- Markdown tables are fine for simple value tables (arguments | value). `finalize.py` sets them as he likes: a rule under the header and one before the value column, no other vertical rules. More than 12 rows are split into blocks side by side. Inside a table cell write `\vert` or `\mid` instead of `|` in math.
- **No table may sit half a page down after a gap.** A long table (his ε table: 27 rows) is laid out horizontally, in blocks side by side; in a display `array`, write the blocks yourself (`lint` and `finalize` warn above 12 rows).
- No raw HTML except comments (notes to yourself, on their own line). Anything the lecturer or the user must see or decide goes in a «Вопрос» callout (§5), not in a comment.
- Blockquotes are only for the header block, the draft banner and callouts (§5).

**Figures**

```markdown
![](figures/level-lines.svg)

*Рис. 2. Линейная функция $f(x, y) = 2x + y$: линии уровня — параллельные прямые.*
```

The image goes on its own line. The caption is the next paragraph, wholly in italics, starting with «Рис. N.». In the text, refer to it as «(рис. 2)». Figures are numbered within the lecture.

## 4. Russian typography

- Quotation marks «ёлочки»; nested ones „лапки“.
- Em dash with spaces: « — ». Hyphen in compounds: «Леви-Чивиты».
- Write ё: «начнётся», «чётные», «её».
- Abbreviations with a space: «т. е.», «т. д.», «и т. п.».
- Decimal comma in math: `$3{,}14$`.

## 5. Callouts in drafts

A callout is a blockquote whose first words are a label. One convention serves VS Code (a plain blockquote), the website and the preview (styled by label), and `finalize.py` (handled by label).

```markdown
> **Идея.** Сумма значений индексной функции — число; в этом и состоит аналогия с определённым интегралом. *(00:48:12–00:50:20)*

Сумма значений индексной функции — число, так же как …

> **Вопрос 2.** (00:41:03) В записи «визуализировать лучше … табличкой, которая левая». Понято как таблица-список. Варианты: а) таблица-список; б) двумерная таблица.

> *Замечание.* Полезно переформулировать знакомые понятия на строгом языке множеств и отображений. …
```

- **`> **Идея.** …`** — draft only. One sentence: what the next paragraph establishes (not a summary of its words), with the transcript time it comes from. One before every new paragraph, side remarks included; not before figures, captions or a paragraph that continues after a display formula (it starts in lower case). The lecturer reads these to check that the main idea was understood; when they correct one, rewrite the paragraph from the corrected idea. Left out of the .tex/.pdf; removed from the .md when the lecture is approved (`finalize.py --strip-ideas`).
- **`> **Вопрос N.** (hh:mm:ss) …`** — draft only. Numbers are stable identifiers the lecturer and the user refer to: a new question takes the next free number, even when it sits earlier in the text, and answered numbers are not reused. A question meant for the user rather than the lecturer (when you can't ask them directly, e.g. as a subagent) is labelled `> **Вопрос N (для пользователя).** …`. Something only the lecturer (or the user) can settle: a garbled passage, two possible readings, a term, a proposal that goes beyond the lecture. Say what is unclear and give the options; the text meanwhile carries the most defensible version. Numbered through the lecture. `finalize.py` refuses to run while one is left. (These replace the old invisible `<!-- ПРОВЕРИТЬ … -->` comments: the lecturer reads the rendered page and must see them.)
- **Statements set apart** — a paragraph opening with **Определение.**, **Лемма.**, **Теорема.** or *Доказательство.* — are paragraphs like any other: the statement gets its Идея (what it states), the proof its own (how it goes).
- **`> *Замечание.* …`, `> *Предупреждение.* …`, `> *Забегая вперёд.* …`** — side remarks, part of the book: material that belongs here but isn't used later in the lecture, and is still worth keeping (a bridge to other knowledge, a physics aside). Set smaller and lighter, like a figure caption, never boxed; he approved this look. Use them rarely. His lecture 1 drops such asides altogether and keeps warnings inline.
- **Our own additions are not labelled in the text.** «Замечание редактора» is no longer used (author-rulings 29). Mark an addition in its paragraph's Идея callout, e.g. `> **Идея.** … *(добавление)*`, and list it in the report. `lint_text.py` flags «Замечание редактора», and `finalize.py` refuses it.

## 6. The model: the opening of his lecture 1

His own lecture 1 (`raw/reviews/lecture-01/lecture1_indices.tex`), in this Markdown format, word for word except for typos. `scripts/tex_to_md.py` converts the whole file. This is the standard for format *and* voice: header block, a one-paragraph introduction, display math, a value table, «Вспомним», «Следует понимать», «Как мы увидим», bold only for «Индексной функцией». Figures are where we may add (he praised them): introduce one in the text as a visualization, at most a third of a page, with a short caption.

```markdown
# Лекция 1. Индексы

> **Необходимые знания:** множество, декартово произведение множеств, отображение, числовая функция, последовательность, матрица, умножение матриц.
>
> **О чем лекция:** понятие индексной и многоиндексной функции, операции над ними. Суммы и перестановочность сумм. Символы Кронекера и Леви-Чивиты.

Сегодня — нулевая, вводная лекция курса. Сам тензорный анализ начнётся позже, сейчас нужно навести порядок с индексами. Это материал, который обычно считается «очевидным» и поэтому подробно не объясняется. Между тем, без аккуратного отношения к индексам последующее изложение тензоров и линейной алгебры невозможно. Неформально говоря, цель лекции — научиться работать с такими конструкциями, как

$$
a_i, \quad b_{ij}, \quad \sum_{k=1}^{n} a_{ik} b_{kj}, \quad \delta_{ij}, \quad \varepsilon_{ijk},
$$

понимая их как функции на некотором конечном множестве.

## 1. Функции и отображения

Вспомним понятие функции как частного случая отображения между двумя множествами. Пусть $X, Y$ — два множества. Отображением $f\colon X \to Y$ называется правило, которое каждому элементу $x \in X$ сопоставляет единственный элемент $f(x) \in Y$. Когда $X$ и $Y$ — числовые множества (например, множества действительных чисел $\mathbb{R}$), отображение принято называть числовой функцией, или просто функцией. Так, запись

$$
f\colon \mathbb{R} \to \mathbb{R}, \qquad f(x) = x^2
$$

означает, что каждому действительному числу сопоставлен квадрат этого самого числа. Следует понимать, что имя функции — это $f$. Буква $x$ в записи $f(x) = x^2$ — лишь обозначение аргумента функции; никакого собственного смысла она не несёт. Записи

$$
f(x) = x^2 \qquad \text{и} \qquad f(y) = y^2
$$

описывают одну и ту же функцию $f$. А вот запись $f(x) = y^2$ — бессмыслица.

Заметим, что в физике традиция диктует противоположное: одну и ту же физическую величину часто обозначают конкретной буквой: давление $p(T, V)$ и $p(T, S)$ как функции температуры и объёма в одном случае и температуры и энтропии в другом. Этим удобством мы дальше злоупотреблять не будем: с математической точки зрения это две разные функции, следовательно, должны обозначаться разными буквами.

## 2. Индексные функции

Дальнейшие рассуждения, как, по существу, и вся лекция, будут посвящены некоторому специальному случаю числовых функций, а именно такому, когда область определения функции представляет из себя конечное множество. Как мы увидим, этот случай гораздо проще, чем случай функций, определённых на всём множестве вещественных чисел, однако он менее привычен. Это обстоятельство мы и собираемся устранить, причём уже имеющийся опыт работы с «обычными» функциями будет в этом полезен: многие факты будут перенесены на специальный случай путём полной аналогии.

Зафиксируем натуральное $n \in \mathbb{N}$ и рассмотрим множество

$$
I = \{1, 2, 3, \ldots, n\}.
$$

**Индексной функцией** называется любое отображение $a\colon I \to \mathbb{R}$.

Для таких функций по чисто визуальным причинам принята особая запись: вместо $a(i)$ пишут $a_i$. По определению

$$
a_i \equiv a(i), \qquad \forall i \in I.
$$

Вновь подчеркнём, что $a$ — это имя функции, а $i$ — имя её аргумента. […]
```

The only changes from his file are typos («собсвтенного» → «собственного»), «ё», «» quotes for his "…", and math spacing. When a lecture is rebuilt from his text, every such change is listed for him.
