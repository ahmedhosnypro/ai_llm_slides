#!/usr/bin/env python3
"""Pass B: connected-component forensics — red elements, orange blocks, dots, photos."""
import numpy as np
from PIL import Image
from scipy import ndimage

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def comps(mask, min_px=15, name=""):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_px:
            continue
        out.append((xs.min(), ys.min(), xs.max(), ys.max(), len(ys)))
    out.sort(key=lambda t: (t[1], t[0]))
    print(f"== {name}: {len(out)} comps (x0,y0,x1,y1,npix) ==")
    for c in out:
        print(f"  ({c[0]},{c[1]})..({c[2]},{c[3]}) w={c[2]-c[0]+1} h={c[3]-c[1]+1} n={c[4]}")
    return out

# looser red for washed strokes
red = (r > 110) & (r - g > 60) & (r - b > 60)
comps(red, 20, "RED (loose)")

orange = (r > 150) & (g > 80) & (g < 180) & (b < 90) & (r - b > 90)
comps(orange, 60, "ORANGE blocks")

# dot column region: x 390..425, y 180..260 — print pixel color map of non-white
print("== dot column region scan x388..428 y180..260: distinct colors per row ==")
sub = im[178:262, 388:430]
for yy in range(sub.shape[0]):
    row = sub[yy]
    nz = [(x + 388, tuple(row[x])) for x in range(sub.shape[1]) if not (row[x] > 200).all()]
    if nz:
        xs = [t[0] for t in nz]
        print(f" y={yy+178}: {len(nz)} px x{min(xs)}..{max(xs)} sample {nz[len(nz)//2]}")
