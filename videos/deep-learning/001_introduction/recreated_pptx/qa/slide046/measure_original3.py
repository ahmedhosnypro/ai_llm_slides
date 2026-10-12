#!/usr/bin/env python3
"""PIL forensics pass 3 — slide_046.jpg: precise structures, colors, font fitting."""
from PIL import Image, ImageFont, ImageDraw
import numpy as np
from collections import Counter

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_046.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

redm   = (R > 110) & (R - G > 25) & (R - B > 25)
bluem  = (B - R > 30) & (B - G > 25) & (B > 100)
greenm = (G - R > 40) & (G - B > 40) & (G > 120)
textm  = (R + G + B < 620) & ~redm & ~bluem & ~greenm

def bbox(mask, x0, y0, label):
    ys, xs = np.nonzero(mask[y0:y0+mask.shape[0], x0:x0+mask.shape[1]] if False else mask)
    return None

def bb(x0, y0, x1, y1, mask, label):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        print(f"{label:36s} EMPTY"); return None
    r = (x0+xs.min(), y0+ys.min(), x0+xs.max(), y0+ys.max())
    print(f"{label:36s} x {r[0]}..{r[2]}  y {r[1]}..{r[3]}  (w {r[2]-r[0]+1} h {r[3]-r[1]+1})")
    return r

def core_color(x0, y0, x1, y1, mask, label, pct=8):
    sub = a[y0:y1, x0:x1][mask[y0:y1, x0:x1]]
    if len(sub) == 0: print(f"{label}: no px"); return
    lum = sub.sum(axis=1)
    idx = np.argsort(lum)[:max(1, int(len(lum)*pct/100))]
    sel = sub[idx]
    print(f"{label:36s} core modal {Counter(map(tuple, sel)).most_common(2)} (n={len(sub)})")

print("== gray region (chrome fill) extent ==")
graym = (abs(R-232) < 7) & (abs(G-232) < 7) & (abs(B-232) < 7)
ys, xs = np.nonzero(graym)
print(f"gray bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(xs)}")
for (yy, xx) in [(100, 20), (100, 930), (300, 890), (300, 910), (480, 20), (480, 900), (480, 940), (505, 480), (60, 480), (120, 480), (465, 100)]:
    print(f"  px(x={xx},y={yy}) = {a[yy, xx].tolist()}")

print("== content panel borders (red stroke) ==")
bb(40, 128, 900, 140, redm, "panel top border band")
bb(40, 450, 900, 464, redm, "panel bottom border band")
for x in (875, 876, 877, 878, 879, 880, 881):
    ys2 = np.nonzero(redm[130:465, x])[0]
    if len(ys2) > 100:
        print(f"  col x={x}: red n={len(ys2)} y {130+ys2.min()}..{130+ys2.max()}")
for x in (55, 56, 57, 58, 59, 60):
    ys2 = np.nonzero(redm[130:465, x])[0]
    print(f"  col x={x}: red n={len(ys2)}", f"y {130+ys2.min()}..{130+ys2.max()}" if len(ys2) else "")
core_color(130, 131, 880, 136, redm, "panel border red core")

print("== title POOLING ==")
tb = bb(300, 60, 700, 130, redm, "title ink")
core_color(300, 60, 700, 130, redm, "title red core")
bb(300, 60, 700, 130, textm, "title ink (loose mask)")

print("== bullets (loose text mask) ==")
sub = textm[140:245, 100:800]
rows = sub.sum(axis=1)
run = None
bands = []
for i, v in enumerate(rows):
    y = 140 + i
    if v > 0 and run is None: run = y
    elif v == 0 and run is not None:
        bands.append((run, y-1)); run = None
if run is not None: bands.append((run, 244))
for (y0, y1) in bands:
    r = bb(100, y0, 800, y1+1, textm, f"line y{y0}..{y1}")
# markers vs text split (main)
bb(130, 148, 152, 172, textm, "main marker")
bb(130, 175, 152, 193, textm, "sub1 marker")
bb(130, 197, 152, 216, textm, "sub2 marker")
bb(130, 222, 152, 240, textm, "sub3 marker")
core_color(150, 150, 700, 170, textm, "main text core")
core_color(150, 175, 780, 240, textm, "sub text core")

print("== option boxes ==")
# horizontal border lines: blue count per row
for y in range(244, 316):
    n = int(bluem[y, 100:320].sum())
    if n > 100: print(f"  blue row y={y}: n={n}")
print("  --")
for x in range(100, 320):
    n = int(bluem[245:315, x].sum())
    if n > 40: print(f"  blue col x={x}: n={n}")
core_color(100, 245, 320, 315, bluem, "box border blue core")
bb(112, 246, 290, 282, textm, "box1 text ink (excl borders)")
bb(112, 286, 290, 312, textm, "box2 text ink (excl borders)")
bb(112, 246, 152, 282, textm, "box1 marker")

