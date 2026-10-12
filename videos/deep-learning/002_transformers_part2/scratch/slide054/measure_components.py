#!/usr/bin/env python3
"""Color-component analysis of slide_054.jpg — every major diagram element's frame bbox."""
from PIL import Image
import numpy as np
from scipy import ndimage
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg"
img = Image.open(SRC).convert("RGB")
A = np.asarray(img).astype(int)
H, W, _ = A.shape
R, G, B = A[..., 0], A[..., 1], A[..., 2]

def near(hexc, tol=40):
    r = int(hexc[0:2], 16); g = int(hexc[2:4], 16); b = int(hexc[4:6], 16)
    return (abs(R - r) <= tol) & (abs(G - g) <= tol) & (abs(B - b) <= tol)

# exclude the outer chrome border zone from content search
inner = np.zeros((H, W), bool)
inner[46:516, 62:899] = True

def components(mask, min_px=25, label=""):
    m = mask & inner
    lab, n = ndimage.label(m)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_px:
            continue
        out.append({
            "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
            "w": int(xs.max() - xs.min() + 1), "h": int(ys.max() - ys.min() + 1),
            "npx": int(len(ys)),
        })
    out.sort(key=lambda c: (-c["npx"]))
    print(f"== {label}: {len(out)} comps (min_px={min_px})")
    for c in out[:40]:
        print(f"   bbox={c['bbox']} w={c['w']} h={c['h']} npx={c['npx']}")
    return out

res = {}
res["pink_panel"] = components(near("FF9EC7", 45), 5000, "PINK PANEL FF9EC7")
res["green"]      = components(near("92D050", 45), 150, "GREEN 92D050")
res["yellow"]     = components(near("FFFF00", 55), 40, "YELLOW FFFF00")
res["tan"]        = components(near("C9A26B", 45), 500, "TAN C9A26B")
res["palepink"]   = components(near("FFC4D6", 30), 500, "PALEPINK FFC4D6")
res["nearwhite"]  = components(near("F0ECFA", 22), 500, "NEARWHITE F0ECFA")
res["paleblue"]   = components(near("ADD8E6", 35), 300, "PALEBLUE ADD8E6")
res["bluedots"]   = components(near("0070C0", 60), 30, "BLUEDOT 0070C0")
res["magenta"]    = components(near("DA70D6", 50), 80, "MAGENTA DA70D6")
res["wqpink"]     = components(near("FF99CC", 30), 80, "WQ-PINK FF99CC")
