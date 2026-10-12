#!/usr/bin/env python3
"""Produce slide_034 photo crops from the original frame + verify.

Crops (frame px, 1px = 1pt; exact-size embeds, never rescaled):
  meme034.png      x 83..330  y 251..444  — Grumpy Cat meme incl. baked white captions
                     AND the baked red 3x3 Sobel matrix + oversized red brackets
                     (matrix is an overlay ON the photo in the original; slide-029
                     baked-captions precedent — cannot be separated, rides in the crop)
  rgbstack034.png  x 438..727 y 218..452  — three tinted RGB channel copies (red back /
                     green middle / blue front), diagonal offset
  cube034.png      x 680..880 y 268..456  — isometric 3x3x3 numbered cube + black depth
                     arrow + yellow 'Third D' label (all intertwined line-art)
"""
import json
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
im = Image.open(f"{BASE}/unique_slides/slide_034.jpg").convert("RGB")
arr = np.asarray(im).astype(int)

CROPS = {
    "meme034.png":     (83, 251, 331, 445),   # PIL box: right/bottom exclusive
    "rgbstack034.png": (433, 215, 733, 456),  # widened v2: AA fringe of the red copy
                                               # reaches x434..437 / y216 / y454 / x728..731
    "cube034.png":     (680, 268, 881, 481),  # v3: bottom-left depth edge reaches its lowest vertex (780,479)
}
out = {}
for name, (x0, y0, x1, y1) in CROPS.items():
    c = im.crop((x0, y0, x1, y1))
    p = f"{BASE}/recreated_pptx/build/assets/{name}"
    c.save(p)
    a = np.asarray(c).astype(int)
    out[name] = {"box_px": [x0, y0, x1 - x0, y1 - y0],
                 "place_in_pt": [x0, y0, (x1 - x0), (y1 - y0)],
                 "size": c.size, "mean": [round(v, 1) for v in a.mean(axis=(0, 1))]}
    print(f"{name}: {c.size} mean={out[name]['mean']} -> {p}")

# sanity: crop corners should be white-ish (no content cut at edges except intended)
for name, (x0, y0, x1, y1) in CROPS.items():
    a = arr[y0:y1, x0:x1]
    edge = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    frac_nonwhite = ((edge < 240).any(axis=1)).mean()
    print(f"{name}: edge nonwhite frac {frac_nonwhite:.3f} (small = clean crop edges)")

with open(f"{BASE}/recreated_pptx/qa/slide034/crops_manifest.json", "w") as f:
    json.dump(out, f, indent=1)
print("manifest written")
