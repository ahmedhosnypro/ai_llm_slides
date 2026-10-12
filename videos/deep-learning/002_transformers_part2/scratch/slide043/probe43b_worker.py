#!/usr/bin/env python3
"""Slide 043 probe B: arrows below/right of block, left-stack right region map,
text-run black clusters, borders via luminance dips, pencil census."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

print("=== A. h-arrow below right block (y305..345, x630..830) ===")
# washed red: r > g, r > b, r>150, saturation moderate
wash = (r > 150) & (r - g > 25) & (r - b > 15) & (g < 180)
sub = wash[305:345, 630:830]
ys, xs = np.where(sub)
if len(xs):
    print("washed-red bbox: x", xs.min()+630, "..", xs.max()+630, " y", ys.min()+305, "..", ys.max()+305, " n=", len(xs))
for y in range(308, 342):
    n = wash[y, 630:830].sum()
    if n > 3:
        xs2 = np.where(wash[y, 630:830])[0]
        print(f"  y{y}: n={n} x {xs2.min()+630}..{xs2.max()+630}")
print("--- 'Channels' label hunt y335..365 (red cores) ---")
redc = (r > 130) & (r - g > 50) & (r - b > 40) & (g < b + 35)
for y in range(335, 368):
    n = redc[y, 630:830].sum()
    if n > 2:
        xs2 = np.where(redc[y, 630:830])[0]
        print(f"  y{y}: n={n} x {xs2.min()+630}..{xs2.max()+630}")

print("=== B. diagonal arrow + label (x790..915, y225..410) ===")
sub = wash[225:410, 790:915]
ys, xs = np.where(sub)
print("washed bbox: x", xs.min()+790, "..", xs.max()+790, " y", ys.min()+225, "..", ys.max()+225, " n=", len(xs))
# shaft trace: for each y, the wash pixels
for y in range(228, 400, 4):
    xs2 = np.where(wash[y, 790:915])[0]
    if len(xs2):
        print(f"  y{y}: x {xs2.min()+790}..{xs2.max()+790} n={len(xs2)}")

print("=== C. left-stack right region color map (rows 150,180,210,240,270,300 col runs) ===")
def rowruns(y, x0, x1, tol=40):
    out, start = [], x0
    prev = a[y, x0]
    for x in range(x0+1, x1):
        cur = a[y, x]
        if abs(int(cur[0])-int(prev[0])) + abs(int(cur[1])-int(prev[1])) + abs(int(cur[2])-int(prev[2])) > tol:
            out.append((start, x-1, f"#{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}"))
            start = x
        prev = cur
    out.append((start, x1-1, f"#{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}"))
    return [(s, e, c) for s, e, c in out if e-s >= 2]
for y in [150, 165, 180, 210, 240, 270, 300, 330]:
    print(f"y={y}:", rowruns(y, 100, 340))

print("=== D. left stack: top-face band map (cols 150,190,230,270,305) ===")
def colruns(x, y0, y1, tol=40):
    out, start = [], y0
    prev = a[y0, x]
    for y in range(y0+1, y1):
        cur = a[y, x]
        if abs(int(cur[0])-int(prev[0])) + abs(int(cur[1])-int(prev[1])) + abs(int(cur[2])-int(prev[2])) > tol:
            out.append((start, y-1, f"#{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}"))
            start = y
        prev = cur
    out.append((start, y1-1, f"#{prev[0]:02X}{prev[1]:02X}{prev[2]:02X}"))
    return [(s, e, c) for s, e, c in out if e-s >= 2]
for x in [150, 190, 230, 270, 305]:
    print(f"x={x}:", colruns(x, 95, 345))

print("=== E. C-L3 black clusters (y222..237, x340..620) ===")
dark = (r < 110) & (g < 110) & (b < 110)
cols = dark[222:238, 340:620].sum(axis=0)
clusters = []
in_c = False
for i, v in enumerate(cols):
    if v > 0 and not in_c: s = i; in_c = True
    elif v == 0 and in_c:
        clusters.append((340+s, 340+i-1, int(cols[s:i].sum()))); in_c = False
if in_c: clusters.append((340+s, 619, int(cols[s:].sum())))
print("black clusters:", clusters)
print("--- blue clusters same window ---")
blue = (b - r > 40) & (b - g > 20) & (b > 80)
cols = blue[222:238, 340:620].sum(axis=0)
clusters = []
in_c = False
for i, v in enumerate(cols):
    if v > 0 and not in_c: s = i; in_c = True
    elif v == 0 and in_c:
        clusters.append((340+s, 340+i-1, int(cols[s:i].sum()))); in_c = False
print("blue clusters:", [c for c in clusters if c[2] > 5])

print("=== F. B-L2 black clusters (y431..449, x600..820) ===")
cols = dark[431:450, 600:820].sum(axis=0)
clusters = []
in_c = False
for i, v in enumerate(cols):
    if v > 0 and not in_c: s = i; in_c = True
    elif v == 0 and in_c:
        if cols[s:i].sum() > 3: clusters.append((600+s, 600+i-1, int(cols[s:i].sum())))
        in_c = False
print("B-L2 black clusters:", clusters)
print("--- B-L2 blue extent ---")
cols = blue[431:450, 90:820].sum(axis=0)
nz = [90+i for i, v in enumerate(cols) if v > 0]
print("B-L2 blue x:", nz[0], "..", nz[-1])
print("--- B-L3 red extent + black clusters (y474..492) ---")
redc2 = (r > 130) & (r - g > 50) & (r - b > 40) & (g < b + 35)
cols = redc2[474:493, 90:860].sum(axis=0)
nz = [90+i for i, v in enumerate(cols) if v > 0]
print("B-L3 red x:", nz[0], "..", nz[-1])
cols = dark[474:493, 90:860].sum(axis=0)
clusters = []
in_c = False
for i, v in enumerate(cols):
    if v > 0 and not in_c: s = i; in_c = True
    elif v == 0 and in_c:
        if cols[s:i].sum() > 3: clusters.append((90+s, 90+i-1, int(cols[s:i].sum())))
        in_c = False
print("B-L3 black clusters:", clusters)

print("=== G. callout border via luminance dips (rows/cols) ===")
lum = (r + g + b) / 3
# horizontal borders: rows where many cols in x340..635 dip below 200
for y in range(165, 275):
    dips = (lum[y, 340:635] < 205).sum()
    if dips > 200: print(f"  callout h-border row y{y}: dips={dips}")
for x in range(325, 655):
    dips = (lum[175:262, x] < 205).sum()
    if dips > 50: print(f"  callout v-border col x{x}: dips={dips}")
print("--- callout border color samples ---")
for (y, x) in [(172, 400), (264, 400), (200, 332), (200, 643), (200, 644), (200, 645)]:
    print(f"  ({x},{y}) #{a[y,x,0]:02X}{a[y,x,1]:02X}{a[y,x,2]:02X}", end="")
print()
print("--- bottom box green border color ---")
for (y, x) in [(358, 400), (497, 400), (400, 73), (400, 877)]:
    print(f"  ({x},{y}) #{a[y,x,0]:02X}{a[y,x,1]:02X}{a[y,x,2]:02X}", end="")
print()

print("=== H. pencil icon dense census (x345..405, y230..262) ===")
sub = a[230:262, 345:405]
nonbg = (np.abs(sub[:, :, 0] - 250) + np.abs(sub[:, :, 1] - 251) + np.abs(sub[:, :, 2] - 235)) > 100
ys, xs = np.where(nonbg)
print("ink n=", len(xs))
from collections import Counter
cc = Counter()
for i in range(len(xs)):
    px = tuple((sub[ys[i], xs[i]] // 40) * 40)
    cc[px] += 1
print("quantized colors:", cc.most_common(10))
# icon shape: per-row extent
for y in range(230, 262, 2):
    xs2 = np.where(nonbg[y-230])[0]
    if len(xs2): print(f"  y{y}: x {xs2.min()+345}..{xs2.max()+345} n={len(xs2)}")

print("=== I. v-arrow heads: ink profile at x638..665, y165..320 (washed) ===")
for y in range(165, 320, 3):
    xs2 = np.where(wash[y, 638:666])[0]
    if len(xs2): print(f"  y{y}: x {xs2.min()+638}..{xs2.max()+638} n={len(xs2)}")

print("=== J. left stack: front grid row/col runs strict magenta ===")
mag = (r > 110) & (g < 60) & (b > 110) & (b - g > 80) & (r - g > 90)
for x in [120, 160, 195]:
    colv = mag[:, x]
    runs = []
    cur = False
    for y in range(150, 350):
        if colv[y] and not cur: start = y; cur = True
        elif not colv[y] and cur: runs.append((start, y-1)); cur = False
    if cur: runs.append((start, 349))
    print(f"x={x} magenta row-runs:", runs)
for y in [200, 260, 320]:
    rowv = mag[y, :]
    runs = []
    cur = False
    for x in range(100, 240):
        if rowv[x] and not cur: start = x; cur = True
        elif not rowv[x] and cur: runs.append((start, x-1)); cur = False
    if cur: runs.append((start, 239))
    print(f"y={y} magenta col-runs:", runs)
