#!/usr/bin/env python3
"""Forensics pass 1 for slide_033.jpg: color masks -> bounding boxes."""
import numpy as np
from PIL import Image
import sys

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"frame {W}x{H}")

def mask_bbox(name, mask, min_px=8):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        print(f"{name}: EMPTY")
        return
    print(f"{name}: n={len(xs)} bbox x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]")

def near(c, tol=28):
    return (np.abs(a - np.array(c)).sum(axis=2) <= tol)

def label_regions(mask, name, min_area=30):
    """connected-component labeling, 4-connectivity, on boolean mask"""
    from scipy import ndimage
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_area:
            continue
        out.append((xs.min(), xs.max(), ys.min(), ys.max(), len(xs)))
    out.sort(key=lambda r: (r[2], r[0]))
    print(f"-- {name}: {len(out)} regions (min_area {min_area})")
    for x0, x1, y0, y1, area in out:
        print(f"   x[{x0}..{x1}] y[{y0}..{y1}] area={area}")

try:
    import scipy
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False
    print("no scipy")

# 1. peach panel
peach = near((252, 228, 198), 30)
label_regions(peach, "peach panel FCE4C6", 5000) if HAVE_SCIPY else None

# 2. taupe dot product box
taupe = near((179, 170, 164), 20)
label_regions(taupe, "taupe B3AAA4", 500) if HAVE_SCIPY else None

# 3. orchid softmax
orchid = near((231, 193, 231), 22)
label_regions(orchid, "orchid E7C1E7", 500) if HAVE_SCIPY else None

# 4. light blue sigma box
lblue = near((204, 228, 247), 18)
label_regions(lblue, "light blue CCE4F7", 300) if HAVE_SCIPY else None

# 5. yellow boxes FFFF00
yellow = near((255, 255, 0), 60)
label_regions(yellow, "yellow FFFF00", 200) if HAVE_SCIPY else None

# 6. pale yellow pills FFFFCC
pale_y = near((255, 255, 204), 12)
label_regions(pale_y, "pale yellow FFFFCC", 150) if HAVE_SCIPY else None

# 7. pale green containers EAF6EA
pale_g = near((234, 246, 234), 8)
label_regions(pale_g, "pale green EAF6EA", 400) if HAVE_SCIPY else None

# 8. mini-vector squares
for c, nm in [((237, 226, 138), "sq EDE28A"), ((201, 168, 224), "sq C9A8E0"), ((242, 184, 198), "sq F2B8C6")]:
    m = near(c, 26)
    label_regions(m, nm, 15) if HAVE_SCIPY else None

# 9. white boxes inside containers (pure white)
white = near((255, 255, 255), 6)
label_regions(white, "white boxes", 150) if HAVE_SCIPY else None
