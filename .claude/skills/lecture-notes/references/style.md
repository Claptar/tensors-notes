# Style and format

Contents: 1. Voice · 2. Document skeleton · 3. Markdown and math rules · 4. Russian typography · 5. Transcript → text, a worked example · 6. The target: opening of lecture 1 in Markdown

## 1. Voice

The text reads as if the lecturer had sat down and written the lecture out carefully. It is not an account of the lecture ("лектор отметил…") and not a textbook by someone else.

- First person plural and impersonal constructions: «Рассмотрим…», «Заметим, что…», «Следует понимать…», «мы будем называть…». Present tense.
- Keep the lecturer's characteristic moves, because they are the course's pedagogy:
  - the analogy with ordinary functions on $\mathbb{R}$ ("в полной аналогии с $h(x) = f(x)g(x)$");
  - questions that drive the argument ("Что за объект должен стоять в правой части равенства?");
  - warnings and forward references: «**Предупреждение:** …», «Забегая вперёд, скажем…»;
  - the insistence that nothing is magic: "это утомительно, но *концептуально просто*".
- Definitions put the defined term in **bold** in the sentence that defines it: «**Индексной функцией** называется любое отображение $a\colon I \to \mathbb{R}$». Use *italics* for emphasis, sparingly.
- Remarks and proofs stay in prose: «*Замечание.*», «*Доказательство.*» … «что и завершает доказательство.»
- Cut everything that belongs to speech rather than writing: «ну», «вот», «короче», «как бы», «поставьте плюсики», «я сегодня устал», repeated restarts, "понятно, да?".
- Prose, not bullet points. A list is fine for a genuine enumeration (three properties, four cases). It is not a substitute for an explanation.

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
- For a draft, the banner goes right under the title (see SKILL.md).

## 3. Markdown and math rules

The draft is read in VS Code's preview (markdown-it + KaTeX) and later converted to LaTeX by `scripts/finalize.py`. Everything below keeps both working.

**Math**
- Inline: `$a_i$`, with no space just inside the dollars (`$ a_i $` does not render).
- Display: `$$` on its own line, the formula, `$$` on its own line, with a blank line before and after. In LaTeX the formula still stays inside the sentence: text after it that starts in lower case continues the paragraph.
- Cyrillic inside formulas only within `\text{…}`: `\underbrace{(1,2,3)}_{\text{чётные}}`. Other symbols as commands, never as Unicode: `\alpha`, `\varepsilon`, `\to`, `\le`, `\in`, `\infty`. The final build is pdfLaTeX, as on Overleaf. KaTeX renders `ε` or `→` happily and pdfLaTeX stops on them, and the same holds for Greek letters or arrows typed into running text: put them in `$…$`. `render_preview.py` flags all of these as `NOT LATEX-SAFE`.
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
- No raw HTML except comments. Comments carry the `<!-- ПРОВЕРИТЬ 00:41:12: … -->` markers, on their own line.

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

## 5. Transcript → text, a worked example

The transcript (lecture 1, about 10 minutes in; Whisper output, unpunctuated):

> есть понятие функция функция то в принципе такое школьное знание в на первом курсе его обобщают говорят это словом отображения … функция обычно называют отображение из множества чисел множество чисел … Как мы задаем вот обычные функции, которые в девятом классе вы проходили там дорам написали f от x равно x квадрат что-то значит это значит что если мы берем число x ему соответствие ставится число x квадрата вот почему именно x никакого разницы нет вот нам надо четко понимать что f это название функции x никакого отношения к этой функции не имеет то есть если я напишу f от y равно y квадрат то это будет описание той же самой функции … значит это важно это реально важно … у нас из физики кто вот физикой занимается у нас проблема большая потому что мы достаточно часто пишем функции одной и той же буквой … если вы занимаетесь какой-то там термодинамикой то мы можете часто писать pt и там пэт в и как-то приравнивать это все разные вещи … ну так все же все понимаю да поставьте плюсики …

What the finished lecture made of it (section 1 below):
- Kept the idea and its weight: the name of the function is $f$, the letter $x$ means nothing on its own. "Это реально важно" becomes the firm statement «Следует понимать…» and the counterexample «$f(x) = y^2$ — бессмыслица», which was crossed out in the handnotes.
- Kept the lecturer's physics aside, reconstructed from the garbled «pt и там пэт в» as $p(T, V)$ against $p(T, S)$, and turned it into a stated convention for the course: «Этим удобством мы дальше злоупотреблять не будем».
- Dropped the school reminiscences, "поставьте плюсики", and the repetition.
- Promoted the informal "отображение — это когда спарили элементы" to a proper definition, because the lecturer was clearly giving one.

## 6. The target: opening of lecture 1 in Markdown

This is the finished "Лекция 1. Индексы" (the PDF in `raw/examples/`) as it looks in this Markdown format. Match its density, tone and precision.

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
