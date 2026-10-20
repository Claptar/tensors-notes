# The author model

What the lecturer wants, worked out from the evidence: his own written lecture, what he cut from it, his two reviews and the books he named. **Read this first, every time, before `author-rulings.md`, `register.md` and `style.md`.** Where they disagree with this file, this file wins.

Every claim carries its evidence and a grade:

| Grade | Meaning |
|---|---|
| **(a)** | his written text does it |
| **(b)** | he cut it from his text |
| **(c)** | he said it in a review |
| **(d)** | our inference: treat as a working hypothesis, and ask when it decides something |

Sources:
- his lecture 1: `raw/reviews/lecture-01/lecture1_indices.tex`, as a PDF in `raw/examples/Лекция_1__Индексы_261009_134430.pdf`;
- review 1, 2026-10-12: `raw/reviews/lecture-01/review.utf8.txt`;
- review 2, 2026-10-19: `raw/reviews/lecture-01/monday19.10.26.utf8.txt` (a UTF-8 copy of the UTF-16 original);
- his notes on reference books, 2026-10-19: `raw/reviews/lecture-01/style.utf8.txt` (likewise);
- the lecture 1 recording: `raw/transcipts/lecture1/`;
- the lecture 1 handnotes: `raw/handnotes/1 Индексы_260114_204948.pdf`.

Times in the form 00:00 refer to a review; times in the form 00:00:00 refer to the lecture recording.

## 1. The standard

- **His written lecture 1 is the standard («референс — это абсолютная правда для нас»).** Every other comment in review 2 says how our draft differs from it, and the target is «максимально похоже». *(c, review 2 00:00–01:28, 04:42–05:20, 08:04–09:10)*
- **The task is to learn the step from his lecture to that text** and repeat it for lectures 2, 3, 5 and the rest: «у тебя есть моя лекция записанная текстом, мой конспект, и референс файл… это тот идеал». *(c, 08:04–09:10)*
- **He was already measuring us against it in review 1.** At 04:12 he compared our draft with «тот файл, который мы засылали текстовом», and the paragraphs he praised were those that matched it: «дословно, как в нём… стиль мне здесь очень нравится». *(c)* **Praise tracks how close we came to his text.** *(d)*
- **The order of authority:** his text, then what he decided explicitly in a review, then the recording. Our own taste ranks below all three.
- **Reading a review comment.** A comment means "you drifted from how I write", and it is resolved by looking at how his text does it. Don't turn a comment into a general ban. After review 1 we did exactly that and banned words his own text uses (§4). *(d, learned the hard way)*
- **Only book register for now.** A conversational mode may come later. *(c, 00:49)*

## 2. From the recording to his text (lecture 1)

The recording is 66.5k characters over 1 h 19 min. His text is 22.6k characters of prose, excluding formulas, in 190 sentences: about 34% of the recording. Section by section:

