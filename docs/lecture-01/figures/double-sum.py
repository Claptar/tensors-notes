"""Рис. 4. Таблица c_ij = a_i b_j (таблица умножения) для a = (1, 2, 3), b = (4, 5, 6).
Сумма по i сворачивает столбцы (красная строка), сумма по j — строки (синий столбец);
в обоих порядках сумма всех клеток одна и та же: 90 = (1 + 2 + 3)(4 + 5 + 6)."""

from _house import f, save

a = [1, 2, 3]
b = [4, 5, 6]
n = len(a)
c = [[a[i] * b[j] for j in range(n)] for i in range(n)]
row_sums = [sum(c[i]) for i in range(n)]                       # сумма по j
col_sums = [sum(c[i][j] for i in range(n)) for j in range(n)]  # сумма по i
total = sum(row_sums)
assert total == sum(col_sums) == sum(a) * sum(b)

W, H = 640, 300
DX = 40                     # общий сдвиг вправо, чтобы центрировать рисунок
CW, CH = 62, 44
HX = 160 + DX               # столбец заголовков a_i
CX = [240 + DX + CW * j for j in range(n)]
SX = 476 + DX               # столбец сумм по j
HY = 66                     # строка заголовков b_j (базовая линия)
CY = [112 + CH * i for i in range(n)]
SY = 280                    # строка сумм по i (базовая линия)

left, right = CX[0] - CW / 2, CX[-1] + CW / 2
top, bottom = CY[0] - CH / 2, CY[-1] + CH / 2

body = []
# таблица и сетка
body.append(f'  <rect class="ink tint-grey" x="{f(left)}" y="{f(top)}" width="{f(right - left)}" height="{f(bottom - top)}"/>')
for j in range(1, n):
    x = left + CW * j
    body.append(f'  <path class="grid" d="M{f(x)},{f(top)} L{f(x)},{f(bottom)}"/>')
for i in range(1, n):
    y = top + CH * i
    body.append(f'  <path class="grid" d="M{f(left)},{f(y)} L{f(right)},{f(y)}"/>')

# значения
for i in range(n):
    for j in range(n):
        body.append(f'  <text class="t mid" x="{f(CX[j])}" y="{f(CY[i] + 7)}">{c[i][j]}</text>')

# заголовки: a_i слева, b_j сверху
for i in range(n):
    body.append(f'  <text class="t mid" x="{f(HX)}" y="{f(CY[i] + 7)}">{a[i]}</text>')
for j in range(n):
    body.append(f'  <text class="t mid" x="{f(CX[j])}" y="{f(HY)}">{b[j]}</text>')
body.append(f'  <text class="m" x="{f(HX - 62)}" y="{f(CY[1] + 7)}">a<tspan class="sub" dy="5">i</tspan></text>')
body.append(f'  <text class="m mid" x="{f(CX[1])}" y="{f(HY - 34)}">b<tspan class="sub" dy="5">j</tspan></text>')

# суммы по j (строки) — синий столбец справа
for i in range(n):
    body.append(f'  <path class="ink blue" d="M{f(right + 8)},{f(CY[i])} L{f(SX - 26)},{f(CY[i])}" marker-end="url(#arrow-blue)"/>')
    body.append(f'  <text class="t mid lbl-blue" x="{f(SX)}" y="{f(CY[i] + 7)}">{row_sums[i]}</text>')
body.append(f'  <text class="m mid lbl-blue" x="{f(SX)}" y="{f(HY)}"><tspan class="t">Σ</tspan><tspan class="sub" dy="6">j</tspan></text>')

# суммы по i (столбцы) — красная строка снизу
for j in range(n):
    body.append(f'  <path class="ink red" d="M{f(CX[j])},{f(bottom + 8)} L{f(CX[j])},{f(SY - 24)}" marker-end="url(#arrow-red)"/>')
    body.append(f'  <text class="t mid lbl-red" x="{f(CX[j])}" y="{f(SY)}">{col_sums[j]}</text>')
body.append(f'  <text class="m mid lbl-red" x="{f(HX)}" y="{f(SY)}"><tspan class="t">Σ</tspan><tspan class="sub" dy="6">i</tspan></text>')

# общий итог: из обоих направлений
body.append(f'  <path class="ink blue" d="M{f(SX)},{f(CY[-1] + 16)} L{f(SX)},{f(SY - 24)}" marker-end="url(#arrow-blue)"/>')
body.append(f'  <path class="ink red" d="M{f(right + 8)},{f(SY - 7)} L{f(SX - 26)},{f(SY - 7)}" marker-end="url(#arrow-red)"/>')
body.append(f'  <text class="t mid" x="{f(SX)}" y="{f(SY)}" font-weight="bold">{total}</text>')

save("double-sum", W, H, "\n".join(body) + "\n")
