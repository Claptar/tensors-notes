# The author's rulings

What the lecturer decided while reviewing drafts. These rulings override the recordings: if the lecturer said something one way in a lecture and has since ruled otherwise, the ruling wins. They also override the skill's own defaults. Read this file before writing or revising any lecture. Apply each ruling to every lecture, not only the one where it came up.

Each entry gives the ruling, its source (the review and the time in that recording) and, where useful, what to do. Reviews are kept in `raw/reviews/lecture-NN/` (decoded as `review.utf8.txt`). Add new rulings at the end of their section, with the date. When the lecturer answers a «Вопрос» with something general, it belongs here too.

## Register and form

1. **Book language, not lecture speech.** The model is Landau–Lifshitz; Feynman's lectures are the most freedom allowed. *(Lecture 1 review, 2026-10-12, 00:39–02:21, 16:29.)* How: `register.md`.
2. **No personal pronouns or addressing the reader where it can be avoided.** «нас сейчас интересует» → «в данном случае важна сама операция»; «пока примем на веру» → «пока следует принять как данность»; «не запишешь» → «не записать». The authorial «Рассмотрим», «будем называть» stays. *(19:22–19:54, 37:14, 44:19.)*
3. **No references to textbooks, to the reader's past experience or difficulties, and no emotion.** The book is a sequential exposition in which the reader builds the subject. The physics conventions ("физики пишут так, мы так не будем") are not this: they are useful remarks and they stay. *(39:10–41:04.)*
4. **No clipped sentences** («Вот и всё.», «Обычно пишут самую короткую.»): fold them into the neighbouring sentence. Don't chop one thought into several sentences. *(33:52–36:34.)*
5. **The narrative is linear, and nothing falls from the sky.** A question, a picture or an example needs a lead-in. Spoken jumps (a digression, then back) are not allowed. *(16:29–17:22, 46:42.)*
6. **Decide each paragraph's idea first, then the words.** The main idea must be stated, not buried. In drafts this is the «Идея» callout. *(22:22–23:19.)*
7. **«Неформально: …»** before an informal restatement is approved. *(43:48–44:19.)*
8. **Questions the text has prepared for are fine**, e.g. «Как задать индексную функцию?». *(04:49.)*

## Content and claims

9. **Keep every detail, as in the lectures.** The author decides what to cut («что сокращать, я сам решу»). Don't shorten on our own. *(05:14, 03:07.)*
10. **Remarks that no additional structure is assumed must never be dropped.** For example, $\mathbb{R}^2$ is just a set of ordered pairs, not the plane with distances and angles. *(09:42–10:12.)*
11. **Visualizations are optional.** Write «могут быть изображены / если расположить … , то …», never «расположены». Facts hold by definition, and the picture only helps to see them. The reader must not come away thinking the picture is always there or always needed. *(11:55–13:31, 18:27, 46:42.)*
12. **Sum and integral are analogous, not the same.** Say «аналог» and «внешнее сходство», and say what is analogous: the result is a number; summing over one index leaves a function of the others. Never «ту же роль». In lecture 1 the lecturer did say «то, что с непрерывными интеграл называется, тут будет суммами» (00:20:47) and «полный аналог» (00:50:13); this ruling supersedes that. *(20:12–21:53.)*
13. **No concept before its definition.** In lecture 1, §4.3 must not use «матрица» or $A^{\mathrm{T}}$: matrices are defined in §7. Say «если записать функцию двумерной таблицей, она симметрична относительно главной диагонали». *(18:27–19:22.)*
14. **Before tensors are introduced, mentions of tensors are side remarks.** «Вектор — столбец, тензор — трёхмерная таблица» is at most a remark. Tensor ≠ its components. *(14:21–14:54, 44:47.)*
15. **Be precise about what components are.** The goal of lecture 1 is to learn to work with expressions such as $a_i$, $b_{ij}$, $\sum_k a_{ik}b_{kj}$. It is not true that tensor components *are* such sums. *(01:20–02:21.)*
16. **Motivate computations and draw conclusions.** Example: why the contraction of two $\varepsilon$ is worth computing (double cross product, curl of a cross product); what the computation showed. *(48:59–50:57.)*

## Pictures and layout

17. **Captions may carry secondary details.** Don't repeat the caption in the text. *(02:44–03:07.)*
18. **Side remarks** («Замечание», «Предупреждение», forward references) are typographically subordinate, «как подпись к рисунку»: smaller or lighter text. Not boxes, which are reserved for the rare thing the author marks as very important. Design for paper first. *(05:37–06:43, 26:31–28:00.)* The exact style is open (see below).
19. **«Предупреждение» is a caution, not something essential: not bold.** «Доказательство» may be bold. *(31:05.)* Pending the style choice.
20. **Figures must not stick out.** Labels go inside the figure's rectangle. Tints don't touch brackets. A correspondence is drawn with arrows, not described as «положить A под B». *(32:24–32:58, 38:11–38:54.)*
21. **Tables:** align signed numbers so that −1 doesn't stand out. *(48:03.)*

## Terms

22. **«таблица-список» is approved.** *(13:53.)*
23. **«квадратная таблица» is rejected.** It is odd for three indices or for $m \ne n$. The lecturer suggested «"многомерная" таблица», in quotes. The replacement is open (lecture 1, «Вопрос»). *(13:53–14:21.)*

## What to keep doing (praised in review)

- Figures that show a mechanism: the summed table (fig. 4, «шикарная картинка») and matrix times column (fig. 5, «волшебные»). Captions that explain them. *(31:35–32:09, 37:52.)*
- The physics convention paragraph ($p(T,V)$ against $p(T,S)$): «мои слова, всё супер». *(03:33–04:30.)*
- The composition paragraph («гениально»), the «Предупреждение» on the Einstein rule, the proof of the interchange of sums, and the «Неформально:» paragraph on $\delta$. *(08:19, 26:31–29:01, 31:35, 43:48.)*
- The editor's remark on antisymmetry: «это вообще чётко». *(47:14.)*

## Open: the author still has to decide

Each item is also a «Вопрос» in the draft where it arises. Move it up into a ruling once it is answered.

- **The style of side remarks:** one of the options on `raw/reviews/lecture-01/aside-options.pdf`.
- **§3 of lecture 1:** expository version, or questions and answers in book register. The lecturer asked for both. Speaker 2 likes the dialogue tone, Speaker 1 prefers the book. Afterwards keep one register for the whole book. *(06:43–07:51.)*
- **A single definition of «индексная функция»:** any $a\colon I^k \to \mathbb{R}$, with no separate «многоиндексная». *(00:01, 10:12–11:07.)*
- **A definition of even and odd permutations that doesn't depend on dimension.** *(46:10–46:42.)*
- **Whether fig. 3 (the grid of $I^2$) is needed at all.** *(08:56.)*
- **Whether the remarks on functions, operators and functionals, and on $T(x,y)$ against $T(\vec r)$, stay.** The lecturer may cut them; until then keep them, improved. *(03:07, 17:22.)*
