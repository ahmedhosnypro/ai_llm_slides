#!/usr/bin/env python3
"""slide033 measurement pass 3: text-free fill samples, borders, remaining boxes."""
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

def fillmed(y0, y1, x0, x1):
    return tuple(int(v) for v in np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0))

print("=== PAIR BOX text lines (gap=2) ===")
for (y0, y1) in rowbands(127, 209, 96, 182, dark=185, gap=2, minpx=1):
    r = colruns(y0, y1, 96, 182, dark=185)
    if not r: continue
    print(f"  y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1], 20))
    band(y0, y1, r[0][0], r[-1][1], "pairline")

print("=== INFO box fill (text-free) ===")
print("  fill strip y285..298 x75..200:", fillmed(285, 298, 75, 200))
print("  border rows probe x100..200:")
for y in range(219, 232):
    print(f"    y{y}", tuple(a[y, 140]), tuple(a[y, 90]))
print("  border cols probe y270..290:")
for x in range(60, 70): print(f"    x{x}", tuple(a[280, x]), end="")
print()
for x in range(208, 218): print(f"    x{x}", tuple(a[280, x]), end="")
print()

print("=== VECTOR col fills (text-free strips) ===")
for (nm, sy0, sy1) in [("box0", 166, 180), ("box1", 231, 246), ("box2", 297, 312), ("boxK", 392, 406), ("boxd2", 497, 506)]:
    print(f"  {nm} fill y{sy0}..{sy1} x228..246:", fillmed(sy0, sy1, 228, 246))
# borders of box0: probe around y126 and y183 at x 235..245
print("  box0 top/bottom border probe x238:")
for y in list(range(120, 130)) + list(range(178, 188)):
    print(f"    y{y}", tuple(a[y, 238]))
print("  box0 left/right border probe y150:")
for x in list(range(216, 226)) + list(range(248, 258)):
    print(f"    x{x}", tuple(a[150, x]), end="")
print()

print("=== SIN/COS boxes: fill via left margin x326..332, borders ===")
# find box vertical extents via fill at margin
margin = a[110:520, 326:333]
ismar = (np.abs(margin - np.array([233, 233, 231])).sum(axis=2) > 40).any(axis=1)
runs = []; s = None
for i, v in enumerate(ismar):
    if v and s is None: s = i
    elif not v and s is not None:
        if i - s > 8: runs.append((s + 110, i - 1 + 110))
        s = None
if s is not None: runs.append((s + 110, 519))
print("  box y-runs at margin:", runs)
for (y0, y1) in runs:
    print(f"    box y{y0}..{y1}", end=" ")
    band(y0, y1, 322, 405, "")
    print("      fill med (x340..390, text-free rows):", fillmed(y0 + 4, y0 + 12, 340, 390), fillmed(y1 - 12, y1 - 4, 340, 390))
print("  box borders: probe y135 x322..326 & x400..406:")
for x in list(range(320, 328)) + list(range(400, 408)): print(f"    x{x}", tuple(a[135, x]), end="")
print()
print("=== SIN/COS box text ===")
for (by0, by1, nm) in [(122, 190, "b1"), (188, 258, "b2"), (255, 325, "b3"), (345, 425, "b4"), (445, 515, "b5")]:
    for (y0, y1) in rowbands(by0, by1, 324, 405, dark=150, gap=3, minpx=2):
        r = colruns(y0, y1, 324, 405, dark=150)
        if not r: continue
        print(f"  {nm} y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1], 25))
        band(y0, y1, r[0][0], r[-1][1], nm)

print("=== BRACKETS + dx1 ===")
for (x_lo, x_hi, nm) in [(303, 322, "LEFT"), (406, 424, "RIGHT")]:
    reg = a[110:520, x_lo:x_hi]
    redm = (reg[:, :, 0] > 135) & (reg[:, :, 1] < 100) & (reg[:, :, 2] < 100)
    ys, xs = np.where(redm)
    if len(ys):
        print(f"  {nm} stroke x {xs.min()+x_lo}..{xs.max()+x_lo} y {ys.min()+110}..{ys.max()+110} core", corecolor(ys.min()+110, ys.max()+110, xs.min()+x_lo, xs.max()+x_lo, 60))
        band(ys.min() + 110, ys.max() + 110, xs.min() + x_lo, xs.max() + x_lo, nm)
        prof_r = redm.sum(axis=1)
        fw = np.where(prof_r > 5)[0]
        if len(fw): print(f"    wide rows (feet?): {int(fw.min())+110}..{int(fw.max())+110}, n={len(fw)}")
for (y0, y1) in rowbands(486, 520, 420, 472, dark=160):
    r = colruns(y0, y1, 420, 472, dark=160)
    if not r: continue
    print(f"  dx1 y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1], 20))
    band(y0, y1, r[0][0], r[-1][1], "dx1")

print("=== DEFS BOX ===")
reg = a[92:300, 420:775]
cream = (np.abs(reg[:, :, 0] - 251) < 12) & (np.abs(reg[:, :, 1] - 253) < 10) & (np.abs(reg[:, :, 2] - 232) < 16)
ys, xs = np.where(cream)
y0d, y1d, x0d, x1d = ys.min() + 92, ys.max() + 92, xs.min() + 420, xs.max() + 420
band(y0d, y1d, x0d, x1d, "defs fill")
print("  fill med:", fillmed(y0d + 8, y0d + 20, x0d + 10, x0d + 60))
print("  border probe y97..104 @x500:")
for y in range(95, 106): print(f"    y{y}", tuple(a[y, 500]))
print("  border probe left/right @y200:")
for x in list(range(422, 432)) + list(range(756, 766)): print(f"    x{x}", tuple(a[200, x]), end="")
print()
ltb = rowbands(y0d + 2, y1d - 1, x0d + 2, x1d - 1, dark=155, gap=4, minpx=2)
print(f"  {len(ltb)} line bands:")
for (y0, y1) in ltb:
    r = colruns(y0, y1, x0d, x1d, dark=155, gap=8)
    print(f"    y{y0}..{y1} x{r[0][0]}..{r[-1][1]}", end=" ")
    band(y0, y1, r[0][0], r[-1][1], "")
    for (rx0, rx1) in r:
        c = corecolor(y0, y1 + 1, rx0, rx1 + 1, 10)
        print(f"      run x{rx0}..{rx1} core {c}")

print("=== EXAMPLE BOX ===")
reg = a[92:300, 770:900]
cream = (np.abs(reg[:, :, 0] - 251) < 12) & (np.abs(reg[:, :, 1] - 253) < 10) & (np.abs(reg[:, :, 2] - 232) < 16)
ys, xs = np.where(cream)
y0e, y1e, x0e, x1e = ys.min() + 92, ys.max() + 92, xs.min() + 770, xs.max() + 92 + 0
x1e = xs.max() + 770
band(y0e, y1e, x0e, x1e, "example fill")
print("  border probe top @x820:")
for y in range(95, 106): print(f"    y{y}", tuple(a[y, 820]))
etb = rowbands(y0e + 2, y1e - 1, x0e + 2, x1e - 1, dark=155, gap=4, minpx=1)
print(f"  {len(etb)} line bands:")
for (y0, y1) in etb:
    r = colruns(y0, y1, x0e, x1e, dark=155, gap=8)
    if not r: continue
    print(f"    y{y0}..{y1} x{r[0][0]}..{r[-1][1]}", end=" ")
    band(y0, y1, r[0][0], r[-1][1], "")
    for (rx0, rx1) in r:
        c = corecolor(y0, y1 + 1, rx0, rx1 + 1, 10)
        print(f"      run x{rx0}..{rx1} core {c}")

print("=== BLUE BOX ===")
reg = a[288:520, 465:890]
ltb2 = (np.abs(reg[:, :, 0] - 233) < 13) & (np.abs(reg[:, :, 1] - 252) < 11) & (np.abs(reg[:, :, 2] - 247) < 13)
ys, xs = np.where(ltb2)
y0b, y1b, x0b, x1b = ys.min() + 288, ys.max() + 288, xs.min() + 465, xs.max() + 465
band(y0b, y1b, x0b, x1b, "blue fill")
print("  fill med:", fillmed(y0b + 10, y0b + 22, x0b + 10, x0b + 80))
print("  border probe top @x600:")
for y in range(290, 302): print(f"    y{y}", tuple(a[y, 600]))
print("  border probe left/right @y420:")
for x in list(range(468, 478)) + list(range(872, 884)): print(f"    x{x}", tuple(a[420, x]), end="")
print()
btb = rowbands(y0b + 2, y1b - 1, x0b + 2, x1b - 1, dark=155, gap=4, minpx=2)
print(f"  {len(btb)} line bands:")
for (y0, y1) in btb:
    r = colruns(y0, y1, x0b, x1b, dark=155, gap=8)
    if not r: continue
    print(f"    y{y0}..{y1} x{r[0][0]}..{r[-1][1]}", end=" ")
    band(y0, y1, r[0][0], r[-1][1], "")
    for (rx0, rx1) in r:
        c = corecolor(y0, y1 + 1, rx0, rx1 + 1, 10)
        print(f"      run x{rx0}..{rx1} core {c}")

print("=== WHITE EQ SUBBOX + EQUATION ===")
reg = a[335:410, 695:885]
wh = (reg[:, :, 0] > 242) & (reg[:, :, 1] > 242) & (reg[:, :, 2] > 242)
ys, xs = np.where(wh)
y0w, y1w, x0w, x1w = ys.min() + 335, ys.max() + 335, xs.min() + 695, xs.max() + 695
band(y0w, y1w, x0w, x1w, "white subbox")
print("  border probe top @x780:")
for y in range(340, 352): print(f"    y{y}", tuple(a[y, 780]))
# equation ink
reg2 = a[y0w + 2:y1w - 1, x0w + 2:x1w - 1]
dk = reg2.sum(axis=2) < 580
ys, xs = np.where(dk)
print(f"  eq ink frame x {xs.min()+x0w+2}..{xs.max()+x0w+2} y {ys.min()+y0w+2}..{ys.max()+y0w+2}")
band(ys.min() + y0w + 2, ys.max() + y0w + 2, xs.min() + x0w + 2, xs.max() + x0w + 2, "eq ink bbox")
full = a[y0w + 2:y1w - 1, x0w + 2:x1w - 1]
redm = (full[:, :, 0] > 135) & (full[:, :, 1] < 100) & (full[:, :, 2] < 100)
blum = (full[:, :, 2] > 115) & (full[:, :, 0] < 115) & (full[:, :, 1] < 115)
for nm, m in [("RED", redm), ("BLUE", blum)]:
    ys2, xs2 = np.where(m)
    if len(ys2):
        print(f"    {nm}: x {xs2.min()+x0w+2}..{xs2.max()+x0w+2} y {ys2.min()+y0w+2}..{ys2.max()+y0w+2} core", corecolor(ys2.min()+y0w+2, ys2.max()+y0w+2, xs2.min()+x0w+2, xs2.max()+x0w+2, 20))
# fine structure: row profile of ink
prof = dk.sum(axis=1)
print("  ink row profile (y: count):")
for i, v in enumerate(prof):
    if v > 0: print(f"    y{i+y0w+2}: {v}")