| His section | Prose chars | From the recording | What happened |
|---|---|---|---|
| Header + intro (1 paragraph) | 530 | 00:00:00–00:08:05; 01:18:26 | 8 minutes of logistics, the course programme and motivation become one paragraph. «у нас это всё считают простым» moved from the end of the lecture to the opening |
| 1 Функции и отображения | 1 040 | 00:08:05–00:10:20; 00:16:06 | Kept: function as a map, f vs its argument, f(x)=y² is nonsense (moved here from the §3 discussion), physics p(T,V)/p(T,S). Dropped: operators and functionals |
| 2 Индексные функции | 2 520 | 00:10:20–00:14:00; 00:20:39; 00:37:19 | Kept: I, a: I→ℝ, notation a_i «по чисто визуальным причинам», ways to specify (graph, formula, table), sequences. Dropped: 2−x=3 (boxed in the handnotes!), the 4-row example table |
| 3 Равенство и операции | 1 670 | 00:14:53–00:19:33 | Kept as questions answered at once. Dropped: b=a+1 and the function «1» (00:23:50–00:27:27), composition (00:27:27–00:28:32) |
| 4 Многоиндексные функции | 5 010 | 00:28:32–00:41:40; 01:02:08 | Kept: I^k, ordered pairs, both tables (he enlarged 3×3 to 4×4), operations, renumbering. Symmetry moved here from the end, antisymmetry added. Dropped: ℝ² «без дополнительной структуры», ℝ² as a plane, «тензор ≠ компоненты», T(x,y)/T(r⃗), «вектор — столбик… тензор — трёхмерная таблица» |
| 5 Суммы. Перестановочность сумм | 3 730 | 00:43:44–01:02:08 | Kept: integral ↔ sum, subsets, the «что за объект?» question, dummy/free indices, renaming, Einstein warning, the interchange proof, one sum sign, free indices. Dropped: Taylor lower limit, dt′/t′, upper/lower indices, p(x)=h(x,x,x) |
| 6.1 Прогрессии | 570 | — | **Added by him** |
| 6.2 Матрицы | 2 270 | 00:44:47; 01:02:08–01:06:46 | Kept: matrix as a map, row = column, A·b example, C=AB. Added: Σa_ik b_kk and Σa_iki don't fit the matrix algorithm; associativity proof. Dropped: «если открыть книжку», «мне на первом курсе — бред» |
| 6.3 Символ Кронекера | 1 250 | 01:06:46–01:13:52 | Kept: definition, unit matrix, proof at fixed j, f_i… → f_j…, «Неформально говоря». Dropped: «вы знаете ответ… допустим, не знаем», «никакой магии» (here), n = 3 or 4 in physics |
| 6.4 Символ Леви-Чивиты | 1 560 | 00:41:40–00:46:52 | **Moved** from the middle of the lecture to the examples. Kept: definition, 6 permutations, parity, the 27-row table (in 3 blocks), the 3D table remark, «Забегая вперёд» on the tensor. Dropped: «пятнашки», «когда их 50» |
| 6.5 Сумма двух символов | 1 910 | 01:13:52–01:18:26 | Kept: physics motivation, «что за объект?», zeros, i=1, j=2. Added: εε = δδ − δδ as «интересный факт», cyclic symmetry, a forward reference to the determinant. «Никакой магии» kept once, with its reason. Dropped: «по-хитрому… нас не учили руками» |

### 2.1 What he drops *(b, except where marked)*
- **Always:**
  - logistics, homework, the course programme;
  - interaction with the room («ставьте плюсики», «Тёмыч, а ты что молчишь?»);
  - personal stories («я себя словил», «мне на первом курсе»);
  - textbooks and bad courses («если открыть книжку», «плохие курсы»).
- **Asides that later parts of the lecture don't use, even ones he enjoyed saying:**
  - operators/functionals;
  - 2−x=3;
  - b=a+1 with the function «1»;
  - composition;
  - ℝ² as a metric plane;
  - T(x,y)/T(r⃗);
  - Taylor's lower limit;
  - dt′/t′;
  - upper/lower indices;
  - p(x)=h(x,x,x);
  - «пятнашки»;
  - «тензор — трёхмерная таблица».

  In his text these are **dropped, not demoted**: it has no small print at all. In review 2 he allows either: «выносить в качестве замечания чуть более мелким шрифтом… либо вообще убрать» *(c, 03:03)*. The test is **«если какое-то знание не используется в дальнейшем… значит, это знание не фундаментально»** *(c, 03:03–03:54)*.
- **Boxed is not kept.** The handnotes box 2+x=3 with y: ℝ→{да, нет}, and his text drops it. The board shows what he stressed *in the room*, not what the book keeps. *(b)*
- **His own cut lines in the .tex:**
  - line 136: «для конечного n… никакой формулы не требуется»;
  - line 160: the gloss on a_i = b_i;
  - lines 233–235: a «не путайте c_ij с тензором» remark;
  - line 379: the matrix product «с потолка… мы оценим позже»;
  - the «Краткое резюме» list with a closing paragraph, moved after `\end{document}` so it never prints.

  **No end-of-lecture summary.** *(b)*

### 2.2 What he adds *(a)*
- progressions (6.1);
- functions on $I_1\times I_2\times\dots$ (§4);
- the remark on the term «индексная» (§4);
- antisymmetry next to symmetry (§4);
- «Впрочем, это вопрос определений» on sequences (§2);
- the associativity proof (6.2);
- matrix-notation limits (6.2, 6.3);
- the δδ−δδ formula, the cyclic symmetry and the determinant forward reference (6.5).

