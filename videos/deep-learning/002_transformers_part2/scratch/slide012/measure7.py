#!/usr/bin/env python3
# measure7.py — cell grids + tall braces + y-text colors, fast
from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

print("=== H1 modal color grid (fx 245..393 step 7, fy 155..345 step 9) ===")
for y in range(155, 346, 9):
    row = []
    for x in range(245, 394, 7):
        px_ = a[y:y+2, x:x+2].reshape(-1, 3)
        m = np.median(px_, axis=0).astype(int)
        rr, gg, bb = m
        if rr > 244 and gg > 244 and bb > 244: c = '.'   # white
        elif abs(rr-206)<25 and gg>235 and abs(bb-227)<25: c = 'g'  # panel green
        elif rr>240 and gg>245 and bb<225: c = 'y'  # pale yellow cell
        elif rr<120 and gg<80: c = 'R'  # deep red ink
        elif rr>140 and gg<95 and bb<95: c = 'r'
        elif bb>140 and bb-rr>40: c = 'B'
        elif rr>150 and gg<90 and bb>150: c = 'M'
        elif rr>120 and gg<110 and bb>120: c = 'm'
        elif rr<90 and gg<90 and bb<90: c = 'k'
        else: c = '?'
        row.append(c)
    print(f"fy {y:3d} " + "".join(row))

print("\n=== tall braces: deep-red vertical strokes in gaps fy 130..345 ===")
br = (r > 140) & (g < 95) & (b < 95)
for x0, x1, nm in [(394, 412, "gap12"), (560, 572, "gap23"), (720, 745, "right")]:
    sub = br[125:348, x0:x1]
    ys, xs = np.where(sub)
    if len(ys) > 10:
        print(f"{nm}: fx {xs.min()+x0}..{xs.max()+x0} fy {ys.min()+125}..{ys.max()+125} n={len(ys)}")
        # column histogram
        import collections
        cnt = collections.Counter(xs + x0)
        print("   col counts:", sorted(cnt.items()))

print("\n=== y-box text colors: sample glyph pixels per strip ===")
def glyph_colors(x0, x1, y0, y1):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    ink = (sub.max(axis=1) - sub.min(axis=1) > 60) | (sub.max(axis=1) < 150)
    if ink.sum() == 0: return None
    return tuple(int(v) for v in np.median(sub[ink], axis=0)), int(ink.sum())
print("strip1 y1 (257..286):", glyph_colors(260, 284, 364, 378))
print("strip1 y2 (293..316):", glyph_colors(295, 314, 364, 378))
print("strip2 y1 (420..446):", glyph_colors(423, 444, 364, 378))
print("strip3 y1 (582..606):", glyph_colors(585, 604, 364, 378))
print("strip3 y2 (619..641):", glyph_colors(622, 639, 364, 378))

print("\n=== H2 cells: modal grid (fx 411..559) — cols of cell rims ===")
# find colored vertical strokes (rims) inside H2 across fy 165..330
rim = (np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b) > 50)
colc = rim[165:330, 411:559].sum(axis=0)
cols = [(x + 411, int(colc[x])) for x in range(148) if colc[x] > 40]
print("H2 rim-heavy cols:", cols)
rowc = rim[165:330, 411:559].sum(axis=1)
rows = [(y + 165, int(rowc[y])) for y in range(165) if rowc[y] > 40]
print("H2 rim-heavy rows:", rows)

print("\n=== H2 grid: white cell boxes via >235 in fy 160..340 ===")
white = (r > 235) & (g > 235) & (b > 235)
sub = white[160:340, 411:559]
rowc = sub.sum(axis=1)
bands = []
for i, n in enumerate(rowc):
    y = i + 160
    if n > 20:
        if bands and y - bands[-1][1] <= 4: bands[-1] = (bands[-1][0], y)
        else: bands.append((y, y))
print("H2 white row bands:", bands)
if bands:
    y0, y1 = bands[0]
    colc = white[y0:y1+1, 411:559].sum(axis=0)
    xs = [x + 411 for x in range(148) if colc[x] > (y1-y0)//2]
    groups = []
    if xs:
        s = xs[0]; prev = xs[0]
        for x in xs[1:]:
            if x - prev > 3: groups.append((s, prev)); s = x
            prev = x
        groups.append((s, prev))
    print("H2 row1 cell col groups:", groups)
