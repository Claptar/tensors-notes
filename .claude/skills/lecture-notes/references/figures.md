# Figures

Illustrations are the main way these notes can improve on the original lecture 1 (philosophy 5: *a picture must show something the formula hides*). This file covers when to draw, what to draw, how to draw it in house style, and how to check it.

## When a figure earns its place

Draw where at least one of these holds:
- **The handnotes have a sketch.** The lecturer drew it on the board, so it was part of the explanation. Redraw it properly: clean, correct and labelled. Don't trace the hand sketch.
- **The transcript points at a picture** that isn't in the notes: «смотрите», «нарисуем», «вот так вот идёт», «представьте плоскость…». The words without the picture lose the point.
- **A mechanism is invisible in the formula** and a picture makes it obvious, even though the lecturer didn't draw it. Mark these mentally as your addition; they still need no label in the text, but mention them in the report.

Don't draw: decoration, a formula restated as a picture, a diagram of the lecture's structure, or anything you can't make correct.

## What tends to work in this course

| Idea | Picture |
|---|---|
| Map / function between sets | Two blobs, points, arrows (see `assets/figure-template.svg`) |
| Index function $a\colon I\to\mathbb{R}$ | Its "graph": $n$ isolated points, next to the table |
| Two-index function, symmetry | A square table with the diagonal marked; mirror arrows for $a_{ij}=a_{ji}$ |
| Vectors, basis, decomposition | Arrows from the origin, the parallelogram of $\alpha_1\vec e_1+\alpha_2\vec e_2$ |
| Change of basis | The same vector over two grids (old basis grey, new basis red) with both sets of components |
| Linear form on the plane | Parallel, equally spaced level lines $f=-1,0,1,2$, and the vector being "measured" crossing them |
| Linear function as a graph | A plane through the origin over the $(x,y)$ plane (3D, see below) |
| Dual basis | $\vec e_1,\vec e_2$ with the level lines of $e^1, e^2$; each $e^i$ is $1$ on its own $\vec e_i$ and $0$ on the other |
| Levi-Civita symbol | The cyclic triangle $1\to2\to3\to1$ (even) against the reverse direction (odd) |
| Manifold, chart | A surface patch mapped to a square in $\mathbb{R}^2$ |
| Tangent space | A surface (sphere) with the tangent plane at a point and a vector in it |
| Configuration space | Double pendulum → torus with the angles $\varphi_1,\varphi_2$ marked |

## House style

Start from `assets/figure-template.svg`: copy it, keep `<defs>` and `<style>`, replace the drawing.
- Dark ink on no background: ink `#1a1a1a`, red `#c0392b` for the main object (the lecturer's red pen), blue `#2563a8` for a second contrasting object. Light tints only. Use a white fill only to hide what lies behind a shape (e.g. a sphere in front of a plane).
- **Then make it theme-aware:** `python3 <skill-dir>/scripts/theme_svg.py docs/lecture-NN/figures/*.svg`. It removes the white background and puts a dark-mode rule inside the SVG (hue-preserving inversion: ink turns light, red stays red), so the figure follows light/dark on the website, on github.com and in VS Code. Run it again whenever a figure script regenerates an SVG, because the scripts write plain SVGs. `render_preview.py` reports any figure that isn't themed. All this only works for dark ink on a light ground, hence the colour rules above.
- Width 640, height as needed. `width`/`height` attributes equal the `viewBox`.
- Math labels in serif italic (`class="m"`), subscripts via `<tspan class="sub" dy="5">`. Labels sit near what they name, never on top of a line.
- One idea per figure. Two panels side by side ("было / стало", "чётные / нечётные") are fine when the comparison *is* the idea.
- Text inside a figure is minimal: labels, not sentences. The explanation goes in the caption and the text.

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

1. Render it in both themes: `python3 <skill-dir>/scripts/snap_svg.py figure.svg --out <scratch-dir>` writes `figure.light.png` (what the PDF gets) and `figure.dark.png` (what dark-theme readers see), each on the website's page colour. Look at both. Don't use QuickLook for this: it follows the Mac's own appearance, so it shows only one theme.
2. Ask: is it mathematically right (recompute one point)? Is every label legible and clear of lines? Is it obvious within two seconds what the figure is about? Would the caption alone explain it?
3. Look at it again in context in the PDF from `render_preview.py`: is it next to the paragraph that discusses it, and is the size right?

Fix and re-render until all of the above holds. A wrong or confusing figure is worse than none.