**Additions by the author are normal in the book** (review 2: progressions «я сам добавил… можешь подгрузить» *(c, 08:04)*). Additions by *us* still need his approval (`SKILL.md`, principle 5).

### 2.3 What he moves *(a)*
- f(x)=y² into §1;
- «считается очевидным» into the intro;
- symmetry from after the sums into §4;
- Levi-Civita from minute 41 into the examples;
- the determinant from minute 44 into the last paragraph.

**The order is logical, not the order of speaking:** definitions, then operations, then sums, then examples.

### 2.4 Spoken → written, verbatim pairs

1. **Intro.** *Speech* (00:07:10, 01:18:26): «…чтобы не было никакой каши в голове… у нас это всё считают простым, поэтому нигде это нету». *His text:* «Это материал, который обычно считается «очевидным» и поэтому подробно не объясняется. Между тем, без аккуратного отношения к индексам последующее изложение тензоров и линейной алгебры невозможно.»
2. **Name vs argument.** *Speech* (00:09:11): «нам надо чётко понимать, что f это название функции, x никакого отношения к этой функции не имеет, то есть если я напишу f от y равно y квадрат, то это будет описание той же самой функции». *His text:* «Следует понимать, что имя функции — это f. Буква x в записи f(x) = x² — лишь обозначение аргумента функции; никакого собственного смысла она не несёт. Записи … описывают одну и ту же функцию f.»
3. **Physics.** *Speech* (00:09:11–00:10:20): «мы достаточно часто пишем функции одной и той же буквой… если вы занимаетесь какой-то там термодинамикой, то можете часто писать „pt“ и там „пэт в“… это всё разные вещи… хотя это, строго говоря, не…» (Whisper). *His text:* «Заметим, что в физике традиция диктует противоположное… Этим удобством мы дальше злоупотреблять не будем: с математической точки зрения это две разные функции, следовательно, должны обозначаться разными буквами.»
4. **A question to the room becomes a question with its answer.** *Speech* (00:16:06–00:18:29): «Могу ли я написать, например, A равно B? Кто за? Ставьте плюсик… Могу, правильно… A ИТА равно B ЖИТА?… эта запись, она бессмысленная. Это полный бред». *His text:* «Имеет ли смысл писать a = b? Да. Это утверждение о функциях… Имеет ли смысл писать a_i = b_j? Это бессмыслица в том виде, в каком написана.»
5. **The kind of object first.** *Speech* (00:50:03–00:51:09): «Это что за объект получится? Ну, не чему он будет равен, а хотя бы что за объект получится? Нет, это уже не число будет. Какой-то b житая». *His text:* «Что за объект должен стоять в правой части равенства? При каждом фиксированном j правая часть — какое-то число; меняя j, мы получаем разные числа. Следовательно, необходимый объект есть *новая функция* от оставшегося индекса j.»
6. **A warning.** *Speech* (00:54:26): «будет такое правило суммирования Эйнштейна, что якобы там не может быть больше двух индексов. Пока может. Там на это свои будут причины… мы говорим про абстрактные функции». *His text:* «Предупреждение: позже, в контексте тензоров, появится «правило Эйнштейна», запрещающее одному индексу встречаться более двух раз. Однако к самим индексным функциям оно не относится, причина его появления лежит в природе тензорных операций и будет раскрыта позже.»
7. **The informal rule.** *Speech* (01:13:52): «суммируемый индекс он вырезает из всех и своего брата… везде где что здесь было написано вместо и будет написано же, а всё остальное не меняется» (Whisper). *His text:* «Неформально говоря, суммирование с δ_ij заменяет индекс i на j во всех вхождениях, а на остальные индексы никак не влияет.»
8. **Emotion becomes a stated fact.** *Speech* (01:14:59–01:17:18): «есть способы, как это сделать по-хитрому… нас не учили руками… магии здесь нет… это муторно, но это очень важно… двойное векторное произведение, там всякие роторы». *His text:* «…которое часто встречается в физических задачах: двойное векторное произведение, ротор векторного произведения и т. п. … Следует очень чётко понимать, что никакой магии тут нет: достаточно построить таблицу всех значений руками. Это утомительно, но *концептуально просто*.»

