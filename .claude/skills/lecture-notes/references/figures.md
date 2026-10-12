# Figures

Illustrations are the main way the book can improve on the spoken lectures, and the author's first review praised them most (figs. 4 and 5 of lecture 1). Philosophy 6 has two halves, and both matter: *a picture reveals what the formula hides* — and *it never adds what the text forbids*. This file covers when to draw, what to draw, how to frame it, how to draw it in house style, and how to check it.

## When a figure earns its place

Draw where at least one of these holds:
- **The handnotes have a sketch.** The lecturer drew it on the board, so it was part of the explanation. Redraw it properly: clean, correct and labelled. Don't trace the hand sketch.
- **The transcript points at a picture** that isn't in the notes: «смотрите», «нарисуем», «вот так вот идёт», «представьте плоскость…». The words without the picture lose the point.
- **A mechanism is invisible in the formula** and a picture makes it obvious, even though the lecturer didn't draw it. The user asked for such illustrations, so you may add them — but they are your additions: list them in the report, and if the picture could be read as a claim the lecturer didn't make, ask in a «Вопрос» callout.

Don't draw: decoration, a formula restated as a picture, a diagram of the lecture's structure, or anything you can't make correct.

## Frame every picture as a visualization

The course insists that a set carries no structure beyond what was defined: $I^2$ is a set of ordered pairs, not a grid; $\{1,2,3\}$ is not a circle. A picture adds structure — positions, neighbours, a diagonal, a direction — and a reader may take it for part of the object. The lecturer's review of lecture 1 caught exactly this (fig. 3 «расположенных так же, как клетки таблицы»: «это уже ваша вольность»). So:

- **Introduce the picture in the text before it appears, as an option**: «Элементы $I^2$ удобно изобразить точками на сетке…», «Если расположить числа 1, 2, 3 на окружности, то…». Never «расположены», «лежат», «образуют сетку» about the object itself.
- **Facts hold by definition; the picture only helps to see them.** «$(1,2)$ и $(2,1)$ — разные элементы $I^2$ по определению упорядоченной пары; на рисунке это видно как …», not the other way round.
- **Statements that use the picture are conditional**: «если записать функцию двумерной таблицей, то она симметрична относительно главной диагонали».
- **The caption carries the secondary details** (what the colours mean, which numbers were used); the text doesn't repeat them, and the caption doesn't restate the text.

## What tends to work in this course

| Idea | Picture |
|---|---|
| Map / function between sets | Two blobs, points, arrows (see `assets/figure-template.svg`) |
| Index function $a\colon I\to\mathbb{R}$ | Its "graph": $n$ isolated points, next to the table |
| Two-index function, symmetry | Its values written as a two-dimensional table (an option, see above), the main diagonal marked; mirror arrows for $a_{ij}=a_{ji}$ |
| Vectors, basis, decomposition | Arrows from the origin, the parallelogram of $\alpha_1\vec e_1+\alpha_2\vec e_2$ |
| Change of basis | The same vector over two grids (old basis grey, new basis red) with both sets of components |
| Linear form on the plane | Parallel, equally spaced level lines $f=-1,0,1,2$, and the vector being "measured" crossing them |
| Linear function as a graph | A plane through the origin over the $(x,y)$ plane (3D, see below) |
| Dual basis | $\vec e_1,\vec e_2$ with the level lines of $e^1, e^2$; each $e^i$ is $1$ on its own $\vec e_i$ and $0$ on the other |
| Levi-Civita symbol | $1, 2, 3$ placed on a circle (introduced as a device for reading off even permutations), read one way and the other |
| Manifold, chart | A surface patch mapped to a square in $\mathbb{R}^2$ |
| Tangent space | A surface (sphere) with the tangent plane at a point and a vector in it |
| Configuration space | Double pendulum → torus with the angles $\varphi_1,\varphi_2$ marked |

## House style

Start from `assets/figure_house.py`: copy it into the lecture's `figures/` folder as `_house.py`, and write each figure as a short script that imports it (`save`/`write`, `arrow`, `vec` for $\vec a$, `form` for $\tilde\omega$, `blob` for sets, `P` for 3D, clipping helpers). It carries the house style of `assets/figure-template.svg` (the same `<defs>` and `<style>`). Lectures 1 and 4 keep their own older copies; don't edit those to change another lecture.
- White background, ink `#1a1a1a`, red `#c0392b` for the main object (the lecturer's red pen), blue `#2563a8` for a second contrasting object. Light tints only. The white background keeps a figure readable in any viewer (VS Code, github.com, the PDF). On the website, `docs/assets/reader.css` makes figures follow the theme: the white blends into the paper, and in dark mode the figure is inverted with hues kept (ink turns light, red stays red). That only works for dark ink on white, hence these colour rules. Don't put a dark-mode rule inside the SVG itself: Safari doesn't apply it reliably for SVGs shown as images (tested).
- Width 640, height as needed. `width`/`height` attributes equal the `viewBox`.
- Math labels in serif italic (`class="m"`), subscripts via `<tspan class="sub" dy="5">`. Labels sit near what they name, never on top of a line.
- One idea per figure. Two panels side by side ("было / стало", "чётные / нечётные") are fine when the comparison *is* the idea.
- Text inside a figure is minimal: labels, not sentences. The explanation goes in the caption and the text.
- Everything stays inside the figure's rectangle: row and column labels sit within the frame, not sticking out at a corner. Tinted backgrounds keep a margin from brackets and lines.
- A correspondence (this entry goes with that one) is drawn with arrows, not described in the caption as «положить A под B».

## Draw with computed coordinates

Don't eyeball geometry. Write a short Python script (standard library only; there is no numpy/matplotlib here) that computes the points and prints the SVG. Keep the script beside the figure (`docs/lecture-NN/figures/<name>.py`) so the figure can be regenerated. This is what makes level lines actually parallel and equally spaced, a vector actually equal $2\vec e_1 + \vec e_2$, and a tangent plane actually tangent.

For 3D, use the frontal dimetric projection common in Russian textbooks (and in the lecturer's sketches): $y$ to the right, $z$ up, $x$ toward the viewer drawn down-left at 45° and shortened by half:

```python
import math
def P(x, y, z, s=60, ox=320, oy=230, k=0.5, a=math.radians(45)):
    """3D point -> SVG coordinates (SVG y grows downward)."""
    return (ox + s * (y - k * x * math.cos(a)), oy - s * (z - k * x * math.sin(a)))
```

Surfaces are drawn as a few mesh lines or an outline, not shading. Hidden parts get the `.dash` class (the back half of a sphere's equator, the part of an axis behind a plane).

## Check every figure

1. Render it as the website shows it, in both themes: `python3 <skill-dir>/scripts/snap_svg.py figure.svg --out <scratch-dir>` writes `figure.light.png` and `figure.dark.png`, rendered by WebKit (Safari's engine, the strictest) with the site's figure styling. Look at both: nothing may vanish in dark mode.
2. Ask: is it mathematically right (recompute one point)? Is every label legible, clear of lines and inside the frame? Is it obvious within two seconds what the figure is about? Would the caption alone explain it? Is it introduced in the text before it appears, and framed as a visualization rather than as the structure of the object?
3. Look at it again in context in the PDF from `render_preview.py`: is it next to the paragraph that discusses it, and is the size right?

Fix and re-render until all of the above holds. A wrong or confusing figure is worse than none.
