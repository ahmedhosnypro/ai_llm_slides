#!/usr/bin/env python3
"""Closed-loop self-check attempt 1: render_1.png (150dpi, 2000x1125) vs PIL-measured
original-frame constants (960x540, 1px=1pt). Scale: render = frame * 2.08333.
Tolerance: ~8 render px (~4 frame px) per the pipeline closed-loop standard."""
from PIL import Image
import numpy as np

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide049/render_1.png"
im = Image.open(RENDER).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
S = H / 540.0
print(f"render {W}x{H}  scale {S:.4f} render-px per frame-px")
TOL = 8.0  # render px
fails, warns = [], []

def cv(v): return v * S

# ---- title ----
sub = a[int(cv(55)):int(cv(150)), int(cv(240)):int(cv(720))]
redm = (sub[:,:,0]>120) & (sub[:,:,1]<80) & (sub[:,:,2]<80)
ys, xs = np.where(redm)
if not len(ys):
    fails.append("title: no red ink found")
else:
    x0, x1 = xs.min()/S+240, xs.max()/S+240
    y0, y1 = ys.min()/S+55, ys.max()/S+55
    print(f"title ink: x {x0:.1f}..{x1:.1f} (w {x1-x0:.1f})  y {y0:.1f}..{y1:.1f}   [orig x 252..707 (w 456) y 84..117(baseline 116.5)]")
    if abs((x0+x1)/2 - 479.5) > 4: fails.append(f"title center {(x0+x1)/2:.1f} vs 479.5")
    if abs(x0-252) > 4 or abs(x1-707) > 4: fails.append(f"title x-extent vs 252..707")
    if abs(y0-84) > 4: fails.append(f"title cap-top {y0:.1f} vs 84")
    # baseline: last row with >=25 ink px in the band
    rc = redm.sum(axis=1)
    idx = np.where(rc >= int(25*S))[0]
    base = idx[-1]/S+55 if len(idx) else -1
    print(f"title baseline {base:.1f} [orig 116.5]")
    if abs(base-116.5) > 4: fails.append(f"title baseline {base:.1f} vs 116.5")

# ---- blue box ----
bluem = (a[:,:,2]>110) & (a[:,:,0]<110) & (a[:,:,1]<110)
sub = bluem[int(cv(140)):int(cv(510)), int(cv(80)):int(cv(880))]
rowc = sub.sum(axis=1); colc = sub.sum(axis=0)
RY0, CX0 = int(cv(140)), int(cv(80))
rows = [ (y+RY0)/S for y in range(len(rowc)) if rowc[y] > int(300*S) and (y+RY0) > 100*S ]
cols = [ (x+CX0)/S for x in range(len(colc)) if colc[x] > int(150*S) and (x+CX0) > 90*S ]
print(f"box border rows {rows}  cols {cols}   [orig stroke-center y 153.5/491.5, x 99.5/860.5]")
if rows:
    if abs(rows[0]-153.5) > 4 or abs(rows[-1]-491.5) > 4:
        fails.append(f"box y {rows[0]:.1f}..{rows[-1]:.1f} vs 153.5..491.5")
if cols:
    if abs(cols[0]-99.5) > 4 or abs(cols[-1]-860.5) > 4:
        fails.append(f"box x {cols[0]:.1f}..{cols[-1]:.1f} vs 99.5..860.5")

# ---- 8 text bands ----
EXP_BANDS = [
    ("band0", 160, 177, 111.8, 575),
    ("band1", 199, 216.5, 111.8, 838),
    ("band2", 228, 245.5, 142, 401),
    ("band3", 268, 284.5, 111.8, 813),
    ("band4", 308, 325.3, 111.8, 457),
    ("band5", 343, 360.5, 194.8, 697),
    ("band6", 378, 395.5, 194.8, 739),
    ("band7", 414, 431, 194.8, 797),
]
ix0, ix1 = int(cv(106)), int(cv(855))
iy0, iy1 = int(cv(158)), int(cv(488))
inner = a[iy0:iy1, ix0:ix1]
dark = inner.sum(axis=2) < 420  # RGB-sum threshold is resolution-independent
rowhas = dark.any(axis=1)
bands = []; inb=False
for i, v in enumerate(rowhas):
    if v and not inb: s=i; inb=True
    elif not v and inb:
        if i-s >= 2: bands.append((s,i-1))
        inb=False
