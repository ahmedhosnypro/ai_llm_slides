#!/usr/bin/env python3
"""Fine-grained component census for slide_055.jpg."""
from PIL import Image
import numpy as np
from scipy import ndimage
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
A = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W, _ = A.shape
R, G, B = A[..., 0], A[..., 1], A[..., 2]
X0, SX, SY = 17.63, 0.96123, 0.95657
def sl(bb):
    x0, y0, x1, y1 = bb
    return [round((x0 - X0) / SX, 1), round(y0 / SY, 1), round((x1 - X0) / SX, 1), round(y1 / SY, 1),
            round((x1 - x0) / SX, 1), round((y1 - y0) / SY, 1)]
inner = np.zeros((H, W), bool)
inner[46:515, 62:899] = True

def comps(mask, min_px, name, topn=30, x0=62, x1=899):
    m = mask & inner
    m[:, :x0] = False; m[:, x1:] = False
    lab, n = ndimage.label(m)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_px: continue
        bb = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        out.append({"fbox": bb, "w": bb[2] - bb[0] + 1, "h": bb[3] - bb[1] + 1, "n": int(len(ys)), "slide": sl(bb)})
    out.sort(key=lambda c: (c["fbox"][1], c["fbox"][0]))
    print(f"\n== {name}: {len(out)}")
    for c in out[:topn]:
        print(f"   f={c['fbox']} {c['w']}x{c['h']} n={c['n']} slide={c['slide']}")
    return out

# fill-point samples for exact hexes
pts = {
    "dotprod_fill": (330, 300), "dotprod_fill2": (300, 250),
    "scaling_fill": (420, 300), "scaling_fill2": (430, 200),
    "softmax_fill": (500, 200), "softmax_fill2": (505, 350),
    "sigma_fill": (530, 200), "sigma_fill2": (660, 220),
    "wk_fill": (210, 240), "wv_fill": (730, 355),
    "ycont_fill": (140, 250), "zcont_fill": (230, 480),
    "pill_sim": (330, 165), "pill_prob": (520, 165), "pill_wsum": (640, 165),
    "legend_fill": (800, 470), "wq_fill": (300, 425),
    "hatchL": (130, 120), "hatchR": (800, 120),
    "title_black": (300, 64), "cap_fill": (640, 475),
    "panel": (480, 300),
}
print("== fill point samples ==")
for k, (x, y) in pts.items():
    r, g, b = A[y, x]
    print(f"   {k} @({x},{y}): #{r:02X}{g:02X}{b:02X} ({r},{g},{b})")

comps((np.abs(R - 216) <= 14) & (np.abs(G - 200) <= 14) & (np.abs(B - 185) <= 16), 400, "TAN box (DotProduct)")
comps((np.abs(R - 250) <= 6) & (np.abs(G - 215) <= 8) & (np.abs(B - 219) <= 8), 400, "PINK col (Scaling)")
comps((np.abs(R - 248) <= 6) & (np.abs(G - 222) <= 8) & (np.abs(B - 250) <= 6), 400, "PALE-VIOLET col (Softmax)")
comps((np.abs(R - 234) <= 8) & (G >= 246) & (np.abs(B - 252) <= 8), 400, "LT-CYAN (Sigma box)")
comps((np.abs(R - 204) <= 25) & (G >= 235) & (np.abs(B - 204) <= 25), 100, "PALE-GREEN (W_k, O?)")
comps((B - R >= 60) & (B - G >= 30) & (B >= 160) & (R < 150), 60, "BLUE (W_v, dots, text)")
comps((R >= 235) & (G >= 235) & (B <= 175) & (R - B >= 80), 300, "YELLOW containers")
comps((np.abs(R - 250) <= 10) & (np.abs(G - 240) <= 10) & (np.abs(B - 216) <= 12) & (R - B >= 20) & (R - B <= 50), 150, "PALE-YELLOW pills")
comps((R - G >= 70) & (R - B >= 60) & (R >= 150), 40, "RED strong", topn=40)
comps((R - G >= 45) & (R - B >= 35) & (R >= 140), 25, "RED loose", topn=50)
comps((R >= 190) & (B >= 150) & (R - G >= 40) & (B - G >= 25), 40, "MAGENTA/PURPLE", topn=30)
comps((R >= 242) & (G >= 242) & (B >= 242), 200, "WHITE", topn=25)
comps((R < 100) & (G < 100) & (B < 100), 40, "DARK ink", topn=40)
comps((np.abs(R - 204) <= 22) & (G >= 235) & (np.abs(B - 204) <= 22), 100, "PALEGREEN2", x0=700)
