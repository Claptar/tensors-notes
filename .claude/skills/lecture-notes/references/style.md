# Style and format

Contents: 1. Voice · 2. Document skeleton · 3. Markdown and math rules · 4. Russian typography · 5. Callouts in drafts · 6. Format example: the opening of lecture 1

## 1. Voice

The register is a book's, not a lecture's: read `register.md` (what to transform, what to keep, before/after examples) and `author-rulings.md` (what the author has decided) every time. The typographic conventions that go with it:

- Definitions put the defined term in **bold** in the sentence that defines it: «**Индексной функцией** называется любое отображение $a\colon I \to \mathbb{R}$». Use *italics* for emphasis, sparingly.
- Proofs stay in prose: «*Доказательство.*» … «что и завершает доказательство.»
- Side remarks («Замечание», «Предупреждение», «Забегая вперёд») are callouts, see §5: they are set apart typographically, so the main line stays linear.
- Prose, not bullet points. A list is fine for a genuine enumeration (three properties, four cases); it is not a substitute for an explanation.

## 2. Document skeleton

```markdown
# Лекция 4. Линейные формы

> **Необходимые знания:** линейное пространство, базис, разложение вектора по базису (лекции 2–3).
>
> **О чем лекция:** функции на линейном пространстве; линейные формы и их геометрический смысл; компоненты линейной формы в базисе.

Вводный абзац: что сегодня и зачем, как это связано с прошлой лекцией — в той рамке, которую задал сам лектор в начале записи.

## 1. Название раздела

Текст…

### 1.1. Подраздел

Текст…

## 2. …

---

*Конец лекции 4.*
```

- **Необходимые знания**: what the lecture actually relies on, both general mathematics and earlier lectures (name them).
- **О чем лекция**: the topics as noun phrases, one or two sentences.
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
- Markdown tables are fine for simple value tables. Inside a table cell write `\vert` or `\mid` instead of `|` in math.
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
- **`> *Замечание.* …`, `> *Предупреждение.* …`, `> *Забегая вперёд.* …`, `> *Замечание редактора.* …`** — side remarks, part of the book: material that belongs here but doesn't carry the main line (a bridge to other knowledge, a caution, a forward reference to tensors, a physics aside). Set smaller and lighter, like a figure caption; never boxed. «Замечание редактора» marks our own addition in a draft; when the author accepts it, relabel it «Замечание».

## 6. Format example: the opening of lecture 1

The original "Лекция 1. Индексы" (the PDF in `raw/examples/`) as it looks in this Markdown format — header block, display math, a value table, a figure with its caption. Use it for format. For register, `register.md` and `author-rulings.md` take precedence: this text predates the author's review (e.g. its «Сегодня» is lecture-time phrasing the book now avoids), and the current `docs/lecture-01/lecture-01.md` is the reviewed version.

```markdown
# Лекция 1. Индексы

> **Необходимые знания:** множество, декартово произведение множеств, отображение, числовая функция, последовательность, матрица, умножение матриц.
>
> **О чем лекция:** понятие индексной и многоиндексной функции, операции над ними. Суммы и перестановочность сумм. Символы Кронекера и Леви-Чивиты.

Сегодня — нулевая, вводная лекция курса. Сам тензорный анализ начнётся позже, сейчас нужно навести порядок с индексами. Это материал, который обычно считается «очевидным» и поэтому подробно не объясняется. Между тем без аккуратного отношения к индексам последующее изложение тензоров и линейной алгебры невозможно. Неформально говоря, цель лекции — научиться работать с такими конструкциями, как

$$
a_i, \qquad b_{ij}, \qquad \sum_{k=1}^{n} a_{ik} b_{kj}, \qquad \delta_{ij}, \qquad \varepsilon_{ijk},
$$

понимая их как функции на некотором конечном множестве.

## 1. Функции и отображения

Вспомним понятие функции как частного случая отображения между двумя множествами. Пусть $X, Y$ — два множества. **Отображением** $f\colon X \to Y$ называется правило, которое каждому элементу $x \in X$ сопоставляет единственный элемент $f(x) \in Y$. Когда $X$ и $Y$ — числовые множества (например, множество действительных чисел $\mathbb{R}$), отображение принято называть числовой функцией, или просто функцией. Так, запись

$$
f\colon \mathbb{R} \to \mathbb{R}, \qquad f(x) = x^2
$$

означает, что каждому действительному числу сопоставлен квадрат этого самого числа. Следует понимать, что имя функции — это $f$. Буква $x$ в записи $f(x) = x^2$ — лишь обозначение аргумента функции; никакого собственного смысла она не несёт. Записи

$$
f(x) = x^2 \qquad \text{и} \qquad f(y) = y^2
$$

описывают одну и ту же функцию $f$. А вот запись $f(x) = y^2$ — бессмыслица.

Заметим, что в физике традиция диктует противоположное: одну и ту же физическую величину часто обозначают одной буквой — давление $p(T, V)$ и $p(T, S)$ как функцию температуры и объёма в одном случае и температуры и энтропии в другом. Этим удобством мы дальше злоупотреблять не будем: с математической точки зрения это две разные функции, следовательно, они должны обозначаться разными буквами.

## 2. Индексные функции

Дальнейшие рассуждения, как, по существу, и вся лекция, будут посвящены специальному случаю числовых функций, а именно такому, когда область определения функции представляет собой конечное множество. Этот случай гораздо проще, чем случай функций, определённых на всём множестве вещественных чисел, однако он менее привычен. Опыт работы с «обычными» функциями здесь будет полезен: многие факты переносятся на новый случай путём полной аналогии.

Зафиксируем натуральное $n \in \mathbb{N}$ и рассмотрим множество

$$
I = \{1, 2, 3, \dots, n\}.
$$

**Индексной функцией** называется любое отображение $a\colon I \to \mathbb{R}$. Для таких функций по чисто визуальным причинам принята особая запись: вместо $a(i)$ пишут $a_i$. По определению

$$
a_i \equiv a(i), \qquad \forall i \in I.
$$

Вновь подчеркнём, что $a$ — это имя функции, а $i$ — имя её аргумента.

[…] Множество определения индексной функции конечно, поэтому самым естественным способом её задания является перечисление значений при всех возможных аргументах — таблица:

| $i$ | $1$ | $2$ | $3$ | $\cdots$ | $n$ |
|---|---|---|---|---|---|
| $a_i$ | $a_1$ | $a_2$ | $a_3$ | $\cdots$ | $a_n$ |

График индексной функции на декартовой плоскости вырождается в конечное множество точек (рис. 1), поэтому графический способ не имеет преимуществ перед таблицей.

![](figures/index-function-graph.svg)

*Рис. 1. График индексной функции $a\colon I \to \mathbb{R}$ — всего $n$ точек; таблица несёт ту же информацию нагляднее.*
```

(The figure in this excerpt shows *where* a figure fits naturally. The original lecture 1 has no figures, and adding them is the kind of improvement that's wanted.)
