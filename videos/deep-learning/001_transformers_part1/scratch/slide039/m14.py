#!/usr/bin/env python3
"""m14.py — follow-up PIL: Y2 label hunt, sticker/Y-label core hex, mesh line color."""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
org = np.asarray(Image.open(BASE + "unique_slides/slide_039.jpg").convert("RGB")).astype(int)
out = []

def blumask(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (B > 100) & (B - R > 25) & (B - G > 18)

# 1. Y2 hunt: expect near (505-545, 125-160); scan wider with lower threshold
for (x0, x1, y0, y1, tag) in [(495, 550, 120, 165, "Y2 window"), (460, 500, 135, 160, "Y1 window"), (630, 660, 100, 125, "Y4 window")]:
    reg = org[y0:y1, x0:x1]
    m = blumask(reg)
    out.append(f"{tag} x[{x0},{x1}] y[{y0},{y1}]: blue_px={m.sum()}")
    if m.sum() > 8:
        ys, xs = np.where(m)
        out.append(f"   blue bbox x[{xs.min()+x0},{xs.max()+x0}] y[{ys.min()+y0},{ys.max()+y0}]")

# core hex of the big blue labels (darkest 25% of blue px)
reg = org[108:160, 470:580]
m = blumask(reg)
if m.sum():
    px = reg[m]
    s = px.sum(axis=1)
    idx = np.argsort(s)[: max(5, int(len(s) * 0.25))]
    out.append(f"Y-label core hex (darkest quartile avg): #{''.join(f'{v:02X}' for v in px[idx].mean(axis=0).round(0).astype(int))}")

# 2. sticker text core hex (unrotated)
cy, cx = 477, 790
patch = org[420:535, 680:905]
im = Image.fromarray(patch.astype(np.uint8)).rotate(-18.43, resample=Image.BICUBIC, center=(cx - 680, cy - 420), fillcolor=(255, 255, 255))
u = np.asarray(im).astype(int)
ym = (u[..., 0] > 200) & (u[..., 1] > 200) & (u[..., 2] < 140)
ys, xs = np.where(ym)
y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
band = u[y0:y1 + 1, x0:x1 + 1]
R, G, B = band[..., 0], band[..., 1], band[..., 2]
bluecore = (B - R > 35) & (B > 110)
if bluecore.sum() > 5:
    px = band[bluecore]
    s = px.sum(axis=1)
    idx = np.argsort(s)[: max(5, int(len(s) * 0.3))]
    out.append(f"sticker blue-core px={bluecore.sum()} darkest-30% avg: #{''.join(f'{v:02X}' for v in px[idx].mean(axis=0).round(0).astype(int))}")
# where does blue ink sit horizontally inside the sticker (text extent)?
bm = blumask(band)
cols = bm.sum(axis=0)
nz = np.where(cols > 0)[0]
if len(nz):
    out.append(f"sticker blue ink col extent: x[{nz.min()+x0+680},{nz.max()+x0+680}] (sticker x[{x0+680},{x1+680}])")

# 3. mesh line color between dots (DOTS from build): sample midpoints of pairs
DOTS = [[318, 299], [307, 327], [293, 355], [281, 385], [311, 313], [299, 341], [286, 369], [303, 369]]
def sample_line(p, q):
    xs = np.linspace(p[0], q[0], 40).round().astype(int)
    ys = np.linspace(p[1], q[1], 40).round().astype(int)
    px = org[ys, xs]
    dark = px.sum(axis=1) < 560
    if dark.sum() > 3:
        return px[dark].mean(axis=0).round(0), int(dark.sum())
    return None, int(dark.sum())
for (a, b) in [(0, 4), (1, 5), (0, 1), (2, 6)]:
    avg, n = sample_line(DOTS[a], DOTS[b])
    out.append(f"mesh {DOTS[a]}->{DOTS[b]}: dark_px={n} avg={avg}")

# 4. Y1..Y4 red arrows bboxes for label placement (red mask above boxes)
def redmask(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (R > 120) & (R - G > 55) & (R - B > 55)
for i in range(4):
    xc = 486 + 73 * i
    reg = org[100 + 27 * (3 - i) if False else 120:240, xc - 20:xc + 20]
    m = redmask(reg)
    if m.sum() > 5:
        ys, xs = np.where(m)
        out.append(f"Y{i+1} arrow red bbox: x[{xs.min()+xc-20},{xs.max()+xc-20}] y[{ys.min()+120},{ys.max()+120}] px={m.sum()}")

print("\n".join(out))
