#!/usr/bin/env python3
"""PIL forensics on the original frame unique_slides/slide_011.jpg (960x540, 1px=1pt)."""
import numpy as np
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_011.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def bbox(mask, name):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(f"{name}: NO PIXELS")
        return None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    n = int(mask.sum())
    print(f"{name}: x[{x0},{x1}] y[{y0},{y1}] w={x1-x0+1} h={y1-y0+1} n={n}")
    return (x0, y0, x1, y1, n)

# coarse color masks with JPEG tolerance
orange = (abs(r - 247) < 25) & (abs(g - 161) < 30) & (abs(b - 99) < 35)
yellow = (r > 210) & (g > 200) & (b < 90)
lavend = (abs(r - 214) < 18) & (abs(g - 214) < 18) & (abs(b - 242) < 14)
gray   = (abs(r - 191) < 12) & (abs(g - 191) < 12) & (abs(b - 191) < 12)
beige  = (abs(r - 240) < 10) & (abs(g - 237) < 10) & (abs(b - 228) < 12)
red    = (r > 150) & (g < 90) & (b < 90)
blue   = (b > 140) & (r < 120) & (g < 120)
black  = (r < 80) & (g < 80) & (b < 80)

print("== big color regions ==")
bbox(orange, "orange block")
bbox(yellow, "yellow block")
bbox(lavend, "lavender (all)")
bbox(gray,   "gray strip")
bbox(beige,  "beige note box")

# per-row counts to find strip bounds for gray
ys, xs = np.where(gray)
if len(ys):
    import collections
    rowc = collections.Counter(ys)
    rows = sorted([y for y, c in rowc.items() if c > 200])
    print("gray rows with >200px:", rows[:5], "...", rows[-5:] if len(rows) > 5 else "")

# lavender per-row profile to separate two sub-blocks
ys, xs = np.where(lavend)
if len(ys):
    rowc = collections.Counter(ys)
    rows = sorted(rowc)
    # find contiguous row runs with >30 px
    runs = []
    s = p = None
    for y in rows:
        if rowc[y] < 30:
            continue
        if s is None:
            s = p = y
        elif y == p + 1:
            p = y
        else:
            runs.append((s, p)); s = p = y
    if s is not None:
        runs.append((s, p))
    print("lavender row runs (>=30px):", runs)
    for (rs, re) in runs:
        band = lavend[rs:re+1, :]
        xs2 = np.where(band.sum(axis=0) > 5)[0]
        print(f"  lavender run y[{rs},{re}] x[{xs2.min()},{xs2.max()}]")

# yellow: column profile
ys, xs = np.where(yellow)
if len(ys):
    rowc = collections.Counter(ys)
    rows = sorted([y for y, c in rowc.items() if c > 50])
    colc = collections.Counter(xs)
    cols = sorted([x for x, c in colc.items() if c > 20])
    print(f"yellow dense rows: {rows[0]}..{rows[-1]}, dense cols: {cols[0]}..{cols[-1]}")

# orange: column profile
ys, xs = np.where(orange)
if len(ys):
    rowc = collections.Counter(ys)
    rows = sorted([y for y, c in rowc.items() if c > 50])
    colc = collections.Counter(xs)
    cols = sorted([x for x, c in colc.items() if c > 20])
    print(f"orange dense rows: {rows[0]}..{rows[-1]}, dense cols: {cols[0]}..{cols[-1]}")

print("== red ink ==")
# red frame border vs title vs labels: row profile
ys, xs = np.where(red)
if len(ys):
    rowc = collections.Counter(ys)
    rows = sorted([y for y, c in rowc.items() if c > 15])
    print("red rows(>15px):", rows)
    colc = collections.Counter(xs)
    cols = sorted([x for x, c in colc.items() if c > 10])
    print("red cols(>10px):", cols[:20], "..." if len(cols) > 20 else "")

# title region: red ink in y<120
tit = red[:120, :]
ys, xs = np.where(tit)
if len(xs):
    print(f"red title ink: x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] n={len(xs)}")

# blue ink overall + regions
print("== blue ink ==")
ys, xs = np.where(blue)
if len(xs):
    rowc = collections.Counter(ys)
    rows = sorted([y for y, c in rowc.items() if c > 5])
    # runs
    runs = []
    s = p = None
    for y in rows:
        if s is None: s = p = y
        elif y <= p + 3: p = y
        else: runs.append((s, p)); s = p = y
    if s is not None: runs.append((s, p))
    print("blue row runs:", runs)
    for (rs, re) in runs:
        band = blue[rs:re+1, :]
        ys2, xs2 = np.where(band)
        print(f"  blue band y[{rs},{re}] x[{xs2.min()},{xs2.max()}] n={len(xs2)}")

print("== black ink ==")
ys, xs = np.where(black)
if len(xs):
    rowc = collections.Counter(ys)
    rows = sorted([y for y, c in rowc.items() if c > 4])
    runs = []
    s = p = None
    for y in rows:
        if s is None: s = p = y
        elif y <= p + 2: p = y
        else: runs.append((s, p)); s = p = y
    if s is not None: runs.append((s, p))
    print("black row runs(>4px):", runs)
    for (rs, re) in runs:
        band = black[rs:re+1, :]
        ys2, xs2 = np.where(band)
        # x runs in band
        colc = collections.Counter(xs2)
        colsr = sorted([x for x, c in colc.items() if c >= 1])
        xruns = []
        s2 = p2 = None
        for x in colsr:
            if s2 is None: s2 = p2 = x
            elif x <= p2 + 6: p2 = x
            else: xruns.append((s2, p2)); s2 = p2 = x
        if s2 is not None: xruns.append((s2, p2))
        xruns = [xr for xr in xruns if xr[1] - xr[0] >= 2]
        print(f"  black band y[{rs},{re}]: xruns={xruns[:12]}")
