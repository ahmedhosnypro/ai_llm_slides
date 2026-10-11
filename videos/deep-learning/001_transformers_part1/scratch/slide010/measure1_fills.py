#!/usr/bin/env python3
"""Measure slide_010.jpg fill-color regions (containers, cells, boxes, node).

Ground truth = the frame. Finds connected components per target fill color
(JPEG-tolerant matching), reports bbox + core color, in frame px (960x540).
"""
from PIL import Image
import numpy as np
from scipy import ndimage

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_010.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
H, W = im.shape[:2]

TARGETS = {
    # name: (r,g,b) center, tolerance per channel, min area
    "dec_container_yellow": ((247, 247, 90), 28, 4000),
    "dec_green_cells":      ((184, 240, 184), 30, 400),
    "dec_tan_cells":        ((245, 215, 110), 26, 400),
    "enc_container_orange": ((248, 203, 173), 22, 4000),
    "enc_cells":            ((247, 190, 129), 18, 400),
    "attention_lavender":   ((217, 217, 243), 16, 1200),
    "attention_node_white": ((255, 255, 255), 6, 150),
    "green_callout":        ((201, 247, 201), 16, 800),
    "pink_callout":         ((249, 201, 212), 16, 800),
    "gray_summary":         ((234, 234, 234), 8, 2000),
}

for name, ((tr, tg, tb), tol, minarea) in TARGETS.items():
    m = (abs(r - tr) <= tol) & (abs(g - tg) <= tol) & (abs(b - tb) <= tol)
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        ys, xs = sl
        area = int((lab[sl] == i + 1).sum())
        if area < minarea:
            continue
        reg = im[sl]
        rm = (lab[sl] == i + 1)
        core = tuple(int(np.median(reg[..., c][rm])) for c in range(3))
        out.append((area, xs.start, ys.start, xs.stop - 1, ys.stop - 1, core))
    out.sort(reverse=True)
    print(f"== {name}: {len(out)} comps")
    for area, x0, y0, x1, y1, core in out[:8]:
        print(f"   bbox x{x0}..{x1} y{y0}..{y1} (w{x1-x0+1} h{y1-y0+1}) area={area} core={core}")
