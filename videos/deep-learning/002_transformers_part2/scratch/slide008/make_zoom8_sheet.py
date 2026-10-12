#!/usr/bin/env python3
"""Zoom sheet #2: 8x crops to settle superscript glyph, Y label, node glyph,
q2 label, X2 highlight. Plus micro-PIL: exact box edges/fills."""
from PIL import Image, ImageDraw
import numpy as np

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_008.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide008/crops_zoom8_sheet.png"
im = Image.open(SRC).convert("RGB")

CROPS = [
    ("P", 168, 224, 212, 254, 8, "W_k box1 label+superscript"),
    ("Q", 693, 224, 737, 254, 8, "W_v box1 label+superscript"),
    ("R", 276, 403, 332, 452, 7, "W_q box label (under circle)"),
    ("S", 512, 212, 548, 246, 8, "node1 glyph/ring/fill"),
    ("T", 562, 116, 602, 146, 8, "Y label: Y or Y2? color"),
    ("U", 278, 384, 318, 414, 8, "q2 label zoom"),
    ("V", 280, 452, 334, 494, 6, "X2 widget + magenta highlight"),
]

panels = []
for (lbl, x0, y0, x1, y1, s, cap) in CROPS:
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * s, c.height * s), Image.LANCZOS)
    panels.append((lbl, c, cap))

pad = 14
label_h = 30
rows = [[0, 1, 2], [3, 4], [5, 6]]
total_w = pad + max(sum(p[1].width for p in panels[i:i+3]) + pad * (len(range(i, min(i+3, len(panels)))) ) for i in [0])  # simple below
# simpler: fixed 3-col grid
colw = max(p[1].width for p in panels) + pad
rowh = [max(panels[i][1].height for i in r) + label_h + pad for r in rows]
W = pad + colw * 3
H = pad + sum(rowh)
sheet = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(sheet)
y = pad
for r_i, row in enumerate(rows):
    x = pad
    for idx in row:
        lbl, c, cap = panels[idx]
        draw.rectangle([x - 2, y - 2, x + c.width + 2, y + c.height + label_h + 2], outline=(200, 0, 0), width=2)
        draw.text((x + 4, y + 2), f"[{lbl}] {cap}", fill=(0, 0, 200))
        sheet.paste(c, (x, y + label_h))
        x += colw
    y += rowh[r_i]
sheet.save(OUT)
print("sheet:", OUT, sheet.size)

# ---- micro-PIL: exact W_k / W_v box edges at clean rows
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
AX, SX, SY = 17.628, 0.961232, 0.955556
def sx(fx): return (fx - AX) / SX
def sy(fy): return fy / SY

print("\n== W_k box1: row y=229 and y=247 color runs (x 140..220) ==")
for yy in (229, 247):
    s = ""
    for x in range(140, 221):
        R, G, B = a[yy, x]
        if G > 180 and G - R > 25 and G - B > 20: c = "G"
        elif R > 225 and G > 195 and B > 165: c = "."
        elif R < 140 and G < 140 and B < 140: c = "#"
        elif R > 150 and R - G > 50: c = "R"
        else: c = "?"
        s += c
    print(f"y={yy}: {s}")
print("x legend 140..220")

print("\n== W_v box1: row y=229 and y=247 (x 685..745) ==")
for yy in (229, 247):
    s = ""
    for x in range(685, 746):
        R, G, B = a[yy, x]
        if B > R + 30 and B > 130 and G < 235: c = "B"
        elif G > 200 and R > 150 and B > 150 and G - R > 20: c = "g"
        elif R > 225 and G > 195 and B > 165: c = "."
        elif R < 140 and G < 140 and B < 140: c = "#"
        else: c = "?"
        s += c
    print(f"y={yy}: {s}")
print("x legend 685..745")

print("\n== W_k box1 fill+text histogram (x 172..204, y 228..250) ==")
from collections import Counter
px = a[228:250, 172:204].reshape(-1, 3)
cnt = Counter(map(tuple, px))
for c, n in cnt.most_common(8): print("  ", c, n)
print("== W_v box1 fill+text histogram (x 699..728, y 229..250) ==")
px = a[229:250, 699:728].reshape(-1, 3)
cnt = Counter(map(tuple, px))
for c, n in cnt.most_common(8): print("  ", c, n)

print("\n== Y label ink census (x 568..598, y 118..146) ==")
sub = a[118:146, 568:598]
dk = (sub[:, :, 0] < 170) & (sub[:, :, 1] < 190)
ys, xs = np.where(dk)
if len(xs):
    print("ink bbox x", 568 + xs.min(), "..", 568 + xs.max(), " y", 118 + ys.min(), "..", 118 + ys.max(), "n=", len(ys))
    # ink pixel color clusters
    cols = sub[dk]
    print("mean ink color:", cols.mean(axis=0).round(0))
    # column histogram to spot a separate subscript blob
    colh = np.zeros(30, int)
    for x in xs: colh[x] += 1
    print("col histogram (x568+i):", list(colh))
    rowh = np.zeros(28, int)
    for y in ys: rowh[y] += 1
    print("row histogram (y118+i):", list(rowh))

print("\n== node rings: red arcs at low threshold around estimated centers ==")
red = (r > 110) & (r - g > 35) & (r - b > 35)
for (cx, cy) in [(528, 228), (558, 277), (584, 316), (614, 358)]:
    win = red[cy - 16:cy + 17, cx - 16:cx + 17]
    ys, xs = np.where(win)
    if len(ys):
        print(f"  node~({cx},{cy}): red px n={len(ys)} bbox x {cx-16+xs.min()}..{cx-16+xs.max()} y {cy-16+ys.min()}..{cy-16+ys.max()}")
