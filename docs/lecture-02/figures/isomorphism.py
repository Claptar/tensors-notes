"""Рис. 3. Схема с доски (заметки, с. 7): V1 и V2 одной размерности n, базисы задают отображения
φ1: V1 -> S_n и φ2: V2 -> S_n; вектору v из V1 сопоставляется вектор w из V2 с тем же столбцом
компонент (штриховая двусторонняя стрелка). Высота уменьшена до 290 (≤ 1/3 страницы). Множества — схематические контуры, как на рис. 1 лекции 1.
"""

from _house import arrow, blob, column, dot, fmt, text, vec, write

W, H = 640, 290
SN, V1, V2 = (320, 70), (128, 196), (512, 196)

body = []
body.append(f'<path class="ink tint-grey" d="{blob(*SN, 105, 56, 0.9)}"/>')
body.append(f'<path class="ink tint-grey" d="{blob(*V1, 100, 58, 0.3)}"/>')
body.append(f'<path class="ink tint-grey" d="{blob(*V2, 100, 58, 2.2)}"/>')

col = (SN[0] + 10, SN[1] + 4)
body += column(col[0], col[1], ["<tspan class=\"m\">α</tspan><tspan class=\"sub t\" dy=\"5\">1</tspan>",
                                 "⋮",
                                 "<tspan class=\"m\">α</tspan><tspan class=\"sub m\" dy=\"5\">n</tspan>"],
               h_line=22, w=36)

v, w = (V1[0] + 18, V1[1] - 14), (V2[0] - 18, V2[1] - 14)
body += [dot(v, "dot-red", 4), dot(w, "dot-red", 4)]
body.append(vec(v[0] - 8, v[1] + 26, "v", color="red"))
body.append(vec(w[0] - 4, w[1] + 26, "w", color="red"))

# phi_1 : v -> column, phi_2 : w -> column (straight arrows stopping at the column's brackets)
body.append(arrow((v[0] + 6, v[1] - 6), (col[0] - 30, col[1] + 14)))
body.append(arrow((w[0] - 6, w[1] - 6), (col[0] + 30, col[1] + 14)))
body.append(text(195, 132, "φ<tspan class=\"sub t\" dy=\"5\">1</tspan>", "m"))
body.append(text(428, 132, "φ<tspan class=\"sub t\" dy=\"5\">2</tspan>", "m"))

# pairing v <-> w
body.append(f'<path class="ink red dash" d="M{fmt(v[0] + 10)},{fmt(v[1] + 4)} L{fmt(w[0] - 10)},{fmt(w[1] + 4)}" '
            f'marker-start="url(#arrow-red)" marker-end="url(#arrow-red)"/>')

body.append(text(SN[0] - 78, SN[1] - 8, "S<tspan class=\"sub m\" dy=\"5\">n</tspan>", "m"))
body.append(text(V1[0] - 62, V1[1] + 30, "V<tspan class=\"sub t\" dy=\"5\">1</tspan>", "m"))
body.append(text(V2[0] + 42, V2[1] + 30, "V<tspan class=\"sub t\" dy=\"5\">2</tspan>", "m"))
body.append(text(V1[0], H - 8, "dim <tspan class=\"m\">V</tspan><tspan class=\"sub t\" dy=\"5\">1</tspan>"
                 "<tspan dy=\"-5\"> = </tspan><tspan class=\"m\">n</tspan>", "t small", "middle"))
body.append(text(V2[0], H - 8, "dim <tspan class=\"m\">V</tspan><tspan class=\"sub t\" dy=\"5\">2</tspan>"
                 "<tspan dy=\"-5\"> = </tspan><tspan class=\"m\">n</tspan>", "t small", "middle"))

write("isomorphism.svg", W, H, body)
