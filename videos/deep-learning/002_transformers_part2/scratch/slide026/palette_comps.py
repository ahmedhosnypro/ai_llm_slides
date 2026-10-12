#!/usr/bin/env python3
"""Palette census + per-color connected components (scipy) for slide_026 frame."""
from PIL import Image
import numpy as np
from scipy import ndimage

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg"
img = Image.open(F).convert("RGB")
a = np.asarray(img).astype(int)

# 1) palette census in diagram+panel area (exclude outer canvas)
sub = a[45:516, 59:902]
cols, counts = np.unique(sub.reshape(-1, 3), axis=0, return_counts=True)
o = np.argsort(counts)[::-1]
print("TOP 30 colors in panel area:")
for i in o[:30]:
    c = cols[i]
    print(f"  #{c[0]:02X}{c[1]:02X}{c[2]:02X} {c.tolist()} n={counts[i]}")

def comps(mask, label, min_size=60, show=12):
    lab, n = ndimage.label(mask)
    out = []
    for sl in ndimage.find_objects(lab):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        npx = mask[sl].sum()
        if npx >= min_size and w > 4 and h > 4:
            out.append((int(npx), sl[1].start, sl[0].start, sl[1].stop - 1, sl[0].stop - 1))
    out.sort(reverse=True)
    print(f"\n{label}: {len(out)} comps (npx, x0,y0,x1,y1)")
    for c in out[:show]:
        print("  ", c)
    return out

r, g, b = a[..., 0], a[..., 1], a[..., 2]
def near(c, tol):
    return (abs(r - c[0]) < tol) & (abs(g - c[1]) < tol) & (abs(b - c[2]) < tol)

comps(near((14, 191, 235), 55), "BLUE 00A9E0 box")
comps(near((150, 150, 148), 28), "DARKGRAY bars ~909090")
comps(near((191, 191, 191), 20), "GRAY BFBFBF")
comps(near((213, 231, 189), 14), "LTGREEN container")
comps(near((247, 150, 70), 45), "ORANGE F79646")
comps(near((250, 220, 186), 16), "PEACH light-orange")
comps(near((108, 206, 147), 45), "GREEN triangles")
comps(near((192, 0, 0), 70), "RED C00000 arrow+caption", 30)
