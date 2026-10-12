# Book register

Contents: 1. The target · 2. What a lecture does that a book doesn't · 3. What stays · 4. Paragraphs: the idea first, the reader led · 5. Claims and pictures · 6. Before and after

Read this every time, together with `author-rulings.md`, which records what the author decided in reviews and overrides anything here.

## 1. The target

The lectures become a **book of lectures**. The titles stay «Лекция N», as in Feynman's lectures, but the text is written for a reader alone with the book who is learning the subject from it. It is not a record of what was said in the room. The lecturer's own description of the goal is to turn the spoken, informal language of the lectures into book language. Every idea of the lecture stays, and the way it is said changes.

Reference points, as the lecturer named them:
- **Landau and Lifshitz, *Course of Theoretical Physics*: the ideal.**
  - Full sentences.
  - Impersonal or authorial-plural voice.
  - Each statement says exactly what is true.
  - Logical connectives carry the argument.
  - No evaluations, no addressing the reader.
  - Digressions are rare and visibly set apart.
- **Feynman's lectures: the outer limit of freedom.** Reasoning aloud, informal remarks and vivid comparisons are allowed, but always in written sentences. Never fragments, and never the room («как вы видите на доске»).

If `raw/style-samples/` exists (pages the lecturer chose as references), read a couple of pages before writing. Don't copy excerpts from these books into the repository, which is public. Describe the register, as here.

## 2. What a lecture does that a book doesn't, and the written equivalent

The lecturer's name for this is «обычное замечание»: a thought that is right, said the way one talks in a lecture, and to be said again in book language. Every example below comes from the review of lecture 1.

| Spoken move | Book form |
|---|---|
| A question thrown at the audience with no build-up: «Можно ли написать $c_{ij} = d_k$?» | First the reason the question arises: «Для индексных функций существует возможность, которой нет у функций на $\mathbb{R}$: …». Then the question or a statement. |
| Addressing the listener: «вы», «попробуйте», «обратите внимание», «уже не запишешь» | Impersonal: «нетрудно убедиться», «следует обратить внимание», «полезно проделать», «записать … уже нельзя» |
| Personal phrasing: «нас сейчас интересует», «нам понадобится» | «В данном случае важна сама операция», «понадобится в дальнейшем» |
| Appeals to experience, school or textbooks: «в учебниках пишут…», «вы учились и не поняли» | State the fact itself. The book builds the subject on its own: «Теперь можно записать определение произведения матриц: …» |
| Emotions and verdicts: «никакой магии», «хитрыми способами», «муторно», «бред», «каша в голове», «ничего сложного» | The precise statement behind them: «вычисление не требует специальных приёмов: все значения находятся непосредственно из определения»; «вычисление громоздко, но не содержит принципиальных трудностей». «Бессмыслица» is a term of the course and stays. |
| Clipped one-liners: «Вот и всё.», «Обычно пишут самую короткую.» | Fold them into the previous sentence, or write a full one: «…матрица — не более чем отображение…»; «Как правило, используется самая короткая из этих записей.» |
| Colloquialisms: «как угодно», «всё равно», «выживают», «на жаргоне», «примем на веру», «ровно для этого и придумано» | «произвольно»; «при отсутствии дополнительных соображений разницы нет»; «входят в результат» / «остаётся одно слагаемое»; drop it; «пока следует принять как данность»; «придумано именно для этого» |
| The time and place of the lecture: «сегодня», «в прошлый раз», «на доске», «позже появится», «я говорил» | «в этой лекции», «в лекции 3», «в дальнейшем». A forward reference to tensors becomes a side remark «*Забегая вперёд.*» |
| Jumps: a digression in the middle of an argument, then back | The main line stays linear. The digression becomes a side remark after the paragraph it belongs to. |
| An analogy stated too strongly: «ту же роль играет сумма» | «аналог», «внешне похожая операция», and what exactly is analogous: the result is a number; the result is a function of the remaining variable. |
| A thought in three short jabs | One sentence joined by a comma or a conjunction: «Обычно матрицу определяют как таблицу чисел, однако на языке множеств и отображений…» |

`scripts/lint_text.py` flags candidates for most of these. The patterns live in `register-patterns.tsv`; add new ones from each review. A flag is a prompt to reread the sentence, not a verdict.

## 3. What stays

