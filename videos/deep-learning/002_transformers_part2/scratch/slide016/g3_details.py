#!/usr/bin/env python3
# g3_details.py — detail gaps left by m2/m3:
#   1. blue ink comps in the embedding area (bracket glyphs around pills?)
#   2. dark-navy comps in the embedding area (pill outlines / glyph ink)
#   3. embedding X_N vector-label bboxes (red, fx 140..182)
#   4. glyph core colors: embedding circle x_i, output y_i, matrix w_ij
#   5. right annotations: per-LINE bboxes (m2 merged all 5 into one block)
#   6. caption line-2 'Head N' blue vs red confirmation (x-run extents)
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

def darkcore(x0, y0, x1, y1, n=15):
    p = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    lum = p.sum(axis=1)
    idx = np.argsort(lum)[:n]
    m = np.median(p[idx], axis=0).astype(int)
    return "#%02X%02X%02X" % (m[0], m[1], m[2])

print("=== 1. BLUE ink comps, embedding area (fx 60..315, fy 112..318) ===")
reg = np.zeros((H, W), bool); reg[112:319, 60:316] = True
bm = reg & ((B - (R + G) / 2 > 30) & (B > 100))
bcs = cc(bm, 8)
print(f"  {len(bcs)} comps")
for c in bcs:
    px = a[c[1]:c[3] + 1, c[0]:c[2] + 1][bm[c[1]:c[3] + 1, c[0]:c[2] + 1]]
    m = np.median(px, axis=0).astype(int)
    print(f"    fx {c[0]:3d}..{c[2]:3d}  fy {c[1]:3d}..{c[3]:3d}  w{c[4]:3d} h{c[5]:3d} ({c[6]:4d}px)  median #{m[0]:02X}{m[1]:02X}{m[2]:02X}")

print("=== 2. DARK-NAVY comps, embedding area (B-R>=8, B-G>=5, sum<420) ===")
nm_ = reg & ((B - R >= 8) & (B - G >= 5) & (R + G + B < 420))
ncs = cc(nm_, 8)
print(f"  {len(ncs)} comps")
for c in ncs[:30]:
    px = a[c[1]:c[3] + 1, c[0]:c[2] + 1][nm_[c[1]:c[3] + 1, c[0]:c[2] + 1]]
    m = np.median(px, axis=0).astype(int)
    print(f"    fx {c[0]:3d}..{c[2]:3d}  fy {c[1]:3d}..{c[3]:3d}  w{c[4]:3d} h{c[5]:3d} ({c[6]:4d}px)  median #{m[0]:02X}{m[1]:02X}{m[2]:02X}")

print("=== 3. EMBEDDING X_N vector labels (red comps fx 140..182, fy 128..316) ===")
reg2 = np.zeros((H, W), bool); reg2[128:317, 140:183] = True
rm = reg2 & ((R - (G + B) / 2 > 50) & (R > 110))
rcs = cc(rm, 5)
for c in rcs:
    print(f"    fx {c[0]:3d}..{c[2]:3d}  fy {c[1]:3d}..{c[3]:3d}  w{c[4]:3d} h{c[5]:3d} ({c[6]:4d}px)")

print("=== 4. GLYPH CORE COLORS ===")
print(f"  embedding circle x_i (row1 c1, fx 182..200 fy 144..162): {darkcore(182, 144, 200, 162)}")
print(f"  output y_i (g1 row1 first glyph, fx 300..318 fy 340..354): {darkcore(300, 340, 318, 354)}")
print(f"  matrix w_ij (Head1 cell1, fx 320..340 fy 155..167): {darkcore(320, 155, 340, 167)}")

print("=== 5. RIGHT ANNOTATIONS: per-LINE bboxes (red, fx 826..914, fy 316..498) ===")
reg3 = np.zeros((H, W), bool); reg3[316:499, 826:915] = True
am = reg3 & ((R - (G + B) / 2 > 45) & (R > 100))
acs = cc(am, 4)
rowink = am[:, 826:915].sum(axis=1)
lines = []
cur = None
last = None
for fy in range(316, 499):
    if rowink[fy] >= 2:
        if cur is None:
            cur = [fy, fy]
        elif last is not None and fy - last > 4:
            lines.append(cur); cur = [fy, fy]
        cur[1] = fy
        last = fy
if cur is not None:
    lines.append(cur)
for i, (y0, y1) in enumerate(lines, 1):
    sub = am[y0:y1 + 1, 826:915]
    ys2, xs2 = np.nonzero(sub)
    x0, x1 = int(xs2.min()) + 826, int(xs2.max()) + 826
    sy0, sy1 = y0 / 0.955556, y1 / 0.955556
    sx0, sx1 = (x0 - 17.628) / 0.961232, (x1 - 17.628) / 0.961232
    print(f"  line {i:2d}: fx {x0}..{x1} fy {y0}..{y1} (h{y1 - y0 + 1})  -> slide x {sx0:.1f}..{sx1:.1f} y {sy0:.1f}..{sy1:.1f}")

print("=== 6. CAPTION line-2 runs per group (fy 496..507, red vs blue) ===")
reg4 = np.zeros((H, W), bool); reg4[496:508, 300:800] = True
cm_r = reg4 & ((R - (G + B) / 2 > 45) & (R > 100))
cm_b = reg4 & ((B - (R + G) / 2 > 30) & (B > 100))
for nm, m in (("RED", cm_r), ("BLUE", cm_b)):
    colmask = m.any(axis=0)
    runs = []
    inrun = False
    for x in range(300, 800):
        if colmask[x] and not inrun:
            s = x; inrun = True
        elif not colmask[x] and inrun:
            runs.append((s, x - 1)); inrun = False
    merged = []
    for s, e in runs:
        if merged and s - merged[-1][1] <= 5:
            merged[-1][1] = e
        else:
            merged.append([s, e])
    print(f"  {nm} runs: " + "  ".join(f"{s}..{e}(w{e - s + 1})" for s, e in merged))

print("=== 7. MATRIX BRACKET pair: left-bracket tick cols + right-bracket spine proof ===")
reg5 = np.zeros((H, W), bool); reg5[108:318, 296:336] = True
lm = reg5 & ((R - (G + B) / 2 > 45) & (R > 100))
lcs = cc(lm, 10)
for c in lcs:
    print(f"  L-bracket comp fx {c[0]}..{c[2]} fy {c[1]}..{c[3]} w{c[4]} h{c[5]} ({c[6]}px)")
reg6 = np.zeros((H, W), bool); reg6[108:318, 770:800] = True
rm2 = reg6 & ((R - (G + B) / 2 > 45) & (R > 100))
rcs2 = cc(rm2, 10)
for c in rcs2:
    print(f"  R-bracket comp fx {c[0]}..{c[2]} fy {c[1]}..{c[3]} w{c[4]} h{c[5]} ({c[6]}px)")
