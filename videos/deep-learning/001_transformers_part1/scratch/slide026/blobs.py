#!/usr/bin/env python3
"""Connected-component blobs of the quantized frame: every blob with area>=180,
as bbox + mean color + centroid. This reveals the TRUE layout of the diagram."""
import numpy as np
from PIL import Image
try:
    from scipy import ndimage
except ImportError:
    print("NO SCIPY"); raise SystemExit

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
q = np.asarray(IM.quantize(colors=32, method=Image.MEDIANCUT).convert("RGB")).astype(int)

# group quantized colors into ~14 coarse families to avoid splitting one shape
fams = {
    "peach":   (247, 227, 206), "white": (255, 255, 255), "graypanel": (233, 233, 231),
    "ltgreen": (230, 254, 232), "strip_yg": (252, 254, 208), "tan": (213, 204, 192),
    "plum":    (249, 217, 248), "ltblue": (197, 224, 245), "purpleblue": (156, 161, 237),
    "medgreen": (170, 220, 167), "yellow": (255, 255, 153), "pink": (255, 153, 204),
    "lavender": (217, 179, 255), "red": (255, 0, 0), "blue": (0, 51, 204),
    "green": (0, 176, 80), "black": (0, 0, 0), "brown": (139, 69, 19),
}
keys = list(fams)
cent = np.array([fams[k] for k in keys])
d = np.abs(q[:, :, None, :] - cent[None, None, :, :]).sum(axis=3)
lab = d.argmin(axis=2)

print(f"{'family':10s} {'n':>6s}  bbox                 centroid")
for i, k in enumerate(keys):
    m = lab == i
    m = ndimage.binary_opening(m, np.ones((2, 2)))
    L, n = ndimage.label(m)
    for sl in ndimage.find_objects(L):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        area = h * w
        if area < 180: continue
        mm = (L[sl] > 0)
        real = int(mm.sum())
        if real < 150: continue
        ys, xs = np.where(mm)
        cy = sl[0].start + ys.mean(); cx = sl[1].start + xs.mean()
        mc = q[sl][mm].mean(axis=0).astype(int)
        print(f"{k:10s} {real:6d}  x{sl[1].start:3d}..{sl[1].stop-1:3d} y{sl[0].start:3d}..{sl[0].stop-1:3d}  c=({cx:5.0f},{cy:5.0f})  #{mc[0]:02X}{mc[1]:02X}{mc[2]:02X}")
