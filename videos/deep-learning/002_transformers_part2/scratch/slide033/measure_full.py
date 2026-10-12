#!/usr/bin/env python3
"""slide033 full measurement: boxes, text line bands, colors, equation ink.
Frame 960x540, 1px=1pt. Mapping (certified slide-032, re-verified on this frame):
  slide_x = (fx - 18.63)/0.96123 ; slide_y = fy/0.95556
"""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W = a.shape[:2]
SX = lambda fx: (fx - 18.63) / 0.96123
SY = lambda fy: fy / 0.95556

def band(y0, y1, x0, x1, label):
    """print slide-space coords of a frame-px rect"""
    print(f"  {label}: frame[{x0},{y0}..{x1},{y1}] slide x[{SX(x0):.1f}..{SX(x1):.1f}] y[{SY(y0):.1f}..{SY(y1):.1f}] w={SX(x1)-SX(x0):.1f} h={SY(y1)-SY(y0):.1f}")

def corecolor(y0, y1, x0, x1, n=40):
    """darkest core pixels median color in region"""
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    lum = reg.sum(axis=1)
    idx = np.argsort(lum)[:max(n, 1)]
    return tuple(int(v) for v in np.median(reg[idx], axis=0))

def colhist(y0, y1, x0, x1):
    """count pixels near candidate stroke colors"""
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    out = {}
    for nm, c in [("C00000", (192, 0, 0)), ("8B0000", (139, 0, 0)), ("0000CC", (0, 0, 204)),
                  ("000080", (0, 0, 128)), ("00B050", (0, 176, 80)), ("7030A0", (112, 48, 160)),
                  ("ED7D31", (237, 125, 49)), ("0070C0", (0, 112, 192)), ("black", (0, 0, 0)),
                  ("FF0000", (255, 0, 0))]:
        d = np.abs(reg - np.array(c)).sum(axis=1)
        out[nm] = int((d < 110).sum())
    return out

def rowbands(y0, y1, x0, x1, dark=120, gap=4, minpx=2):
    """find text-line bands: rows with >=minpx dark pixels, split on gaps>gap"""
    reg = a[y0:y1, x0:x1]
    dk = (reg.sum(axis=2) < dark * 3)
    prof = dk.sum(axis=1)
    rows = prof >= minpx
    bands = []
    s = None; last = None
    for i, v in enumerate(rows):
        if v:
            if s is None: s = i
            last = i
        else:
            if s is not None and i - last > gap:
                bands.append((s + y0, last + y0)); s = None
    if s is not None: bands.append((s + y0, last + y0))
    return bands

def colruns(y0, y1, x0, x1, dark=120, gap=3):
    """ink x-runs in a band"""
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

