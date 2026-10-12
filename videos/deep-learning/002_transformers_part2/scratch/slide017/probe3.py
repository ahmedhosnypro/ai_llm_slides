#!/usr/bin/env python3
"""Probe 3: locate K/V bar rows + pale-cell columns in the frame; swoosh ink direction."""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
F = np.asarray(Image.open(f"{VID}/unique_slides/slide_017.jpg").convert("RGB")).astype(np.int16)
AX, SX, AY, SY = 18.250, 0.96150, 1.950, 0.95500

def fpx(sx, sy):
    return F[int(round(AY + SY * sy)), int(round(AX + SX * sx))]

def hexc(c):
    return "%02X%02X%02X" % tuple(int(v) for v in c)

# 1. column scan through the K-bar zone (slide x 165..182) -> find rows where cells are pale
print("== K bar zone: rows where ANY of slide x 166..182 is pale (yellow/white) ==")
for sy in range(320, 445):
    pale = 0
    for sx in range(166, 183):
        c = fpx(sx, sy)
        if c[0] > 215 and c[1] > 200 and c[2] > 140:  # pale yellow/white/tan
            pale += 1
    if pale >= 8:
        print(f"  slide y {sy}: pale cols {pale}")

print("== V bar zone: rows where ANY of slide x 482..497 is pale ==")
for sy in range(320, 445):
    pale = 0
    for sx in range(482, 498):
        c = fpx(sx, sy)
        if c[0] > 215 and c[1] > 200 and c[2] > 140:
            pale += 1
    if pale >= 8:
        print(f"  slide y {sy}: pale cols {pale}")

# 2. horizontal profile of one K bar row + one V bar row (once rows known, use 335 guess first)
print("== frame raw frame-coord ASCII map: K bar region (frame x 165..205, y 305..345) ==")
for fy in range(305, 346, 2):
    row = ""
    for fx in range(165, 206):
        c = F[fy, fx]
        if c[0] > 225 and c[1] > 210 and c[2] > 150: row += "w"   # pale/white
        elif c[0] > 200 and c[1] > 180 and c[2] < 140: row += "y" # pale yellow
        elif c[0] > 150 and c[1] < 140 and c[2] < 140: row += "r" # red/darkred
        elif c[0] > 180 and c[1] > 150 and c[2] < 110: row += "g" # gold
        elif abs(int(c[0]) - 240) + abs(int(c[1]) - 137) + abs(int(c[2]) - 147) < 90: row += "p"  # card pink
        else: row += "."
    print(f"  fy{fy}: {row}")
print("  legend: w=pale white y=pale-yellow r=red g=gold p=card-pink .=other")

print("== V bar region frame ASCII (frame x 470..515, y 305..345) ==")
for fy in range(305, 346, 2):
    row = ""
    for fx in range(470, 516):
        c = F[fy, fx]
        if c[0] > 225 and c[1] > 210 and c[2] > 150: row += "w"
        elif c[0] > 200 and c[1] > 180 and c[2] < 140: row += "y"
        elif c[0] > 150 and c[1] < 140 and c[2] < 140: row += "r"
        elif c[0] > 180 and c[1] > 150 and c[2] < 110: row += "g"
        elif abs(int(c[0]) - 240) + abs(int(c[1]) - 137) + abs(int(c[2]) - 147) < 90: row += "p"
        else: row += "."
    print(f"  fy{fy}: {row}")

# 3. swoosh blue-ink principal direction
hits = []
for sy in range(370, 435):
    for sx in range(590, 720):
        c = fpx(sx, sy)
        if c[2] > 120 and int(c[2]) - int(c[0]) > 50 and int(c[2]) - int(c[1]) > 40:
            hits.append((sx, sy))
pts = np.array(hits, dtype=float)
if len(pts):
    mean = pts.mean(axis=0)
    u, s, vt = np.linalg.svd(pts - mean, full_matrices=False)
    d = vt[0]
    proj = (pts - mean) @ d
    e1 = mean + d * proj.min(); e2 = mean + d * proj.max()
    ang = np.degrees(np.arctan2(e2[1] - e1[1], e2[0] - e1[0]))
    print(f"== swoosh blue ink: n={len(pts)} center ({mean[0]:.0f},{mean[1]:.0f}) "
          f"axis angle {ang:.1f} deg, endpoints ({e1[0]:.0f},{e1[1]:.0f})->({e2[0]:.0f},{e2[1]:.0f}), "
          f"length {np.linalg.norm(e2-e1):.0f}")
