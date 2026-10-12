#!/usr/bin/env python3
"""Probe 4: 2D red/orange map of diagram region; eqbox full-res map; outline colors."""
import numpy as np
from PIL import Image
import math, json

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
H, W = r.shape

# ---- 2D map of diagram region: reddish / orangeish ink only
print("== RED/ORANGE INK MAP (x 300..940, y 40..480), 4px blocks; R=red O=orange .=none ==")
redm = (r > 140) & (r - g > 35) & (r - b > 35)
orm = (r > 150) & (g > 60) & (g < 170) & (b < 90) & (r - g > 30)
rows = []
for y0 in range(40, 480, 4):
    line = ""
    for x0 in range(300, 940, 4):
        blk = slice(y0, y0+4), slice(x0, x0+4)
        if redm[blk].sum() >= 3: line += "R"
        elif orm[blk].sum() >= 3: line += "O"
        else: line += " "
    rows.append(line)
print("\n".join(rows))

# ---- full-res class map of eqbox interior
print("\n== EQBOX MAP (x 82..217, y 180..248) full res: B=blue R=red G=green k=dark o=olive-edge .=fill ==")
for y in range(180, 249):
    line = ""
    for x in range(82, 218):
        rr, gg, bb = im[y, x]
        if rr > 130 and int(rr)-int(gg) > 55 and int(rr)-int(bb) > 55: line += "R"
        elif bb > 110 and int(bb)-int(rr) > 40 and int(bb)-int(gg) > 40: line += "B"
        elif gg > 100 and int(gg)-int(rr) > 40 and int(gg)-int(bb) > 40: line += "G"
        elif rr < 120 and gg < 120 and bb < 120: line += "k"
        elif 170 < rr < 235 and 160 < gg < 235 and bb < 190: line += "o"
        else: line += "."
    print(line)

# ---- circle outline color: walk r=118..140 along clean angles
print("\n== OUTLINE radial scans (r, rgb) ==")
CX, CY = 577.2, 284.0
for a in (20, -20, 45, -45, 155, 205):
    samples = []
    for rad in range(116, 142):
        x = int(round(CX + rad * math.cos(math.radians(a))))
        y = int(round(CY - rad * math.sin(math.radians(a))))
        samples.append((rad, tuple(int(v) for v in im[y, x])))
    print(a, samples)

# ---- gray line end samples
print("\n== GRAY LINE samples y=283/284 ==")
for x in (258, 300, 350, 700, 800, 850, 888):
    print(x, tuple(int(v) for v in im[283, x]), tuple(int(v) for v in im[284, x]))

# ---- chip border color (dark green ring) + text color: sample W0 chip bbox edges
print("\n== CHIP W0 (bbox 718,273,785,295) edge/text samples ==")
print("top edge:", [tuple(int(v) for v in im[273, x]) for x in (730, 750, 770)])
print("bottom edge:", [tuple(int(v) for v in im[295, x]) for x in (730, 750, 770)])
print("left edge:", [tuple(int(v) for v in im[y, 718]) for y in (278, 284, 290)])
# darkest pixels in chip (text)
sub = im[273:296, 718:786]
sr, sg, sb = sub[...,0], sub[...,1], sub[...,2]
dark = (sg < 180) & (sg - sr > 20) & (sg - sb > 20)
ys, xs = np.where(dark)
if len(ys):
    print("text-green mean:", float(sr[ys, xs].mean()), float(sg[ys, xs].mean()), float(sb[ys, xs].mean()), "n=", len(ys))

# ---- arc stroke color sample list (near W0->W1 arc mid, angle 15deg, r 200..230)
print("\n== ARC mid scans angle 15deg ==")
for rad in range(190, 240, 2):
    x = int(round(CX + rad * math.cos(math.radians(15))))
    y = int(round(CY - rad * math.sin(math.radians(15))))
    print(rad, (x, y), tuple(int(v) for v in im[y, x]))

# ---- arrowhead bbox colors (4 heads)
print("\n== ARROWHEAD mean colors ==")
for tag, (x0, y0, x1, y1) in {"W2W3": (577, 63, 586, 73), "W1W2": (681, 91, 688, 101),
                              "W0W1": (760, 176, 770, 184), "W3W4": (470, 92, 477, 102)}.items():
    sub = im[y0:y1+1, x0:x1+1]
    warm = (sub[...,0] > 150) & (sub[...,1] < 180) & (sub[...,0] - sub[...,2] > 40)
    if warm.sum():
        print(tag, "n=", int(warm.sum()),
              "mean=", float(sub[...,0][warm].mean()), float(sub[...,1][warm].mean()), float(sub[...,2][warm].mean()))

# ---- title color core
print("\n== TITLE color ==")
sub = im[59:80, 73:305]
sr, sg, sb = sub[...,0], sub[...,1], sub[...,2]
core = (sr > 140) & (sg < 90) & (sb < 90)
print("title red mean:", float(sr[core].mean()), float(sg[core].mean()), float(sb[core].mean()), "n=", int(core.sum()))

# ---- eqbox line1/line2 pixel dump around the green zone (x 140..160)
print("\n== eqbox line1 x135..160, y188..206 ==")
for y in range(188, 207):
    print(y, [tuple(int(v) for v in im[y, x]) for x in range(135, 161, 3)])
