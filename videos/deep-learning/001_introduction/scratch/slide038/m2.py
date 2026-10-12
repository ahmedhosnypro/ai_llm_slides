#!/usr/bin/env python3
"""Slide 038 forensics pass 2: ASCII color map + targeted ink runs."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[..., 0], a[..., 1], a[..., 2]

# ASCII map: 96 cols x 54 rows (10x10 px cells)
def cls(cell_r, cell_g, cell_b):
    rr, gg, bb = cell_r.mean(), cell_g.mean(), cell_b.mean()
    if rr > 225 and gg > 225 and bb > 225: return '.'   # white
    if abs(rr - 232) < 15 and abs(gg - 232) < 15 and abs(bb - 231) < 15: return ' '  # gray bg
    if rr > 120 and gg < 110 and bb < 110: return 'R'   # red
    if bb > 130 and bb - rr > 40 and bb - gg > 30: return 'B'  # blue
    if rr < 110 and gg < 110 and bb < 110: return '#'   # dark/black
    if rr > 140 and gg > 100 and bb < 110 and rr - bb > 60: return 'o'  # brown/tan
    if gg > 110 and gg - rr > 30 and gg - bb > 20: return 'G'  # green
    if bb > 140 and gg > 140 and rr < 140: return 'c'   # cyan
    if rr > 180 and gg > 180 and bb < 140: return 'y'   # yellow
    if rr > 90 and bb > 90 and gg < 90 and rr - gg > 30: return 'P'  # purple
    if rr > 200 and gg > 200 and bb > 140 and bb < 210: return 'l'  # light blue
    return '+'

print("ASCII map (10x10 px cells, x: 0-960 -> cols 0-95, y: 0-540 -> rows 0-53)")
hdr = '    ' + ''.join(str((i // 10) % 10) for i in range(96))
print(hdr)
for cy in range(54):
    row = ''
    for cx in range(96):
        cell = a[cy*10:(cy+1)*10, cx*10:(cx+1)*10]
        row += cls(cell[..., 0], cell[..., 1], cell[..., 2])
    print(f"{cy*10:3d} {row}")

print()
print("--- top rule y42..45 x extent ---")
rule = (r[42:46] > 120) & (g[42:46] < 120) & (b[42:46] < 120)
xs = np.nonzero(rule.sum(axis=0) >= 2)[0]
print(f"x {xs.min()}..{xs.max()} n={len(xs)}")
print("sample color at (480,43):", a[43, 480], " (58,44):", a[44, 58])

print("--- title band y70..95: ink mask + x extent + color ---")
band = slice(70, 96)
ink = (r[band] < 180) | (g[band] < 180) | (b[band] < 180)
cols = np.where(ink.sum(axis=0) > 0)[0]
print(f"x {cols.min()}..{cols.max()}")
ys = np.where(ink.sum(axis=1) > 0)[0] + 70
print(f"y {ys.min()}..{ys.max()}")
pix = a[band][ink]
print("title ink modal color:", np.median(pix, axis=0), "mean:", pix.mean(axis=0).round(0))

print("--- col x56..62 red runs y40..540 ---")
redcol = (r[:, 56:63] > 120) & (g[:, 56:63] < 110) & (b[:, 56:63] < 110)
for x in range(56, 63):
    ys = np.nonzero(redcol[:, x - 56])[0]
    if len(ys):
        runs = []
        s = p = ys[0]
        for v in ys[1:]:
            if v == p + 1: p = v
            else: runs.append((s, p)); s = p = v
        runs.append((s, p))
        big = [rn for rn in runs if rn[1] - rn[0] > 5]
        print(f"x={x} n={len(ys)} bigruns={big}")

print("--- col x180..186 red runs ---")
redcol2 = (r[:, 180:187] > 120) & (g[:, 180:187] < 110) & (b[:, 180:187] < 110)
for x in range(180, 187):
    ys = np.nonzero(redcol2[:, x - 180])[0]
    if len(ys):
        runs = []
        s = p = ys[0]
        for v in ys[1:]:
            if v == p + 1: p = v
            else: runs.append((s, p)); s = p = v
        runs.append((s, p))
        big = [rn for rn in runs if rn[1] - rn[0] > 5]
        print(f"x={x} n={len(ys)} bigruns={big}")

print("--- red blob x330..350: row runs ---")
redblob = (r[:, 330:351] > 120) & (g[:, 330:351] < 110) & (b[:, 330:351] < 110)
for y in range(60, 520):
    c = redblob[y].sum()
    if c > 8:
        print(f"y={y} n={c}")

print("--- formula line 3? rows y190..235 ink x extent (thr>60) ---")
band3 = slice(190, 236)
ink3 = ((r[band3] < 150) & (g[band3] < 150) & (b[band3] < 150)) | ((r[band3] > 120) & (g[band3] < 110) & (b[band3] < 110))
ys3 = np.where(ink3.sum(axis=1) > 3)[0] + 190
print("rows with ink:", ys3.min() if len(ys3) else None, "..", ys3.max() if len(ys3) else None)
for y in range(190, 236):
    c = ink3[y - 190].sum()
    if c > 3:
        xs = np.nonzero(ink3[y - 190])[0]
        print(f"y={y} n={c} x {xs.min()}..{xs.max()}")

print("--- black bar y518..539 x extent ---")
bar = (r[518:540] < 80) & (g[518:540] < 80) & (b[518:540] < 80)
xs = np.nonzero(bar.sum(axis=0) > 10)[0]
print(f"x {xs.min()}..{xs.max()}")

print("--- formula text lines: per-line ink bbox in box y118..233 x91..878 ---")
sub = slice(120, 232)
inkf = (r[sub] < 150) & (g[sub] < 150) & (b[sub] < 150)
for y in range(120, 232):
    c = inkf[y - 120].sum()
    if c > 8:
        xs = np.nonzero(inkf[y - 120])[0] + 91
        if xs.min() < 870:
            pass
rows_ink = np.where(inkf.sum(axis=1) > 8)[0] + 120
# group into lines
lines = []
if len(rows_ink):
    s = p = rows_ink[0]
    for v in rows_ink[1:]:
        if v <= p + 3: p = v
        else: lines.append((s, p)); s = p = v
    lines.append((s, p))
for (s, e) in lines:
    m = inkf[s - 120:e - 120 + 1]
    xs = np.nonzero(m.sum(axis=0) > 0)[0] + 91
    print(f"line y {s}..{e} x {xs.min()}..{xs.max()}")
