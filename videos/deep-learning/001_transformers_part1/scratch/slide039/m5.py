#!/usr/bin/env python3
"""m5.py — panel rects (fill+border), pill rows, sigma boxes, per panel."""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def runs(m, min_len=2):
    out = []; s = None
    for i, v in enumerate(m):
        if v and s is None: s = i
        elif not v and s is not None:
            if i - s >= min_len: out.append((s, i - 1))
            s = None
    if s is not None and len(m) - s >= min_len: out.append((s, len(m) - 1))
    return out

# panel fill: (240,224,200) tolerant
fill = (np.abs(R - 240) < 12) & (np.abs(G - 224) < 12) & (np.abs(B - 200) < 14)
# panel border tan (224,176,128)ish
bord = (np.abs(R - 224) < 22) & (np.abs(G - 176) < 25) & (np.abs(B - 128) < 30) & (R - B > 55)

# Panel left edges: scan rows deep inside each panel's exclusive zone
# panel1 exclusive: x<194 (before panel2 left edge?) -- measure via fill leftmost per row
print("== leftmost fill x per row:")
for y in [250, 300, 350, 400, 450, 480]:
    xs = np.where(fill[y])[0]
    print(f"  y={y}: left={xs.min() if len(xs) else None} right={xs.max() if len(xs) else None}")

print("== topmost fill y per col:")
for x in [150, 250, 350, 450, 550, 650, 750, 850, 890]:
    ys = np.where(fill[:, x])[0]
    print(f"  x={x}: top={ys.min() if len(ys) else None} bot={ys.max() if len(ys) else None}")

# bottom edge of panel1: scan col x=200 (inside panel1 only)
for x in [160, 200, 600, 660]:
    m = fill[:, x]
    print(f"fill col x={x} runs:", runs(m, 6))

# border clusters -> panel outline visible segments
from scipy import ndimage
lab, n = ndimage.label(bord)
segs = []
for sl in ndimage.find_objects(lab):
    cnt = bord[sl].sum()
    if cnt >= 40:
        segs.append((sl[1].start, sl[0].start, sl[1].stop-1, sl[0].stop-1, int(cnt)))
segs.sort(key=lambda t: -t[4])
print("== tan border segments (x0,y0,x1,y1,count):")
for s in segs[:20]: print("   ", s)

# pills: pale cream fill (248,248,220)ish per panel top
cream = (R > 243) & (G > 243) & (B > 200) & (B < 245) & (np.abs(R - B) < 40) & (G - B > 8)
print("== cream fill rows y[140,270] (pill bands):")
cz = cream[140:270, :]
for s, e in runs(cz.sum(axis=1) > 20, 3):
    band = cz[s:e+1, :]
    cols = band.sum(axis=0)
    rr = runs(cols > 2, 5)
    print(f"  y[{140+s},{140+e}]:", [(r0, r1) for r0, r1 in rr])
