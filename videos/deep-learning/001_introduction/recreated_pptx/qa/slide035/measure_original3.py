#!/usr/bin/env python3
"""measure_original3.py — slide 035 pass 3: ASCII maps, per-cell forensics,
colors, caption line classification."""
import numpy as np
from PIL import Image

FR = "videos/deep-learning/001_introduction/unique_slides/slide_035.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def cls(r, g, b):
    if r > 235 and g > 235 and b > 235: return "W"  # white
    if r > 200 and g > 200 and b > 195 and r - b < 25: return "w"  # panel gray-ish/white-ish
    if abs(r - 233) < 12 and abs(g - 233) < 12 and abs(b - 231) < 12: return "P"  # panel gray
    if r > 180 and g > 170 and b < 140 and r - b > 60: return "Y"  # yellow
    if r > 235 and g > 230 and 195 < b < 245: return "L"  # light yellow (caption)
    if g - r > 25 and g - b > 25 and g > 90: return "G"  # green
    if r - g > 60 and r - b > 60 and r > 120: return "R"  # red
    if b - r > 25 and b > 100: return "B"  # blue
    if r < 110 and g < 110 and b < 110: return "D"  # dark
    if r > 150 and r - b > 25 and r - g > 5: return "T"  # tan/orange
    return "."

