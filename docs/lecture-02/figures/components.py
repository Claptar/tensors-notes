"""Рис. 2. Пример с доски (заметки, с. 6): базис e1, e2 на плоскости,
a = 2e1 + e2 (красный), b = e1 + 3e2 (синий), c = a + b = 3e1 + 4e2 (чёрный, параллелограмм штрихами),
3a = 6e1 + 3e2 (красный штрих). Столбцы компонент стоят в тексте формулой; правая панель со столбцами
убрана после независимого обзора (2026-10-20): она повторяла эту формулу.
Сетка проведена вдоль векторов базиса только для чтения компонент.
"""

from _house import arrow, dot, line, text, vec, write

W, H = 350, 250
O = (48, 222)
S = 42                                   # px per unit along e1 and e2 (as on the board: e1 to the right, e2 up)
E1, E2 = (S, 0.0), (0.0, -S)


def pt(c1, c2):
    """Point c1*e1 + c2*e2."""
    return (O[0] + c1 * E1[0] + c2 * E2[0], O[1] + c1 * E1[1] + c2 * E2[1])


comp = {"a": (2, 1), "b": (1, 3)}
comp["c"] = (comp["a"][0] + comp["b"][0], comp["a"][1] + comp["b"][1])   # a + b
comp["3a"] = (3 * comp["a"][0], 3 * comp["a"][1])
assert comp["c"] == (3, 4) and comp["3a"] == (6, 3)

body = []
# light grid along the basis, 0..6 x 0..4
for i in range(0, 7):
    body.append(line(pt(i, 0), pt(i, 4.4), "grid"))
for j in range(0, 5):
    body.append(line(pt(0, j), pt(6.4, j), "grid"))

A, B, C, A3 = (pt(*comp[k]) for k in ("a", "b", "c", "3a"))
body += [line(A, C, "thin dash"), line(B, C, "thin dash")]
body.append(arrow(O, A3, color="red", dash=True))
body += [arrow(O, C), arrow(O, B, color="blue"), arrow(O, A, color="red")]
body += [arrow(O, pt(1, 0), width=2.2), arrow(O, pt(0, 1), width=2.2), dot(O)]

body.append(vec(pt(1, 0)[0] - 18, pt(1, 0)[1] + 22, "e", "1"))
body.append(vec(pt(0, 1)[0] - 30, pt(0, 1)[1] + 6, "e", "2"))
body.append(vec(A[0] + 2, A[1] + 22, "a", color="red"))
body.append(vec(B[0] - 22, B[1] - 4, "b", color="blue"))
body.append(vec(C[0] + 6, C[1] - 4, "c"))
body.append(text(A3[0] - 14, A3[1] - 12, "3", "t lbl-red"))
body.append(vec(A3[0] - 4, A3[1] - 12, "a", color="red"))

for x, y in (A, B, C, A3):
    assert 10 < x < 340 and 10 < y < H - 10

write("components.svg", W, H, body)