if inb: bands.append((s, len(rowhas)-1))
print(f"\nfound {len(bands)} dark-ink bands (expect 8):")
if len(bands) != 8:
    fails.append(f"band count {len(bands)} != 8")
for k,(s,e) in enumerate(bands):
    y0f, y1f = s/S+158, e/S+158
    seg = inner[s:e+1]; dm = dark[s:e+1]
    ys2, xs2 = np.where(dm)
    x0f, x1f = xs2.min()/S+106, xs2.max()/S+106
    # baseline: last row with count >= 12*S... use descender model inverse: report band bottom
    exp = EXP_BANDS[k] if k < len(EXP_BANDS) else None
    print(f"  band{k}: y {y0f:.1f}..{y1f:.1f}  x {x0f:.1f}..{x1f:.1f}")
    if exp:
        _, etop, ebase, el, er = exp
        if abs(x0f-el) > 4.5: fails.append(f"band{k} ink-left {x0f:.1f} vs {el}")
        if abs(x1f-er) > 5.5: fails.append(f"band{k} ink-right {x1f:.1f} vs {er}")
        if abs(y0f-etop) > 4.5: fails.append(f"band{k} cap-top {y0f:.1f} vs {etop}")
if len(bands) == 8:
    for k,(s,e) in enumerate(bands):
        y1f = e/S+156
        _, etop, ebase, el, er = EXP_BANDS[k]
        # band bottom = descender bottom (baseline + 0.212em) or baseline for band7
        desc = 5.5 if k != 7 else 0
        if abs(y1f - (ebase+desc)) > 4.5: fails.append(f"band{k} bottom {y1f:.1f} vs {ebase+desc:.1f}")

# ---- underline checks ----
print()
def find_underline(yf0, yf1, xf0, xf1, tag, exp_x0, exp_x1, exp_y):
    y0, y1 = int(cv(yf0)), int(cv(yf1))
    x0, x1 = int(cv(xf0)), int(cv(xf1))
    best = None
    for yy in range(y0, y1):
        row = a[yy, x0:x1].sum(axis=1) < 560
        xsr = np.where(row)[0]
        if len(xsr) >= 15*S*0.6:
            runs = []
            cs = prev = None
            for x in xsr:
                if cs is None: cs = prev = x; continue
                if x == prev+1: prev = x
                else: runs.append((cs, prev)); cs = prev = x
            runs.append((cs, prev))
            r = max(runs, key=lambda t: t[1]-t[0])
            if best is None or (r[1]-r[0]) > (best[3]-best[2]): best = (yy, r[0]+x0, r[1]+x0, r[0], r[1])
    if best is None:
        fails.append(f"{tag}: NO underline found in y[{yf0},{yf1}]")
        print(f"  {tag}: NONE")
    else:
        yy, rx0, rx1 = best[0], best[1], best[2]
        xf0r, xf1r, yfr = rx0/S, rx1/S, yy/S
        print(f"  {tag}: y {yfr:.1f} x {xf0r:.1f}..{xf1r:.1f} (len {xf1r-xf0r:.1f})   [orig y {exp_y} x {exp_x0}..{exp_x1} (len {exp_x1-exp_x0})]")
        if abs(yfr-exp_y) > 4: fails.append(f"{tag} underline y {yfr:.1f} vs {exp_y}")
        if abs(xf0r-exp_x0) > 5: fails.append(f"{tag} underline x0 {xf0r:.1f} vs {exp_x0}")
        if abs(xf1r-exp_x1) > 5: fails.append(f"{tag} underline x1 {xf1r:.1f} vs {exp_x1}")
find_underline(215, 226, 430, 700, "band1 'non-linearities'", 463, 621, 219.5)
find_underline(324, 335, 120, 500, "band4 lead-in", 147, 458, 328)

