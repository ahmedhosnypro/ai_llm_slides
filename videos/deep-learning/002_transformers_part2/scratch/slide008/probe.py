#!/usr/bin/env python3
"""Probe remapped 002:8 at parent (001:33) element positions + detect deltas."""
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
f8 = np.asarray(Image.open(f"{ROOT}/002_transformers_part2/scratch/slide008/frame8_remapped_960x540.png").convert("RGB")).astype(int)
f33 = np.asarray(Image.open(f"{ROOT}/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")).astype(int)

def px(img, x, y):
    return tuple(img[y, x])

probes = [
    # (name, x, y, parent-expected)
    ("panel bg", 100, 150, "F7E2CD peach"),
    ("panel bg2", 450, 220, "F7E2CD"),
    ("left container int", 99, 300, "E7FFE9 pale green"),
    ("left container int2", 99, 250, "E7FFE9"),
    ("W_k band area", 175, 300, "F7F96B yellow band"),
    ("W_k box1", 175, 246, "F7F96B"),
    ("DP box", 300, 300, "DCCBBB"),
    ("DP box top", 300, 210, "DCCBBB"),
    ("DP box bottom", 300, 395, "DCCBBB"),
    ("softmax col", 474, 300, "F8DDFC"),
    ("softmax col top", 474, 210, "F8DDFC"),
    ("sigma box", 583, 206, "EAFEFC"),
    ("circle4 (mult)", 622, 372, "white/red ring"),
    ("sentence container", 300, 495, "E7FFE9"),
    ("sentence container2", 220, 490, "E7FFE9"),
    ("legend box", 800, 490, "E7FFE9"),
    ("pill Similarity", 304, 174, "FFFFE3"),
    ("pill Probabilities", 470, 172, "FFFFE3"),
    ("pill WeightedSUM", 640, 172, "FFFFE3"),
    ("W_q box", 296, 448, "F7F96B"),
    ("Y2 strip", 584, 133, "9CCB96-ish"),
    ("right container int", 804, 300, "E7FFE9"),
    ("W_v band", 723, 300, "F7F96B"),
    ("K vector row1", 220, 247, "cells"),
    ("V label row1", 648, 235, "label"),
]
print(f"{'probe':26s} {'remapped-8':16s} {'parent-33':16s}  parent-expected")
for name, x, y, exp in probes:
    print(f"{name:26s} {str(px(f8,x,y)):16s} {str(px(f33,x,y)):16s}  {exp}")

# --- detect translucent blue annotation circle in remapped-8 (spec: 4169E1@55%) ---
r, g, b = f8[:,:,0], f8[:,:,1], f8[:,:,2]
blue = (b - r > 25) & (b - g > 10) & (b > 120) & (r > 80)  # translucent blue over peach
ys, xs = np.where(blue)
m = (xs > 150) & (xs < 500) & (ys > 330) & (ys < 540)
print("\nblue-circle px count (8):", m.sum())
if m.sum() > 100:
    print("  bbox x %d..%d  y %d..%d" % (xs[m].min(), xs[m].max(), ys[m].min(), ys[m].max()))
    print("  center approx (%.0f, %.0f)" % ((xs[m].min()+xs[m].max())/2, (ys[m].min()+ys[m].max())/2))

# same detection in parent frame (should find its dark-red circle instead)
r3, g3, b3 = f33[:,:,0], f33[:,:,1], f33[:,:,2]
redc = (r3 - g3 > 60) & (r3 - b3 > 60) & (r3 > 120)
ys3, xs3 = np.where(redc)
m3 = (xs3 > 180) & (xs3 < 320) & (ys3 > 270) & (ys3 < 360)
print("parent red-circle px:", m3.sum(), "bbox:", (xs3[m3].min(), ys3[m3].min(), xs3[m3].max(), ys3[m3].max()) if m3.sum() else None)

# --- red block arrow (chunky, bottom-left of query) in 8 ---
chunky = (r - g > 70) & (r - b > 70) & (r > 130)
ys2, xs2 = np.where(chunky)
m2 = (xs2 > 220) & (xs2 < 420) & (ys2 > 400) & (ys2 < 540)
print("8 chunky-red px (query region):", m2.sum(), "bbox:", (xs2[m2].min(), ys2[m2].min(), xs2[m2].max(), ys2[m2].max()) if m2.sum() else None)
m2b = (xs2 > 180) & (xs2 < 320) & (ys2 > 470) & (ys2 < 540)
print("33 chunky-red px (its arrow region):", m2b.sum(), "bbox:", (xs2[m2b].min(), ys2[m2b].min(), xs2[m2b].max(), ys2[m2b].max()) if m2b.sum() else None)

# --- title ink rows in remapped-8 vs parent (dark ink in y 40..110) ---
def ink_rows(img, y0, y1, x0=150, x1=830, thr=120):
    reg = img[y0:y1, x0:x1]
    dark = (reg.max(axis=2) < thr)
    rows = dark.sum(axis=1)
    return [(y0+i, int(v)) for i, v in enumerate(rows) if v > 8]

def ink_span(img, y0, y1, x0=150, x1=830, thr=120):
    reg = img[y0:y1, x0:x1]
    dark = (reg.max(axis=2) < thr)
    cols = dark.sum(axis=0)
    xs = np.where(cols > 0)[0]
    return (x0 + int(xs.min()), x0 + int(xs.max())) if len(xs) else None

print("\n8 title ink rows y40..110:", ink_rows(f8, 40, 110))
print("33 title ink rows y40..110:", ink_rows(f33, 40, 110))
print("8 L1 span:", ink_span(f8, 48, 75), " 33 L1 span:", ink_span(f33, 55, 75))
print("8 L2 span:", ink_span(f8, 75, 105), " 33 L2 span:", ink_span(f33, 78, 100))
