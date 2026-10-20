"""Рис. 5. Произведение матрицы на столбец как сумма по общему индексу j:
c_1 = A_11 b_1 + A_12 b_2 + A_13 b_3 = 1·3 + 2·4 + 3·5 = 26.
Слева строка i = 1 и столбец b выделены; справа те же значения A_1j и b_j выписаны
таблицей-списком по j (строка или столбец — лишь способ записи функции одного индекса),
рядом их произведения, сумма которых и есть c_1."""

from _house import f, save

A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
b = [3, 4, 5]
c = [sum(A[i][j] * b[j] for j in range(3)) for i in range(3)]
assert c == [26, 62, 98]

W, H = 640, 250
MY = [84, 126, 168]                 # базовые линии строк матрицы (центр строки = MY - 7)
MX = [64, 108, 152]                 # столбцы матрицы
BX, CX = 236, 334                   # столбец b, столбец c
PAD = 6                             # зазор между подсветкой и скобками
TOP, BOT = MY[0] - 34, MY[2] + 22   # верх и низ скобок


def parens(x_left, x_right, y_top=TOP, y_bot=BOT, bulge=9):
    """Круглые скобки: x_left/x_right — крайние точки дуг (по середине высоты)."""
    xl, xr = x_left + bulge, x_right - bulge
    return (f'  <path class="ink" d="M{f(xl)},{y_top} Q{f(x_left - bulge)},{f((y_top + y_bot) / 2)} {f(xl)},{y_bot}"/>\n'
            f'  <path class="ink" d="M{f(xr)},{y_top} Q{f(x_right + bulge)},{f((y_top + y_bot) / 2)} {f(xr)},{y_bot}"/>')


body = []
# подсветка: строка 1 матрицы, столбец b, элемент c_1 — с зазором до скобок
body.append(f'  <rect class="tint-red" x="{MX[0] - 14}" y="{MY[0] - 24}" width="{MX[2] - MX[0] + 28}" height="32" rx="7"/>')
body.append(f'  <rect class="tint-red" x="{BX - 12}" y="{MY[0] - 24}" width="24" height="{MY[2] - MY[0] + 32}" rx="7"/>')
body.append(f'  <rect class="tint-red" x="{CX - 15}" y="{MY[0] - 24}" width="30" height="32" rx="7"/>')

for i in range(3):
    for j in range(3):
        body.append(f'  <text class="t mid" x="{MX[j]}" y="{MY[i]}">{A[i][j]}</text>')
    body.append(f'  <text class="t mid" x="{BX}" y="{MY[i]}">{b[i]}</text>')
    cls = "t mid lbl-red" if i == 0 else "t mid"
    body.append(f'  <text class="{cls}" x="{CX}" y="{MY[i]}">{c[i]}</text>')
# скобки: внутренний край дуги отстоит от подсветки на PAD
body.append(parens(MX[0] - 14 - PAD - 9, MX[2] + 14 + PAD + 9))
body.append(parens(BX - 12 - PAD - 9, BX + 12 + PAD + 9))
body.append(parens(CX - 15 - PAD - 9, CX + 15 + PAD + 9))
body.append(f'  <text class="t mid" x="{(BX + CX) / 2 + 4}" y="{MY[1]}">=</text>')

# справа: таблица-список по j — значения A_1j, b_j и их произведения (обозначения его § 6.2)
TX = [432, 486, 540, 600]           # столбцы: j, A_1j, b_j, A_1j b_j
TY0 = 58                            # строка заголовков
TY = [96, 132, 168]                 # строки j = 1, 2, 3
SY = 214                            # строка суммы
body.append(f'  <rect class="tint-red" x="{TX[1] - 16}" y="{TY[0] - 25}" width="32" height="{TY[2] - TY[0] + 34}" rx="7"/>')
body.append(f'  <rect class="tint-red" x="{TX[2] - 16}" y="{TY[0] - 25}" width="32" height="{TY[2] - TY[0] + 34}" rx="7"/>')
body.append(f'  <text class="m mid" x="{TX[0]}" y="{TY0}">j</text>')
body.append(f'  <text class="m mid" x="{TX[1]}" y="{TY0}">A<tspan class="t sub" dy="5">1</tspan><tspan class="sub">j</tspan></text>')
body.append(f'  <text class="m mid" x="{TX[2]}" y="{TY0}">b<tspan class="sub" dy="5">j</tspan></text>')
body.append(f'  <text class="m mid" x="{TX[3]}" y="{TY0}">A<tspan class="t sub" dy="5">1</tspan><tspan class="sub">j</tspan>'
            f'<tspan dy="-5">b</tspan><tspan class="sub" dy="5">j</tspan></text>')
body.append(f'  <path class="thin" d="M{TX[0] - 20},{TY0 + 14} L{TX[3] + 32},{TY0 + 14}"/>')
for j in range(3):
    body.append(f'  <text class="t mid" x="{TX[0]}" y="{TY[j]}" fill-opacity="0.7">{j + 1}</text>')
    body.append(f'  <text class="t mid" x="{TX[1]}" y="{TY[j]}">{A[0][j]}</text>')
    body.append(f'  <text class="t mid" x="{TX[2]}" y="{TY[j]}">{b[j]}</text>')
    body.append(f'  <text class="t mid" x="{TX[3]}" y="{TY[j]}">{A[0][j] * b[j]}</text>')
body.append(f'  <path class="thin" d="M{TX[3] - 26},{TY[2] + 14} L{TX[3] + 26},{TY[2] + 14}"/>')
body.append(f'  <text class="t end" x="{TX[3] - 30}" y="{SY}">Σ =</text>')
body.append(f'  <text class="t mid lbl-red" x="{TX[3]}" y="{SY}" font-weight="bold">{c[0]}</text>')

save("matrix-column", W, H, "\n".join(body) + "\n")
