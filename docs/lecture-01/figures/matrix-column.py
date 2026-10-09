"""Рис. 5. Произведение матрицы на столбец как сумма по общему индексу j:
c_1 = a_11 b_1 + a_12 b_2 + a_13 b_3 = 1·3 + 2·4 + 3·5 = 26. Справа столбец b «положен»
под строку i = 1, так что элементы с одинаковым j стоят друг под другом."""

from _house import f, save

A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
b = [3, 4, 5]
c = [sum(A[i][j] * b[j] for j in range(3)) for i in range(3)]
assert c == [26, 62, 98]

W, H = 640, 250
MY = [80, 122, 164]                 # базовые линии строк (центр строки = MY - 7)
MX = [64, 108, 152]                 # столбцы матрицы
BX, CX = 228, 326                   # столбец b, столбец c
RX = [440, 492, 544]                # правая часть: позиции j = 1, 2, 3


def parens(x_left, x_right, y_top=52, y_bot=184, bulge=9):
    """Круглые скобки матрицы."""
    return (f'  <path class="ink" d="M{f(x_left + bulge)},{y_top} Q{f(x_left - bulge)},{f((y_top + y_bot) / 2)} '
            f'{f(x_left + bulge)},{y_bot}"/>\n'
            f'  <path class="ink" d="M{f(x_right - bulge)},{y_top} Q{f(x_right + bulge)},{f((y_top + y_bot) / 2)} '
            f'{f(x_right - bulge)},{y_bot}"/>')


body = []
# подсветка: строка 1 матрицы, столбец b, элемент c_1
body.append(f'  <rect class="tint-red" x="{MX[0] - 20}" y="{MY[0] - 26}" width="{MX[2] - MX[0] + 40}" height="34" rx="8"/>')
body.append(f'  <rect class="tint-red" x="{BX - 16}" y="{MY[0] - 26}" width="32" height="{MY[2] - MY[0] + 36}" rx="8"/>')
body.append(f'  <rect class="tint-red" x="{CX - 20}" y="{MY[0] - 26}" width="40" height="34" rx="8"/>')

# матрица, столбец, результат
for i in range(3):
    for j in range(3):
        body.append(f'  <text class="t mid" x="{MX[j]}" y="{MY[i]}">{A[i][j]}</text>')
    body.append(f'  <text class="t mid" x="{BX}" y="{MY[i]}">{b[i]}</text>')
    cls = "t mid lbl-red" if i == 0 else "t mid"
    body.append(f'  <text class="{cls}" x="{CX}" y="{MY[i]}">{c[i]}</text>')
body.append(parens(MX[0] - 26, MX[2] + 26))
body.append(parens(BX - 22, BX + 22))
body.append(parens(CX - 26, CX + 26))
body.append(f'  <text class="t mid" x="{(BX + CX) / 2 + 2}" y="{MY[1]}">=</text>')

# правая часть: строка a_1j, под ней b_j, ниже произведения
body.append(f'  <text class="m end" x="{RX[0] - 22}" y="{MY[0] - 34}">j<tspan class="t">:</tspan></text>')
for j in range(3):
    body.append(f'  <text class="t small mid" x="{RX[j]}" y="{MY[0] - 34}" fill-opacity="0.7">{j + 1}</text>')
    body.append(f'  <text class="t mid" x="{RX[j]}" y="{MY[0]}">{A[0][j]}</text>')
    body.append(f'  <text class="t mid" x="{RX[j]}" y="{MY[1]}">{b[j]}</text>')
    body.append(f'  <text class="t mid" x="{RX[j]}" y="{MY[2] + 6}">{A[0][j] * b[j]}</text>')
    body.append(f'  <path class="thin" d="M{RX[j]},{MY[0] + 8} L{RX[j]},{MY[1] - 22}" stroke-opacity="0.5"/>')
for j in range(2):
    body.append(f'  <text class="t mid" x="{(RX[j] + RX[j + 1]) / 2}" y="{MY[2] + 6}">+</text>')
body.append(f'  <path class="thin" d="M{RX[0] - 22},{MY[1] + 18} L{RX[2] + 22},{MY[1] + 18}"/>')
body.append(f'  <text class="t" x="{RX[2] + 28}" y="{MY[2] + 6}">=</text>')
body.append(f'  <text class="t lbl-red" x="{RX[2] + 50}" y="{MY[2] + 6}" font-weight="bold">{c[0]}</text>')
body.append(f'  <text class="m" x="{RX[2] + 34}" y="{MY[0]}">a<tspan class="t sub" dy="5">1</tspan><tspan class="sub">j</tspan></text>')
body.append(f'  <text class="m" x="{RX[2] + 34}" y="{MY[1]}">b<tspan class="sub" dy="5">j</tspan></text>')

# столбец b «поворачивается» и ложится под строку
# путь проходит ниже скобок столбца c (их низ — y = 184)
body.append(f'  <path class="thin dash" d="M{BX},{MY[2] + 30} C{BX + 20},{MY[2] + 78} {RX[0] - 50},{MY[2] + 78} '
            f'{RX[0] - 30},{MY[1] + 4}" marker-end="url(#arrow)"/>')

save("matrix-column", W, H, "\n".join(body) + "\n")
