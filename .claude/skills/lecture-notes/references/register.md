# Book register

Contents: 1. The target · 2. What a lecture does that a book doesn't · 3. What stays · 4. Paragraphs: the idea first, the reader led · 5. Claims and pictures · 6. Before and after

Read this every time, after `author-model.md` (how his own lecture 1 was made from his recording; it overrides anything here) and together with `author-rulings.md` (what he decided in reviews).

## 1. The target

The lectures become a **book of lectures**. The titles stay «Лекция N», as in Feynman's lectures, but the text is written for a reader alone with the book who is learning the subject from it. It is not a record of what was said in the room. **The target is his own lecture 1**: book language made from his spoken lecture. What the rest of the lecture builds on stays; asides it doesn't use go (`author-model.md` §2).

Reference books, each for one thing (his notes, `raw/reviews/lecture-01/style.utf8.txt`; details in `author-model.md` §6):
- **Wording: Landau–Lifshitz** (vols. 1 and 5; vol. 2 acceptable). Full, exact sentences in the authorial «мы»; logical connectives carry the argument; no evaluations, no addressing the reader.
- **How the narrative is built: Slobodyanyuk «Физика для любознательных»** (`raw/examples/Слободянюк т1–т4.pdf`), **Feynman's lectures, the Berkeley course**. A problem before the concept; questions at turning points, answered at once; recurring themes flagged; arbitrariness of conventions stressed; small print for what isn't needed later.
- **Layout: MTW «Гравитация»**: what goes into a footnote, a figure, a supplement. Its captions are too long for us.
- **Feynman and Slobodyanyuk are the ceiling of chattiness.** Ours stays below it, as his text does: no «вы», no exclamations, no jokes.

Don't copy excerpts from these books into the repository, which is public. Describe the features, as here.

## 2. What a lecture does that a book doesn't, and the written equivalent

The lecturer's name for this is «обычное замечание»: a thought that is right, said the way one talks in a lecture, and to be said again in book language. Every example below comes from the review of lecture 1.

| Spoken move | Book form |
|---|---|
| A question thrown at the audience with no build-up: «Можно ли написать $c_{ij} = d_k$?» | First the reason the question arises: «Для индексных функций появляется одна особенность, аналога которой нет для одноиндексных…». A question the text has prepared stays a question, answered at once: «Имеет ли смысл писать $a = b$? Да.»; «Что за объект должен стоять в правой части равенства?» |
| Addressing the listener: «вы», «попробуйте», «уже не запишешь», «поставьте плюсики» | Impersonal: «нетрудно убедиться», «полезно проделать», «записать … уже нельзя». His own «заметьте», «обратите внимание» (three times in lecture 1) are allowed, sparingly |
| Personal phrasing: «нас сейчас интересует», «нам понадобится» | «В данном случае важна сама операция», «понадобится в дальнейшем» |
| Appeals to experience, school or textbooks: «в учебниках пишут…», «вы учились и не поняли» | State the fact itself. The book builds the subject on its own: «Теперь можно записать определение произведения матриц: …» |
| Emotions and verdicts: «хитрыми способами», «муторно», «бред», «каша в голове», «ничего сложного», «магия» as a mood | The fact behind them. His: «Следует очень чётко понимать, что никакой магии тут нет: достаточно построить таблицу всех значений руками. Это утомительно, но *концептуально просто*.» — once, with the reason right after it. «Бессмыслица» is a term of the course and stays. |
| Clipped one-liners: «Вот и всё.», «Обычно пишут самую короткую.» | Fold them into the previous sentence, or write a full one: «…матрица — не более чем отображение…»; «Как правило, используется самая короткая из этих записей.» |
| Colloquialisms: «как угодно», «всё равно», «выживают», «на жаргоне», «примем на веру», «ровно для этого и придумано» | «произвольно»; «при отсутствии дополнительных соображений разницы нет»; «входят в результат» / «остаётся одно слагаемое»; drop it; «пока следует принять как данность»; «придумано именно для этого» |
| The time and place of the lecture: «в прошлый раз», «на доске», «сегодня мы…», «я говорил» | «в этой лекции», «в лекции 3». «Сегодня — нулевая, вводная лекция курса» opening the chapter and «позже», «в дальнейшем» are his. A forward reference to tensors is one sentence («Забегая вперёд скажем, что…»), kept only if it prevents a misreading |
| Jumps: a digression in the middle of an argument, then back | The main line stays linear. The digression becomes a side remark after the paragraph it belongs to. |
| An analogy stated too strongly: «ту же роль играет сумма» | «аналог», «внешне похожая операция», and what exactly is analogous: the result is a number; the result is a function of the remaining variable. |
| A thought in three short jabs | One sentence joined by a comma or a conjunction: «Обычно матрицу определяют как таблицу чисел, однако на языке множеств и отображений…» |

`scripts/lint_text.py` flags candidates for most of these. The patterns live in `register-patterns.tsv`; add new ones from each review. A flag is a prompt to reread the sentence, not a verdict.

## 3. What stays

- **The authorial «мы»**, as in his text (17 times in lecture 1): «Рассмотрим», «Докажем», «мы будем по определению называть», «мы имеем дело», «Как мы увидим», «Это обстоятельство мы и собираемся устранить», «Этим удобством мы дальше злоупотреблять не будем». What goes is the room's «мы»: «мы привыкли», «нас сейчас интересует», «давайте».
- **His connectives**, which call back to what has been said: «Как уже было сказано», «Как было выяснено», «Вновь подчеркнём», «Вновь прослеживается полная аналогия», «Для полноты картины скажем», «Строго говоря», «Следует понимать», «Неформально говоря». Prefer them to generic «Заметим», «Таким образом».
- **Questions that the text has prepared for.** «Как задать индексную функцию?» is acceptable in a book; the lecturer approved it.
- **«Неформально: …»** before an informal restatement of a precise statement. Approved.
- **What the rest of the lecture builds on:** definitions, the comparison with functions on ℝ (one analogy per point), warnings that prevent a misreading, and the computations the reader needs. Asides the lecture doesn't use later go (review 2, 03:03; `author-model.md` §2.1). Repeated cases become one argument.
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

  Side remarks are typographically subordinate. Boxes are reserved for the rare thing the author marks as essential: never box anything on our own initiative. First apply the "used later?" test: in his lecture 1, such material is mostly dropped, not demoted.

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

The real pairs are in `author-model.md` §2.4: eight places where his spoken lecture 1 and his written text say the same thing. Read them before writing. Two short ones:

- *Spoken* (00:16:06–00:18:29): «Могу ли я написать, например, A равно B? Кто за? Ставьте плюсик… Могу, правильно… A ИТА равно B ЖИТА?… эта запись, она бессмысленная. Это полный бред». *His text*: «Имеет ли смысл писать $a = b$? Да. Это утверждение о функциях… Имеет ли смысл писать $a_i = b_j$? Это бессмыслица в том виде, в каком написана.»
- *Spoken* (01:13:52): «суммируемый индекс он вырезает из всех и своего брата…». *His text*: «Неформально говоря, суммирование с $\delta_{ij}$ заменяет индекс $i$ на $j$ во всех вхождениях, а на остальные индексы никак не влияет.»

The replacements suggested in review 1 («пока следует принять как данность», «при отсутствии дополнительных соображений разницы нет») show a direction. They are not wording to paste: where his text says such a thing, it says it in its own full sentence.
