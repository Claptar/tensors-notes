"""Рис. 6. Числа 1, 2, 3 на окружности: по часовой стрелке (красные стрелки, слева) с любого места
читаются чётные перестановки 123, 231, 312; против часовой (синие, справа) — нечётные 132, 321, 213.
После второго обзора (2026-10-19, «рисовать эти циклические перестановки нет смысла»): только две
окружности, без строк перестановок, низко и узко."""

import math

from _house import f, save

W, H = 400, 132
R = 42
CENTERS = [(100, 68), (300, 68)]
ANG = {1: -90, 2: 30, 3: 150}       # градусы; в SVG рост угла = по часовой стрелке
GAP = 22                             # угловой зазор вокруг цифр


def pt(c, deg, r=R):
    t = math.radians(deg)
    return c[0] + r * math.cos(t), c[1] + r * math.sin(t)


def read_cycle(order):
    """Все три прочтения цикла, начиная с каждого элемента."""
    return ["".join(str(order[(s + k) % 3]) for k in range(3)) for s in range(3)]


def parity(p):
    inv = sum(1 for x in range(3) for y in range(x + 1, 3) if p[x] > p[y])
    return 1 if inv % 2 == 0 else -1


body = []
panels = [(CENTERS[0], [1, 2, 3], "red", +1), (CENTERS[1], [1, 3, 2], "blue", -1)]
for c, order, col, expected in panels:
    # проверка: каждое прочтение цикла в этом направлении имеет ожидаемую чётность
    assert {parity([int(ch) for ch in p]) for p in read_cycle(order)} == {expected}
    for k in range(3):
        u, v = order[k], order[(k + 1) % 3]
        a0, a1 = ANG[u], ANG[v]
        if col == "red":                 # по часовой: угол растёт
            a1 = a1 if a1 > a0 else a1 + 360
            s0, s1, sweep = a0 + GAP, a1 - GAP, 1
        else:                            # против часовой: угол убывает
            a1 = a1 if a1 < a0 else a1 - 360
            s0, s1, sweep = a0 - GAP, a1 + GAP, 0
        (x0, y0), (x1, y1) = pt(c, s0), pt(c, s1)
        body.append(f'  <path class="ink {col}" d="M{f(x0)},{f(y0)} A{R},{R} 0 0 {sweep} {f(x1)},{f(y1)}" '
                    f'marker-end="url(#arrow-{col})"/>')
    for num, deg in ANG.items():
        x, y = pt(c, deg)
        body.append(f'  <text class="t mid" x="{f(x)}" y="{f(y + 7)}">{num}</text>')

save("levi-civita-cycle", W, H, "\n".join(body) + "\n")