def amap(x0, x1, y0, y1, step, label):
    print(f"--- ASCII map {label} x{x0}..{x1} y{y0}..{y1} step {step} (each char = {step}x{step}px median) ---")
    hdr = "     " + "".join(str((x // 10) % 10) for x in range(x0, x1 + 1, step))
    print(hdr)
    for y in range(y0, y1 + 1, step):
        row = ""
        for x in range(x0, x1 + 1, step):
            blk = a[y:y+step, x:x+step].reshape(-1, 3)
            m = np.median(blk, axis=0)
            row += cls(*m)
        print(f"y{y:4d} {row}")

print("=== M1. OUTPUT GRID + '4' cell + arrow head region ===")
amap(685, 885, 183, 240, 3, "output top rows")
amap(685, 885, 240, 385, 4, "output lower rows")

print("=== M2. CURSOR REGION ===")
amap(695, 795, 330, 425, 3, "cursor")

print("=== M3. ARROW FULL PATH (top area over yellow block) ===")
amap(520, 700, 185, 215, 3, "arrow path")

print("=== M4. PANEL GRID TOP-LEFT + multipliers zoom ===")
amap(400, 585, 196, 250, 3, "panel r1")

print("=== COLORS: exact samples ===")
def s(x, y, lab):
    r, g, b = a[y, x]
    print(f"  ({x},{y}) #{r:02X}{g:02X}{b:02X} ({r},{g},{b}) {lab}")
s(433, 221, "panel yellow cell r1c1 fill")
s(490, 260, "panel yellow r2c2 fill")
s(605, 350, "panel green c4/r4 fill")
s(650, 395, "panel green c5/r5 fill")
s(285, 230, "filter yellow r1c1 fill")
s(300, 230, "filter border between c1c2")
s(285, 243, "filter border between r1r2")
s(105, 222, "left grid digit r1c1 area")
s(150, 300, "left grid mid")
s(750, 200, "output r1c2 top")
s(750, 250, "output r2c2")
s(760, 300, "output r2c3?")
s(840, 300, "output r3c3?")
s(700, 195, "output r1c1 top edge")
s(710, 205, "output r1c1 upper")
s(710, 220, "output r1c1 lower")
s(740, 210, "output r1c1 right")
s(500, 460, "caption line1 text")
s(500, 452, "caption line1 upper")
s(120, 490, "caption line2 start")
s(250, 490, "caption line2 mid")
s(400, 490, "caption line2 later")
s(470, 490, "caption line2 PERCEPTRON")
s(560, 490, "caption line2 after?")
s(700, 490, "caption line2 right end")
s(58, 250, "panel left border (original)")
s(902, 250, "right border zone x902")
s(500, 44, "panel top edge y44")
s(500, 46, "panel top edge y46")
s(500, 48, "panel top edge y48")
s(60, 44, "left border top corner")
s(500, 440, "caption box top edge?")
s(500, 505, "caption box bottom edge?")
s(80, 480, "caption box left edge zone")
s(880, 480, "caption box right edge zone")

print("=== CAPTION LINE 2 full-run classification x80..520 y478..505 ===")
reg = a[478:506, 80:520]
rr, gg, bb = reg[:,:,0], reg[:,:,1], reg[:,:,2]
redm = (rr - gg > 60) & (rr - bb > 60) & (rr > 120)
blum = (bb - rr > 25) & (bb > 90)
darkm = (rr < 110) & (gg < 110) & (bb < 110)
print(f"red px: {redm.sum()}, blue px: {blum.sum()}, dark px: {darkm.sum()}")
ys, xs = np.where(redm)
if len(xs): print(f"red bbox x{xs.min()+80}..{xs.max()+80} y{ys.min()+478}..{ys.max()+478}")
ys, xs = np.where(blum)
if len(xs): print(f"blue bbox x{xs.min()+80}..{xs.max()+80} y{ys.min()+478}..{ys.max()+478}")
# red column runs => which words are red
colprof = redm.sum(axis=0)
runs = []
inrun = False
for x in range(reg.shape[1]):
    if colprof[x] > 0 and not inrun: s_ = x; inrun = True
    elif colprof[x] == 0 and inrun:
        if x - s_ > 1: runs.append((s_+80, x-1+80))
        inrun = False
print("red col runs (gaps>1 merged):", runs)

print("=== CAPTION LINE 1 full-run classification x60..900 y450..475 ===")
reg = a[450:476, 60:900]
rr, gg, bb = reg[:,:,0], reg[:,:,1], reg[:,:,2]
blum = (bb - rr > 20) & (bb > 80)
redm = (rr - gg > 60) & (rr - bb > 60) & (rr > 120)
print(f"blue px: {blum.sum()}, red px: {redm.sum()}")
ys, xs = np.where(blum)
if len(xs): print(f"blue bbox x{xs.min()+60}..{xs.max()+60} y{ys.min()+450}..{ys.max()+450} n={len(xs)}")

print("=== TITLE modal red ===")
tz = np.zeros((540, 960), bool); tz[60:105, 260:720] = True
redm2 = (R - G > 80) & (R - B > 80) & (R > 130) & tz
ys, xs = np.where(redm2)
reg = a[ys, xs]
print(f"title red n={len(xs)} modal:", tuple(np.median(reg, axis=0).astype(int)))

print("=== LEFT GRID: per-cell ink (5x5) ===")
greenm = (G - R > 45) & (G - B > 45) & (G > 80)
darkg = (G < 150) & (G - R > 20) & (G - B > 20)  # darker green digits
bx0, bx1, by0, by1 = 78, 242, 208, 337
cw = (bx1 - bx0) / 5.0
ch = (by1 - by0) / 5.0
for r in range(5):
    line = []
    for c in range(5):
        x0 = int(bx0 + c * cw) + 3; x1 = int(bx0 + (c + 1) * cw) - 3
        y0 = int(by0 + r * ch) + 2; y1 = int(by0 + (r + 1) * ch) - 2
        sub = darkg[y0:y1, x0:x1]
        n = int(sub.sum())
        w = 0
        if n:
            ys, xs = np.where(sub)
            w = xs.max() - xs.min() + 1
        line.append(f"n={n:3d} w={w:2d}")
    print(f"  row{r+1}: " + " | ".join(line))

print("=== FILTER GRID: per-cell ink (3x3) + exact rows ===")
darkf = (R < 110) & (G < 110) & (B < 110)
fx0, fx1, fy0, fy1 = 271, 364, 220, 291
cw = (fx1 - fx0) / 3.0
ch = (fy1 - fy0) / 3.0
for r in range(3):
    line = []
    for c in range(3):
        x0 = int(fx0 + c * cw) + 2; x1 = int(fx0 + (c + 1) * cw) - 2
        y0 = int(fy0 + r * ch) + 2; y1 = int(fy0 + (r + 1) * ch) - 2
        sub = darkf[y0:y1, x0:x1]
        n = int(sub.sum())
        w = 0; hgt = 0
        if n:
            ys, xs = np.where(sub)
            w = xs.max() - xs.min() + 1
            hgt = ys.max() - ys.min() + 1
        line.append(f"n={n:3d} w={w:2d} h={hgt:2d}")
    print(f"  row{r+1}: " + " | ".join(line))
# filter numeral row bands (excluding label leak): y215..295
nzz = np.zeros((540, 960), bool); nzz[215:295, 265:370] = True
nm = darkf & nzz
rowprof = nm.sum(axis=1)
print("filter digit row bands:")
inrun = False
for y in range(215, 295):
    if rowprof[y] > 2 and not inrun: s_ = y; inrun = True
    elif rowprof[y] <= 2 and inrun:
        print(f"  y{s_}..{y-1}"); inrun = False

print("=== PANEL GRID: per-cell ink (5x5) ===")
bx0, by0 = 404, 200
cw, ch = 57.5, 43.3
for r in range(5):
    line = []
    for c in range(5):
        x0 = int(bx0 + c * cw) + 3; x1 = int(bx0 + (c + 1) * cw) - 3
        y0 = int(by0 + r * ch) + 3; y1 = int(by0 + (r + 1) * ch) - 3
        sub = darkf[y0:y1, x0:x1]
        n = int(sub.sum())
        w = 0; hgt = 0
        if n:
            ys, xs = np.where(sub)
            w = xs.max() - xs.min() + 1
            hgt = ys.max() - ys.min() + 1
        line.append(f"n={n:3d} w={w:2d} h={hgt:2d}")
    print(f"  row{r+1}: " + " | ".join(line))
# panel digit color sample: darkest pixel in r1c1
sub = a[203:238, 407:458]
dk = sub.reshape(-1, 3)
idx = dk.sum(axis=1).argmin()
print("panel r1c1 darkest px:", tuple(dk[idx]))

print("=== PANEL MULTIPLIERS per yellow cell ===")
redm3 = (R - G > 70) & (R - B > 70) & (R > 130)
for r in range(3):
    line = []
    for c in range(3):
        x0 = int(bx0 + c * cw); x1 = int(bx0 + (c + 1) * cw)
        y0 = int(by0 + r * ch); y1 = int(by0 + (r + 1) * ch)
        sub = redm3[y0:y1, x0:x1]
        n = int(sub.sum())
        bb2 = ""
        if n:
            ys, xs = np.where(sub)
            bb2 = f"x{xs.min()+x0}..{xs.max()+x0} y{ys.min()+y0}..{ys.max()+y0}"
        line.append(f"n={n:3d} {bb2}")
    print(f"  row{r+1}: " + " || ".join(line))

print("=== OUTPUT GRID: '4' cell dense ===")
amap(686, 760, 186, 236, 2, "'4' cell zoom 2px")

print("=== LABELS: 'Image' 'Filter' metrics ===")
darkl = (R < 110) & (G < 110) & (B < 110)
for (x0, x1, y0, y1, lab) in [(100, 190, 175, 210, "Image"), (270, 345, 175, 210, "Filter")]:
    zz = np.zeros((540, 960), bool); zz[y0:y1, x0:x1] = True
    lm = darkl & zz
    ys, xs = np.where(lm)
    if len(xs):
        print(f"{lab}: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(xs)}")
        colprof = lm.sum(axis=0)
        tops = [np.where(lm[:, x])[0].min() for x in range(x0, x1) if lm[:, x].any()]
        bots = [np.where(lm[:, x])[0].max() for x in range(x0, x1) if lm[:, x].any()]
        print(f"   col-top p10={np.percentile(tops,10):.0f} col-bot p90={np.percentile(bots,90):.0f} max={max(bots)}")

print("=== TITLE: serif check via stroke analysis (T-junction count) ===")
# count horizontal-to-vertical transitions: serif fonts have flared stroke ends.
# Simple proxy: ink density vs advance for cap letters. Print row band widths of 'H' (first word x266..333)
zz = np.zeros((540, 960), bool); zz[60:110, 260:340] = True
redm2 = (R - G > 80) & (R - B > 80) & (R > 130) & zz
for y in range(66, 100, 2):
    row = np.where(redm2[y, :])[0]
    if len(row):
        segs = []
        s_ = row[0]; p = row[0]
        for x in row[1:]:
            if x - p > 1:
                segs.append((s_, p)); s_ = x
            p = x
        segs.append((s_, p))
        print(f"  y={y}: segs {[(int(u),int(v)) for u,v in segs]}")
