#!/usr/bin/env python3
"""Generate the slide-021 underbrace PNG by TRACING the original frame's ink
(crop-judge rounds 1-3 rejected synthetic cusps; the traced-alpha raster
reproduces the measured geometry exactly - same certified mechanism family:
PIL raster -> transparent PNG -> addImage at exact size w=px/600 in).

Method: crop the brace region (frame x 176..866, y 335..353) from
slide_021.jpg, build an alpha channel from the redness field
(r - (g+b)/2, normalized, gamma-shaped), resize to the target 600dpi box
(718.27 x 16.25 pt -> 5986 x 136 px) with LANCZOS, and paint it with the
census core color 882830.
"""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_021.jpg"
A = np.asarray(Image.open(FR).convert("RGB")).astype(float)

X0, X1, Y0, Y1 = 176, 866, 336, 352
crop = A[Y0:Y1, X0:X1]
red = crop[..., 0] - (crop[..., 1] + crop[..., 2]) / 2.0
red = np.clip(red, 0, None)
p99 = np.percentile(red, 99.5)
alpha = np.clip(red / max(p99, 1e-6), 0, 1) ** 0.85

W_PT, H_PT = 718.27, 16.25
DPI = 600
W = round(W_PT / 72 * DPI)   # 5986
H = round(H_PT / 72 * DPI)   # 136
a_img = Image.fromarray((alpha * 255).astype(np.uint8), "L")
a_img = a_img.resize((W, H), Image.LANCZOS)

rgba = np.zeros((H, W, 4), dtype=np.uint8)
rgba[..., 0] = 139
rgba[..., 1] = 40
rgba[..., 2] = 48
rgba[..., 3] = np.asarray(a_img)

out = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/brace_021.png"
Image.fromarray(rgba, "RGBA").save(out)
print("saved", out, (W, H))
