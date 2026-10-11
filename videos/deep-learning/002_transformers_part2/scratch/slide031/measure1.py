#!/usr/bin/env python3
"""Measure slide_031.jpg structure (960x540, 1px = 1pt)."""
import numpy as np
from PIL import Image

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(img).astype(int)
H, W, _ = a.shape
print(f"size {W}x{H}")

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def runs(mask_1d, minlen=2):
    out = []
    i = 0
    n = len(mask_1d)
    while i < n:
        if mask_1d[i]:
            j = i
            while j < n and mask_1d[j]:
                j += 1
            if j - i >= minlen:
                out.append((i, j - 1))
            i = j
        else:
            i += 1
    return out

# --- strong color masks ---
red = (R > 150) & (G < 100) & (B < 100)                # FF0000-ish / C00000
blue = (B > 120) & (R < 100) & (G < 100)               # 0000CC
black = (R < 70) & (G < 70) & (B < 70)
# green fill (CCFFCC) and yellow fills
mintfill = (R > 180) & (G > 240) & (B > 180) & (R < 230) & (B < 230)
yel = (R > 200) & (G > 200) & (B < 180)
white = (R > 235) & (G > 235) & (B > 235)

# footer black bar rows: rows where black spans nearly full width
blackrow = black.sum(axis=1)
fr = np.where(blackrow > 700)[0]
print("full-width black rows:", runs(blackrow > 700, 1)[:5], "..." if len(fr) > 5 else "")

# gray chrome panel rows (E9E9E7-ish)
gray = (np.abs(R - 0xE9) < 12) & (np.abs(G - 0xE9) < 12) & (np.abs(B - 0xE7) < 12)
grow = gray.sum(axis=1)
print("gray rows>500:", runs(grow > 500, 2)[:4])

# chrome red border rows/cols (panel border) — red spanning wide
redrow = red.sum(axis=1); redcol = red.sum(axis=0)
print("red rows>600:", runs(redrow > 600, 2)[:4])
print("red cols>250:", runs(redcol > 250, 2)[:8])

# badge circle: FDFD96-ish fill near (893,71)
byel = (R > 235) & (G > 235) & (B > 120) & (B < 190)
sub = byel[40:105, 850:935]
rr, cc = np.where(sub)
if len(rr):
    print(f"badge fill bbox x{850+cc.min()}..{850+cc.max()} y{40+rr.min()}..{40+rr.max()}")

# --- top band panels ---
# scan rows 30..240 for panel borders: red verticals inside x<750, blue verticals
print("\n--- vertical red strokes rows 30..250 (cols with many red px) ---")
redsub = red[30:250, :]
rc = redsub.sum(axis=0)
print("cols red count>60:", [(c, int(rc[c])) for c in np.where(rc > 60)[0]][:20])
print("\n--- vertical blue strokes rows 30..250 ---")
bluesub = blue[30:250, :]
bc = bluesub.sum(axis=0)
print("cols blue count>60:", [(c, int(bc[c])) for c in np.where(bc > 60)[0]][:20])

# horizontal borders in top band: rows where red or blue count high in x 50..720
print("\n--- horizontal strokes (red) x50..720 rows 30..260 ---")
for (y0, y1) in runs((red[:, 50:720] > 0).sum(axis=1) > 200, 1):
    print(f"  y{y0}..{y1} redcount={(red[y0:y1+1,50:720]>0).sum()}")
print("--- horizontal strokes (blue) x50..940 rows 30..260 ---")
for (y0, y1) in runs((blue[:, 50:940] > 0).sum(axis=1) > 150, 1):
    print(f"  y{y0}..{y1} bluecount={(blue[y0:y1+1,50:940]>0).sum()}")

# mint fill bbox and yellow panel fill bbox
for name, m in [("mint", mintfill), ("yellow-panel", yel)]:
    ys, xs = np.where(m)
    if len(ys):
        print(f"{name} fill bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} count={len(ys)}")
