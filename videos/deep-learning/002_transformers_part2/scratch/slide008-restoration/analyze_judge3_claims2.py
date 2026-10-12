#!/usr/bin/env python3
"""Part 2: aligned red-density maps + frame-side component list (read-only)."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
render = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide008/render_2.png").convert("RGB")).astype(int)
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_008.jpg").convert("RGB")).astype(int)

def redmask(a):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (R >= 140) & (G <= 120) & (B <= 120) & ((R - np.maximum(G, B)) >= 50)

mr, mf = redmask(render), redmask(frame)
RW, RH = render.shape[1], render.shape[0]

# Map the FRAME's red mask into render coordinate space (same fit as build header).
FH, FW = mf.shape
ys, xs = np.nonzero(mf)
sx = ((xs - 17.628) / 0.961232) * (RW / 960.0)
sy = (ys / 0.955556) * (RH / 540.0)
H, W = 56, 100  # grid: x 380..1560 step ~11.8, y 300..900 step ~10.7
x0, x1, y0, y1 = 380, 1560, 300, 900
cw, ch = (x1 - x0) / W, (y1 - y0) / H
gr = np.zeros((H, W), dtype=int)
gf = np.zeros((H, W), dtype=int)
ry, rx = np.nonzero(mr)
for yy, xx in zip(ry.tolist(), rx.tolist()):
    if x0 <= xx < x1 and y0 <= yy < y1:
        gr[int((yy - y0) / ch), int((xx - x0) / cw)] += 1
for yy, xx in zip(sy.tolist(), sx.tolist()):
    if x0 <= xx < x1 and y0 <= yy < y1:
        gf[int((yy - y0) / ch), int((xx - x0) / cw)] += 1

def sym(n):
    return " " if n == 0 else ("." if n < 5 else ("+" if n < 20 else ("*" if n < 60 else "#")))

print("Red density maps over x 380..1560, y 300..900 (render coords).")
print("LEFT = recreation render, RIGHT = original frame (mapped). '.':1-4 '+' 5-19 '*' 20-59 '#' 60+")
print("     " + "".join(str((x0 + int(i * cw * 10)) // 100 % 10) for i in range(W // 10)) )
for i in range(H):
    lft = "".join(sym(n) for n in gr[i])
    rgt = "".join(sym(n) for n in gf[i])
    print(f"y{y0 + int(i * ch):4d} {lft} | {rgt}")
