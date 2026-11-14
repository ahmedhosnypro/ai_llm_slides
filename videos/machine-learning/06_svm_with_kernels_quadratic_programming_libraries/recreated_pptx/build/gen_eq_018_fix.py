#!/usr/bin/env python3
import json, sys
import numpy as np
from PIL import Image

sys.path.insert(0, "/home/codespace/ai_llm_slides/scripts")
from render_eq_wide import render

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_018"
DPI = 600
PAD = 10
BLACK = "#000000"

def seg(latex, fs=16):
    return render(latex, f"{OUT}/_seg.png", fs, BLACK)

def vector(rows, fs=16):
    parts = [seg(r, fs) for r in rows]
    w = max(p["w_px"] for p in parts) + 2 * PAD + 8
    h = sum(p["h_px"] for p in parts) + 8 * (len(parts) - 1) + 2 * PAD
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    y = PAD
    for p in parts:
        x = PAD + 4 + (w - 2 * PAD - 8 - p["w_px"]) // 2
        arr = np.array(Image.open(p["path"]).convert("RGBA"))
        canvas[y:y + p["h_px"], x:x + p["w_px"]] = arr
        y += p["h_px"] + 8
    for x in (PAD, w - PAD - 2):
        canvas[PAD: h - PAD, x:x + 2] = 255
        canvas[PAD: h - PAD, x:x + 2, :3] = 0
    return canvas

def compose():
    left = vector(["x", "y"])
    arrow = np.array(Image.open(seg(r"\Rightarrow")["path"]).convert("RGBA"))
    right = vector(["x^{2}", "y^{2}", r"\sqrt{2}xy"])
    gap = 18
    w = left.shape[1] + gap + arrow.shape[1] + gap + right.shape[1] + 2 * PAD
    h = max(left.shape[0], arrow.shape[0], right.shape[0]) + 2 * PAD
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    y = (h - left.shape[0]) // 2
    canvas[y:y + left.shape[0], PAD:PAD + left.shape[1]] = left
    x = PAD + left.shape[1] + gap
    y = (h - arrow.shape[0]) // 2
    canvas[y:y + arrow.shape[0], x:x + arrow.shape[1]] = arrow
    x += arrow.shape[1] + gap
    y = (h - right.shape[0]) // 2
    canvas[y:y + right.shape[0], x:x + right.shape[1]] = right
    out = f"{OUT}/eq18_colvec_fix.png"
    Image.fromarray(canvas).save(out)
    meta = {"path": out, "w_px": int(w), "h_px": int(h),
            "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5), "dpi": DPI}
    with open(f"{OUT}/eq18_colvec_fix.json", "w") as fh:
        json.dump(meta, fh)
    print(meta)

compose()
