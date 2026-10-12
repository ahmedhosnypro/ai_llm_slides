#!/usr/bin/env python3
"""Pass A: global red/orange/structural forensics on slide_048.jpg (960x540, 1px=1pt)."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

red = (r > 120) & (g < 110) & (b < 110)
orange = (r > 150) & (g > 80) & (g < 180) & (b < 90)

print("== red row profile (rows with >=5 red px), grouped runs ==")
rows = np.where(red.sum(axis=1) >= 5)[0]
def runs(idx, gap=2):
    out = []; s = p = None
    for i in idx:
        if s is None: s = p = i
        elif i <= p + gap: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return out
for s, e in runs(rows):
    band = red[s:e+1]
    cols = np.where(band.sum(axis=0) > 0)[0]
    print(f"rows {s}..{e} (h={e-s+1}) redcount={band.sum()} cols {cols.min()}..{cols.max()}")

print("== orange row runs ==")
orows = np.where(orange.sum(axis=1) >= 5)[0]
for s, e in runs(orows):
    band = orange[s:e+1]
    cols = np.where(band.sum(axis=0) > 0)[0]
    print(f"rows {s}..{e} (h={e-s+1}) count={band.sum()} cols {cols.min()}..{cols.max()}")

# Yellow (Flatten tag): strong yellow
yel = (r > 200) & (g > 200) & (b < 120)
print("== yellow row runs ==")
yrows = np.where(yel.sum(axis=1) >= 4)[0]
for s, e in runs(yrows):
    band = yel[s:e+1]
    cols = np.where(band.sum(axis=0) > 0)[0]
    print(f"rows {s}..{e} (h={e-s+1}) count={band.sum()} cols {cols.min()}..{cols.max()}")

# Blue-ish (labels border 2222CC, dots 0000CD, Non Linearity)
blu = (b > 120) & (b - r > 50) & (b - g > 40)
print("== blue row runs ==")
brows = np.where(blu.sum(axis=1) >= 4)[0]
for s, e in runs(brows):
    band = blu[s:e+1]
    cols = np.where(band.sum(axis=0) > 0)[0]
    print(f"rows {s}..{e} (h={e-s+1}) count={band.sum()} cols {cols.min()}..{cols.max()}")

# Black bottom strip check
dark = (r < 60) & (g < 60) & (b < 60)
print("== dark rows (>=200 dark px) ==")
drows = np.where(dark.sum(axis=1) >= 200)[0]
for s, e in runs(drows):
    band = dark[s:e+1]
    cols = np.where(band.sum(axis=0) > 100)[0]
    print(f"rows {s}..{e} count={band.sum()} strongcols {cols.min() if len(cols) else '-'}..{cols.max() if len(cols) else '-'}")
