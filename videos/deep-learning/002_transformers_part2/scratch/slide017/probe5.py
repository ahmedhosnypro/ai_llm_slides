#!/usr/bin/env python3
"""Probe 5: strict-blue (0033CC-like) ink comparison, frame vs parent, slide window."""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
F = np.asarray(Image.open(f"{VID}/unique_slides/slide_017.jpg").convert("RGB")).astype(np.int16)
P = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide043/render_2.png"
).convert("RGB").resize((960, 540), Image.LANCZOS)).astype(np.int16)
AX, SX, AY, SY = 18.250, 0.96150, 1.950, 0.95500

def fpx(sx, sy):
    return F[int(round(AY + SY * sy)), int(round(AX + SX * sx))]

def strict_blue(c):
    r, g, b = int(c[0]), int(c[1]), int(c[2])
    return b > 140 and b - r > 80 and b - g > 60

def ink(sampler, x0, x1, y0, y1):
    hits = []
    for sy in range(y0, y1):
        for sx in range(x0, x1):
            if strict_blue(sampler(sx, sy)):
                hits.append((sx, sy))
    return np.array(hits, dtype=float) if hits else None

for name, fn in (("frame", fpx), ("parent", lambda sx, sy: P[sy, sx])):
    pts = ink(fn, 560, 760, 340, 470)
    if pts is None:
        print(f"{name}: no strict-blue ink")
        continue
    mean = pts.mean(axis=0)
    u, s, vt = np.linalg.svd(pts - mean, full_matrices=False)
    d = vt[0]
    proj = (pts - mean) @ d
    e1 = mean + d * proj.min(); e2 = mean + d * proj.max()
    ang = np.degrees(np.arctan2(e2[1] - e1[1], e2[0] - e1[0]))
    print(f"{name}: n={len(pts)} bbox x{int(pts[:,0].min())}..{int(pts[:,0].max())} y{int(pts[:,1].min())}..{int(pts[:,1].max())} "
          f"center ({mean[0]:.0f},{mean[1]:.0f}) axis {ang:.1f}deg endpoints ({e1[0]:.0f},{e1[1]:.0f})->({e2[0]:.0f},{e2[1]:.0f}) len {np.linalg.norm(e2-e1):.0f}")

print("\nframe strict-blue ASCII slide x600..760 y340..470 (step x1,y3):")
for sy in range(340, 471, 3):
    row = ""
    for sx in range(600, 761):
        row += "B" if strict_blue(fpx(sx, sy)) else "."
    print(f"  y{sy}: {row}")

print("\nparent strict-blue ASCII slide x600..760 y340..470 (step x1,y3):")
for sy in range(340, 471, 3):
    row = ""
    for sx in range(600, 761):
        row += "B" if strict_blue(P[sy, sx]) else "."
    print(f"  y{sy}: {row}")