- **The authorial «мы»** in its standard mathematical forms: «Рассмотрим», «Докажем», «Обозначим», «будем называть», «Этим удобством мы злоупотреблять не будем». The lecturer approved the last one in review as their own words. What goes is the personal «мы»: «мы привыкли», «нас интересует», «как мы увидим».
- **Questions that the text has prepared for.** «Как задать индексную функцию?» is acceptable in a book; the lecturer approved it.
- **«Неформально: …»** before an informal restatement of a precise statement. Approved.
- **Every analogy, warning and remark of the lecturer, and every step of every computation,** rewritten into book form. The author does the cutting («что сокращать, я сам решу»), not us.
- **The terms of the course:** «бессмыслица», «таблица-список», «индекс суммирования», «свободный индекс». See `author-rulings.md` for rejected terms.

## 4. Paragraphs: the idea first, the reader led

The lecturer asked for the work to be done at the level of ideas: decide what idea a paragraph is meant to convey, then choose the words.

- **One paragraph, one idea, and the paragraph says it**, usually in its first sentence. In a draft, the idea is written above the paragraph as an `> **Идея.** …` callout (see SKILL.md). If a paragraph doesn't deliver its stated idea, or delivers two, rewrite it or split it.
- **Each paragraph starts where the previous one stopped.** Connectives make the logic visible: «поскольку, как только что показано, …», «таким образом», «следовательно», «в отличие от …», «аналогично».
- **Before an important formula, say in words what it will say.** For the interchange of sums: «двойную сумму можно вычислять, суммируя сначала по одному индексу, затем по другому, или в обратном порядке, и результат будет одним и тем же». After a computation, draw the conclusion.
- **Nothing appears without a reason.** No question, figure or example arrives unannounced. The text first shows why it is needed.
- **Side material goes into side remarks:**
  - a useful link to other knowledge that the rest of the lecture doesn't need;
  - a forward reference;
  - a historical or physical aside.

  Side remarks are typographically subordinate. Boxes are reserved for the rare thing the author marks as essential: never box anything on our own initiative.

## 5. Claims and pictures

- **Claim exactly what is true.**
  - Components of a tensor are a set of numbers labelled by indices. They are not the sums one computes with them.
  - Sum and integral are analogous in what they produce, not the same operation.
- **No concept before its definition.** If matrices are defined in §7, §4 talks about «запись в виде двумерной таблицы», not «матрица». Reordering the lecture is allowed, but every move needs this check again (`lint_text.py` flags «BEFORE DEF» candidates).
- **A visualization is an option, never the structure.** The course insists that sets carry no structure beyond what is defined. A picture of $I^2$ as a grid, or of $1, 2, 3$ on a circle, is one convenient way to look at them.
  - Say «можно изобразить», «если расположить … , то …», «удобно представлять».
  - Never «расположены», and never let the logic rest on the picture.
  - A fact such as $(1,2) \ne (2,1)$ holds by definition. A picture only helps to see it.

## 6. Before and after

**Matrix** (§7.1 of lecture 1). Before:

> Самый известный пример функции двух индексов — матрица. Обычно матрицу определяют как «таблицу чисел». На языке множеств и отображений **матрица** — это отображение $a\colon I_1 \times I_2 \to \mathbb{R}$, где … — два конечных множества индексов, вообще говоря разные, потому что матрицы бывают прямоугольными. Вот и всё. Строка и столбец — это функции одного индекса, и записать функцию одного индекса строкой или столбцом — всё равно.

After:

> Самый известный пример функции двух индексов — матрица. Обычно матрицу определяют как таблицу чисел, однако на языке множеств и отображений **матрица** — не более чем отображение $a\colon I_1 \times I_2 \to \mathbb{R}$, где … — два конечных множества индексов, вообще говоря различные, поскольку матрицы бывают прямоугольными. Строка и столбец при этом — функции одного индекса, и при отсутствии дополнительных соображений разницы между ними нет: одну и ту же функцию можно записать и строкой, и столбцом.

**Sums** (§5). The draft listed notation details and buried the point. The idea, stated first:

> **Идея.** Сумма значений индексной функции — число; в этом и состоит аналогия с определённым интегралом, и, как интеграл, сумму можно брать не только по всему множеству определения, но и по его части.

> Сумма значений индексной функции — число, так же как определённый интеграл функции на $\mathbb{R}$ — число. В этом и состоит аналогия между двумя операциями: сумма по всем $i \in I$ — аналог интеграла по всей прямой. Аналогия идёт и дальше: интеграл можно брать по отрезку, а сумму — по части множества определения (по отрезку значений индекса, только по чётным $i$, по $i \ne j$ и т. д.), и результат по-прежнему будет числом. По какому множеству суммировать, определяется задачей.