## 3. How he writes *(a; counts per his live text)*

- **The authorial «мы» is his** (17 occurrences): «мы имеем дело», «мы будем по определению называть», «мы и собираемся устранить», «Как мы увидим», «Этим удобством мы дальше злоупотреблять не будем». **«вы», «вас», «вам»: 0.** Addressing the reader in the imperative is rare but present: «заметьте», «обратите внимание» (×3).
- **The opening is framed as a lecture-chapter:** «Сегодня — нулевая, вводная лекция курса». Forward references use «позже» (×5), «в дальнейшем», «значительно позже».
- **His connectives** show the logic and bring back recurring themes:
  - «Как уже было сказано» (×3);
  - «Вновь подчеркнём», «Вновь обратите внимание», «Вновь прослеживается полная аналогия», «Вновь обратим внимание»;
  - «Для полноты картины скажем»;
  - «Строго говоря»;
  - «Как бы то ни было»;
  - «Как всегда, резонность… диктуется практикой»;
  - «Забегая вперёд скажем»;
  - «Неформально говоря» (×2);
  - «Следует понимать», «Следует чётко понимать».
- **Questions are answered at once:** «Имеет ли смысл писать a = b? Да.», «Что за объект должен стоять в правой части равенства?», «Первый вопрос — что за объект получится? Получится, как несложно понять, …», «Следующий вопрос — когда A заведомо равно нулю?».
- **Everything new is compared with functions on ℝ:** «аналог» ×15, «полная аналогия», «полный аналог h(x) = f(x)g(x)», «в полной аналогии с h(x,y,z)». The analogy is stated as an analogy, with what is analogous.
- **Arbitrariness and convention are a leitmotif:** the name of the argument, renumbering («не принципиально, какому именно»), «вопрос определений», «по чисто визуальным причинам», «оставлять столько индексов, сколько диктует структура задачи».
- **Informal words go in quotes:** «очевидным», «обычными», «клетки», «строка за строкой», «немым», «свободными», «одноиндексную», «странного».
- **Typography:**
  - bold only for the defined term (**Индексной функцией**, **многоиндексными функциями**) and the two header labels;
  - italics for a stressed word (*новая функция*, *символе*, *концептуально просто*);
  - «Предупреждение:» and «Забегая вперёд» inline in the main text;
  - no side-remark boxes, no footnotes;
  - display formulas for every construction;
  - tables in LaTeX.
- **Sentences:** median 16 words, rarely under 6. Complete, with subordinate clauses; no fragments. «Да.» after a question is his only short sentence.
- **Structure:**
  - numbered sections (1–6) with subsections only under «Примеры»;
  - each section opens by linking to the previous one («До сих пор…», «Как уже было сказано…»);
  - no end-of-section summaries; the lecture ends with «Конец лекции 1».
- **Header:** «Необходимые знания:» is a comma list. «О чем лекция:» is two short sentences listing topics, with no parentheses.

## 4. Things our earlier rules banned that are his *(a)*

Review 1 was turned into bans that his own text breaks. Each has been narrowed (see `author-rulings.md`, `register-patterns.tsv`):

| Banned by us | In his text |
|---|---|
| «сегодня» | «Сегодня — нулевая, вводная лекция курса» |
| «позже» | ×5 |
| «как мы увидим» | «Как мы увидим, этот случай гораздо проще» |
| «обратите внимание», «заметьте» | ×3 |
| «полный аналог» | «Это полный аналог h(x)=f(x)g(x)», «полная аналогия с интегралами» |
| «никакой магии» | once, with the reason right after the colon |
| «одну и ту же роль» | about two equivalent functions, not about sum and integral |

What review 1 actually objected to was **the spoken version**: «нас сейчас интересует», «пока примем на веру», «уже не запишешь», «магия» as a mood with no content, «вот и всё». *(c)*

## 5. How he reviews, and what draws criticism *(c)*