print("== diagram ==")
bb(150, 320, 280, 430, greenm, "matrix green")
bb(150, 320, 280, 430, textm, "matrix dark ink")
bb(172, 336, 209, 369, textm, "cell a letter")
bb(205, 336, 243, 369, textm, "cell b letter")
bb(172, 364, 209, 400, textm, "cell c letter")
bb(205, 364, 243, 400, textm, "cell d letter")
core_color(172, 336, 209, 369, textm, "cell-a letter core")
bb(250, 340, 322, 400, textm, "arrow ink")
bb(305, 340, 365, 400, greenm, "z square green")
bb(305, 340, 365, 400, textm, "z dark ink")
# Pool ( : split text vs paren by column profile
sub = textm[335:415, 360:445]
cols = sub.sum(axis=0)
print("  Pool( col profile x360..444:", list(zip(range(360,445), cols.tolist())))
bb(360, 335, 415, 415, textm, "Pool ( ink")
core_color(360, 335, 445, 415, textm, "Pool text core")
# ) and ==
sub = textm[335:415, 590:670]
cols = sub.sum(axis=0)
print("  )== col profile x590..669:", list(zip(range(590,670), cols.tolist())))
bb(590, 335, 670, 415, textm, ") == ink")
# tiger photos: notwhite density per column
notw = (R + G + B < 660)
for x0, x1, lbl in [(415, 640, "large tiger"), (655, 800, "small tiger")]:
    prof = notw[320:420, x0:x1].sum(axis=0)
    dens = [x0+i for i, v in enumerate(prof) if v > 40]
    if dens:
        xs0, xs1 = dens[0], dens[-1]
        ys2 = np.nonzero(notw[320:420, xs0:xs1+1].sum(axis=1) > 40)[0]
        print(f"  {lbl}: x {xs0}..{xs1} y {320+ys2.min()}..{320+ys2.max()} (w {xs1-xs0+1} h {ys2.max()-ys2.min()+1})")
bb(640, 390, 810, 420, bluem, "caption ink")
core_color(640, 390, 810, 420, bluem, "caption core")

print("== bottom strip ==")
for y in (516, 517, 518, 519):
    dk = np.nonzero(a[y].sum(axis=1) < 200)[0]
    print(f"  y={y}: n={len(dk)}", (int(dk.min()), int(dk.max())) if len(dk) else "")

# ---------- font fitting (Liberation = metric-compatible) ----------
print("== font fitting ==")
FONTS = {
    "LSans-Bold":  "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "LSerif-Bold": "/usr/share/fonts/liberation/LiberationSerif-Bold.ttf",
    "LSans-Reg":   "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
    "LSerif-It":   "/usr/share/fonts/liberation/LiberationSerif-Italic.ttf",
    "LSans-It":    "/usr/share/fonts/liberation/LiberationSans-Italic.ttf",
}
import os
for k, p in list(FONTS.items()):
    if not os.path.exists(p):
        alt = p.replace("/liberation/", "/TTF/")
        FONTS[k] = alt if os.path.exists(alt) else None
print("fonts:", {k: bool(v) for k, v in FONTS.items()})

def fit(fontkey, text, target_w, target_h=None, lo=8, hi=60):
    fp = FONTS[fontkey]
    if not fp: return None
    best = None
    for s10 in range(lo*10, hi*10):
        s = s10/10
        f = ImageFont.truetype(fp, int(round(s*4)))  # 4x for sub-px precision
        b = f.getbbox(text)
        wpx = (b[2]-b[0])/4; hpx = (b[3]-b[1])/4
        err = abs(wpx - target_w)
        if best is None or err < best[0]:
            best = (err, s, wpx, hpx)
    print(f"  {fontkey:12s} '{text[:28]}' tgt_w={target_w} -> size {best[1]:.1f}pt (w {best[2]:.1f}, h {best[3]:.1f}, err {best[0]:.1f})")
    return best

if tb:
    tw = tb[2]-tb[0]+1
    fit("LSans-Bold", "POOLING", tw)
    fit("LSerif-Bold", "POOLING", tw)

# bullet text fits (text-only widths measured after markers)
main_w = 539 - 156 + 1
fit("LSans-Reg", "Aggregate multiple values into a single value", main_w)
fit("LSans-Reg", "Invariance to small transformations", 409-152+1)
fit("LSans-Reg", "Reduces the size of the layer output/input to next layer \u2192 Faster computations", 757-152+1)
fit("LSans-Reg", "Keeps most important information for the next layer", 544-152+1)
fit("LSans-Reg", "Max pooling", 250-120)
fit("LSans-Reg", "Average pooling", 275-120)
