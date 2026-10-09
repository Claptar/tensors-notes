"""Рис. 2. Слева график f: R -> R, f(x) = x^2 (кривая); справа график индексной функции
a: I -> R, a_i = i^2, n = 4 (четыре точки)."""

from _house import f, save

W, H = 640, 300
SX, SY = 55, 12.5          # px на единицу по горизонтали и по вертикали
BASE = 262                 # y оси абсцисс
XMAX, YMAX = 4.5, 18.5     # длина осей в единицах


def panel(ox, xlabel):
    """Оси с началом в (ox, BASE), засечки 1..4 по горизонтали, 5..15 по вертикали."""
    P = lambda x, y: (ox + SX * x, BASE - SY * y)  # noqa: E731
    out = []
    x_end, _ = P(XMAX, 0)
    _, y_end = P(0, YMAX)
    out.append(f'  <path class="ink" d="M{f(ox - 12)},{BASE} L{f(x_end)},{BASE}" marker-end="url(#arrow)"/>')
    out.append(f'  <path class="ink" d="M{ox},{BASE + 12} L{ox},{f(y_end)}" marker-end="url(#arrow)"/>')
    out.append(f'  <text class="m" x="{f(x_end - 4)}" y="{BASE + 24}">{xlabel}</text>')
    for k in range(1, 5):
        x, _ = P(k, 0)
        out.append(f'  <path class="thin" d="M{f(x)},{BASE - 4} L{f(x)},{BASE + 4}"/>')
        out.append(f'  <text class="t small mid" x="{f(x)}" y="{BASE + 21}">{k}</text>')
    for v in (5, 10, 15):
        _, y = P(0, v)
        out.append(f'  <path class="thin" d="M{ox - 4},{f(y)} L{ox + 4},{f(y)}"/>')
        out.append(f'  <text class="t small end" x="{ox - 8}" y="{f(y + 5)}">{v}</text>')
    return P, out


body = []

# левая панель: f(x) = x^2 на [0; 4.25]
PL, axes = panel(70, "x")
body += axes
pts = [PL(t / 40, (t / 40) ** 2) for t in range(0, 171)]       # x от 0 до 4.25
body.append('  <path class="ink" d="M' + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + '"/>')
body.append(f'  <text class="m" x="{f(PL(0.9, 0)[0])}" y="{f(PL(0, 13)[1])}">f<tspan class="t">(</tspan>x<tspan class="t">)</tspan> <tspan class="t">=</tspan> x<tspan class="t sub" dy="-8">2</tspan></text>')

# правая панель: a_i = i^2, i = 1..4
PR, axes = panel(375, "i")
body += axes
for i in range(1, 5):
    x, y = PR(i, i * i)
    body.append(f'  <path class="thin dash" d="M{f(x)},{BASE} L{f(x)},{f(y)}" stroke-opacity="0.5"/>')
    body.append(f'  <circle class="dot-red" cx="{f(x)}" cy="{f(y)}" r="5"/>')
    body.append(f'  <text class="m lbl-red" x="{f(x - 30)}" y="{f(y - 6)}">a<tspan class="t sub" dy="5">{i}</tspan></text>')

# заголовки панелей
body.append('  <text class="m" x="150" y="22">f<tspan class="t">:</tspan> ℝ <tspan class="t">→</tspan> ℝ</text>')
body.append('  <text class="m" x="455" y="22">a<tspan class="t">:</tspan> I <tspan class="t">→</tspan> ℝ</text>')

save("index-function-graph", W, H, "\n".join(body) + "\n")
