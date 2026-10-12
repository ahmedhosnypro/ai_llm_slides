#!/usr/bin/env python3
"""Build a labeled composite of uncertain regions for one batched vision analysis."""
from PIL import Image, ImageDraw

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg"
img = Image.open(SRC).convert("RGB")

crops = [
    # (x0,y0,x1,y1, scale, label)
    (66, 55, 580, 95, 1.6, "C1 TITLE (top-left)"),
    (715, 42, 912, 100, 2.2, "C2 TOP-RIGHT LEGEND + badge"),
    (62, 205, 268, 395, 1.6, "C3 LEFT: container Z1-Z4, W_k boxes, K strips"),
    (252, 178, 458, 402, 1.6, "C4 DotProduct box + Scaling column + fraction"),
    (440, 180, 548, 448, 1.6, "C5 Mask column + LookAhead ellipse + Softmax column"),
    (540, 95, 725, 200, 2.0, "C6 output Z box + green arrow + WeightedSUM pill + Sigma"),
    (535, 208, 705, 385, 1.6, "C7 ⊗ nodes + V strips + arrows (right-center)"),
    (695, 208, 855, 388, 1.6, "C8 W_v boxes + right Z container"),
    (252, 388, 368, 515, 2.2, "C9 W_q box + q2 strip + red arrows"),
    (178, 450, 505, 515, 1.6, "C10 BOTTOM container Z1-Z4 (Z2 magenta)"),
    (688, 438, 902, 515, 2.0, "C11 BOTTOM-RIGHT legend 1xd W dxd = 1xd"),
]
pad = 14
tiles = []
for (x0, y0, x1, y1, sc, lab) in crops:
    c = img.crop((x0, y0, x1, y1))
    c = c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS)
    tiles.append((c, lab))

cols = 2
colw = max(t[0].width for t in tiles) + pad
rowh = []
cur = 0; rh = 0
for i, (c, lab) in enumerate(tiles):
    rh = max(rh, c.height + 26)
    if (i + 1) % cols == 0:
        rowh.append(rh); rh = 0
if rh: rowh.append(rh)
W = cols * colw + pad
H = sum(rowh) + pad
canvas = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(canvas)
y = pad
i = 0
for r, h in enumerate(rowh):
    x = pad
    for cidx in range(cols):
        if i >= len(tiles): break
        c, lab = tiles[i]
        d.rectangle([x-2, y-2, x+c.width+2, y+20], outline=(0,0,0), width=2)
        d.text((x+4, y+2), lab, fill=(200, 0, 0))
        canvas.paste(c, (x, y+22))
        d.rectangle([x-2, y+20, x+c.width+2, y+22+c.height+2], outline=(0,0,0), width=2)
        x += colw
        i += 1
    y += h
canvas.save("composite_crops.png")
print("saved composite_crops.png", canvas.size)
