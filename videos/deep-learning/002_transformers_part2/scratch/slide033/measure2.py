#!/usr/bin/env python3
"""slide033 measure-2: locate boxes by fill families + key ink bboxes."""
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

def comps(mask, min_area=300):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_area:
            continue
        out.append({
            "x0": int(xs.min()), "x1": int(xs.max()),
            "y0": int(ys.min()), "y1": int(ys.max()),
            "area": int(len(ys)),
            "med": [int(np.median(a[ys, xs, k])) for k in range(3)],
        })
    out.sort(key=lambda c: (c["y0"], c["x0"]))
    return out

FAMS = {
    "cream(FFF2CC)": (lambda r, g, b: (r > 225) & (g > 215) & (b > 170) & (b < 225) & (r - b > 20) & (g - b > 15)),
    "ltblue(DAEEF3)": (lambda r, g, b: (r > 195) & (r < 240) & (g > 220) & (b > 225) & (b - r > 12)),
    "grn_lt(C6E0B4)": (lambda r, g, b: (r > 170) & (r < 215) & (g > 200) & (b > 150) & (b < 200) & (g - b > 30) & (g > r)),
    "grn_mid(D6E8CE)": (lambda r, g, b: (r > 195) & (g > 215) & (b > 190) & (b < 215) & (g - b > 10) & (g - r > 8)),
    "orange_lt(F8CBAD)": (lambda r, g, b: (r > 235) & (g > 175) & (g < 215) & (b > 145) & (b < 185) & (r - b > 60) & (r - g > 30)),
    "yellow_badge": (lambda r, g, b: (r > 230) & (g > 215) & (b < 170) & (r - b > 80)),
    "white": (lambda r, g, b: (r > 245) & (g > 245) & (b > 245)),
}
for name, f in FAMS.items():
    print(f"--- {name} ---")
    for c in comps(f(r, g, b)):
        if c["area"] >= 500:
            m = c["med"]
            print(f"  frame[{c['x0']},{c['y0']}..{c['x1']},{c['y1']}] area={c['area']} med=({m[0]},{m[1]},{m[2]})"
                  f"  slide_x[{MAPX(c['x0']):.1f},{MAPX(c['x1']):.1f}] slide_y[{MAPY(c['y0']):.1f},{MAPY(c['y1']):.1f}]")

# --- dark inks: red text (C00000), blue text (0000CC), black ---
def ink(mask, label, min_area=8, gap=6):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    boxes = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_area:
            continue
        boxes.append([int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())])
    # merge into bands by y with gap
    boxes.sort(key=lambda b: (b[1], b[0]))
    print(f"--- {label}: {len(boxes)} glyphs; y-bands (gap>{gap}) ---")
    bands = []
    cur = None
    for bx in boxes:
        if cur is None or bx[1] - cur[3] > gap:
            if cur: bands.append(cur)
            cur = [bx[0], bx[1], bx[2], bx[3]]
        else:
            cur[0] = min(cur[0], bx[0]); cur[1] = min(cur[1], bx[1])
            cur[2] = max(cur[2], bx[2]); cur[3] = max(cur[3], bx[3])
    if cur: bands.append(cur)
    for bd in bands:
        print(f"  band frame[{bd[0]},{bd[1]}..{bd[2]},{bd[3]}]  slide_x[{MAPX(bd[0]):.1f},{MAPX(bd[2]):.1f}] slide_y[{MAPY(bd[1]):.1f},{MAPY(bd[3]):.1f}]")
    return bands

# red title/subtitle ink: dark red C00000-ish (exclude the border strokes cols 58/901, rows 43/517)
red_ink = (r > 120) & (r < 210) & (g < 70) & (b < 70)
red_ink[:, :62] = False; red_ink[:, 898:] = False; red_ink[:45, :] = False; red_ink[515:, :] = False
red_ink = red_ink & ~((np.arange(W)[None, :] < 90) & (np.arange(H)[:, None] > 510))  # keep dx1 area though
bands = ink(red_ink, "RED INK (C00000 text)")

blue_ink = (b > 110) & (b < 220) & (r < 90) & (g < 110) & (b - r > 60) & (b - g > 50)
blue_ink[:, :62] = False; blue_ink[:, 898:] = False
ink(blue_ink, "BLUE INK (0000CC text)")

black_ink = (r < 90) & (g < 90) & (b < 90)
black_ink[:, :62] = False; black_ink[:, 898:] = False
ink(black_ink, "BLACK INK", gap=8)
