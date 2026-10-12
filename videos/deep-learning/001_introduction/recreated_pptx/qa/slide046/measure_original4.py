#!/usr/bin/env python3
"""PIL forensics pass 4 — slide_046.jpg: text starts, box text metrics, matrix
letters, paren glyphs, photo rects, settled colors. Then crop tiger assets."""
from PIL import Image, ImageFont
import numpy as np
from collections import Counter
import os, json

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
IMG = f"{BASE}/unique_slides/slide_046.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

redm   = (R > 110) & (R - G > 25) & (R - B > 25)
bluem  = (B - R > 30) & (B - G > 25) & (B > 100)
greenm = (G - R > 40) & (G - B > 40) & (G > 120)
textm  = (R + G + B < 620) & ~redm & ~bluem & ~greenm

def bb(x0, y0, x1, y1, mask, label):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0: print(f"{label:34s} EMPTY"); return None
    r = (x0+int(xs.min()), y0+int(ys.min()), x0+int(xs.max()), y0+int(ys.max()))
    print(f"{label:34s} x {r[0]}..{r[2]}  y {r[1]}..{r[3]}  (w {r[2]-r[0]+1} h {r[3]-r[1]+1})")
    return r

def core(x0, y0, x1, y1, mask, label, pct=10):
    sub = a[y0:y1, x0:x1][mask[y0:y1, x0:x1]]
    if len(sub) == 0: print(f"{label}: no px"); return None
    lum = sub.sum(axis=1)
    idx = np.argsort(lum)[:max(1, int(len(lum)*pct/100))]
    print(f"{label:34s} core {Counter(map(tuple, sub[idx])).most_common(2)}")

print("== bullet text starts (col profiles) ==")
for (y0, y1, lbl) in [(148, 172, "main"), (174, 192, "sub1"), (196, 216, "sub2"), (221, 240, "sub3")]:
    prof = textm[y0:y1, 110:780].sum(axis=0)
    runs = []
    s = None
    for i, v in enumerate(prof):
        if v > 0 and s is None: s = i
        elif v == 0 and s is not None:
            if i - s >= 1: runs.append((110+s, 110+i-1))
            s = None
    if s is not None: runs.append((110+s, 110+len(prof)-1))
    # merge runs separated by <=4 px (intra-word gaps)
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= 4: merged[-1] = (merged[-1][0], r[1])
        else: merged.append(list(r))
    print(f"  {lbl}: first runs {merged[:4]} ... last x {merged[-1][1] if merged else '-'}")

print("== box text (marker vs text split) ==")
for (y0, y1, lbl) in [(250, 278, "box1 'Max pooling'"), (284, 312, "box2 'Average pooling'")]:
    prof = textm[y0:y1, 110:292].sum(axis=0)
    runs, s = [], None
    for i, v in enumerate(prof):
        if v > 0 and s is None: s = i
        elif v == 0 and s is not None:
            runs.append((110+s, 110+i-1)); s = None
    if s is not None: runs.append((110+s, 110+len(prof)-1))
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= 4: merged[-1] = (merged[-1][0], r[1])
        else: merged.append(list(r))
    print(f"  {lbl}: runs {merged}")

print("== matrix letters (dark-on-green, borders excluded) ==")
for lbl, (cx0, cy0, cx1, cy1) in [("a", (176, 340, 204, 364)), ("b", (209, 340, 238, 364)),
                                   ("c", (176, 370, 204, 395)), ("d", (209, 370, 238, 395)),
                                   ("z", (318, 356, 344, 379))]:
    bb(cx0, cy0, cx1, cy1, textm, f"letter '{lbl}'")

print("== parens and == (photo cols excluded) ==")
# '(' between Pool text and photo: x 412..422
bb(410, 330, 423, 415, textm, "'(' paren")
# ')' right of photo: x 608..620 — photo ends 610; check
bb(611, 330, 621, 415, textm, "')' paren")
# '==' x 622..655
bb(622, 330, 658, 415, textm, "'==' ink")
bb(622, 350, 658, 380, textm, "'==' restricted")
core(370, 355, 410, 380, textm, "'Pool' text core")
core(622, 355, 655, 380, textm, "'==' core")
core(410, 335, 423, 415, textm, "'(' core")
core(611, 335, 621, 415, textm, "')' core")

print("== tiger photo rects (row/col density) ==")
notw = (R + G + B < 690)
for x0, x1, y0, y1, lbl in [(415, 620, 315, 420, "large"), (660, 780, 330, 396, "small")]:
    colp = notw[y0:y1, x0:x1].sum(axis=0)
    rowp = notw[y0:y1, x0:x1].sum(axis=1)
    xs = [x0+i for i, v in enumerate(colp) if v > (y1-y0)*0.5]
    ys = [y0+i for i, v in enumerate(rowp) if v > (xs[-1]-xs[0] if xs else 1)*0.5]
    print(f"  {lbl}: x {xs[0]}..{xs[-1]} y {ys[0]}..{ys[-1]} (w {xs[-1]-xs[0]+1} h {ys[-1]-ys[0]+1})")

print("== settled colors ==")
core(130, 131, 878, 137, redm, "panel border red")
core(300, 60, 700, 130, redm, "title red")
core(245, 248, 320, 313, bluem, "box border blue (vert strokes only)")
core(660, 396, 800, 413, bluem, "caption blue")
print("  matrix green modal:", Counter(map(tuple, a[340:395, 175:240][greenm[340:395, 175:240]])).most_common(1))
print("  gray chrome modal:", Counter(map(tuple, a[100:120, 480:600])).most_common(1))
print("  panel white modal:", Counter(map(tuple, a[420:450, 340:600])).most_common(1))

# ---------- crop tiger assets ----------
os.makedirs(f"{BASE}/recreated_pptx/build/assets", exist_ok=True)
# large tiger: x 424..610 y 325..413 → refine to density box above
im.crop((424, 325, 611, 414)).save(f"{BASE}/recreated_pptx/build/assets/tiger_large.png")
im.crop((670, 342, 768, 390)).save(f"{BASE}/recreated_pptx/build/assets/tiger_small.png")
print("assets cropped:",
      os.path.getsize(f"{BASE}/recreated_pptx/build/assets/tiger_large.png"),
      os.path.getsize(f"{BASE}/recreated_pptx/build/assets/tiger_small.png"))

# ---------- font fitting round 2 ----------
print("== font fits round 2 ==")
FP = "/usr/share/fonts/liberation"
def fit(fontfile, text, target_w, lo=8, hi=60):
    best = None
    for s10 in range(lo*10, hi*10):
        s = s10/10
        f = ImageFont.truetype(f"{FP}/{fontfile}", int(round(s*4)))
        b = f.getbbox(text)
        wpx = (b[2]-b[0])/4
        err = abs(wpx - target_w)
        if best is None or err < best[0]: best = (err, s, wpx)
    print(f"  {fontfile:28s} '{text[:30]}' tgt={target_w} -> {best[1]:.1f}pt (w {best[2]:.1f})")
    return best[1]

fit("LiberationSans-Bold.ttf", "POOLING", 161)
fit("LiberationSans-Regular.ttf", "Aggregate multiple values into a single value", 384)
fit("LiberationSans-Regular.ttf", "Invariance to small transformations", 256)
fit("LiberationSans-Regular.ttf", "Reduces the size of the layer output/input to next layer \u2192 Faster computations", 604)
fit("LiberationSans-Regular.ttf", "Keeps most important information for the next layer", 391)
fit("LiberationSerif-Italic.ttf", "Pool", 38)
fit("LiberationSans-Bold.ttf", "Size is reduced", 98)
