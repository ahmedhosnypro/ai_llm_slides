#!/usr/bin/env python3
"""measure1 — slide 022 frame: chrome landmarks + mapping fit.
Frames are ~0.958-scale zoomed-out captures with black letterbox below.
Fit the four chrome stroke centers with red-weighted subpixel centroids."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(float)
H, W, _ = a.shape
print("frame size:", W, H)

R, Gc, B = a[..., 0], a[..., 1], a[..., 2]
redness = R - (Gc + B) / 2.0

# --- chrome border strokes: thin red verticals at left/right, horizontal at top/bottom
# search windows (from certified 020/021: left ~57-61, right ~900-904, top ~41-45, bottom ~514-518)
def centroid_subpix(profile, lo, hi):
    ys = np.arange(lo, hi)
    wgt = np.clip(profile[lo:hi], 0, None)
    if wgt.sum() <= 0:
        return None, 0.0
    c = (ys * wgt).sum() / wgt.sum()
    peak = wgt.max()
    return c, peak

# left stroke: x window 50..70, rows 100..400 (avoid title/box ink)
profL = redness[100:400, :].mean(axis=0)
cL, pL = centroid_subpix(profL, 50, 70)
# right stroke: x 893..910
profR = redness[100:400, :].mean(axis=0)
cR, pR = centroid_subpix(profR, 893, 910)
# top stroke: rows 35..50, x 150..800
profT = redness[:, 150:800].mean(axis=1)
cT, pT = centroid_subpix(profT, 35, 50)
# bottom stroke: rows 508..522 (letterbox edge at ~516-517)
profB = redness[:, 150:800].mean(axis=1)
cB, pB = centroid_subpix(profB, 508, 522)

print(f"left   stroke center: {cL:.2f} (peak {pL:.1f})")
print(f"right  stroke center: {cR:.2f} (peak {pR:.1f})")
print(f"top    stroke center: {cT:.2f} (peak {pT:.1f})")
print(f"bottom stroke center: {cB:.2f} (peak {pB:.1f})")

# profile printouts for verification
print("\nleft x-profile rows100-400 (50..70):")
for x in range(50, 70):
    print(f"  x={x}: {profL[x]:.1f}")
print("\nright x-profile (893..910):")
for x in range(893, 910):
    print(f"  x={x}: {profR[x]:.1f}")
print("\ntop y-profile (35..50):")
for y in range(35, 50):
    print(f"  y={y}: {profT[y]:.1f}")
print("\nbottom y-profile (505..525):")
for y in range(505, 525):
    print(f"  y={y}: {profB[y]:.1f}")

# mapping: chrome panel in slide pts = 42..919 (incl border), 45..540
# left stroke center ~ 42.5? certified fits: 020 ax=18.628 sx=0.961231; 021 ax=18.13
# Solve from left/right/top/bottom stroke centers as in certified runs:
sx = (cR - cL) / (918 - 42)
ax = cL - sx * 42
sy = (cB - cT) / (540 - 45)
ay = cT - sy * 45
print(f"\nfit: slide_x = (frame_x - {ax:.3f}) / {sx:.6f}")
print(f"     slide_y = (frame_y - {ay:.3f}) / {sy:.6f}")

# badge cross-check: yellow bbox center
yellow = (R > 200) & (Gc > 200) & (B < 140)
ys, xs = np.nonzero(yellow)
if len(xs):
    m = (xs > 850) & (ys < 110)
    print(f"badge yellow bbox center: ({xs[m].mean():.1f}, {ys[m].mean():.1f}) n={m.sum()}")