- **He reads the typeset PDF** and refers to page and figure numbers. Review 2 was made on the typeset preview, which has no callouts; the review PDF with «Идея» and the nine «Вопрос» of round 1 got no response. He expects us to do the comparison («я сейчас не буду вчитываться… сам возьми сравни»). *(c, 04:42, 06:37)*
- **He notices small things:** a swapped item in «Необходимые знания» (01:28), bold he didn't ask for (02:42, 04:18), the label «Замечание редактора» (09:23, 10:06).
- **Signs of irritation** — «Боже», «полный бред», «не понял, зачем оно» — come with: layout gaps, oversized figures, our labels, repeating a deviation he already pointed out.
- **What he praised** in review 2:
  - every figure: fig. 1 and fig. 3 «супер», the matrix figures «все хорошие, супер», fig. 2 «окей»; fig. 6 only too big;
  - the look of side remarks («замечание очень нравится»);
  - tables without inner vertical rules («без промежуточных палочек»);
  - «перенумерация пар» as a subsection;
  - the physics remark.

  In review 1 he praised figs. 4 and 5, the composition paragraph, the Einstein warning, the interchange proof and «Неформально:» on δ.
- **Layout requirements** (09:23–11:12):
  - no figure takes half a page (fig. 6 was too big);
  - captions are not long (fig. 3);
  - a table must not start half a page down after a gap;
  - a long table goes horizontal, in blocks side by side as in his text, or with text wrapped around it.

  «Референс всё-таки оформлен более красиво.»

## 6. The books he named *(c, `style.txt`)*

He gives each book a role:

| Role | Books | Not for |
|---|---|---|
| **Wording**: how sentences and phrases are built («речь идеальная») | Landau–Lifshitz, vols. 1 and 5 (vol. 2 is acceptable) | structure, content, citing it |
| **Narrative**: when to ask a question, how to motivate, how to give examples and definitions, what goes into small print, what to say and what to leave out | Slobodyanyuk «Физика для любознательных» (`raw/examples/Слободянюк т1–т4.pdf`), Feynman's lectures, the Berkeley course | facts, and their level of chattiness |
| **Layout**: what goes into a footnote, a figure or a supplement | Misner–Thorne–Wheeler «Гравитация» | its long captions |
| **In between**, to draw on occasionally | Berkeley course, Zorich «Математический анализ» | copying |

**Feynman and Slobodyanyuk are the ceiling of conversational style, and ours stays below it** («точно не больше, на самом деле даже меньше»). **No jokes.** None of these books is cited or quoted in our text, and nothing is copied from them into the repository.

### 6.1 Slobodyanyuk, from the text *(a for the book; the application to us is d)*

Measured over the four volumes and read in samples (vol. 1 §§1, 10, 28; vol. 3 §§1.2, 2):
- **A problem comes before the concept.** Coordinates start from «Где находится Белгосуниверситет?»: answers that suit one asker and not another, then the requirements, the flaws of describing a place in words, then numbers, then the term. The field starts from long-range against short-range action.
- **A concept is reached by reasoning, then stated formally.** Force ∝ charge, so force/charge doesn't depend on the charge, so it characterises the field, «которая называется напряжённостью». Then a separate definition sentence follows.
- **A law is followed by comments on its wording:** a dashed list explaining why each condition in the statement matters.
- **Questions sit only at turning points and are answered at once.** A section title may itself be a question («Существует ли четвёртое измерение?»).
- **Recurring themes are flagged:** «Как мы уже подчёркивали», «В очередной раз мы сталкиваемся…», «Мы неоднократно подчёркивали, что… выбирается произвольно». **Arbitrariness of choices** (origin, sign, zero of energy, notation) is his constant theme too.
- **New things are compared with known ones** (Coulomb with Newton), and then the single difference is named.
- **It is honest about rigour:** «не будем стремиться к абсолютной математической строгости», «приведём окончательную формулу без доказательства».
- **About 20% of the text is small print** (in vol. 1, about 2% more is footnotes). It carries:
  - longer justifications;
  - generalisations beyond the current scope;
  - notation conventions;
  - paradoxes;
  - warnings about common mistakes;
  - long worked problems;
  - history and biographies.

  It has no label; it is simply set smaller across the full width. Footnotes carry a small precision.
