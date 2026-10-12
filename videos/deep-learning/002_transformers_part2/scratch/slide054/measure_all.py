#!/usr/bin/env python3
"""Comprehensive component map of slide_054.jpg with frame->slide mapping.
Mapping (fit from chrome landmarks 59/902/42/516, same as slide_002):
  slide_x = (frame_x - 18.63)/0.96123 ; slide_y = frame_y/0.95556
"""
from PIL import Image
import numpy as np
from scipy import ndimage
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg"
img = Image.open(SRC).convert("RGB")
A = np.asarray(img).astype(int)
H, W, _ = A.shape
R, G, B = A[..., 0], A[..., 1], A[..., 2]

X0, SX = 18.63, 0.96123   # slide_x = (fx - X0)/SX
SY = 0.95556              # slide_y = fy/SY
def to_slide(bb):
    x0, y0, x1, y1 = bb
    sx0 = (x0 - X0) / SX; sx1 = (x1 - X0) / SX
    sy0 = y0 / SY; sy1 = y1 / SY
    return [round(sx0, 1), round(sy0, 1), round(sx1, 1), round(sy1, 1),
            round((sx1 - sx0), 1), round((sy1 - sy0), 1)]

inner = np.zeros((H, W), bool)
inner[46:516, 62:899] = True

def comps(mask, min_px, name, topn=45):
    m = mask & inner
    lab, n = ndimage.label(m)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_px: continue
        bb = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        out.append({"fbox": bb, "w": bb[2]-bb[0]+1, "h": bb[3]-bb[1]+1,
                    "npx": int(len(ys)), "slide": to_slide(bb)})
    out.sort(key=lambda c: (c["fbox"][1], c["fbox"][0]))
    print(f"\n== {name}: {len(out)} comps")
    for c in out[:topn]:
        print(f"   f={c['fbox']} {c['w']}x{c['h']} n={c['npx']} slide={c['slide']}")
    return out

mask_panel  = (np.abs(R-245)<=10) & (np.abs(G-209)<=12) & (np.abs(B-246)<=10)
mask_tan    = (np.abs(R-216)<=15) & (np.abs(G-200)<=15) & (np.abs(B-185)<=15)
mask_palepk = (np.abs(R-247)<=8)  & (np.abs(G-212)<=10) & (np.abs(B-215)<=10)
mask_lgreen = (G - R >= 14) & (G - B >= 14) & (G >= 228) & (R >= 190)
mask_yellow = (R >= 235) & (G >= 235) & (B <= 215) & (R - B >= 35)
mask_red    = (R - G >= 70) & (R - B >= 60) & (R >= 150)
mask_dark   = (R < 110) & (G < 110) & (B < 110)
mask_blue   = (B - R >= 60) & (B >= 130) & (R < 200)
mask_magent = (R >= 190) & (B >= 190) & (G <= 175) & (R - G >= 40)
mask_wht    = (R >= 238) & (G >= 238) & (B >= 238) & ~mask_panel

res = {}
res["panel"]  = comps(mask_panel, 8000, "PINK PANEL")
res["tan"]    = comps(mask_tan, 400, "TAN (DotProduct)")
res["palepk"] = comps(mask_palepk, 300, "PALE-PINK (Scaling)")
res["lgreen"] = comps(mask_lgreen, 120, "LIGHT-GREEN fills")
res["yellow"] = comps(mask_yellow, 30, "YELLOW cells/chips")
res["red"]    = comps(mask_red, 60, "RED ink")
res["dark"]   = comps(mask_dark, 40, "DARK ink")
res["blue"]   = comps(mask_blue, 20, "BLUE ink")
res["magent"] = comps(mask_magent, 60, "MAGENTA")
json.dump({k: [c["fbox"] for c in v] for k, v in res.items()}, open("components.json", "w"), indent=1)
