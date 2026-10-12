#!/usr/bin/env python3
"""Probe 6: HSV-filtered blue label ink (sat>0.45, hue 200..255) frame vs parent."""
from PIL import Image
import numpy as np
import colorsys

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
F = np.asarray(Image.open(f"{VID}/unique_slides/slide_017.jpg").convert("RGB")).astype(np.float64) / 255.0
P = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide043/render_2.png"
).convert("RGB").resize((960, 540), Image.LANCZOS)).astype(np.float64) / 255.0
AX, SX, AY, SY = 18.250, 0.96150, 1.950, 0.95500

def fpx(sx, sy):
    return F[int(round(AY + SY * sy)), int(round(AX + SX * sx))]

def blue_ink(c):
    r, g, b = c
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return s > 0.45 and v > 0.35 and 0.55 <= h <= 0.71  # hue 198..256 deg

def ink(sampler, x0, x1, y0, y1):
    hits = []
    for sy in range(y0, y1):
        for sx in range(x0, x1):
            if blue_ink(sampler(sx, sy)):
                hits.append((sx, sy))
    return np.array(hits, dtype=float) if hits else None

for name, fn in (("frame", fpx), ("parent", lambda sx, sy: P[sy, sx])):
    pts = ink(fn, 560, 770, 340, 470)
    if pts is None:
        print(f"{name}: no blue ink")
        continue
    mean = pts.mean(axis=0)
    u, s, vt = np.linalg.svd(pts - mean, full_matrices=False)
    d = vt[0]
    proj = (pts - mean) @ d
    e1 = mean + d * proj.min(); e2 = mean + d * proj.max()
    ang = np.degrees(np.arctan2(e2[1] - e1[1], e2[0] - e1[0]))
    print(f"{name}: n={len(pts)} bbox x{int(pts[:,0].min())}..{int(pts[:,0].max())} y{int(pts[:,1].min())}..{int(pts[:,1].max())} "
          f"center ({mean[0]:.0f},{mean[1]:.0f}) axis {ang:.1f}deg endpoints ({e1[0]:.0f},{e1[1]:.0f})->({e2[0]:.0f},{e2[1]:.0f}) len {np.linalg.norm(e2-e1):.0f}")

print("\nframe HSV-blue ASCII slide x615..705 y360..460 (step x1, y3):")
for sy in range(360, 461, 3):
    row = ""
    for sx in range(615, 706):
        row += "B" if blue_ink(fpx(sx, sy)) else "."
    print(f"  y{sy}: {row}")
