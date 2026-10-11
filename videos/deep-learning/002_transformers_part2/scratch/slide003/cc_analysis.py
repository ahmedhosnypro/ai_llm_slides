#!/usr/bin/env python3
"""Connected-component analysis of the blue title/subtitle bands in slide_003.jpg.
Counts letters per word-block, gives each CC's bbox. Settles the word text.
"""
import numpy as np
from PIL import Image
import json
from collections import deque

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_003.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
blue = (B > 110) & (B - R > 60) & (B - G > 60) & (R < 120)

def cc_label(mask, x0, x1, y0, y1):
    """label CCs of mask within window; 4-connectivity on dilated-by-1 mask
    (letters' anti-aliased parts may split - dilate 1px to join)"""
    sub = mask[y0:y1 + 1, x0:x1 + 1].copy()
    # dilate horizontally+vertically by 1
    d = sub.copy()
    d[1:, :] |= sub[:-1, :]
    d[:-1, :] |= sub[1:, :]
    d[:, 1:] |= sub[:, :-1]
    d[:, :-1] |= sub[:, 1:]
    lab = np.zeros_like(d, dtype=int)
    cur = 0
    comps = []
    for yy in range(d.shape[0]):
        for xx in range(d.shape[1]):
            if d[yy, xx] and lab[yy, xx] == 0:
                cur += 1
                q = deque([(yy, xx)])
                lab[yy, xx] = cur
                pix = []
                while q:
                    cy, cx = q.popleft()
                    pix.append((cy, cx))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < d.shape[0] and 0 <= nx < d.shape[1] and d[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = cur
                            q.append((ny, nx))
                pys = [p[0] for p in pix]; pxs = [p[1] for p in pix]
                comps.append({"x0": x0+min(pxs), "x1": x0+max(pxs), "y0": y0+min(pys),
                              "y1": y0+max(pys), "w": max(pxs)-min(pxs)+1, "h": max(pys)-min(pys)+1,
                              "npix": len(pix)})
    comps.sort(key=lambda c: c["x0"])
    return comps

out = {}
# band 1: title, y 165..222 (pad), words at gaps
bands = [
    ("title", 165, 222, [(286, 398), (405, 479), (498, 549), (569, 651), (668, 674)]),
    ("subtitle", 278, 325, [(209, 288), (302, 492), (512, 748)]),
]
for name, y0, y1, words in bands:
    out[name] = []
    for (wx0, wx1) in words:
        comps = cc_label(blue, wx0, wx1, y0, y1)
        out[name].append({"span": [wx0, wx1], "n_cc": len(comps), "ccs": comps})

print(json.dumps(out, indent=1))
