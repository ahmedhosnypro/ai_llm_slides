#!/usr/bin/env python3
"""Probe 4: compare blue-ink (hlabel) placement frame vs parent render, same slide window."""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
F = np.asarray(Image.open(f"{VID}/unique_slides/slide_017.jpg").convert("RGB")).astype(np.int16)
Pa = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide043/render_2.png").convert("RGB")
P = np.asarray(Pa.resize((960, 540), Image.LANCZOS)).astype(np.int16)
AX, SX, AY, SY = 18.250, 0.96150, 1.950, 0.95500

def fpx(sx, sy):
    return F[int(round(AY + SY * sy)), int(round(AX + SX * sx))]

def ppx(sx, sy):
    return P[sy, sx]

def blue_ink(sampler, x0, x1, y0, y1):
    hits = []
    for sy in range(y0, y1):
        for sx in range(x0, x1):
            c = sampler(sx, sy)
            if c[2] > 120 and int(c[2]) - int(c[0]) > 50 and int(c[2]) - int(c[1]) > 40:
                hits.append((sx, sy))
    return np.array(hits, dtype=float) if hits else None

for name, fn in (("frame", fpx), ("parent", ppx)):
    pts = blue_ink(fn, 585, 725, 360, 455)
    if pts is None:
        print(f"{name}: NO blue ink in window")
        continue
    mean = pts.mean(axis=0)
    u, s, vt = np.linalg.svd(pts - mean, full_matrices=False)
    d = vt[0]
    proj = (pts - mean) @ d
    e1 = mean + d * proj.min(); e2 = mean + d * proj.max()
    ang = np.degrees(np.arctan2(e2[1] - e1[1], e2[0] - e1[0]))
    print(f"{name}: n={len(pts)} bbox x{int(pts[:,0].min())}..{int(pts[:,0].max())} y{int(pts[:,1].min())}..{int(pts[:,1].max())} "
          f"center ({mean[0]:.0f},{mean[1]:.0f}) axis {ang:.1f} deg endpoints ({e1[0]:.0f},{e1[1]:.0f})->({e2[0]:.0f},{e2[1]:.0f}) len {np.linalg.norm(e2-e1):.0f}")

# ASCII map of frame blue ink region (slide coords 620..665 x 370..445)
print("\nframe ASCII slide x618..668 step1, y368..448 step2 ('B'=blue):")
for sy in range(368, 449, 2):
    row = ""
    for sx in range(618, 669):
        c = fpx(sx, sy)
        if c[2] > 120 and int(c[2]) - int(c[0]) > 50 and int(c[2]) - int(c[1]) > 40:
            row += "B"
        elif int(c[0]) > 150 and int(c[1]) < 130 and int(c[2]) < 130:
            row += "r"
        else:
            row += "."
    print(f"  y{sy}: {row}")
