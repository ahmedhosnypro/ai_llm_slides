#!/usr/bin/env python3
"""Pass 5: proper cursor/residual scan + font fitting for typed texts."""
import numpy as np
from PIL import Image, ImageFont

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
im = np.asarray(Image.open(f"{BASE}/unique_slides/slide_034.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def runs(idx):
    out, s, p = [], None, None
    for i in idx:
        if s is None: s = p = i
        elif i == p + 1: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return out

print("== cursor/anomaly scan: content-ink outside known content rects ==")
white = (r > 246) & (g > 246) & (b > 246)
panel = (abs(r - 231) < 12) & (abs(g - 233) < 12) & (abs(b - 230) < 12)
ink = ~white & ~panel
# subtract all known content rects (with margins)
for (x0, y0, x1, y1) in [(55, 60, 900, 500),    # box + title + everything inside
                          (40, 40, 925, 520)]:   # whole panel — too broad? no: we want ink OUTSIDE these
    pass
res = ink.copy()
res[60:500, 55:900] = False   # everything inside the box/title zone
ys, xs = np.where(res)
print(f"  residual ink px outside x55..900 y60..500: {len(xs)}")
if len(xs):
    rr = runs(sorted(set(int(x) for x in xs))[:0] or [])
    pts = set(zip(ys.tolist(), xs.tolist()))
    seen, clusters = set(), []
    for p in pts:
        if p in seen: continue
        stack = [p]; comp = []; seen.add(p)
        while stack:
            cy, cx = stack.pop(); comp.append((cy, cx))
            for dy in (-2, -1, 0, 1, 2):
                for dx in (-2, -1, 0, 1, 2):
                    q = (cy + dy, cx + dx)
                    if q in pts and q not in seen:
                        seen.add(q); stack.append(q)
        clusters.append(comp)
    big = [c for c in clusters if len(c) > 3]
    print(f"  clusters>3: {len(big)}")
    for c in sorted(big, key=len, reverse=True)[:15]:
        ys_ = [p[0] for p in c]; xs_ = [p[1] for p in c]
        print(f"    n={len(c)} x {min(xs_)}..{max(xs_)} y {min(ys_)}..{max(ys_)} sample {tuple(im[c[0][0], c[0][1]])}")

print("== known-rect sweep INSIDE panel for unexplained ink ==")
# inside panel but outside: title, box interior contents, box strokes
res2 = ink.copy()
res2[60:500, 55:900] = False
res2[500:520, 40:925] = False
# box strokes are inside 60..500 — already subtracted; also subtract panel border cols
res2[40:520, 40:62] = False
res2[40:520, 895:925] = False
res2[40:50, 40:925] = False
ys, xs = np.where(res2)
print(f"  residual2: {len(xs)}")
if len(xs):
    pts = set(zip(ys.tolist(), xs.tolist()))
    seen, clusters = set(), []
    for p in pts:
        if p in seen: continue
        stack = [p]; comp = []; seen.add(p)
        while stack:
            cy, cx = stack.pop(); comp.append((cy, cx))
            for dy in (-2, -1, 0, 1, 2):
                for dx in (-2, -1, 0, 1, 2):
                    q = (cy + dy, cx + dx)
                    if q in pts and q not in seen:
                        seen.add(q); stack.append(q)
        clusters.append(comp)
    big = [c for c in clusters if len(c) > 3]
    for c in sorted(big, key=len, reverse=True)[:15]:
        ys_ = [p[0] for p in c]; xs_ = [p[1] for p in c]
        print(f"    n={len(c)} x {min(xs_)}..{max(xs_)} y {min(ys_)}..{max(ys_)} sample {tuple(im[c[0][0], c[0][1]])}")

print("== font fitting ==")
def fit(font_path, text, target_adv, target_cap, sizes):
    for s in sizes:
        f = ImageFont.truetype(font_path, s)
        bb = f.getbbox(text)
        adv = bb[2] - bb[0]
        capbb = f.getbbox("H")
        cap = capbb[3] - capbb[1]
        print(f"  {font_path.split('/')[-1]} {s}pt: adv={adv} (target {target_adv}), capH={cap} (target {target_cap})")

ARIALB = "/usr/share/fonts/TTF/Arialbd.TTF"
LIBB = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
COMIC = "/usr/share/fonts/TTF/Comic.TTF"
COMICB = "/usr/share/fonts/TTF/Comicbd.TTF"

print(" TITLE 'What would a k-D filter looks like?' target adv 565, cap 26:")
for fp in (ARIALB, LIBB):
    fit(fp, "What would a k-D filter looks like?", 565, 26, range(34, 40))
print(" HEADER 'e.g. Sobel 2-D filter' target adv 250 (x86..335), asc-desc 35 (y209..243):")
for fp in (COMIC, COMICB):
    for s in (22, 23, 24, 25, 26):
        f = ImageFont.truetype(fp, s)
        bb = f.getbbox("e.g. Sobel 2-D filter")
        adb = f.getbbox("eg")  # x-height-ish
        bbH = f.getbbox("Sg")  # ascender+descender
        print(f"  {fp.split('/')[-1]} {s}pt: adv={bb[2]-bb[0]}, Sg-span={bbH[3]-bbH[1]}")
print(" LABEL '3-D Filter' target adv 104 (x749..852), cap 17 (y234..250):")
for fp in (ARIALB, LIBB):
    fit(fp, "3-D Filter", 104, 17, range(21, 26))
