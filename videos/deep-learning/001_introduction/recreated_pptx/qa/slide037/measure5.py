#!/usr/bin/env python3
"""Measure slide_037.jpg pass 5 — fix slicing bug; cube, question, equation, labels;
compare parent 36 slab scale vs slide 37 slab scale."""
from PIL import Image
import numpy as np
from collections import Counter

VID = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
a = np.asarray(Image.open(VID + '/unique_slides/slide_037.jpg').convert('RGB')).astype(int)
b36 = np.asarray(Image.open(VID + '/unique_slides/slide_036.jpg').convert('RGB')).astype(int)

def runs(mask, min_gap=2):
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return []
    out = []
    s = p = idx[0]
    for v in idx[1:]:
        if v - p > min_gap:
            out.append((s, p)); s = v
        p = v
    out.append((s, p))
    return out

# ---- '=' modal color
eq = (a[:, :, 2] > 140) & (a[:, :, 0] < 130) & (a[:, :, 2] - a[:, :, 0] > 60)
z = eq[340:380, 480:525]
print("'=' bbox:", [(y, x) for y in range(340, 380) for x in []] and None or "")
ys, xs = np.where(z)
if len(ys):
    print(f"'=' ink x{480+xs.min()}..{480+xs.max()} y{340+ys.min()}..{340+ys.max()} n={len(ys)}")
    print("modal '=':", Counter(map(tuple, a[340:380, 480:525][z])).most_common(3))

# ---- cube tan region
tan = (a[:, :, 0] > 195) & (a[:, :, 1] > 140) & (a[:, :, 1] < 220) & (a[:, :, 2] > 95) & (a[:, :, 2] < 190)
z = tan[265:515, :]
rp = z.sum(axis=1); cp = z.sum(axis=0)
print("\ncube rows:", [(265 + s0, 265 + e0) for s0, e0 in runs(rp > 10, min_gap=6)])
print("cube cols:", [(s0, e0) for s0, e0 in runs(cp > 10, min_gap=6)])
ys, xs = np.where(z)
print(f"cube bbox x{xs.min()}..{xs.max()} y{265+ys.min()}..{265+ys.max()}")
print("modal tan:", Counter(map(tuple, a[265:515][z])).most_common(3))

# ---- question text
q = a.sum(axis=-1) < 300
z = q[435:495, 55:640]
rp = z.sum(axis=1)
print("\nquestion lines:")
for s0, e0 in runs(rp > 2, min_gap=4):
    xs2 = np.where(z[s0:e0 + 1].sum(axis=0) > 0)[0]
    print(f"  y{435+s0}..{435+e0} h={e0-s0+1} x{55+xs2[0]}..{55+xs2[-1]}")

# ---- equation (red)
r = (a[:, :, 0] > 140) & (a[:, :, 0] - a[:, :, 1] > 60) & (a[:, :, 0] - a[:, :, 2] > 60)
z = r[470:520, 100:500]
rp = z.sum(axis=1)
print("\nequation lines:")
for s0, e0 in runs(rp > 1, min_gap=3):
    xs3 = np.where(z[s0:e0 + 1].sum(axis=0) > 0)[0]
    print(f"  y{470+s0}..{470+e0} h={e0-s0+1} x{100+xs3[0]}..{100+xs3[-1]}")
ys, xs = np.where(z)
print("modal eq red:", Counter(map(tuple, a[470:520, 100:500][z])).most_common(3))

# ---- Depth=5 dims label
z = q[280:320, 700:910]
rp = z.sum(axis=1)
print("\nDepth label lines:")
for s0, e0 in runs(rp > 0, min_gap=3):
    xs4 = np.where(z[s0:e0 + 1].sum(axis=0) > 0)[0]
    print(f"  y{280+s0}..{280+e0} x{700+xs4[0]}..{700+xs4[-1]}")

# ---- RGB label
z = q[258:295, 190:330]
rp = z.sum(axis=1)
print("\nRGB label lines:")
for s0, e0 in runs(rp > 0, min_gap=3):
    xs5 = np.where(z[s0:e0 + 1].sum(axis=0) > 0)[0]
    print(f"  y{258+s0}..{258+e0} x{190+xs5[0]}..{190+xs5[-1]}")

# ---- 3 dims label
z = q[305:345, 45:135]
rp = z.sum(axis=1)
print("\n'3 dims' lines:")
for s0, e0 in runs(rp > 0, min_gap=3):
    xs6 = np.where(z[s0:e0 + 1].sum(axis=0) > 0)[0]
    print(f"  y{305+s0}..{305+e0} x{45+xs6[0]}..{45+xs6[-1]}")

# ---- blue X-circle on slab (cyan/blue ring)
bl = (a[:, :, 2] > 120) & (a[:, :, 2] - a[:, :, 0] > 40)
z = bl[315:385, 235:305]
ys, xs = np.where(z)
if len(ys):
    print(f"\nX-circle bbox x{235+xs.min()}..{235+xs.max()} y{315+ys.min()}..{315+ys.max()} n={len(ys)}")
    print("modal X blue:", Counter(map(tuple, a[315:385, 235:305][z])).most_common(3))

# ---- small labels zones ('5', '3', '7's)
for nm, (yy0, yy1, xx0, xx1) in {
    "'5' above stack": (310, 345, 310, 350),
    "'3' below stack": (385, 420, 300, 340),
    "'7' near dashes top": (325, 360, 270, 310),
    "'7' at slab lower-left": (360, 405, 160, 205),
    "'7' left of slab": (360, 405, 90, 130),
}.items():
    z = q[yy0:yy1, xx0:xx1]
    ys, xs = np.where(z)
    if len(ys):
        print(f"{nm}: x{xx0+xs.min()}..{xx0+xs.max()} y{yy0+ys.min()}..{yy0+ys.max()} n={len(ys)}")
    else:
        print(f"{nm}: empty")

# ---- fan arrows from '3' to filters: black thin lines below stack y392..445
z = q[390:450, 300:470]
rp = z.sum(axis=1)
print("\nfan arrow rows:", [(390 + s0, 390 + e0) for s0, e0 in runs(rp > 2, min_gap=3)])

# ---- parent 36 slab scale comparison (orange mask, same thresholds)
for nm, img in (("36", b36), ("37", a)):
    o = (img[:, :, 0] > 140) & (img[:, :, 0] < 235) & (img[:, :, 1] > 55) & (img[:, :, 1] < 165) & (img[:, :, 2] < 85)
    z = o[150:520, 100:420]
    ys, xs = np.where(z)
    print(f"\nslide {nm} orange (x100..420): x{100+xs.min()}..{100+xs.max()} y{150+ys.min()}..{150+ys.max()} n={len(ys)}")
    print(f"  modal:", Counter(map(tuple, img[150:520, 100:420][z])).most_common(2))

# ---- filter front-row colors at proper y
print("\nfilter front colors y372..386:")
for x in [325, 350, 375, 400, 425, 448]:
    cols = [tuple(a[y, x]) for y in range(372, 387, 3)]
    print(f"  x={x}:", cols)
