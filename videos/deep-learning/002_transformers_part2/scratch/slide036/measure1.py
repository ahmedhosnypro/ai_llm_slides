#!/usr/bin/env python3
"""Stage 1 measurement for slide 036: chrome landmark fit + big rectangles + color census.
Frame: videos/deep-learning/002_transformers_part2/unique_slides/slide_036.jpg (960x540, 1px=1pt on frame).
Canonical slide chrome (slide pts): panel border left col 42, right col ~918/919, top row 45,
bottom red stroke rows 538-539, badge center (893,71) d36.
"""
import numpy as np
from PIL import Image

FRAME = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_036.jpg"
im = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"frame {W}x{H}")
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# red mask (borders / title / labels)
red = (r > 120) & (g < 110) & (b < 110)
# gray panel
gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
# badge yellow (FDFD96-ish)
yel = (r > 200) & (g > 200) & (b < 190)

# --- chrome landmarks ---
# left/right red border columns at mid height (use rows 250..300 median of red col extents)
mid = slice(250, 300)
colred = red[mid].sum(axis=0)
cols = np.where(colred > 20)[0]
print("red cols in mid band:", cols[:8], "...", cols[-8:] if len(cols) > 8 else "")
# top red border row: search rows 0..120 for a wide red row
rowred_wide = [(y, int(red[y].sum())) for y in range(0, 130)]
wide_rows = [y for y, s in rowred_wide if s > 300]
print("top wide red rows (0..130):", wide_rows[:6])
# bottom red stroke rows
bot_rows = [(y, int(red[y].sum())) for y in range(H - 60, H)]
print("bottom rows red counts (last 60):", [(y, s) for y, s in bot_rows if s > 50])
# badge yellow bbox in top right
win = np.s_[0:130, 780:960]
ys, xs = np.where(yel[win])
if len(ys):
    print(f"badge yellow bbox: x {xs.min()+780}..{xs.max()+780}  y {ys.min()}..{ys.max()}",
          f"center ({(xs.min()+xs.max())/2+780},{(ys.min()+ys.max())/2})")
# purple ring pixels near badge
pur = (b > 150) & (r > 70) & (r < 180) & (g < 130)
ys, xs = np.where(pur[0:130, 780:960])
if len(ys):
    print(f"purple ring bbox: x {xs.min()+780}..{xs.max()+780}  y {ys.min()}..{ys.max()} count {len(ys)}")
# gray panel extent
band = gray[130:500]
gcols = np.where(band.sum(axis=0) > (500 - 130) * 0.5)[0]
print("gray cols extent:", gcols.min(), gcols.max())
gband = gray[:, 60:120]
grows = np.where(gband.sum(axis=1) > 40)[0]
print("gray rows extent (left band):", grows.min(), grows.max())

# --- big content rectangles (non-gray, non-white regions inside panel) ---
# white canvas is 255-ish; panel gray 233; find cream (FFFFE6-ish) region
cream = (r > 240) & (g > 240) & (b > 200) & (b < 245)
ys, xs = np.where(cream)
if len(ys):
    print(f"cream-ish bbox: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()} count {len(ys)}")
# navy banner (000080-ish): dark blue
navy = (r < 60) & (g < 60) & (b > 90) & (b < 170)
ys, xs = np.where(navy)
if len(ys):
    print(f"navy bbox: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()} count {len(ys)}")
    # separate banner row band from token-cell blues by row histogram
    rows = np.bincount(ys, minlength=H)
    big = [y for y in range(H) if rows[y] > 100]
    print("navy rows with >100 px:", big[:5], "...", big[-5:] if len(big) > 5 else "")

# --- color census of saturated ink (for measured-color law) ---
sat = (np.max(im, axis=2) - np.min(im, axis=2)) > 60
ys, xs = np.where(sat)
cols_ink = im[ys, xs]
# bucket by coarse color
def cname(px):
    rr, gg, bb = px
    if rr > 150 and gg < 90 and bb < 90: return "red"
    if rr < 90 and gg < 90 and bb > 120: return "blue"
    if rr < 90 and gg < 90 and 60 <= bb <= 120: return "navy"
    if rr > 200 and gg > 200 and bb < 150: return "yellow"
    if rr > 200 and gg < 190 and bb > 140: return "pink"
    if rr < 120 and gg > 120 and bb < 120: return "green"
    return None
from collections import Counter
cnt = Counter()
core = {}
for (yy, xx) in zip(ys[::7], xs[::7]):
    n = cname(im[yy, xx])
    if n:
        cnt[n] += 1
        core.setdefault(n, []).append(tuple(im[yy, xx]))
for n, c in cnt.most_common():
    arr = np.array(core[n])
    print(f"{n}: {c} px, median {np.median(arr, axis=0)}, p10 {np.percentile(arr, 10, axis=0)}, p90 {np.percentile(arr, 90, axis=0)}")
