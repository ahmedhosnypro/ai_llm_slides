#!/usr/bin/env python3
"""Scanline RLE analysis: cube stacks, middle grid, right block layers+bands,
arrows, outlines. Full-resolution run-length encoding of color classes."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)

def cls(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if R > 240 and G > 240 and B > 235: return "."
    if R > 140 and G < 120 and B < 120 and R - G > 50 and R - B > 50: return "R"
    if B > 120 and B - R > 30 and B - G > 20: return "B"
    if G > 170 and G - R > 60 and G - B > 60: return "G"      # bright lime
    if G > 90 and G - R > 20 and G - B > 40: return "d"       # mid/dark green
    if R > 120 and B > 120 and G < 110: return "M"
    if R > 170 and G > 150 and B < 130: return "Y"
    if R > 170 and 80 < G < 170 and B < 100: return "O"
    if R < 100 and G < 100 and B < 100: return "K"
    return "?"

def rle_line(tag, y=None, x=None, x0=0, x1=None, y0=0, y1=None):
    if y is not None:
        seq = [(x, cls(a[y, x])) for x in range(x0, x1)]
        axis = f"y={y} x{x0}..{x1}"
    else:
        seq = [(y, cls(a[y, x])) for y in range(y0, y1)]
        axis = f"x={x} y{y0}..{y1}"
    runs, cur, st = [], None, 0
    for i, (pos, c) in enumerate(seq + [(None, None)]):
        if c != cur:
            if cur is not None: runs.append((cur, seq[st][0], seq[i - 1][0]))
            cur, st = c, i
    compact = " ".join(f"{c}[{s}-{e}]" if e - s > 0 else f"{c}{s}" for c, s, e in runs if not (c == "." and e - s > 4))
    print(f"{tag} {axis}:\n   {compact}")

print("===== LEFT STACK =====")
rle_line("L", y=300, x0=140, x1=240)
rle_line("L", x=190, y0=250, y1=440)
rle_line("L", x=205, y0=250, y1=440)

print("===== MIDDLE GRID =====")
rle_line("M", y=310, x0=360, x1=540)
rle_line("M", x=430, y0=240, y1=440)
rle_line("M", y=268, x0=360, x1=540)

print("===== RIGHT BLOCK =====")
rle_line("R", y=400, x0=630, x1=900)
rle_line("R", x=700, y0=230, y1=500)
rle_line("R", x=730, y0=230, y1=500)
rle_line("R", y=330, x0=630, y1=None, x1=900)
rle_line("R", y=285, x0=630, x1=900)
rle_line("R", x=810, y0=230, y1=500)
rle_line("R", x=845, y0=230, y1=500)
rle_line("R", y=460, x0=630, x1=900)

print("===== ARROWS: red double-heads =====")
# vertical arrow left of block (spec x 63-66% => slide 605-634 => frame ~600-628)
rle_line("V-arr", x=610, y0=300, y1=500)
rle_line("V-arr", y=400, x0=590, x1=650)
# horizontal arrow below block
rle_line("H-arr", y=475, x0=600, x1=900)
rle_line("H-arr", y=480, x0=600, x1=900)
rle_line("H-arr", x=700, y0=455, y1=500)
# diagonal arrow right side
rle_line("D-arr", y=380, x0=840, x1=900)
rle_line("D-arr", y=430, x0=840, x1=900)
rle_line("D-arr", x=870, y0=300, y1=500)
rle_line("D-arr", x=880, y0=300, y1=500)
