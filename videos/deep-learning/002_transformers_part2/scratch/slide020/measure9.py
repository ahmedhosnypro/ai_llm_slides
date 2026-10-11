#!/usr/bin/env python3
"""Phase 9: pixel transects across rows to read box edges + cell strips exactly."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_020.jpg"
img = Image.open(SRC).convert("RGB")
px = img.load()
out = {}


def classify(p):
    r, g, b = p
    if r > 150 and (r - g) > 60 and (r - b) > 60:
        return "R"          # strong red
    if 110 < r <= 150 and g < 70 and b < 70:
        return "D"          # dark red (990000)
    if r > 200 and 140 < g < 215 and b < 150 and (r - b) > 60:
        return "O"          # orange/yellow cell
    if r > 220 and g < 200 and 150 < b < 220 and (r - g) > 30:
        return "P"          # pink cell / pink fill
    if r > 235 and g > 235 and b > 235:
        return "W"          # white
    if g > 130 and (g - r) > 30 and (g - b) > 15:
        return "G"          # green
    if b > 160 and (b - r) > 50 and (b - g) > 50:
        return "B"          # strong blue
    if abs(r - 233) < 14 and abs(g - 233) < 14 and abs(b - 231) < 16:
        return "."          # panel gray
    return "?"


def transect(y, x0, x1, step=1):
    s = []
    for x in range(x0, x1, step):
        s.append(classify(px[x, y]))
    return "".join(s)


# row1: label row 115, box top ~?, box bottom ~?
out["r1_y96"] = transect(96, 150, 910)
out["r1_y104"] = transect(104, 150, 910)
out["r1_y115"] = transect(115, 150, 910)
out["r1_y126"] = transect(126, 150, 910)
out["r1_y133"] = transect(133, 150, 910)
# row2: strip mid 172, box top 156, box bottom 191
out["r2_y156"] = transect(156, 130, 910)
out["r2_y172"] = transect(172, 130, 910)
out["r2_y191"] = transect(191, 130, 910)
# row3: 222 (top border), 236 (label mid), 254 (bottom)
out["r3_y221"] = transect(221, 130, 910)
out["r3_y236"] = transect(236, 130, 910)
out["r3_y253"] = transect(253, 130, 910)
# row4: 340 (top?), 380 (label), 397 (bottom)
out["r4_y332"] = transect(332, 100, 910)
out["r4_y340"] = transect(340, 100, 910)
out["r4_y380"] = transect(380, 100, 910)
out["r4_y397"] = transect(397, 100, 910)
# vertical transects through box1 column (x=220) rows 85..145, 150..200, 215..260, 328..420
def vtran(x, y0, y1):
    return "".join(classify(px[x, y]) for y in range(y0, y1))

out["v_x220_r1"] = vtran(220, 85, 145)
out["v_x220_r2"] = vtran(220, 150, 200)
out["v_x220_r3"] = vtran(220, 213, 262)
out["v_x220_r4"] = vtran(220, 328, 420)
out["v_x480_r4"] = vtran(480, 328, 420)
out["v_x480_r1"] = vtran(480, 85, 145)
out["v_x700_r1"] = vtran(700, 85, 145)
out["v_x700_r2"] = vtran(700, 150, 200)
print(json.dumps(out, indent=1))
