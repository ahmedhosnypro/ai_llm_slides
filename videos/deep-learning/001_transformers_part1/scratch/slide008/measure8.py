#!/usr/bin/env python3
"""Pass 8: wait-box underline re-check; italic slant test on (Challenges) + callout line 1."""
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
im = Image.open(BASE + "unique_slides/slide_008.jpg").convert("RGB")
ld = im.load()

def blueink(p):
    r, g, b = p
    return b > 110 and b - r > 40 and g < 140

# 1. wait1 "Wait" column band x 100..140, rows 258..296: full profile
print("wait1 'Wait' band (x100..140) rows:")
for y in range(258, 296):
    n = sum(1 for x in range(100, 141) if blueink(ld[x, y]))
    print(f"  y={y}: n={n}")
print("wait2 'Wait' band (x260..300) rows:")
for y in range(256, 294):
    n = sum(1 for x in range(260, 301) if blueink(ld[x, y]))
    print(f"  y={y}: n={n}")

# 2. italic slant test on '(Challenges)': per-row COM over the full word
pts = []
for y in range(88, 112):
    xs = [x for x in range(370, 540) if blueink(ld[x, y])]
    if len(xs) > 3:
        pts.append((y, sum(xs) / len(xs)))
print("challenges per-row COM:", [(y, round(c, 1)) for y, c in pts])
if len(pts) > 4:
    n = len(pts)
    my = sum(p[0] for p in pts) / n
    mx = sum(p[1] for p in pts) / n
    num = sum((p[0] - my) * (p[1] - mx) for p in pts)
    den = sum((p[0] - my) ** 2 for p in pts)
    slope = num / den  # px shift per row, positive = top leans right = italic
    print(f"challenges COM slope: {slope:.3f} px/row (italic ~ +0.2..0.3, upright ~ 0)")

# 3. same test on a single stem: 'T' of Till in wait1 line2? better: 'P' stem x~? use wait1 line2 word 'Processing'
# find leftmost stem columns: line2 ink x 64..173. take x 64..90 rows 276..290
pts2 = []
for y in range(276, 291):
    xs = [x for x in range(64, 96) if blueink(ld[x, y])]
    if xs:
        pts2.append((y, sum(xs) / len(xs)))
print("wait1 'Till' region per-row COM:", [(y, round(c, 1)) for y, c in pts2])

# 4. callout line1 per-row COM (x 77..293) rows 183..197
pts3 = []
for y in range(183, 198):
    xs = [x for x in range(70, 300) if blueink(ld[x, y])]
    if len(xs) > 5:
        pts3.append((y, sum(xs) / len(xs)))
print("callout line1 per-row COM:", [(y, round(c, 1)) for y, c in pts3])
