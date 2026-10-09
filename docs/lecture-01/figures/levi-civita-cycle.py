"""Рис. 6. Числа 1, 2, 3 на окружности. По часовой стрелке (красные стрелки) с любого места
читаются чётные перестановки 123, 231, 312 (epsilon = +1); против часовой (синие) —
нечётные 132, 321, 213 (epsilon = -1)."""

import math

from _house import f, save

W, H = 640, 290
R = 62
CENTERS = [(165, 120), (475, 120)]
ANG = {1: -90, 2: 30, 3: 150}       # градусы; в SVG рост угла = по часовой стрелке
GAP = 20                             # угловой зазор вокруг цифр


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
panels = [(CENTERS[0], [1, 2, 3], "red"), (CENTERS[1], [1, 3, 2], "blue")]
for c, order, col in panels:
    perms = read_cycle(order)
    sign = {parity([int(ch) for ch in p]) for p in perms}
    assert len(sign) == 1
    sign = sign.pop()
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
    lbl = "lbl-red" if col == "red" else "lbl-blue"
    for k, p in enumerate(perms):            # три прочтения, каждое отдельной подписью
        body.append(f'  <text class="t mid" x="{c[0] + 92 * (k - 1)}" y="{c[1] + R + 52}">({p[0]}, {p[1]}, {p[2]})</text>')
    s = "+1" if sign > 0 else "−1"
    body.append(f'  <text class="m mid {lbl}" x="{c[0]}" y="{c[1] + R + 86}">ε <tspan class="t">= {s}</tspan></text>')

save("levi-civita-cycle", W, H, "\n".join(body) + "\n")
