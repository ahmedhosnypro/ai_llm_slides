#!/usr/bin/env python3
"""Probe 2: sample frame AND parent render on the SLIDE coordinate grid.
frame = A + s*slide (fit: AX=18.25 SX=0.96150 AY=1.95 SY=0.95500).
Prints parallel color runs so child/parent geometry is directly comparable."""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
Fr = Image.open(f"{VID}/unique_slides/slide_017.jpg").convert("RGB")
Pa = Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide043/render_2.png"
).convert("RGB")
F = np.asarray(Fr).astype(np.int16)
P = np.asarray(Pa.resize((960, 540), Image.LANCZOS)).astype(np.int16)
AX, SX, AY, SY = 18.250, 0.96150, 1.950, 0.95500

def sample(img, sx, sy):
    if img is F:
        fx, fy = AX + SX * sx, AY + SY * sy
    else:
        fx, fy = float(sx), float(sy)
    x, y = int(round(fx)), int(round(fy))
    if 0 <= y < img.shape[0] and 0 <= x < img.shape[1]:
        return img[y, x]
    return np.array([255, 0, 255])

def runs(img, sy, sx0, sx1, tol=30, minrun=1):
    out, cur = [], None
    for sx in range(sx0, sx1):
        c = sample(img, sx, sy)
        if cur and abs(int(c[0])-cur[1][0]) + abs(int(c[1])-cur[1][1]) + abs(int(c[2])-cur[1][2]) <= tol:
            cur[2] = sx
        else:
            if cur and cur[2] - cur[0] >= minrun:
                out.append((cur[0], cur[2], "%02X%02X%02X" % tuple(int(v) for v in cur[1])))
            cur = [sx, tuple(int(v) for v in c), sx]
    if cur:
        out.append((cur[0], cur[2], "%02X%02X%02X" % tuple(int(v) for v in cur[1])))
    return out

def show(label, img, sy, sx0, sx1):
    rr = runs(img, sy, sx0, sx1)
    print(f"  {label:6s} y{sy}: " + " | ".join(f"{a}-{b}:{h}" for a, b, h in rr))

print("== ff_left rows x88..200 ==")
for sy in (335, 363, 391, 419):
    show("frame", F, sy, 88, 200)
    show("parent", P, sy, 88, 200)
    print()

print("== ff_right rows x425..615 ==")
for sy in (335, 363, 391, 419):
    show("frame", F, sy, 425, 615)
    show("parent", P, sy, 425, 615)
    print()

print("== gold panel vertical extent (sample slide column x=137 / x=521) ==")
for sx in (137, 521):
    ys = []
    for sy in range(280, 470):
        c = sample(F, sx, sy)
        # gold F5CC50-ish OR yellow-green D2E455-ish
        g = abs(c[0]-245) + abs(c[1]-204) + abs(c[2]-80)
        yg = abs(c[0]-210) + abs(c[1]-228) + abs(c[2]-85)
        if min(g, yg) < 90:
            ys.append(sy)
    print(f"  slide x={sx}: gold/yellowgreen rows {min(ys) if ys else '-'}..{max(ys) if ys else '-'} (n={len(ys)})")

print("== swoosh label zone (blue ink 0033CC-ish) x560..760, y380..420 ==")
hits = []
for sy in range(378, 425):
    for sx in range(555, 770):
        c = sample(F, sx, sy)
        if c[2] > 120 and c[2] - int(c[0]) > 50 and c[2] - int(c[1]) > 40:
            hits.append((sx, sy))
if hits:
    xs = [h[0] for h in hits]; ys = [h[1] for h in hits]
    print(f"  blue ink bbox slide: x {min(xs)}..{max(xs)} y {min(ys)}..{max(ys)} n={len(hits)}")
else:
    print("  no blue ink found")