print("=== 1. TITLE ===")
tb = rowbands(44, 70, 300, 640, dark=140)
for (y0, y1) in tb:
    r = colruns(y0, y1, 300, 660, dark=140)
    print(f"  band f y{y0}..{y1} x{r[0][0]}..{r[-1][1]}", "core", corecolor(y0, y1, r[0][0], r[-1][1]))
    print("   hist:", colhist(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "title")

print("=== 2. SUBTITLE ===")
sb = rowbands(66, 95, 100, 860, dark=140)
for (y0, y1) in sb:
    r = colruns(y0, y1, 100, 860, dark=140)
    print(f"  band f y{y0}..{y1} x{r[0][0]}..{r[-1][1]}", "core", corecolor(y0, y1, r[0][0], r[-1][1]))
    print("   hist:", colhist(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "subtitle")

print("=== 3. GENERAL PAIR BOX (sin wt / cos wt) ===")
# border: dark pixels (JPEG-softened brown ~ (110,88,68))
reg = a[90:240, 80:245]
brd = reg.sum(axis=2) < 500
ys, xs = np.where(brd)
print(f"  dark ink frame x {xs.min()+80}..{xs.max()+80} y {ys.min()+90}..{ys.max()+90} core", corecolor(ys.min()+90, ys.max()+90, xs.min()+80, xs.max()+80, 60))
prof_r = brd.sum(axis=1); prof_c = brd.sum(axis=0)
wide_rows = np.where(prof_r > 20)[0] + 90
wide_cols = np.where(prof_c > 15)[0] + 80
print("  border rows:", (wide_rows.min(), wide_rows.max()) if len(wide_rows) else None,
      " cols:", (wide_cols.min(), wide_cols.max()) if len(wide_cols) else None)
if len(wide_rows) and len(wide_cols):
    band(wide_rows.min(), wide_rows.max(), wide_cols.min(), wide_cols.max(), "pairbox border")
band(wide_rows.min(), wide_rows.max(), wide_cols.min(), wide_cols.max(), "pairbox border")
# text rows inside
ptb = rowbands(100, 235, 95, 235, dark=150)
for (y0, y1) in ptb:
    r = colruns(y0, y1, 95, 235, dark=150)
    print(f"    text band f y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "pairtext")
# white fill?
print("  fill sample (150,160):", tuple(a[160, 150]), " (140,120):", tuple(a[140, 120]))

print("=== 4. INFO BOX (green) ===")
# light-green fill region
reg = a[215:335, 55:225]
grn = (np.abs(reg[:, :, 0] - 223) < 25) & (np.abs(reg[:, :, 1] - 248) < 20) & (np.abs(reg[:, :, 2] - 233) < 25)
ys, xs = np.where(grn)
print(f"  fill frame x {xs.min()+55}..{xs.max()+55} y {ys.min()+215}..{ys.max()+215} fill-med", tuple(int(v) for v in np.median(reg[grn], axis=0)))
band(ys.min() + 215, ys.max() + 215, xs.min() + 55, xs.max() + 55, "info fill")
# border color: darkest ring pixels
edge = a[ys.min() + 215:ys.max() + 215, xs.min() + 55:xs.max() + 55]
print("  border core (darkest in 2px ring):", corecolor(ys.min()+215, ys.min()+222, xs.min()+55, xs.max()+55, 25))
itb = rowbands(220, 335, 60, 220, dark=150)
for (y0, y1) in itb:
    r = colruns(y0, y1, 60, 220, dark=150)
    print(f"    text band f y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "infotext")
    # red tokens inside?
    regl = a[y0:y1+1, r[0][0]:r[-1][1]+1]
    redm = (regl[:, :, 0] > 130) & (regl[:, :, 1] < 90) & (regl[:, :, 2] < 90)
    if redm.sum() > 3:
        cys, cxs = np.where(redm)
        print(f"      RED token x {cxs.min()+r[0][0]}..{cxs.max()+r[0][0]}", "core", corecolor(y0, y1, cxs.min()+r[0][0], cxs.max()+r[0][0]))

print("=== 5. VECTOR PAIRS label ===")
vtb = rowbands(90, 125, 205, 270, dark=160)
for (y0, y1) in vtb:
    r = colruns(y0, y1, 205, 270, dark=160)
    print(f"    band f y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "vplabel")
    regl = a[y0:y1+1, r[0][0]:r[-1][1]+1]
    blum = (regl[:, :, 2] > 120) & (regl[:, :, 0] < 110) & (regl[:, :, 1] < 110)
    if blum.sum() > 3:
        cys, cxs = np.where(blum)
        print(f"      BLUE part x {cxs.min()+r[0][0]}..{cxs.max()+r[0][0]}", "core", corecolor(y0, y1, cxs.min()+r[0][0], cxs.max()+r[0][0]))

print("=== 6. VECTOR PAIRS COLUMN boxes ===")
col = a[110:520, 215:262]
# classify rows by fill color at x 225..250
for y in range(110, 519):
    px = a[y, 225:250].mean(axis=0)
    r, g, b = px
    tag = None
    if abs(r-165) < 30 and g > 195 and abs(b-178) < 30: tag = "GREEN"
    elif r > 215 and g > 205 and b < 200 and b > 130: tag = "KHAKI"
    if tag:
        print(f"  y={y} {tag} ({r:.0f},{g:.0f},{b:.0f})", end="\r" if False else "\n") if y % 1 == 0 and (y < 175 or y > 440) else None
# simpler: run-length of fill class
def fillruns(x_lo=226, x_hi=249):
    runs = []
    cur = None
    for y in range(108, 522):
        px = a[y, x_lo:x_hi]
        med = tuple(np.median(px, axis=0))
        r, g, b = med
        if abs(r - 165) < 35 and g > 195 and abs(b - 178) < 40: t = "GREEN"
        elif r > 210 and g > 200 and 130 < b < 205: t = "KHAKI"
        else: t = None
        if t != (cur[0] if cur else None):
            if cur and cur[0]: runs.append((cur[1], y - 1, cur[0]))
            cur = (t, y)
    if cur and cur[0]: runs.append((cur[1], 521, cur[0]))
    return runs
print("  fill runs (frame y):")
for (y0, y1, t) in fillruns():
    if y1 - y0 > 5:
        print(f"    {t} y {y0}..{y1}", end=" ")
        band(y0, y1, 226, 249, "")
# box borders (green/dark border) + value text
vptb = rowbands(110, 522, 218, 258, dark=110, gap=5, minpx=2)
print("  dark-ink bands in col:")
for (y0, y1) in vptb:
    r = colruns(y0, y1, 218, 258, dark=110)
    print(f"    y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]))

print("=== 7. INDEX strip + label ===")
itb2 = rowbands(88, 125, 258, 320, dark=150)
print("  label bands:")
for (y0, y1) in itb2:
    r = colruns(y0, y1, 258, 320, dark=150)
    print(f"    y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "indexlabel")
# strip: cream fill extent
reg = a[105:520, 255:325]
cream = (np.abs(reg[:, :, 0] - 251) < 10) & (np.abs(reg[:, :, 1] - 253) < 8) & (np.abs(reg[:, :, 2] - 232) < 14)
ys, xs = np.where(cream)
print(f"  cream strip frame x {xs.min()+255}..{xs.max()+255} y {ys.min()+105}..{ys.max()+105}")
band(ys.min() + 105, ys.max() + 105, xs.min() + 255, xs.max() + 255, "cream strip")
print("  strip border core:", corecolor(ys.min()+105, ys.min()+110, xs.min()+255, xs.max()+255, 20))
# red numbers bands inside strip
ntb = rowbands(105, 520, 262, 310, dark=170, gap=4, minpx=1)
print("  number ink bands:")
for (y0, y1) in ntb:
    r = colruns(y0, y1, 258, 312, dark=170)
    print(f"    y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]))

print("=== 8. SIN/COS TERMS COLUMN ===")
# fill runs at x 335..390
def fillruns2(x_lo=335, x_hi=392):
    runs = []; cur = None
    for y in range(112, 522):
        px = a[y, x_lo:x_hi]
        med = tuple(np.median(px, axis=0))
        r, g, b = med
        if abs(r - 165) < 35 and g > 195 and abs(b - 178) < 45: t = "GREEN"
        elif r > 225 and 170 < g < 215 and 110 < b < 165: t = "ORANGE"
        elif r > 243 and g > 243 and 195 < b < 225: t = "LTORANGE"
        else: t = None
        if t != (cur[0] if cur else None):
            if cur and cur[0]: runs.append((cur[1], y - 1, cur[0]))
            cur = (t, y)
    if cur and cur[0]: runs.append((cur[1], 521, cur[0]))
    return runs
print("  fill runs:")
for (y0, y1, t) in fillruns2():
    if y1 - y0 > 3:
        print(f"    {t} y {y0}..{y1}", end=" ")
        band(y0, y1, 322, 405, "")
# exact box x extent at box1 mid
row = a[160, 300:420]
nb = np.where(np.abs(row - np.array([233, 233, 231])).sum(axis=1) > 45)[0] + 300
print("  box1 x extent at y160:", nb.min(), nb.max())
row = a[280, 300:420]
nb = np.where(np.abs(row - np.array([233, 233, 231])).sum(axis=1) > 45)[0] + 300
print("  box3 x extent at y280:", nb.min(), nb.max())
# text ink in each box
for (by0, by1, nm) in [(125, 190, "box1"), (188, 252, "box2"), (255, 322, "box3"), (348, 415, "box4"), (448, 515, "box5")]:
    tb2 = rowbands(by0, by1, 322, 410, dark=140, gap=4, minpx=2)
    for (y0, y1) in tb2:
        r = colruns(y0, y1, 322, 410, dark=140)
        print(f"    {nm} text y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]))
# brackets: red vertical strokes near x 310..320 and 410..420
reg = a[110:520, 300:330]
redm = (reg[:, :, 0] > 130) & (reg[:, :, 1] < 90) & (reg[:, :, 2] < 90)
ys, xs = np.where(redm)
if len(ys):
    print(f"  LEFT red stroke frame x {xs.min()+300}..{xs.max()+300} y {ys.min()+110}..{ys.max()+110} core", corecolor(ys.min()+110, ys.max()+110, xs.min()+300, xs.max()+300))
reg = a[110:520, 405:425]
redm = (reg[:, :, 0] > 130) & (reg[:, :, 1] < 90) & (reg[:, :, 2] < 90)
ys, xs = np.where(redm)
if len(ys):
    print(f"  RIGHT red stroke frame x {xs.min()+405}..{xs.max()+405} y {ys.min()+110}..{ys.max()+110} core", corecolor(ys.min()+110, ys.max()+110, xs.min()+405, xs.max()+405))
# dx1
dtb = rowbands(485, 520, 420, 470, dark=150)
for (y0, y1) in dtb:
    r = colruns(y0, y1, 420, 470, dark=150)
    print(f"    dx1 y{y0}..{y1} x{r[0][0]}..{r[-1][1]} core", corecolor(y0, y1, r[0][0], r[-1][1]))
    band(y0, y1, r[0][0], r[-1][1], "dx1")

print("=== 9. DEFINITIONS BOX ===")
# border: red rect around cream
reg = a[90:300, 415:780]
cream = (np.abs(reg[:, :, 0] - 251) < 12) & (np.abs(reg[:, :, 1] - 253) < 10) & (np.abs(reg[:, :, 2] - 232) < 16)
ys, xs = np.where(cream)
x0d, x1d, y0d, y1d = xs.min() + 415, xs.max() + 415, ys.min() + 90, ys.max() + 90
band(y0d, y1d, x0d, x1d, "defs cream fill")
print("  border core:", corecolor(y0d - 6, y0d, x0d, x1d, 25))
# line bands (any dark ink)
ltb = rowbands(y0d + 3, y1d - 2, x0d + 4, x1d - 3, dark=150, gap=5, minpx=2)
print(f"  {len(ltb)} line bands:")
for (y0, y1) in ltb:
    r = colruns(y0, y1, x0d, x1d, dark=150)
    print(f"    y{y0}..{y1} x{r[0][0]}..{r[-1][1]}", end=" ")
    band(y0, y1, r[0][0], r[-1][1], "")

print("=== 10. EXAMPLE BOX ===")
reg = a[90:300, 770:900]
cream = (np.abs(reg[:, :, 0] - 251) < 12) & (np.abs(reg[:, :, 1] - 253) < 10) & (np.abs(reg[:, :, 2] - 232) < 16)
ys, xs = np.where(cream)
x0e, x1e, y0e, y1e = xs.min() + 770, xs.max() + 770, ys.min() + 90, ys.max() + 90
band(y0e, y1e, x0e, x1e, "example cream fill")
etb = rowbands(y0e + 3, y1e - 2, x0e + 3, x1e - 2, dark=150, gap=4, minpx=1)
print(f"  {len(etb)} line bands:")
for (y0, y1) in etb:
    r = colruns(y0, y1, x0e, x1e, dark=150)
    print(f"    y{y0}..{y1} x{r[0][0]}..{r[-1][1]}", end=" ")
    band(y0, y1, r[0][0], r[-1][1], "")
    # red part
    regl = a[y0:y1+1, r[0][0]:r[-1][1]+1]
    redm = (regl[:, :, 0] > 130) & (regl[:, :, 1] < 90) & (regl[:, :, 2] < 90)
    if redm.sum() > 3:
        cys, cxs = np.where(redm)
        print(f"      RED x {cxs.min()+r[0][0]}..{cxs.max()+r[0][0]}")

print("=== 11. BLUE OMEGA BOX ===")
reg = a[290:520, 465:890]
ltb2 = (np.abs(reg[:, :, 0] - 233) < 12) & (np.abs(reg[:, :, 1] - 252) < 10) & (np.abs(reg[:, :, 2] - 247) < 12)
ys, xs = np.where(ltb2)
x0b, x1b, y0b, y1b = xs.min() + 465, xs.max() + 465, ys.min() + 290, ys.max() + 290
band(y0b, y1b, x0b, x1b, "blue fill")
print("  border core:", corecolor(y0b - 8, y0b, x0b, x1b, 25))
btb = rowbands(y0b + 3, y1b - 2, x0b + 4, x1b - 3, dark=150, gap=4, minpx=2)
print(f"  {len(btb)} line bands:")
for (y0, y1) in btb:
    r = colruns(y0, y1, x0b, x1b, dark=150)
    print(f"    y{y0}..{y1} x{r[0][0]}..{r[-1][1]}", end=" ")
    band(y0, y1, r[0][0], r[-1][1], "")
    regl = a[y0:y1+1, r[0][0]:r[-1][1]+1]
    redm = (regl[:, :, 0] > 130) & (regl[:, :, 1] < 90) & (regl[:, :, 2] < 90)
    if redm.sum() > 3:
        cys, cxs = np.where(redm)
        print(f"      RED x {cxs.min()+r[0][0]}..{cxs.max()+r[0][0]}")

print("=== 12. WHITE EQ SUB-BOX + EQUATION INK ===")
reg = a[335:405, 695:880]
wh = (reg[:, :, 0] > 244) & (reg[:, :, 1] > 244) & (reg[:, :, 2] > 244)
ys, xs = np.where(wh)
x0w, x1w, y0w, y1w = xs.min() + 695, xs.max() + 695, ys.min() + 335, ys.max() + 335
band(y0w, y1w, x0w, x1w, "white subbox")
print("  subbox border core:", corecolor(y0w - 6, y0w, x0w, x1w, 25))
# equation ink inside: everything darker than 200 lum
reg2 = a[y0w + 2:y1w - 1, x0w + 2:x1w - 1]
dk = reg2.sum(axis=2) < 560
ys, xs = np.where(dk)
print(f"  eq ink frame x {xs.min()+x0w+2}..{xs.max()+x0w+2} y {ys.min()+y0w+2}..{ys.max()+y0w+2}")
band(ys.min() + y0w + 2, ys.max() + y0w + 2, xs.min() + x0w + 2, xs.max() + x0w + 2, "eq ink bbox")
# component split by color: red / blue / black
reg3 = a[ys.min()+y0w+2:ys.max()+y0w+3, xs.min()+x0w+2:xs.max()+x0w+3]
full = a[y0w+2:y1w-1, x0w+2:x1w-1]
redm = (full[:, :, 0] > 130) & (full[:, :, 1] < 90) & (full[:, :, 2] < 90)
blum = (full[:, :, 2] > 120) & (full[:, :, 0] < 110) & (full[:, :, 1] < 110)
for nm, m in [("RED", redm), ("BLUE", blum), ("BLACK/dk", dk & ~redm & ~blum)]:
    ys2, xs2 = np.where(m)
    if len(ys2):
        print(f"    {nm}: x {xs2.min()+x0w+2}..{xs2.max()+x0w+2} y {ys2.min()+y0w+2}..{ys2.max()+y0w+2} core", corecolor(ys2.min()+y0w+2, ys2.max()+y0w+2, xs2.min()+x0w+2, xs2.max()+x0w+2, 25))

print("=== 13. per-line color runs (defs box lines 1-6) ===")
# sample word colors: print core colors of x-runs per line
for (y0, y1) in ltb:
    runs = colruns(y0, y1, x0d + 2, x1d - 2, dark=170, gap=7)
    desc = []
    for (rx0, rx1) in runs:
        c = corecolor(y0, y1, rx0, rx1 + 1, 12)
        desc.append(f"[{rx0}-{rx1}]{c}")
    print(f"  line y{y0}..{y1}:", " ".join(desc))
