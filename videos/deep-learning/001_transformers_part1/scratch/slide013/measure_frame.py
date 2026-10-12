#!/usr/bin/env python3
"""Measure slide_013.jpg (960x540, 1px = 1pt): panel, border, badge, title ink bbox."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_013.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"frame size: {W}x{H}")
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# ---- panel gray extent (sample rows clear of title/badge) ----
gray = (abs(r - 233) < 18) & (abs(g - 233) < 18) & (abs(b - 231) < 20)
rows_probe = slice(120, 200)  # above title, below badge zone mostly
cols = np.where(gray[rows_probe].sum(axis=0) > 60)[0]
print(f"panel gray cols (probe rows 120-200): {cols.min()}..{cols.max()}")
col_probe = slice(60, 130)
rows = np.where(gray[:, col_probe].sum(axis=1) > 55)[0]
print(f"panel gray rows (probe cols 60-130): {rows.min()}..{rows.max()} (H={H})")

# ---- red border strokes ----
red = (r > 120) & (g < 110) & (b < 110)
# left border: columns 30..60
for name, sl in [("left", np.s_[:, 30:60]), ("right", np.s_[:, 900:935]), ("top", np.s_[35:60, 300:600])]:
    ys, xs = np.where(red[sl])
    if len(ys):
        print(f"red {name} stroke rows {sl[0] if isinstance(sl, tuple) else ''}: count={len(ys)}")
# left border column mean
lc = np.where(red[:, :60].sum(axis=0) > 100)[0]
rc = np.where(red[:, 900:].sum(axis=0) > 100)[0]
print(f"left border cols: {lc.tolist()}  right border cols(+900): {(rc + 900).tolist()}")
tr = np.where(red[:60, 300:600].sum(axis=1) > 100)[0]
print(f"top border rows: {tr.tolist()}")
br = np.where(red[520:, 300:600].sum(axis=1) > 100)[0]
print(f"bottom border rows(+520): {(br + 520).tolist()}")

# ---- badge: yellow disc near top-right ----
yel = (r > 200) & (g > 200) & (b < 190)
ys, xs = np.where(yel[:200, 750:])
if len(ys):
    print(f"badge yellow bbox: x {xs.min()+750}..{xs.max()+750}, y {ys.min()}..{ys.max()} "
          f"(center {(xs.min()+xs.max())/2+750:.1f},{(ys.min()+ys.max())/2:.1f}, "
          f"d={xs.max()-xs.min()+1}x{ys.max()-ys.min()+1})")
pur = (b > 150) & (r > 70) & (r < 190) & (g < 140)
pys, pxs = np.where(pur[:220, 750:])
if len(pys):
    print(f"badge purple ring bbox: x {pxs.min()+750}..{pxs.max()+750}, y {pys.min()}..{pys.max()}")

# ---- badge numeral ink (dark pixels inside badge) ----
dark = (r < 120) & (g < 120) & (b < 120)
ys, xs = np.where(dark[40:105, 860:925])
if len(ys):
    print(f"numeral ink bbox: x {xs.min()+860}..{xs.max()+860}, y {ys.min()+40}..{ys.max()+40}")

# ---- title red ink (search middle region, excluding borders) ----
tred = red.copy()
tred[:100, :] = False  # exclude badge ring zone top
tred[:, :60] = False
tred[:, 900:] = False
tred[520:, :] = False
ys, xs = np.where(tred)
if len(ys):
    print(f"TITLE red ink bbox: x {xs.min()}..{xs.max()} (w={xs.max()-xs.min()+1}), "
          f"y {ys.min()}..{ys.max()} (h={ys.max()-ys.min()+1})")
    print(f"  center: ({(xs.min()+xs.max())/2:.1f},{(ys.min()+ys.max())/2:.1f})")
    # per-column extent to find baseline vs descender: histogram of ink rows
    rowcount = tred.sum(axis=1)
    nz = np.where(rowcount > 0)[0]
    # find rows with dense ink (cap region) vs sparse (descender)
    dense = np.where(rowcount > 30)[0]
    print(f"  dense rows (>30 red px): {dense.min()}..{dense.max()}")
    sparse_rows = [int(x) for x in nz if rowcount[x] <= 30]
    print(f"  sparse ink rows (descender tails): {sparse_rows[:5]}..{sparse_rows[-5:]}")

# ---- gray cursor artifact (spec says ~67% width ~53% height -> ~(643,286)) ----
cgray = (abs(r - 136) < 60) & (abs(g - 136) < 60) & (abs(b - 136) < 60) & (abs(r - g) < 12) & (abs(g - b) < 12)
ys, xs = np.where(cgray[260:320, 600:700])
if len(ys):
    print(f"cursor artifact ink bbox: x {xs.min()+600}..{xs.max()+600}, y {ys.min()+260}..{ys.max()+260} (NOT recreated)")

# ---- any other ink outside panel/badge/title? scan for non-white, non-gray, non-red clusters ----
white = (r > 235) & (g > 235) & (b > 235)
other = ~white & ~gray & ~red & ~yel & ~cgray
# ignore border rows/cols and badge box and title box and numeral
other[:60, :] = False; other[520:, :] = False
other[:, :60] = False; other[:, 900:] = False
other[40:105, 855:930] = False
ys, xs = np.where(other)
if len(ys):
    print(f"unaccounted ink px: {len(ys)}; bbox x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()}")
    # cluster summary
    import collections
    buckets = collections.Counter(((y // 40) * 40, (x // 40) * 40) for y, x in zip(ys[::7], xs[::7]))
    print("  top clusters (y,x)->samplecount:", buckets.most_common(8))
else:
    print("no unaccounted ink outside panel/badge/title zones")