- **Layout:**
  - small figures with the text wrapped around them;
  - captions are only «Рис. 55»;
  - the defined term in bold;
  - numbered bold run-in headings («1. Умножение вектора на число.»);
  - equation numbers within a section;
  - about one figure per 2 000 characters.
- **Chattiness (the ceiling, not the target):** «мы» 5–8 per 10k characters (his text: 3), «вы» under 1 (his: 0), occasional «Вообразили?», «Согласитесь», exclamations, joke footnotes. **We take the narrative moves and the layout, not the chattiness.**

**His text already uses Slobodyanyuk's moves:** questions at turning points, flags for recurring themes, arbitrariness as a leitmotif, comparison with the familiar (functions on ℝ play the role of Newton's law), informal words in quotes. **It is quieter:** no «вы», no exclamations, no small print. So the target sits between Slobodyanyuk and Landau–Lifshitz. *(d)*

### 6.2 The others, from general knowledge *(d: not checked against their text)*
- **Landau–Lifshitz:**
  - terse, exact sentences in the authorial «мы»: «Рассмотрим», «Легко видеть, что», «Отсюда следует», «Существенно, что», «Таким образом»;
  - almost no rhetorical questions;
  - footnotes for side remarks and history;
  - problems at the end of a section.
- **Feynman:**
  - starts from phenomena and "why";
  - lively;
  - says outright what matters and what is detail;
  - many analogies;
  - humour (excluded for us).
- **MTW «Гравитация»:**
  - two levels of reading (the main track and optional deeper material);
  - self-contained boxed inserts;
  - margin notes that sum up each paragraph (close to our «Идея»);
  - exercises inside the text;
  - the geometric picture next to the component computation;
  - long captions (excluded for us).

  For us: a clear split between the main line, footnotes, figures and supplements.
- **Berkeley course, Zorich:**
  - numbered definitions, statements and remarks;
  - motivating openings;
  - problems at the end of chapters;
  - Zorich also uses small print for supplementary material.

## 7. Conflicts between review 1 and his text, and his answers

In these places review 1 and his text disagreed. Each was put to him through the user on 2026-10-19 as «оставить мелким замечанием или убрать». He answered on 2026-10-20 (`raw/reviews/lecture-01/reply.txt`, times below). The answers are rulings 10 and 34–40 in `author-rulings.md`.

| Item | Review 1 | His text / review 2 | Answer (2026-10-20) |
|---|---|---|---|
| ℝ² is only a set of ordered pairs, without distances or angles | «ни в коем случае нельзя выкидывать» (09:42) | absent | **small remark** («сохраняем, выносим замечанием», 00:01) |
| 2−x=3 as a map ℝ→{да, нет} | «супер классно» (06:18) | absent; review 2 likes the remark, maybe its look (04:42) | removed («супер классно. Но убираем», 00:01–00:32) |
| dt′/t′ | «как замечание и выделить, супер» (25:10) | absent | **small remark, our wording** («в таком виде в качестве замечания оставляем», 00:32; 01:24) |
| composition | «гениально» (08:19) | absent | removed (00:32–01:03) |
| «пятнашки» | «сомнительно… ладно, оставляем» (45:33–45:56) | absent | removed; he may edit the permutations himself (01:03) |
| T(x,y) / T(r⃗) | «либо я его просто уберу» (17:22) | absent | removed (01:03–01:24) |
| fig. 6 | — | «рисовать эти циклические перестановки нет смысла» (09:23): drop the permutation rows and shrink, or drop the figure? | kept, compact, «не… полстраницы» (01:24–01:57) |

