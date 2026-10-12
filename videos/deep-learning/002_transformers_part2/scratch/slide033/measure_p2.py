#!/usr/bin/env python3
"""slide033 measurement pass 2: tight windows per element."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)
SX = lambda fx: (fx - 18.63) / 0.96123
SY = lambda fy: fy / 0.95556

def band(y0, y1, x0, x1, label):
    print(f"  {label}: frame[{x0},{y0}..{x1},{y1}] slide x[{SX(x0):.1f}..{SX(x1):.1f}] y[{SY(y0):.1f}..{SY(y1):.1f}] w={SX(x1)-SX(x0):.1f} h={SY(y1)-SY(y0):.1f}")

def corecolor(y0, y1, x0, x1, n=40):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    lum = reg.sum(axis=1)
    idx = np.argsort(lum)[:max(n, 1)]
    return tuple(int(v) for v in np.median(reg[idx], axis=0))

def colhist(y0, y1, x0, x1):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    out = {}
    for nm, c in [("C00000", (192, 0, 0)), ("8B0000", (139, 0, 0)), ("0000CC", (0, 0, 204)),
                  ("000080", (0, 0, 128)), ("00B050", (0, 176, 80)), ("7030A0", (112, 48, 160)),
                  ("ED7D31", (237, 125, 49)), ("0070C0", (0, 112, 192)), ("black", (0, 0, 0)),
                  ("BF8F00", (191, 143, 0)), ("FFC000", (255, 192, 0))]:
        d = np.abs(reg - np.array(c)).sum(axis=1)
        out[nm] = int((d < 120).sum())
    return {k: v for k, v in out.items() if v > 0}

def rowbands(y0, y1, x0, x1, dark=150, gap=4, minpx=2):
    reg = a[y0:y1, x0:x1]
    dk = (reg.sum(axis=2) < dark * 3)
    prof = dk.sum(axis=1)
    rows = prof >= minpx
    bands = []; s = None; last = None
    for i, v in enumerate(rows):
        if v:
            if s is None: s = i
            last = i
        else:
            if s is not None and i - last > gap:
                bands.append((s + y0, last + y0)); s = None
    if s is not None: bands.append((s + y0, last + y0))
    return bands

def colruns(y0, y1, x0, x1, dark=150, gap=3):
    reg = a[y0:y1, x0:x1]
    dk = (reg.sum(axis=2) < dark * 3)
    prof = dk.sum(axis=0)
    cols = prof >= 1
    runs = []; s = None; last = None
    for i, v in enumerate(cols):
        if v:
            if s is None: s = i
            last = i
        else:
            if s is not None and i - last > gap:
                runs.append((s + x0, last + x0)); s = None
    if s is not None: runs.append((s + x0, last + x0))
    return runs

print("=== SUBTITLE (badge excluded) ===")
for (y0, y1) in rowbands(66, 96, 100, 848, dark=140):
    r = colruns(y0, y1, 100, 848, dark=140)
    print(f"  y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]), colhist(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "subtitle")

print("=== PAIR BOX text ===")
for (y0, y1) in rowbands(127, 208, 96, 182, dark=160):
    r = colruns(y0, y1, 96, 182, dark=160)
    print(f"  y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]), colhist(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "pairline")

print("=== INFO BOX fill/border/text ===")
reg = a[218:330, 58:222]
grn = (reg[:, :, 1] > reg[:, :, 0] + 8) & (reg[:, :, 1] > 225) & (reg[:, :, 2] > reg[:, :, 0])
ys, xs = np.where(grn)
y0i, y1i, x0i, x1i = ys.min() + 218, ys.max() + 218, xs.min() + 58, xs.max() + 58
band(y0i, y1i, x0i, x1i, "info fill")
print("  fill median:", tuple(int(v) for v in np.median(a[y0i+5:y1i-5, x0i+5:x0i+30].reshape(-1,3), axis=0)))
print("  border core top:", corecolor(y0i-6, y0i, x0i, x1i, 30), " hist:", colhist(y0i-6, y0i, x0i, x1i))
for (y0, y1) in rowbands(y0i + 2, y1i - 1, x0i + 3, x1i - 2, dark=160):
    r = colruns(y0, y1, x0i, x1i, dark=160)
    print(f"  y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "infoline")
    regl = a[y0:y1+1, r[0][0]:r[-1][1]+1]
    redm = (regl[:, :, 0] > 140) & (regl[:, :, 1] < 100) & (regl[:, :, 2] < 100)
    if redm.sum() > 2:
        cys, cxs = np.where(redm)
        print(f"    RED x {cxs.min()+r[0][0]}..{cxs.max()+r[0][0]} core", corecolor(y0, y1, cxs.min()+r[0][0], cxs.max()+r[0][0], 12))

print("=== VECTOR PAIRS label + column ===")
for (y0, y1) in rowbands(90, 126, 205, 268, dark=165):
    r = colruns(y0, y1, 205, 268, dark=165)
    print(f"  y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]), colhist(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "vplabel")
def fillruns(x_lo, x_hi, y_lo=108, y_hi=522):
    runs = []; cur = None
    for y in range(y_lo, y_hi):
        med = tuple(np.median(a[y, x_lo:x_hi], axis=0))
        r, g, b = med
        if abs(r - 165) < 35 and g > 195 and abs(b - 178) < 45: t = "GREEN"
        elif r > 210 and g > 200 and 130 < b < 205: t = "KHAKI"
        else: t = None
        if t != (cur[0] if cur else None):
            if cur and cur[0]: runs.append((cur[1], y - 1, cur[0]))
            cur = (t, y)
    if cur and cur[0]: runs.append((cur[1], y_hi - 1, cur[0]))
    return [r for r in runs if r[1] - r[0] > 5]
for (y0, y1, t) in fillruns(226, 249):
    print(f"  col box {t} y {y0}..{y1}", end=" ")
    band(y0, y1, 219, 258, "")
    print("    fill med:", tuple(int(v) for v in np.median(a[y0+6:y1-6, 230:245].reshape(-1,3), axis=0)))
    tb = rowbands(y0, y1, 219, 258, dark=120, gap=5, minpx=2)
    for (ty0, ty1) in tb:
        rr = colruns(ty0, ty1, 219, 258, dark=120)
        print(f"    value y{ty0}..{ty1} x{rr[0][0]}..{rr[-1][1]} core", corecolor(ty0, ty1, rr[0][0], rr[-1][1]))

print("=== INDEX label + strip ===")
for (y0, y1) in rowbands(88, 122, 258, 320, dark=165):
    r = colruns(y0, y1, 258, 320, dark=165)
    print(f"  label y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]), colhist(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "idxlabel")
reg = a[100:520, 258:315]
cream = (np.abs(reg[:, :, 0] - 251) < 12) & (np.abs(reg[:, :, 1] - 253) < 10) & (np.abs(reg[:, :, 2] - 232) < 16)
ys, xs = np.where(cream)
y0s, y1s, x0s, x1s = ys.min() + 100, ys.max() + 100, xs.min() + 258, xs.max() + 258
band(y0s, y1s, x0s, x1s, "index strip")
print("  strip fill med:", tuple(int(v) for v in np.median(a[y0s+5:y1s-5, x0s+5:x0s+20].reshape(-1,3), axis=0)))
print("  strip border core:", corecolor(y0s-6, y0s, x0s, x1s, 30), colhist(y0s-6, y0s, x0s, x1s))
for (y0, y1) in rowbands(y0s + 1, y1s - 1, x0s + 1, x1s + 1, dark=175, gap=4, minpx=1):
    r = colruns(y0, y1, x0s - 2, x1s + 2, dark=175)
    if not r: continue
    print(f"  num y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]), colhist(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "idxnum")

print("=== SIN/COS boxes fills ===")
for (y0, y1, t) in fillruns(335, 392):
    print(f"  sc box {t} y {y0}..{y1}", end=" ")
    band(y0, y1, 322, 405, "")
    print("    fill med:", tuple(int(v) for v in np.median(a[y0+8:y1-8, 340:385].reshape(-1,3), axis=0)))
row = a[160, 300:420]
nb = np.where(np.abs(row - np.array([233, 233, 231])).sum(axis=1) > 40)[0] + 300
print("  box1 x extent y160:", nb.min(), nb.max())
row = a[400, 300:420]
nb = np.where(np.abs(row - np.array([233, 233, 231])).sum(axis=1) > 40)[0] + 300
print("  box4 x extent y400:", nb.min(), nb.max())
print("=== SIN/COS box text ===")
for (by0, by1, nm) in [(122, 190, "b1"), (188, 256, "b2"), (255, 325, "b3"), (345, 420, "b4"), (445, 515, "b5")]:
    for (y0, y1) in rowbands(by0, by1, 322, 410, dark=145, gap=4, minpx=2):
        r = colruns(y0, y1, 322, 410, dark=145)
        print(f"  {nm} y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]), colhist(y0, y1, r[0][0], r[-1][1]))
        band(y0, y1, r[0][0], r[-1][1], nm)

print("=== BRACKETS + dx1 ===")
for (x_lo, x_hi, nm) in [(305, 322, "LEFT"), (406, 424, "RIGHT")]:
    reg = a[110:520, x_lo:x_hi]
    redm = (reg[:, :, 0] > 135) & (reg[:, :, 1] < 100) & (reg[:, :, 2] < 100)
    ys, xs = np.where(redm)
    if len(ys):
        print(f"  {nm} red stroke x {xs.min()+x_lo}..{xs.max()+x_lo} y {ys.min()+110}..{ys.max()+110} core", corecolor(ys.min()+110, ys.max()+110, xs.min()+x_lo, xs.max()+x_lo, 60))
        band(ys.min() + 110, ys.max() + 110, xs.min() + x_lo, xs.max() + x_lo, nm)
        # horizontal feet?
        prof_r = redm.sum(axis=1)
        fw = np.where(prof_r > 6)[0]
        print(f"    rows with stroke width>6: {[int(v)+110 for v in fw[:6]]}...{[int(v)+110 for v in fw[-6:]] if len(fw)>6 else ''}")
for (y0, y1) in rowbands(488, 518, 420, 470, dark=155):
    r = colruns(y0, y1, 420, 470, dark=155)
    print(f"  dx1 y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]), colhist(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "dx1")
