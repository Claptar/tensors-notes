"""Рис. 1. Отображение f: X -> Y: из каждой точки X ровно одна стрелка; две стрелки могут
прийти в одну точку Y; некоторые точки Y остаются без стрелок."""

from _house import blob, f, save

W, H = 640, 270
X_C, Y_C = (170, 130), (470, 130)

xs = [(135, 80), (205, 112), (130, 160), (195, 190)]           # точки X
ys = [(440, 78), (500, 128), (440, 182), (515, 196)]           # точки Y; последняя без стрелки
arrows = [(0, 0, -28), (1, 1, -28), (2, 1, 30), (3, 2, -22)]   # x_k -> y_m, изгиб (в y_1 приходят две)

body = []
body.append(f'  <path class="ink tint-grey" d="{blob(*X_C, 105, 95, 0.4)}"/>')
body.append(f'  <path class="ink tint-grey" d="{blob(*Y_C, 100, 95, 2.1)}"/>')

for k, m, bend in arrows:
    (x0, y0), (x1, y1) = xs[k], ys[m]
    # quadratic curve (bend < 0: upward), stopping short of the target dot
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + bend
    dx, dy = x1 - mx, y1 - my
    L = (dx * dx + dy * dy) ** 0.5
    ex, ey = x1 - 7 * dx / L, y1 - 7 * dy / L
    body.append(f'  <path class="ink red" d="M{f(x0 + 5)},{f(y0 - 2)} Q{f(mx)},{f(my)} {f(ex)},{f(ey)}" '
                f'marker-end="url(#arrow-red)"/>')

for x, y in xs:
    body.append(f'  <circle class="dot" cx="{x}" cy="{y}" r="4"/>')
for i, (x, y) in enumerate(ys):
    cls = "dot-red" if i < 3 else "dot"
    body.append(f'  <circle class="{cls}" cx="{x}" cy="{y}" r="4"/>')

body.append(f'  <text class="m" x="{X_C[0] - 6}" y="258">X</text>')
body.append(f'  <text class="m" x="{Y_C[0] - 6}" y="258">Y</text>')
body.append('  <text class="m" x="318" y="50">f</text>')

save("map", W, H, "\n".join(body) + "\n")
