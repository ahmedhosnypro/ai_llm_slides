#!/usr/bin/env python3
"""PIL forensics pass 3 — slide_047.jpg structural details."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_047.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)

red   = lambda s: (s[:,:,0] > 120) & (s[:,:,0] - s[:,:,1] > 60) & (s[:,:,0] - s[:,:,2] > 60)
dark  = lambda s: (s.sum(axis=2) < 330)
blue  = lambda s: (s[:,:,2] > 110) & (s[:,:,2] - s[:,:,0] > 50) & (s[:,:,2] - s[:,:,1] > 40)

def ascii_map(x0, x1, y0, y1, pred, step=1):
    print(f"  map x {x0}..{x1} y {y0}..{y1} ('#'=match, '.'=no):")
    for y in range(y0, y1, step):
        row = "".join("#" if pred(a[y:y+1, x:x+1])[0][0] else "." for x in range(x0, x1))
        print(f"  y={y:3d} {row}")

# --- left border structure at y=350 ---
print("-- left border slice y=350, x 50..100 --")
for x in range(50, 100):
    px = a[350, x]
    tag = "RED" if red(a[350:351, x:x+1])[0][0] else ("dk" if dark(a[350:351, x:x+1])[0][0] else "")
    if tag:
        print(f"  x={x}: {px.tolist()} {tag}")

# --- vertical strokes y-extents ---
for xc in (58, 82, 874):
    col = a[210:500, xc:xc+1]
    ys = np.nonzero(red(col)[:, 0])[0]
    if len(ys):
        print(f"col x={xc}: red y {210+ys.min()}..{210+ys.max()} n={len(ys)}")

# --- marker shapes ---
print("\n-- marker 1 map (x 88..118, y 224..244), dark<600 --")
ascii_map(88, 118, 224, 244, lambda s: s.sum(axis=2) < 600)
print("-- marker 2 map (x 88..118, y 256..272) --")
ascii_map(88, 118, 256, 272, lambda s: s.sum(axis=2) < 600)
print("-- line1 text head map (x 112..200, y 224..244) --")
ascii_map(112, 200, 224, 244, lambda s: s.sum(axis=2) < 600)

# --- legend: fill bbox + border probe ---
print("\n-- legend box probe --")
lightblue = lambda s: (s[:,:,2] > 200) & (s[:,:,0] > 150) & (s[:,:,0] < 240) & (s[:,:,2] - s[:,:,0] > 15)
sub = a[340:495, 445:575]
m = lightblue(sub)
ys, xs = np.nonzero(m)
print(f"  fill bbox x {445+xs.min()}..{445+xs.max()} y {340+ys.min()}..{340+ys.max()}")
# probe top/bottom/left/right edge pixel colors
print("  edge colors: top(y=347,x=500):", a[347, 500].tolist(), " top(y=349):", a[349, 500].tolist())
print("  bottom(y=474):", a[474, 500].tolist(), " bottom(y=476):", a[476, 500].tolist())
print("  left(y=400,x=455):", a[400, 455].tolist(), " left(x=457):", a[400, 457].tolist())
print("  right(y=400,x=565):", a[400, 565].tolist(), " right(x=567):", a[400, 567].tolist())
# any saturated red border rows near 346..352 / 472..478 in x 455..570?
for y in list(range(344, 354)) + list(range(471, 480)):
    cnt = red(a[y:y+1, 455:570]).sum()
    if cnt > 10:
        print(f"  RED row y={y}: n={cnt}")
for x in list(range(452, 462)) + list(range(562, 572)):
    cnt = red(a[348:476, x:x+1]).sum()
    if cnt > 10:
        print(f"  RED col x={x}: n={cnt}")

# legend text bands (x 460..568 only)
sub = a[350:490, 460:568]
mm = (sub.sum(axis=2) < 480)
rows = mm.sum(axis=1)
run = None
bands = []
for i, v in enumerate(rows):
    y = 350 + i
    if v > 1 and run is None: run = y
    elif v <= 1 and run is not None:
        bands.append((run, y-1)); run = None
if run is not None: bands.append((run, 489))
print("  text bands (x 460..568):", bands)
for (b0, b1) in bands:
    seg = a[b0:b1+1, 460:568]
    sm = (seg.sum(axis=2) < 480)
    ys2, xs2 = np.nonzero(sm)
    rm = red(seg); bm = blue(seg)
    ry, rx = np.nonzero(rm); by, bx = np.nonzero(bm)
    print(f"   band y {b0}..{b1}: x {460+xs2.min()}..{460+xs2.max()}"
          + (f" | red x {460+rx.min()}..{460+rx.max()} n={len(rx)}" if len(rx) else " | no-red")
          + (f" | blue x {460+bx.min()}..{460+bx.max()} n={len(bx)}" if len(bx) else ""))

# --- grid: 16 cell centers + row1/2 boundary profile ---
print("\n-- grid profile: colored rowcount y 360..490 x 560..740 --")
green = lambda s: (s[:,:,1] > 120) & (s[:,:,1] - s[:,:,0] > 40) & (s[:,:,1] - s[:,:,2] > 40)
yellow= lambda s: (s[:,:,0] > 180) & (s[:,:,1] > 170) & (s[:,:,2] < 130)
redf  = lambda s: (s[:,:,0] > 180) & (s[:,:,1] < 90) & (s[:,:,2] < 90)
cyan  = lambda s: (s[:,:,2] > 150) & (s[:,:,1] > 120) & (s[:,:,0] < 140) & (s[:,:,2] - s[:,:,0] > 60)
sub = a[355:495, 560:740]
colored = green(sub) | yellow(sub) | redf(sub) | cyan(sub)
rowcount = colored.sum(axis=1)
for i, c in enumerate(rowcount):
    y = 355 + i
    if 385 <= y <= 400 or 415 <= y <= 432 or 448 <= y <= 460:
        print(f"  y={y}: colored n={c}")

print("\n-- 16 cell samples (center px) --")
# column centers from gaps: cols at x 571..608, 611..647, 651..686, 690..726
cols = [(571+608)//2, (611+647)//2, (651+686)//2, (690+726)//2]
# rows: approximate; refine from profile
rows = [380, 408, 438, 468]
grid_vals = [[1,4,1,6],[2,3,0,9],[1,2,7,1],[4,1,0,2]]
for ri, ry in enumerate(rows):
    line = []
    for ci, cx in enumerate(cols):
        line.append(f"{grid_vals[ri][ci]}@({cx},{ry})={a[ry,cx].tolist()}")
    print("  " + "  ".join(line))

# --- eq4 structure: numerator/denominator x-ranges + bar ---
print("\n-- eq4 bands detail x 315..500 --")
sub = a[318:360, 315:500]
mm = (sub.sum(axis=2) < 480)
rows = mm.sum(axis=1)
for i, v in enumerate(rows):
    y = 318 + i
    if v > 0:
        seg = a[y:y+1, 315:500]
        sm = (seg.sum(axis=2) < 480)[0]
        xs2 = np.nonzero(sm)[0]
        # longest run
        runs = []
        s = xs2[0]; p = xs2[0]
        for g in xs2[1:]:
            if g != p+1:
                runs.append((315+s, 315+p)); s = g
            p = g
        runs.append((315+s, 315+p))
        long_runs = [r for r in runs if r[1]-r[0] > 8]
        print(f"  y={y}: n={v} runs>8px: {long_runs}")

# --- eq3: check for fraction bar (horizontal run) ---
print("\n-- eq3 rows with long horizontal runs x 315..545 --")
sub = a[280:315, 315:545]
mm = (sub.sum(axis=2) < 480)
for i in range(mm.shape[0]):
    y = 280 + i
    sm = mm[i]
    xs2 = np.nonzero(sm)[0]
    if len(xs2) == 0: continue
    runs = []
    s = xs2[0]; p = xs2[0]
    for g in xs2[1:]:
        if g != p+1:
            runs.append((315+s, 315+p)); s = g
        p = g
    runs.append((315+s, 315+p))
    long_runs = [r for r in runs if r[1]-r[0] > 10]
    if long_runs:
        print(f"  y={y}: long runs {long_runs}")

# --- title: serif check via stroke map of 'A' (x 140..180, y 68..100) ---
print("\n-- title 'A' map x 138..180 y 68..100 (red) --")
ascii_map(138, 180, 68, 100, red, step=2)

# --- arrow map ---
print("\n-- arrow map x 735..795 y 418..442 (dark<500, not red) --")
notred = lambda s: ~((s[:,:,0] > 120) & (s[:,:,0] - s[:,:,1] > 60) & (s[:,:,0] - s[:,:,2] > 60))
ascii_map(735, 795, 418, 442, lambda s: (s.sum(axis=2) < 500) & notred(s), step=1)

# --- output grid numerals positions ---
print("\n-- output grid cell rects --")
sub = a[390:460, 792:876]
colored = green(sub) | yellow(sub) | redf(sub) | cyan(sub)
ys, xs = np.nonzero(colored)
print(f"  overall x {792+xs.min()}..{792+xs.max()} y {390+ys.min()}..{390+ys.max()}")
for (lbl, (x0, y0)) in [("TL", (810, 408)), ("TR", (850, 408)), ("BL", (810, 440)), ("BR", (850, 440))]:
    print(f"  {lbl} ({x0},{y0}) =", a[y0, x0].tolist())
