#!/usr/bin/env python3
"""slide033 measure-3: region-specific geometry (left columns, pair boxes, borders)."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[..., 0], a[..., 1], a[..., 2]
MAPX = lambda fx: (fx - 18.63) / 0.96123
MAPY = lambda fy: fy / 0.95556
S = lambda x0, x1, y0, y1: (f"slide_x[{MAPX(x0):.1f},{MAPX(x1):.1f}] y[{MAPY(y0):.1f},{MAPY(y1):.1f}]"
                            f"  -> in[{MAPX(x0)/72:.3f},{MAPX(x1)/72:.3f}] [{MAPY(y0)/72:.3f},{MAPY(y1)/72:.3f}]")

def region_bands(x0, x1, y0, y1, mask_fn, label, gap=5, min_area=6):
    sub = mask_fn(r[y0:y1+1, x0:x1+1], g[y0:y1+1, x0:x1+1], b[y0:y1+1, x0:x1+1])
    lab, n = ndimage.label(sub, structure=np.ones((3, 3)))
    boxes = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_area:
            continue
        boxes.append([int(xs.min()) + x0, int(ys.min()) + y0, int(xs.max()) + x0, int(ys.max()) + y0, len(ys)])
    boxes.sort(key=lambda t: (t[1], t[0]))
    print(f"--- {label} ({len(boxes)} comps) ---")
    # y-bands
    bands = []
    cur = None
    for t in boxes:
        if cur is None or t[1] - cur[3] > gap:
            if cur: bands.append(cur)
            cur = [t[0], t[1], t[2], t[3]]
        else:
            cur[0] = min(cur[0], t[0]); cur[1] = min(cur[1], t[1])
            cur[2] = max(cur[2], t[2]); cur[3] = max(cur[3], t[3])
    if cur: bands.append(cur)
    for bd in bands:
        print(f"  band f[{bd[0]},{bd[1]}..{bd[2]},{bd[3]}] h={bd[3]-bd[1]}  {S(bd[0], bd[2], bd[1], bd[3])}")
    return boxes, bands

# ---- general pair box: hunt for the maroon border around x 96..192 y 124..205 ----
# scan a wide window for non-background pixels
win = a[100:230, 60:230]
nb = (np.abs(win[..., 0].astype(int) - 245) + np.abs(win[..., 1] - 244) + np.abs(win[..., 2] - 240)) > 60
print("general-pair-box window non-bg projection:")
rows = np.where(nb.sum(axis=1) > 8)[0]
cols = np.where(nb.sum(axis=0) > 8)[0]
print("  rows(+100):", rows.min() + 100, "..", rows.max() + 100)
print("  cols(+60):", cols.min() + 60, "..", cols.max() + 60)
# maroon border color probe: median color of the extreme rows/cols
mar = win[nb]
print("  non-bg median color:", [int(np.median(mar[:, k])) for k in range(3)])

# ---- sin/cos terms column region: x 300..430 y 100..530 : find green/orange fills ----
grn = (g > 150) & (r < g - 20) & (b < g - 15) & (g < 230)
org = (r > 215) & (g > 140) & (g < 215) & (b < 160) & (r - b > 70)
region_bands(295, 435, 95, 535, lambda r_, g_, b_: grn[95:536, 295:436], "PAIR BOXES: green fills (in col region)", gap=4)
region_bands(295, 435, 95, 535, lambda r_, g_, b_: org[95:536, 295:436], "PAIR BOXES: orange fills", gap=4)

# red text inside pair boxes (sin/cos terms)
red_tx = (r > 130) & (g < 80) & (b < 80)
region_bands(295, 435, 95, 535, lambda r_, g_, b_: red_tx[95:536, 295:436], "PAIR BOXES: red text", gap=4)

# ---- vector pairs column (green boxes): x 200..270 ----
region_bands(200, 275, 95, 535, lambda r_, g_, b_: grn[95:536, 200:276], "VECTOR PAIRS col: green fills", gap=4)
blk = (r < 100) & (g < 100) & (b < 100)
region_bands(200, 275, 95, 535, lambda r_, g_, b_: blk[95:536, 200:276], "VECTOR PAIRS col: black text", gap=4)
region_bands(200, 275, 95, 535, lambda r_, g_, b_: red_tx[95:536, 200:276], "VECTOR PAIRS col: red text", gap=4)
# blue label above
blue = (b > 110) & (r < 90) & (b - g > 40)
region_bands(195, 280, 95, 135, lambda r_, g_, b_: blue[95:136, 195:281], "Vector Pairs label (blue)", gap=4)

# ---- index column: cream strip x 255..320 ----
cream = (r > 230) & (g > 215) & (b > 160) & (b < 225) & (r - b > 20)
region_bands(250, 330, 95, 535, lambda r_, g_, b_: cream[95:536, 250:331], "INDEX col: cream strip", gap=4)
red_tx2 = (r > 120) & (r < 215) & (g < 80) & (b < 80)
region_bands(250, 330, 95, 535, lambda r_, g_, b_: red_tx2[95:536, 250:331], "INDEX col: red text", gap=4)
region_bands(250, 330, 95, 135, lambda r_, g_, b_: red_tx2[95:136, 250:331], "Index label (red)", gap=4)

# ---- green info box: x 60..215 y 220..330 ----
grn_info = (g > 230) & (r > 190) & (b > 210) & (g - r > 12) & (g - b > 5)
region_bands(55, 225, 210, 340, lambda r_, g_, b_: grn_info[210:341, 55:226], "INFO box fill", gap=4)
green_tx = (g > 90) & (g < 180) & (r < 100) & (b < 110)
region_bands(55, 225, 210, 340, lambda r_, g_, b_: green_tx[210:341, 55:226], "INFO box green border", gap=4)
region_bands(55, 225, 215, 340, lambda r_, g_, b_: blk[215:341, 55:226], "INFO box black text", gap=4)
red_tx3 = (r > 120) & (g < 85) & (b < 85)
region_bands(55, 225, 215, 340, lambda r_, g_, b_: red_tx3[215:341, 55:226], "INFO box red text", gap=4)

# ---- general pair box contents (red text) ----
region_bands(85, 200, 115, 215, lambda r_, g_, b_: red_tx[115:216, 85:201], "GENERAL PAIR box red text", gap=4)
# its border: dark red pixels in window
maroon = (r > 100) & (r < 180) & (g < 60) & (b < 60)
region_bands(85, 200, 110, 220, lambda r_, g_, b_: maroon[110:221, 85:201], "GENERAL PAIR maroon border", gap=6)
