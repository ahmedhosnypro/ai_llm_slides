#!/usr/bin/env python3
# v1_spotverify.py — spot-verify 3 banked values (m1/m2), no re-derivation:
#   (a) title ink bbox      banked m2: fx 116..805, fy 56..76
#   (b) badge yellow bbox   banked m1: fx 859..892, fy 57..84
#   (c) equals ink bbox     banked m2: fx 268..297, fy 385..425
# Plus (d): any-ink row-band profile fy 40..140 to place EVERY text row between
# border top and matrix headers (settles the subtitle-position gap: m2's title
# scan (fy 48..100) found nothing below fy 76 and its subtitle scan started at
# fy 100, so band fy 77..99 was never scanned for ANY color).
from PIL import Image
import numpy as np
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_016.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def cc(mask, minpx=4):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    comps = []
    for sl in ndimage.find_objects(lab):
        ys, xs = sl
        npx = int(mask[sl].sum())
        if npx >= minpx:
            comps.append((xs.start, ys.start, xs.stop - 1, ys.stop - 1,
                          xs.stop - xs.start, ys.stop - ys.start, npx))
    return sorted(comps, key=lambda c: (c[1], c[0]))

def check(name, got, banked, tol=2):
    ok = all(abs(g - b) <= tol for g, b in zip(got, banked))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got}  banked {banked}  (tol {tol})")

print("=== (a) TITLE re-scan (red mask, fx 60..900, fy 40..112) ===")
reg = np.zeros((H, W), bool); reg[40:112, 60:901] = True
tm = reg & ((R - (G + B) / 2 > 50) & (R > 110))
tc = cc(tm, 6)
x0 = min(c[0] for c in tc); x1 = max(c[2] for c in tc)
y0 = min(c[1] for c in tc); y1 = max(c[3] for c in tc)
print(f"title ink bbox fx {x0}..{x1} fy {y0}..{y1}  ({len(tc)} comps)")
check("title bbox", [x0, x1, y0, y1], [116, 805, 56, 76], tol=2)

print("=== (b) BADGE yellow re-scan (fx 840..915, fy 40..110) ===")
reg2 = a[40:110, 840:916]
ym = (reg2[:, :, 0] > 215) & (reg2[:, :, 1] > 195) & (reg2[:, :, 2] < 175)
ys, xs = np.nonzero(ym)
bx0, bx1 = int(xs.min()) + 840, int(xs.max()) + 840
by0, by1 = int(ys.min()) + 40, int(ys.max()) + 40
print(f"badge yellow bbox fx {bx0}..{bx1} fy {by0}..{by1}")
check("badge bbox", [bx0, bx1, by0, by1], [859, 892, 57, 84], tol=2)

print("=== (c) EQUALS re-scan (fx 255..301, fy 383..428) ===")
reg3 = np.zeros((H, W), bool); reg3[383:429, 255:302] = True
em = reg3 & ((R - (G + B) / 2 > 45) & (R > 100))
ec = cc(em, 8)
for c in ec:
    print(f"    comp fx {c[0]}..{c[2]} fy {c[1]}..{c[3]} w{c[4]} h{c[5]} ({c[6]}px)")
x0 = min(c[0] for c in ec); x1 = max(c[2] for c in ec)
y0 = min(c[1] for c in ec); y1 = max(c[3] for c in ec)
print(f"= ink bbox fx {x0}..{x1} fy {y0}..{y1}")
check("equals bbox", [x0, x1, y0, y1], [268, 297, 385, 425], tol=2)

print("=== (d) ANY-INK row bands fy 40..140 (dev from panel gray E9E9E7 > 55, fx 50..910) ===")
dev = np.abs(a - np.array([233, 233, 231])).max(axis=2)
ink = dev > 55
rows = []
for fy in range(40, 141):
    n = int(ink[fy, 50:911].sum())
    rows.append((fy, n))
bands = []
cur = None
last_fy_with_ink = None
for fy, n in rows:
    if n >= 3:
        if cur is None:
            cur = [fy, fy, 0, 0]
        else:
            if last_fy_with_ink is not None and fy - last_fy_with_ink > 4:
                bands.append(cur); cur = [fy, fy, 0, 0]
        cur[1] = fy
        sl = ink[fy, 50:911]
        cur[2] += int((sl & ((R[fy, 50:911] - (G[fy, 50:911] + B[fy, 50:911]) / 2 > 50) & (R[fy, 50:911] > 110))).sum())
        cur[3] += int((sl & ((B[fy, 50:911] - (R[fy, 50:911] + G[fy, 50:911]) / 2 > 35) & (B[fy, 50:911] > 110))).sum())
        last_fy_with_ink = fy
if cur is not None:
    bands.append(cur)
for (b0, b1, nr, nb) in bands:
    sub = ink[b0:b1 + 1, 50:911]
    ys2, xs2 = np.nonzero(sub)
    print(f"  band fy {b0}..{b1}  fx {int(xs2.min()) + 50}..{int(xs2.max()) + 50}  red_px {nr}  blue_px {nb}")
