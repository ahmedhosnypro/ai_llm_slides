#!/usr/bin/env python3
import json, sys
sys.path.insert(0, "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
from render_eq_multi import render_segment, DPI, PAD_PX
import numpy as np
from PIL import Image

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_019/eq19_kernel_fix.png"
ROW = [
    ("CC0000", r"a^{T}b"),
    ("0000CC", r"\Rightarrow"),
    ("000000", r"\mathrm{map\ to}"),
    ("009900", r"\phi(a)"),
    ("000000", r"\mathrm{and}"),
    ("009900", r"\phi(b)"),
    ("0000CC", r"\Rightarrow"),
    ("009900", r"\phi(a)^{T}\phi(b)"),
    ("000000", r"\equiv"),
    ("009900", r"K"),
    ("CC0000", r"(a,\ b)"),
]
FS = 16
GAP = 8
parts = [render_segment(latex, "#" + color, FS) for color, latex in ROW]
base = max(b for _, b in parts)
h = max(base + (a.shape[0] - b) for (a, b) in parts) + 2 * PAD_PX
w = sum(a.shape[1] for a, _ in parts) + GAP * (len(parts) - 1) + 2 * PAD_PX
canvas = np.zeros((h, w, 4), dtype=np.uint8)
x = PAD_PX
for (arr, b), _ in zip(parts, ROW):
    y = base - b
    canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
    x += arr.shape[1] + GAP
Image.fromarray(canvas).save(OUT)
meta = {"path": OUT, "w_px": int(w), "h_px": int(h),
        "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5), "dpi": DPI,
        "fontsize_pt": [FS], "rows": ["||".join(f"{c}:{l}" for c, l in ROW)]}
with open(OUT + ".json", "w") as fh:
    json.dump(meta, fh, indent=2)
print(meta["w_in"], meta["h_in"])
