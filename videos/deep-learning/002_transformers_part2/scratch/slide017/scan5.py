#!/usr/bin/env python3
"""h=1 layer internals: input strips, W boxes, Dot Product, pills, Sigma, V path, bottom strip."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def hruns(y, x0, x1, min_len=3, sat_min=22, dark_max=160):
    row = a[y, x0:x1]
    out = []; s = None
    for x in range(x1 - x0):
        r, g, b = row[x]
        sat = max(r, g, b) - min(r, g, b)
        dark = max(r, g, b) < dark_max
        nb = (sat >= sat_min) or dark
        if nb and s is None: s = x
        elif not nb and s is not None:
            if x - s >= min_len:
                med = np.median(row[s:x], axis=0).astype(int)
                out.append((s + x0, x - 1 + x0, "#%02X%02X%02X" % tuple(med)))
            s = None
    if s is not None:
        med = np.median(row[s:], axis=0).astype(int)
        out.append((s + x0, x1 - 1, "#%02X%02X%02X" % tuple(med)))
    return out

def vruns(x, y0, y1, min_len=3, sat_min=22, dark_max=160):
    col = a[y0:y1, x]
    out = []; s = None
    for y in range(y1 - y0):
        r, g, b = col[y]
        sat = max(r, g, b) - min(r, g, b)
        dark = max(r, g, b) < dark_max
        nb = (sat >= sat_min) or dark
        if nb and s is None: s = y
        elif not nb and s is not None:
            if y - s >= min_len:
                med = np.median(col[s:y], axis=0).astype(int)
                out.append((s + y0, y - 1 + y0, "#%02X%02X%02X" % tuple(med)))
            s = None
    if s is not None:
        med = np.median(col[s:], axis=0).astype(int)
        out.append((s + y0, y1 - 1, "#%02X%02X%02X" % tuple(med)))
    return out

print("== h1 left zone horizontal scans (input strips + gold W col + K strips) ==")
for y in [295, 300, 305, 312, 318, 325, 332, 338, 345, 352, 360, 368, 375, 382, 390, 398, 405, 412, 418, 425]:
    print(f"y={y}: {hruns(y, 70, 280)}")

print("\n== vertical scan x=110 (input strip col), x=150 (gold W col), x=200 (dot product) ==")
for x in [85, 100, 110, 120, 135, 150, 165, 180, 195, 205, 215, 225, 240, 250]:
    print(f"x={x}: {vruns(x, 260, 520)}")

print("\n== pills row zone y=280..310 x=260..480 (Similarity / Probabilities ovals) ==")
for y in [283, 288, 293, 298, 303, 308]:
    print(f"y={y}: {hruns(y, 250, 500)}")

print("\n== middle zone x=260..540 y=300..460 (Scaling pill, Softmax pill, Sigma, tensors) ==")
for y in [320, 340, 360, 380, 400, 420, 440, 455]:
    print(f"y={y}: {hruns(y, 250, 545)}")

print("\n== right zone x=540..780 y=280..470 (V labels, W_v gold, output strips) ==")
for y in [300, 320, 340, 360, 380, 400, 420, 440, 460]:
    print(f"y={y}: {hruns(y, 540, 780)}")

print("\n== bottom zone y=460..515 x=70..770 (bottom strip, W_q, q, red arrow) ==")
for y in [465, 472, 478, 484, 490, 496, 502]:
    print(f"y={y}: {hruns(y, 70, 770)}")

print("\n== legend zone y=440..515 x=720..920 ==")
for y in [445, 455, 465, 475, 485, 495, 505]:
    print(f"y={y}: {hruns(y, 700, 925)}")

print("\n== swoosh zone (thick red curved arrow) x=580..850 y=300..520 ==")
m = (np.abs(a - np.array([200, 30, 30])).max(axis=2) <= 60)
sub = m[280:540, 560:900]
ys, xs = np.nonzero(sub)
print(f"red ink in swoosh zone: ({xs.min()+560},{ys.min()+280})-({xs.max()+560},{ys.max()+280}) n={len(xs)}")
# red-ish text (blue label +H* Heads?)
print("\n== blue-ish ink zone x=580..800 y=380..460 ==")
mb = (np.abs(a - np.array([0, 112, 192])).max(axis=2) <= 70)
subb = mb[300:520, 560:900]
ys2, xs2 = np.nonzero(subb)
if len(xs2): print(f"blue ink: ({xs2.min()+560},{ys2.min()+300})-({xs2.max()+560},{ys2.max()+300}) n={len(xs2)}")
else: print("none")
