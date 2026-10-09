"""Рис. 3. Множество I^2 при n = 4 в «табличной» ориентации (i — номер строки, j — номер
столбца): 16 упорядоченных пар; (1, 2) и (2, 1) — разные точки, симметричные относительно
диагонали i = j."""

from _house import f, save

W, H = 640, 330
N, STEP = 4, 62
X0, Y0 = 170, 30           # точка (i, j) стоит в (X0 + STEP*j, Y0 + STEP*i)


def P(i, j):
    return X0 + STEP * j, Y0 + STEP * i


body = []

# диагональ i = j (за точками)
(xa, ya), (xb, yb) = P(0.55, 0.55), P(N + 0.45, N + 0.45)
body.append(f'  <path class="thin dash" d="M{f(xa)},{f(ya)} L{f(xb)},{f(yb)}" stroke-opacity="0.6"/>')
body.append(f'  <text class="m" x="{f(xb + 6)}" y="{f(yb + 6)}">i <tspan class="t">=</tspan> j</text>')

# заголовки: номера столбцов j сверху, номера строк i слева, стрелки направлений
for k in range(1, N + 1):
    x, _ = P(0, k)
    body.append(f'  <text class="t small mid" x="{f(x)}" y="{f(Y0 + STEP * 0.62)}">{k}</text>')
    _, y = P(k, 0)
    body.append(f'  <text class="t small end" x="{f(X0 + STEP * 0.5)}" y="{f(y + 5)}">{k}</text>')
xl, _ = P(0, 1)
xr, _ = P(0, N)
body.append(f'  <path class="thin" d="M{f(xl - 8)},{f(Y0 + 4)} L{f(xr + 14)},{f(Y0 + 4)}" marker-end="url(#arrow)"/>')
body.append(f'  <text class="m" x="{f(xr + 22)}" y="{f(Y0 + 10)}">j</text>')
_, yt = P(1, 0)
_, yb2 = P(N, 0)
body.append(f'  <path class="thin" d="M{f(X0 + 2)},{f(yt - 8)} L{f(X0 + 2)},{f(yb2 + 14)}" marker-end="url(#arrow)"/>')
body.append(f'  <text class="m mid" x="{f(X0 + 2)}" y="{f(yb2 + 34)}">i</text>')

# отрезок, соединяющий зеркальные точки (перпендикулярен диагонали)
(x12, y12), (x21, y21) = P(1, 2), P(2, 1)
body.append(f'  <path class="thin dash" d="M{f(x12)},{f(y12)} L{f(x21)},{f(y21)}"/>')

# точки
for i in range(1, N + 1):
    for j in range(1, N + 1):
        x, y = P(i, j)
        cls = "dot-red" if (i, j) == (1, 2) else "dot-blue" if (i, j) == (2, 1) else "dot"
        r = 5.5 if cls != "dot" else 4
        body.append(f'  <circle class="{cls}" cx="{f(x)}" cy="{f(y)}" r="{r}"/>')

body.append(f'  <text class="t lbl-red" x="{f(x12 + 9)}" y="{f(y12 - 9)}">(1, 2)</text>')
body.append(f'  <text class="t lbl-blue" x="{f(x21 + 9)}" y="{f(y21 + 22)}">(2, 1)</text>')

save("grid-I2", W, H, "\n".join(body) + "\n")
