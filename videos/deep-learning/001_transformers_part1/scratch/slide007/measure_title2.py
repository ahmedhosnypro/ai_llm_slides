#!/usr/bin/env python3
"""Fine measurements: title line1 shift check, subtitle extent, 006 stray ink, callout box."""
from PIL import Image
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides"
a = np.asarray(Image.open(f"{BASE}/slide_006.jpg").convert("RGB")).astype(int)
b = np.asarray(Image.open(f"{BASE}/slide_007.jpg").convert("RGB")).astype(int)

def dark(img, x0, x1, y0, y1, thr=400):
    return img[y0:y1, x0:x1].sum(axis=2) < thr

def bbox(m, x0, y0):
    ys, xs = np.nonzero(m)
    if not len(ys): return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max(), int(m.sum()))

# --- title line 1: cross-correlate to find vertical shift between frames ---
# use x-extent of title only: measure x extent of dark in y59..85
m6 = dark(a, 250, 730, 55, 90); m7 = dark(b, 250, 730, 55, 90)
bb6, bb7 = bbox(m6, 250, 55), bbox(m7, 250, 55)
print("title line1 bbox 006:", bb6)
print("title line1 bbox 007:", bb7)
# per-row ink profile for shift estimate
p6 = m6.sum(axis=1); p7 = m7.sum(axis=1)
best = None
for dy in range(-8, 9):
    s = 0
    for i in range(len(p6)):
        j = i + dy
        if 0 <= j < len(p7): s += min(p6[i], p7[j])
    if best is None or s > best[1]: best = (dy, s)
print("best vertical shift of 007 vs 006 title line1 (dy, overlap):", best, " (total6, total7):", int(p6.sum()), int(p7.sum()))

# --- horizontal shift check via column profiles ---
c6 = m6.sum(axis=0); c7 = m7.sum(axis=0)
bestx = None
for dx in range(-8, 9):
    s = 0
    for i in range(len(c6)):
        j = i + dx
        if 0 <= j < len(c7): s += min(c6[i], c7[j])
    if bestx is None or s > bestx[1]: bestx = (dx, s)
print("best horizontal shift:", bestx)

# --- what is 006's ink at x430..500 y86..106? ---
w6 = dark(a, 420, 520, 86, 106, thr=450)
print("006 ink bbox in x420..520 y86..106:", bbox(w6, 420, 86))
# sample color
ys, xs = np.nonzero(w6)
if len(ys):
    px_ = a[86 + ys[0], 420 + xs[0]]
    print("sample color:", px_)

# --- subtitle '(Challenges)' isolated: x260..660, y84..115 ---
m7s = dark(b, 260, 660, 84, 115, thr=430)
print("subtitle bbox 007 (x<=660):", bbox(m7s, 260, 84))
# per-row bands of the subtitle
rows = m7s.sum(axis=1)
print("subtitle row profile y84..115:", [(84 + i, int(v)) for i, v in enumerate(rows) if v > 0])
# subtitle color: darkest pixel
win = b[84:115, 260:660]
lum = win.sum(axis=2)
iy, ix = np.unravel_index(np.argmin(lum), lum.shape)
print("subtitle darkest color:", win[iy, ix])

# --- Decoder caption in 007: x660..900 y80..120 ---
m7c = dark(b, 660, 900, 80, 120, thr=430)
print("caption bbox 007:", bbox(m7c, 660, 80))
m6c = dark(a, 660, 900, 80, 120, thr=430)
print("caption bbox 006:", bbox(m6c, 660, 80))
