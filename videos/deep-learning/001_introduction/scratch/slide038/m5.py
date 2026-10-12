#!/usr/bin/env python3
"""Slide 038 forensics pass 5: diagram region components (slabs, circles, ink)."""
from PIL import Image
import numpy as np
from scipy import ndimage

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[..., 0], a[..., 1], a[..., 2]

# restrict to diagram box interior (borders excluded)
X0, X1, Y0, Y1 = 186, 807, 254, 508
sub = np.zeros((H, W), bool)
sub[Y0:Y1, X0:X1] = True

masks = {
    "brown_dark":  sub & (r > 100) & (g > 40) & (g < 120) & (b < 90) & ((r - b) > 50),
    "tan":         sub & (r > 150) & (g > 100) & (g < 180) & (b < 130) & ((r - b) > 60),
    "cyan":        sub & (g > 130) & (b > 130) & (r < 130),
    "green":       sub & (g > 110) & (r < 110) & (b < 110),
    "brightred":   sub & (r > 170) & (g < 90) & (b < 90),
    "yellow":      sub & (r > 190) & (g > 170) & (b < 140),
    "purple":      sub & (r > 80) & (r < 190) & (b > 110) & (g < 90) & ((b - g) > 40),
    "lightblue":   sub & (b > 190) & (g > 140) & (g < 200) & (r < 170) & ((b - r) > 50),
    "black_ink":   sub & (r < 110) & (g < 110) & (b < 110),
}

def comps(mask, min_px=12, label=""):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_px: continue
        out.append((len(ys), xs.min(), xs.max(), ys.min(), ys.max()))
    out.sort(reverse=True)
    print(f"--- {label}: {len(out)} components >= {min_px}px ---")
    for (npx, x0, x1, y0, y1) in out[:25]:
        # modal color
        mm = np.zeros((H, W), bool)
        mm[y0:y1 + 1, x0:x1 + 1] = True
        sel = mask & mm
        px = a[sel]
        med = np.median(px, axis=0).astype(int) if len(px) else None
        print(f"  n={npx:5d} x {x0:3d}..{x1:3d} y {y0:3d}..{y1:3d}  w={x1-x0+1:3d} h={y1-y0+1:3d} modal={med}")
    return out

for name in ["brown_dark", "tan", "cyan", "green", "brightred", "yellow", "purple", "lightblue"]:
    comps(masks[name], 25, name)

print()
# black ink components in diagram region — annotations/text
lab, n = ndimage.label(masks["black_ink"], structure=np.ones((3, 3)))
out = []
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 8: continue
    out.append((len(ys), xs.min(), xs.max(), ys.min(), ys.max()))
out.sort(key=lambda t: (t[3], t[1]))
print(f"--- black_ink components >=8px ({len(out)}) sorted by y ---")
for (npx, x0, x1, y0, y1) in out[:60]:
    print(f"  n={npx:5d} x {x0:3d}..{x1:3d} y {y0:3d}..{y1:3d}  w={x1-x0+1:3d} h={y1-y0+1:3d}")
