#!/usr/bin/env python3
"""Forensics pass 5: find arrow strokes + dashed borders at full resolution."""
import numpy as np
from PIL import Image
from scipy import ndimage

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[..., 0], a[..., 1], a[..., 2]

# any reddish ink: R well above both G and B
reddish = (R - G > 55) & (R - B > 55) & (R > 120)
lab, n = ndimage.label(reddish, np.ones((3, 3)))
out = []
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 6:
        continue
    out.append((int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), len(xs)))
out.sort(key=lambda r: (r[2] // 10, r[0]))
print(f"== REDDISH clusters (R-G>55,R-B>55,R>120): {len(out)}")
for x0, x1, y0, y1, area in out:
    w_, h_ = x1 - x0 + 1, y1 - y0 + 1
    # sample the modal color of the cluster's darkest pixels
    sel = a[y0:y1 + 1, x0:x1 + 1][reddish[y0:y1 + 1, x0:x1 + 1]]
    med = np.median(sel, axis=0).astype(int)
    kind = "H-stroke" if h_ <= 5 and w_ > 8 else ("V-stroke" if w_ <= 5 and h_ > 8 else ("diag" if area < 300 else "blob/text"))
    print(f"  x[{x0}..{x1}] y[{y0}..{y1}] w={w_} h={h_} a={area} med={tuple(med)} {kind}")

# greenish strokes (dashed containers + connectors): G dominant
grn = (G - R > 35) & (G - B > 15) & (G > 90)
lab, n = ndimage.label(grn, np.ones((3, 3)))
out = []
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 4:
        continue
    out.append((int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), len(xs)))
out.sort(key=lambda r: (r[2] // 10, r[0]))
print(f"== GREENISH clusters: {len(out)}")
for x0, x1, y0, y1, area in out[:60]:
    w_, h_ = x1 - x0 + 1, y1 - y0 + 1
    sel = a[y0:y1 + 1, x0:x1 + 1][grn[y0:y1 + 1, x0:x1 + 1]]
    med = np.median(sel, axis=0).astype(int)
    kind = "H" if h_ <= 4 and w_ > 6 else ("V" if w_ <= 4 and h_ > 6 else ("txt" if area < 150 else "box"))
    print(f"  x[{x0}..{x1}] y[{y0}..{y1}] w={w_} h={h_} a={area} med={tuple(med)} {kind}")