What the answers show: praise in a review is not a decision to keep. Two of the seven survive, both as small grey remarks, and both are remarks that prevent a misreading (ℝ² has no hidden structure; a dummy variable can't share a name with a limit). The rest he enjoyed and still cut («всё, что лишнее, убираем»).

**Not asked; decided by his text and review 2, and confirmed in his answer (01:57):**
- operators/functionals: drop (03:03);
- the closing summary: drop (cut in his .tex);
- Taylor's lower limit: drop (not praised, not used later).

**Not asked yet:** in review 1 he praised our «Предупреждение» on the Einstein rule (28:32–29:01), which also explained why all indices are written as subscripts for now. His own warning lacks that sentence. *(Raise it with the user.)*

## 8. What the blind test showed (2026-10-19)

**Setup.** A separate agent was given only the recording, the handnotes, his §0–§4 and a version of this model built from §0–§4. Its task was to write the rest of lecture 1. Its text was then compared with his §5–§6. Workspace: `.claude/skills/lecture-notes-workspace/blind-test-01/`.

**Run 1** got the overall length right (10.9k characters of prose against his 11.3k). It also got the big move right: Levi-Civita goes after δ, at the end. It dropped what he drops among the obvious items:
- «пятнашки»;
- Taylor;
- textbooks;
- personal stories;
- «бублик/пончик»;
- the homework framing.

It differed from him systematically as follows. Each item is now a rule *(a, b: evidence from his §5–§6)*.

1. **Structure.** He writes the general theory as sections and then gathers the concrete objects in a final section «Примеры»: 6.1 progressions, 6.2 matrices, 6.3 δ, 6.4 ε, 6.5 the εε sum. Each is presented as an example of an index function («Пожалуй, самым известным примером многоиндексной функции является матрица»). One sentence of «О чём лекция» corresponds to one section: «Суммы и перестановочность сумм» becomes «5. Суммы. Перестановочность сумм». Run 1 made five flat sections instead.
2. **One analogy per point.** He keeps ∫f dx = α, ∫f(x,y)dx = g(y) and «не зависит от переменной интегрирования». He drops the second-order material: dt′/t′, p(x)=h(x,x,x), definite against indefinite integral, «промежуточные значения не пишутся». Review 1 (21:53) had already disliked that last paragraph in our draft. Run 1 kept all of them.
3. **Repeated worked cases are compressed.**
   - Lecture (01:09:16): j = 1, then j = 2, … → his text: «При фиксированном j сумма … содержит лишь одно ненулевое слагаемое».
   - He drops a side case with no summation index in a (01:11:36), «все четыре формы записи» (01:02:08), ε for general n and «в физике n = 3 или 4» (01:06:46), and A = Aᵀ (01:02:08).

   Run 1 kept them.
4. **Clean, general examples replace the improvised ones.**
   - c_iii with p(x)=h(x,x,x) (00:53:21) → «Конструкции, содержащие суммирования, можно обобщить вполне произвольным образом»: Σ a_ij b_i = c_j, Σ a_ii b_i = α.
   - Σ a_i b_jk = c_k (handnotes p. 6) → the chain Σ a_i b_j c_k = c_k Σ a_i b_j = c_k (Σa)(Σb).
   - In §4, 3×3 → 4×4.

   For us this is a proposal to list, not a silent change *(d)*.
5. **Structuring questions stay questions:** «Что за объект должен стоять в правой части равенства?», «Первый вопрос — что за объект получится? Получится, как несложно понять, …», «Следующий вопрос — когда A заведомо равно нулю?». Run 1 flattened them into «следует понять, какой объект получится» (1 question against his 3).
6. **Motivation opens and forward references close.** The εε subsection opens with «которое часто встречается в физических задачах: двойное векторное произведение, ротор…»; in the lecture this came at the end (01:17:18). The tensor note closes 6.4; the determinant is the last sentence of 6.5.
   - **Which forward references stay** *(the reason is d)*: the Einstein rule stays, because the text has just written Σ a_ii b_i; the Levi-Civita tensor stays, because the name collides.
   - **Which go:** «верхние и нижние индексы» (00:55:26), a mere announcement.
   - **"Later" in the "used later?" test means later in this lecture** («в этой лекции больше нигде не используется», review 2, 03:03).
7. **Bold is rare.** His §5–§6 has none: «Символом Кронекера по определению называется отображение», with «немым» and «свободными» in quotes. Bold is for the lecture's central definitions only (here «индексная функция», «многоиндексная функция»). Run 1 bolded three terms.
8. **His connectives call back to what has been said.**
   - «Как было выяснено, самым логичным способом мыслить себе многоиндексную функцию является её табличное представление. Реализуем его:»
   - «Вновь прослеживается полная аналогия…»
   - «Вновь обратим внимание на ограниченность матричной записи»
   - «Для полноты картины скажем…»

   Run 1 used generic «Заметим», «Таким образом», «Рассмотрим» instead (0 of his callbacks).
9. **He says honestly what is not yet explained, in his own sentence.** Lecture (01:03:18): «сейчас мы просто на слово поверим». His text: «…это пока не даёт ответа на вопрос, как и где оно возникает — это, само собой, может быть выяснено только при изучении самой линейной алгебры». The replacement suggested in review 1, «следует принять как данность», shows a direction; it is not wording to paste. Run 1 pasted it.
10. **Short sentences that lead into a formula are his:** «Тогда:», «Реализуем его:», «Сумма по k:», «Рассмотрим выражение». The median sentence in §5–§6 is 15.5 words; run 1's was 19.
11. **Notation:** ℓ (`\ell`) after k; «+1» against «−1» in a case definition; «если среди i, j, k есть повторяющиеся» rather than «иначе».

**Content-level differences, which no model predicts.** These are his own choices and additions. Where the recording only hints at one, the right move for us is a «Вопрос», not a guess:
- progressions;
- Σ a_ik b_kk and Σ a_iki as sums the matrix algorithm can't do;
- why matrices are popular;
- the associativity proof;
- «немой» as a term;
- the generalisation to more than two sums;
- parity defined by cyclic shifts rather than by swaps of adjacent numbers;
- the 3D table remark;
- εε = δδ − δδ as a stated fact (the recording only alludes to «мем про дельта»);
- the cyclic symmetry of A;
- «никакой магии тут нет: …» kept once.

Run 1 correctly declined to state δδ − δδ on its own.

**Run 2** used the same setup, with rules 1–9 and 11 added to the model. It shows whether the rules can be followed. It is **not** blind: the rules were learned from this held-out text, and one rule leaked his term «немым».

**Fixed in run 2:**
- the structure: «5. Суммы. Перестановочность сумм», then «6. Примеры» with matrices, δ and ε;
- questions (4 against his 3);
- motivation first;
- forward references at the end;
- no bold;
- his callbacks («Как уже было сказано», «Как было выяснено», «Вновь подчеркнём», «Следует понимать»);
- an honest sentence of its own about what is not yet explained;
- ℓ and «+1»;
- dt′/t′, A = Aᵀ and «n = 3 или 4» dropped.

Its list of uncertain decisions holds exactly the points where his text decides otherwise: the tensor note for δ, the upper/lower-index note, the definite/indefinite clause. In a real draft each would have been a «Вопрос». That is the mechanism working.

**Still differing after run 2.** These are now rules too *(a, b)*, untested:

12. **After the general rule, one example.** In his δ subsection: one proof at fixed j, the general rule f_{i…} → f_{j…}, «Неформально говоря», one example (Σ δ_ij a_ik = a_jk), a sentence comparing with matrices. The spoken extra cases are dropped: the δ·column multiplication, the case with no summation index in a, «все четыре записи». Both runs kept them.
13. **Shorter sentences.** Median 15.5 words in his §5–§6, against 19 in both runs. He leads into formulas with short sentences («Тогда:», «Реализуем его:», «Сумма по k:») and often splits a long explanation into two sentences.
14. **The same kind of warning is given once,** at the place where it matters most. The tensor-vs-symbol note appears for ε only, not for δ, although the lecture says it for both (01:06:46, 00:41:40).
15. **A computation with its own motivation gets its own subsection** (6.5, «Сумма двух символов Леви-Чивиты по одному общему индексу»), rather than closing the subsection on its object.
16. **«Таким образом»** is rare in his text (once in §5–§6). Both runs used it 2–3 times as a generic closing.

**Content-level, as before:** both runs kept the lecture's own examples (c_iii with p(x)=h(x,x,x); Σ a_i b_jk = c_k) where he wrote cleaner ones. That is his authorial choice; for us it is at most a proposal (rule 4).

**Why stop here.** A third run on the same held-out text would measure how well the rules were memorised, not whether they describe him. Rules 12–16 are checked on lecture 2, where the lecturer is the judge. Workspace: `.claude/skills/lecture-notes-workspace/blind-test-01/` holds the inputs, both runs with their notes and `compare.txt`, and `compare.py`.
