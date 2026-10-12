#!/usr/bin/env python3
"""Definitive faint-line analysis: luminance profiles along rays and axis lines.
Detects dashed/dotted structure (run/gap periodicity) the color masks missed."""
import numpy as np, math, json
from PIL import Image

im = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg"
).convert("RGB")).astype(int)
H, W, _ = im.shape
lum = im.sum(axis=2) / 3.0
CX, CY = 577.2, 284.0

def profile_radial(a_deg, r0, r1, step=1):
    """min-luminance in 3x3 at each radius along ray."""
    out = []
    for rad in range(r0, r1, step):
        x = CX + rad * math.cos(math.radians(a_deg))
        y = CY - rad * math.sin(math.radians(a_deg))
        xi, yi = int(round(x)), int(round(y))
        if not (1 <= xi < W-1 and 1 <= yi < H-1): break
        patch = lum[yi-1:yi+2, xi-1:xi+2]
        out.append((rad, float(patch.min()), float(patch.mean())))
    return out

print("== RAY PROFILES (r 132..300): count of dip samples (<212), longest run, mean dip lum ==")
for k in range(12):
    a = k * 30
    prof = profile_radial(a, 132, 300)
    dips = [p for p in prof if p[1] < 212]
    # runs of consecutive dipped radii
    runs, cur = [], []
    for p in prof:
        if p[1] < 212: cur.append(p[0])
        else:
            if cur: runs.append((cur[0], cur[-1])); cur = []
    if cur: runs.append((cur[0], cur[-1]))
    dl = [p[1] for p in dips]
    print(f"a={a:3d}: dips={len(dips):3d}/{len(prof)} runs={runs[:6]} dipLum[min,mean]={min(dl) if dl else '-'} {round(sum(dl)/len(dl),1) if dl else '-'}")

# skip known ink zones for chips/labels/heads: also profile at OFFSET angles (+/-8 deg) as control
print("\n== CONTROL: same rays +10 deg ==")
for k in range(12):
    a = k * 30 + 10
    prof = profile_radial(a, 132, 300)
    dips = [p for p in prof if p[1] < 212]
    print(f"a={a:3d}: dips={len(dips):3d}/{len(prof)}")

# axis lines: luminance along y=283/284 (x 260..885) and x=577 (y 100..505)
print("\n== H-LINE y=283..284 dip runs (lum<215) x 260..885 ==")
row = np.minimum(lum[283, :], lum[284, :])
seg = row[260:886]
dip = seg < 215
runs, cur = [], None
for i, v in enumerate(dip):
    if v and cur is None: cur = i
    if not v and cur is not None: runs.append((cur+260, i-1+260)); cur = None
if cur is not None: runs.append((cur+260, len(dip)-1+260))
print("runs:", runs[:40])
print("nruns", len(runs), "total dip px", int(dip.sum()))

print("\n== V-LINE x=576..578 dip runs (lum<215) y 105..505 ==")
col = np.minimum(np.minimum(lum[:, 576], lum[:, 577]), lum[:, 578])
seg = col[105:506]
dip = seg < 215
runs, cur = [], None
for i, v in enumerate(dip):
    if v and cur is None: cur = i
    if not v and cur is not None: runs.append((cur+105, i-1+105)); cur = None
if cur is not None: runs.append((cur+105, len(dip)-1+105))
print("runs:", runs[:40])
print("nruns", len(runs), "total dip px", int(dip.sum()))
