#!/usr/bin/env python3
"""Probe 2: locate render's stray red ink above h-arrow; measure rotated diag labels
in rotated space; corrected frame conversion (IX = rx*0.46139+18.63, IY = ry*0.45867)."""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
K = 150 / 72.0
SX = lambda fx: (fx - 18.63) / 0.96123 * K
SY = lambda fy: fy / 0.95556 * K
IX = lambda rx: rx * 0.46139 + 18.63
IY = lambda ry: ry * 0.45867

O = np.asarray(Image.open(f"{VID}/unique_slides/slide_042.jpg").convert("RGB")).astype(int)
R = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide042/render_3.png").convert("RGB")).astype(int)

def red(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 130) & (r - g > 60) & (r - b > 60)

ro, rr = red(O), red(R)

def fr(b):  # render bbox -> frame tuple
    return None if b is None else (round(IX(b[0]), 1), round(IY(b[1]), 1), round(IX(b[2]), 1), round(IY(b[3]), 1))

def bb(mask, x0, y0, x1, y1):
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    m = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)

print("== render: red ink columns in rows 1012..1032 (above h-arrow heads), x1350..1700:")
sub = rr[1012:1032, 1350:1700]
cols = np.nonzero(sub.sum(axis=0) > 0)[0]
if len(cols):
    print("   cols(px):", 1350 + cols.min(), "..", 1350 + cols.max(), " -> frame",
          round(IX(1350 + cols.min()), 1), "..", round(IX(1350 + cols.max()), 1), " count", int(sub.sum()))
    # row extent per column cluster
    ys, xs = np.nonzero(sub)
    print("   rows(px):", 1012 + ys.min(), "..", 1012 + ys.max(), " -> frame",
          round(IY(1012 + ys.min()), 1), "..", round(IY(1012 + ys.max()), 1))
else:
    print("   none")

print("== render: same region rows 1000..1012?")
sub2 = rr[1000:1012, 1350:1700]
print("   count:", int(sub2.sum()))

print("== orig: red ink in rows y460..484 x645..800 (Channels band incl. above):")
b = bb(ro, 645, 460, 800, 484); print("  ", b)

print("== rotated diag labels in rotated space (+46 deg so text is horizontal):")
from scipy import ndimage
def rot_measure(mask, x0, y0, x1, y1, name):
    crop = mask[int(y0):int(y1), int(x0):int(x1)]
    # rotate so the -46deg text becomes horizontal: scipy rotates counterclockwise for positive angle
    rc = ndimage.rotate(crop.astype(np.uint8), -46, reshape=True, order=0)
    ys, xs = np.nonzero(rc)
    if len(xs) == 0:
        print(f"   {name}: none"); return
    # profile rows to separate arrow band from label bands
    rows = rc.sum(axis=1)
    nz = np.nonzero(rows)[0]
    print(f"   {name}: rotated-space bbox x {xs.min()}..{xs.max()} y {nz.min()}..{nz.max()}  (crop {crop.shape})")
    # find horizontal ink bands (label lines vs arrow shaft)
    bands, s = [], None
    for i, v in enumerate(rows):
        if v > 0 and s is None: s = i
        elif v == 0 and s is not None: bands.append((s, i - 1)); s = None
    if s is not None: bands.append((s, len(rows) - 1))
    merged = []
    for b0, b1 in bands:
        if merged and b0 - merged[-1][1] <= 3: merged[-1] = (merged[-1][0], b1)
        else: merged.append((b0, b1))
    for (b0, b1) in merged:
        seg = rc[b0:b1 + 1]
        xs2 = np.nonzero(seg.sum(axis=0))[0]
        print(f"      band y {b0}..{b1} (h={b1-b0+1}) x {xs2.min()}..{xs2.max()} (w={xs2.max()-xs2.min()+1})")
    return rc

print(" ORIG diag region (frame 780..880, 360..490):")
rot_measure(ro, 780, 360, 880, 490, "orig")
print(" RENDER diag region:")
x0, y0, x1, y1 = SX(780), SY(360), SX(880), SY(490)
rot_measure(rr, x0, y0, x1, y1, "render")

print("== h-label bands, rotated? no - horizontal. orig vs render (corrected):")
print("  Channels  orig:", bb(ro, 645, 465, 790, 484), " render:", fr(bb(rr, SX(645), SY(465), SX(790), SY(484))))
print("  (4F)      orig:", bb(ro, 645, 483, 790, 502), " render:", fr(bb(rr, SX(645), SY(483), SX(790), SY(502))))
print("== v-arrow label strip (Feature Vector) orig vs render:")
print("  orig:", bb(ro, 615, 325, 640, 470), " render:", fr(bb(rr, SX(615), SY(325), SX(640), SY(470))))
print("== orig label-box borders with loose mask:")
def redloose(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 150) & (r - g > 30) & (r - b > 30)
lo = redloose(O)
for name, (x0, y0, x1, y1) in dict(Lbox=(70, 188, 312, 244), Mbox=(335, 186, 604, 242), Rbox=(620, 158, 880, 234)).items():
    print(f"  {name}:", bb(lo, x0, y0, x1, y1))
