#!/usr/bin/env python3
"""m4.py — connected-component analysis of key stroke colors in slide_039.jpg.
Prints cluster bboxes for green strokes (dashed X/Y boxes), blue, red, tan(dot box),
pink boxes, cream/yellow."""
from PIL import Image
import numpy as np
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def clusters(mask, name, min_px=25, max_show=40):
    lab, n = ndimage.label(mask)
    out = []
    for sl in ndimage.find_objects(lab):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        cnt = mask[sl].sum()
        if cnt >= min_px:
            out.append((sl[1].start, sl[0].start, sl[1].stop - 1, sl[0].stop - 1, int(cnt), w, h))
    out.sort(key=lambda t: -t[4])
    print(f"== {name}: {len(out)} clusters (x0,y0,x1,y1,count,w,h)")
    for c in out[:max_show]:
        print("   ", c)
    return out

# green strokes: green dominant, mid-dark (borders of dashed boxes, connectors)
green = (G - R > 25) & (G - B > 25) & (G > 90) & (G < 220)
clusters(green, "green strokes", min_px=20)

# strong blue: W-box borders/text, pill text
blue = (B - R > 60) & (B > 120) & (G < 140)
clusters(blue, "blue", min_px=15, max_show=50)

# red
red = (R > 140) & (R - G > 70) & (R - B > 70)
clusters(red, "red", min_px=15, max_show=60)
