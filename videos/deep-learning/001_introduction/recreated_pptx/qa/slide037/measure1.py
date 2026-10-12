#!/usr/bin/env python3
"""Measure slide_037.jpg (960x540, 1px=1pt) — full structural measurement."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_037.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"size {W}x{H}")

def runs(mask, min_gap=2):
    """Return list of (start,end) runs of True along axis 0 of 1-D mask."""
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return []
    out = []
    s = p = idx[0]
    for v in idx[1:]:
        if v - p > min_gap:
            out.append((s, p))
            s = v
        p = v
    out.append((s, p))
    return out

# ---- row profile of "non-chrome" ink: anything far from white/gray panel
# classify rows: white FFFFFF, panel gray E9E9E7
def near(c, target, tol):
    return (np.abs(c - np.array(target)).sum(axis=-1) <= tol)

# Title band: rows 0..~130 gray E8E8E8-ish + red title ink
print("\n== chrome bands (samples) ==")
for y in [2, 20, 44, 46, 60, 100, 120, 125, 130, 135, 140, 200, 240, 250, 255, 258, 262, 300, 500, 510, 515, 520, 530, 538]:
    row = a[y]
    # count colors
    white = near(row, (255, 255, 255), 30).sum()
    gray = near(row, (233, 233, 231), 18).sum()
    red = near(row, (192, 0, 0), 90).sum()
    print(f"y={y}: white={white} gray={gray} red={red} sample@x500={tuple(row[500])} sample@x20={tuple(row[20])} sample@x950={tuple(row[950])}")

# ---- title ink: red text on gray band
print("\n== title ==")
band = a[40:140]
redmask = (band[:, :, 0] > 120) & (band[:, :, 1] < 100) & (band[:, :, 2] < 100)
rows = redmask.sum(axis=1)
print("red rows (y, count):", [(y + 40, int(c)) for y, c in enumerate(rows) if c > 3])
ys = np.where(rows > 3)[0]
if len(ys):
    y0, y1 = ys[0] + 40, ys[-1] + 40
    cols = redmask[ys[0]:ys[-1] + 1].sum(axis=0)
    xs = np.where(cols > 0)[0]
    print(f"title ink bbox x{xs[0]}..{xs[-1]} y{y0}..{y1}")
    # modal color of title ink
    px = band[redmask]
    from collections import Counter
    cc = Counter(map(tuple, px))
    print("modal title colors:", cc.most_common(3))

# ---- pale-yellow box
print("\n== pale-yellow box ==")
ymask = near(a, (255, 255, 225), 40)
rows = ymask.sum(axis=1)
cand = [(y, int(c)) for y, c in enumerate(rows) if c > 400]
print("yellow rows:", cand[:5], "...", cand[-5:] if len(cand) > 5 else "")
ys = [y for y, c in cand]
if ys:
    y0, y1 = ys[0], ys[-1]
    cols = ymask[y0:y1 + 1].sum(axis=0)
    xs = np.where(cols > (y1 - y0) * 0.5)[0]
    print(f"yellow box x{xs[0]}..{xs[-1]} y{y0}..{y1}")
    print("modal yellow:", Counter(map(tuple, a[y0:y1+1][ymask[y0:y1+1]])).most_common(2))

# ---- body text ink inside yellow box
print("\n== body text lines ==")
if ys:
    y0, y1 = ys[0], ys[-1]
    sub = a[y0:y1 + 1]
    ink = (sub.sum(axis=-1) < 400)  # dark ink
    rprof = ink.sum(axis=1)
    for s, e in runs(rprof > 2, min_gap=4):
        band_ink = ink[s:e + 1]
        xs2 = np.where(band_ink.sum(axis=0) > 0)[0]
        print(f"line y{y0+s}..{y0+e}  h={e-s+1}  x{xs2[0]}..{xs2[-1]}")
    # red ink inside yellow box (the bold red 'same location')
    redm = (sub[:, :, 0] > 120) & (sub[:, :, 1] < 110) & (sub[:, :, 2] < 110)
    rp = redm.sum(axis=1)
    for s, e in runs(rp > 1, min_gap=6):
        xs3 = np.where(redm[s:e + 1].sum(axis=0) > 0)[0]
        print(f"red span y{y0+s}..{y0+e} x{xs3[0]}..{xs3[-1]}")

# ---- white panel (diagram) with red border
print("\n== diagram panel ==")
redline = near(a, (192, 0, 0), 110) & (a[:, :, 0] > 130) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
# long horizontal red rows below the yellow box
rsum = redline[:, 100:860].sum(axis=1)
print("long red rows (count>400):", [(y, int(c)) for y, c in enumerate(rsum) if c > 400])
csum = redline[270:510, :].sum(axis=0)
print("long red cols in panel band (count>100):", [(x, int(c)) for x, c in enumerate(csum) if c > 100][:40])