# ---- red accents ----
print()
def red_span(yf0, yf1, xf0, xf1, tag, exp_x0, exp_x1):
    y0, y1 = int(cv(yf0)), int(cv(yf1))
    x0, x1 = int(cv(xf0)), int(cv(xf1))
    sub = a[y0:y1, x0:x1]
    redm = (sub[:,:,0]>120) & (sub[:,:,1]<90) & (sub[:,:,2]<90)
    ys, xs = np.where(redm)
    if not len(xs):
        fails.append(f"{tag}: no red ink"); print(f"  {tag}: NO RED"); return
    rx0, rx1 = xs.min()/S+xf0, xs.max()/S+xf0
    print(f"  {tag}: red x {rx0:.1f}..{rx1:.1f}   [orig {exp_x0}..{exp_x1}]")
    if abs(rx0-exp_x0) > 6: fails.append(f"{tag} red x0 {rx0:.1f} vs {exp_x0}")
    if abs(rx1-exp_x1) > 6: fails.append(f"{tag} red x1 {rx1:.1f} vs {exp_x1}")
red_span(228, 252, 300, 420, "band2 ReLU", 334, 390)
red_span(268, 292, 640, 830, "band3 max pooling", 679, 805)

# ---- dots ----
print()
DOTS_EXP = [(115,168),(115,208),(115,276),(115,316),(198.5,351.5),(198.5,387),(198.5,422)]
for i,(ecx,ecy) in enumerate(DOTS_EXP):
    x0, x1 = int(cv(ecx-14)), int(cv(ecx+14))
    y0, y1 = int(cv(ecy-12)), int(cv(ecy+12))
    reg = a[y0:y1, x0:x1]
    dm = reg.sum(axis=2) < 250
    ys, xs = np.where(dm)
    if not len(ys):
        fails.append(f"dot{i}: no ink at ({ecx},{ecy})"); continue
    cx, cy = xs.mean()/S+ecx-14, ys.mean()/S+ecy-12
    dxs = (xs.max()-xs.min()+1)/S
    print(f"  dot{i}: center ({cx:.1f},{cy:.1f}) w {dxs:.1f}   [orig ({ecx},{ecy}) d~6.75]")
    if abs(cx-ecx) > 3.5 or abs(cy-ecy) > 3.5: fails.append(f"dot{i} center ({cx:.1f},{cy:.1f}) vs ({ecx},{ecy})")

# ---- containment ----
print("\n== containment ==")
# no ink inside box margin strips (between box border and content bands) beyond expected
inner_all = a[int(cv(158)):int(cv(488)), int(cv(106)):int(cv(855))]
dm_all = inner_all.sum(axis=2) < 420
# bottom strip below band7 descender: frame y 437..488 must be empty
strip = dm_all[int(cv(437))-int(cv(158)):, :]
n = int(strip.sum())
print(f"ink px in box bottom strip (frame y437..488): {n}")
if n > 40: fails.append(f"box bottom strip has {n} ink px (unexpected content below band7)")
# right strip: x 842..855 frame
strip2 = dm_all[:, int(cv(842))-int(cv(106)):]
n2 = int(strip2.sum())
print(f"ink px in box right strip (frame x842..855): {n2}")
if n2 > 40: fails.append(f"box right strip has {n2} ink px")

# ---- colors ----
print("\n== colors ==")
def modal(px):
    q = (px//8)*8
    vals, counts = np.unique(q, axis=0, return_counts=True)
    return "#%02X%02X%02X" % tuple(vals[counts.argmax()])
ty = a[int(cv(90)):int(cv(110)), int(cv(300)):int(cv(660))]
redink = ty[(ty[:,:,0]>120)&(ty[:,:,1]<80)]
print("title ink modal:", modal(redink) if len(redink) else "none", "[orig B81020-washed; build C00000]")
b0 = a[int(cv(163)):int(cv(175)), int(cv(160)):int(cv(560))]
ink = b0[b0.sum(axis=2) < 420]
print("band0 ink modal:", modal(ink) if len(ink) else "none", "[orig #100080; build 00008B]")
bx = a[int(cv(300)), int(cv(110)):int(cv(850))]
print("row300 modal (panel/box):", modal(bx), "[box FFFFFF, panel E9E9E7]")
border = a[int(cv(154)), int(cv(300)):int(cv(700))]
print("box top border modal:", modal(border), "[build 0000AA]")

print()
if fails:
    print(f"SELF-CHECK: FAIL ({len(fails)})")
    for f in fails: print("  -", f)
else:
    print("SELF-CHECK: PASS (all within tolerance)")
