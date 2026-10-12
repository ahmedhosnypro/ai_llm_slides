#!/usr/bin/env python3
# probe44_resume4.py — per-column color transitions to pin band front-edges + strip extents.
import numpy as np
from PIL import Image

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_044.jpg").convert("RGB")
a = np.asarray(F).astype(int)

PALETTE = {
    "BLUEGRAY_D": (37,55,68), "YELLOW_D": (84,92,0), "ORANGE_D": (81,40,1), "GREEN_D": (43,94,0),
    "MAG_D": (78,0,78), "MAG": (157,0,166), "SALMON": (216,78,52),
    "GREEN_B": (133,255,9), "ORANGE_B": (238,121,6), "YELLOW_B": (250,255,11), "BLUEGRAY_B": (117,160,202),
    "WHITE": (255,255,255), "PANEL": (233,233,231),
}
def classify(px):
    best, bd = None, 1e9
    for name, c in PALETTE.items():
        d = abs(px[0]-c[0]) + abs(px[1]-c[1]) + abs(px[2]-c[2])
        if d < bd: bd, best = d, name
    return best if bd < 150 else "?"

def colscan(x, y0, y1, name):
    print(f"--- col x{x} ({name}) ---")
    prev, start = None, y0
    for y in range(y0, y1):
        c = classify(a[y, x])
        if c != prev:
            if prev is not None: print(f"  {prev:10s} y {start}..{y-1}")
            prev, start = c, y
    print(f"  {prev:10s} y {start}..{y1-1}")

# LEFT cube: front x66..202. Bands above. Scan at x=100, 160, 195 (inside front), x=210 (strips zone)
for x, nm in ((100, "left-in-front"), (160, "left-in-front"), (195, "left-in-front"), (208, "left-strips"), (240, "left-strips"), (262, "left-strips")):
    colscan(x, 170, 440, nm)
# GN cube: front x277..410 (magenta 277..336, salmon 337..410). Scan x=300, x=370, strips x=418, 436, 452
for x, nm in ((300, "gn-front-mag"), (370, "gn-front-sal"), (418, "gn-strip"), (436, "gn-strip"), (451, "gn-strip")):
    colscan(x, 85, 345, nm)
# IN cube: front x456..548 + salmon col 552..588. Scan x=500, x=560, strips x=598, 617, 634, 651
for x, nm in ((500, "in-front-mag"), (560, "in-sal-col"), (599, "in-strip"), (617, "in-strip"), (634, "in-strip"), (651, "in-strip")):
    colscan(x, 85, 365, nm)
# RT cube: front x689..819. Scan x=750, strips x=829, 848, 865, 882
for x, nm in ((750, "rt-front"), (829, "rt-strip"), (848, "rt-strip"), (865, "rt-strip"), (882, "rt-strip")):
    colscan(x, 85, 345, nm)
