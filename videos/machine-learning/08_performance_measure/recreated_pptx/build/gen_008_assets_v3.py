#!/usr/bin/env python3
"""Slide-008 asset generation + geometry measurement (v3).

- eq_008_frac_v2.png / eq_008_worked_v2.png: 600dpi transparent mathtext PNGs
  (same recipes as gen_008_assets_v2.py).
- brace_008.png: green underbrace beneath the two '+ive' callout boxes,
  sized to the original's measured ink bbox (x108-332, y385-401).
- doodle_008_L.png / doodle_008_R.png: the two gray line-art airplanes cropped
  from the original frame with near-white background made transparent.
Prints measured component bboxes in the tree panel for build-coordinate fixes.
"""
import json
import numpy as np
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
FRAME = f"{NS}/unique_slides/slide_008.jpg"
OUT = f"{NS}/recreated_pptx/build/assets"
DPI = 600
PAD_PX = 8


def render_line(latex, fontsize, color):
    fig = plt.figure(figsize=(10, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color=color,
             ha="center", va="center")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    plt.close(fig)
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rows[0] - PAD_PX, 0), min(rows[-1] + PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0] - PAD_PX, 0), min(cols[-1] + PAD_PX, buf.shape[1])
    return buf[y0:y1, x0:x1]


def save(arr, name):
    im = Image.fromarray(arr)
    im.save(f"{OUT}/{name}")
    return {"name": name, "w_px": im.size[0], "h_px": im.size[1],
            "w_in": round(im.size[0] / DPI, 5), "h_in": round(im.size[1] / DPI, 5)}


frac = render_line(r"\frac{TP}{TP+FP}", 32, "#000000")
info_frac = save(frac, "eq_008_frac_v2.png")

l1 = render_line(r"\mathrm{Precision}=\frac{10}{10+2}", 18, "#000000")
l2 = render_line(r"\mathbf{=\,83.3\%}", 18, "#0070C0")
gap = 10
top_pad = 10
w = max(l1.shape[1], l2.shape[1])
h = top_pad + l1.shape[0] + gap + l2.shape[0]
canvas = np.zeros((h, w, 4), dtype=np.uint8)
canvas[top_pad:top_pad + l1.shape[0], 0:l1.shape[1]] = l1
xoff2 = (l1.shape[1] - l2.shape[1]) // 2
canvas[top_pad + l1.shape[0] + gap:, xoff2:xoff2 + l2.shape[1]] = l2
info_worked = save(canvas, "eq_008_worked_v2.png")

# --- green underbrace, target ink 224x16 px at 1x (drawn, mathtext has no brace) ---
W, H = 224, 16
brace = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(brace)
GREEN = (0, 176, 80, 255)
pts = []
for i in range(W):
    t = i / (W - 1)
    y = 2 + 11 * np.sin(np.pi * t)  # body dips down at center
    pts.append((i, y))
for x, y in pts:
    d.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=GREEN)
# end hooks curving up
d.line([(0, 5), (0, 1), (3, 1)], fill=GREEN, width=3)
d.line([(W - 1, 5), (W - 1, 1), (W - 4, 1)], fill=GREEN, width=3)
brace.save(f"{OUT}/brace_008.png")
info_brace = {"name": "brace_008.png", "w_px": W, "h_px": H}

# --- doodles: crop gray line-art from the original, whiten -> transparent ---
orig = Image.open(FRAME).convert("RGB")
a = np.asarray(orig).astype(int)


def extract_doodle(x0, y0, x1, y1, name):
    reg = a[y0:y1, x0:x1]
    mx = reg.max(axis=2)
    mn = reg.min(axis=2)
    grayish = (mx - mn) < 60
    lum = reg.mean(axis=2)
    alpha = np.where(grayish & (lum < 250), 255, 0).astype(np.uint8)
    # zero alpha outside a small dilation of ink to kill stray JPEG noise
    from scipy.ndimage import binary_dilation
    mask = binary_dilation(alpha > 30, iterations=1)
    alpha = np.where(mask, alpha, 0).astype(np.uint8)
    out = np.dstack([reg.astype(np.uint8), alpha])
    ys, xs = np.where(alpha > 20)
    x0b, x1b = x0 + xs.min(), x0 + xs.max() + 1
    y0b, y1b = y0 + ys.min(), y0 + ys.max() + 1
    im = Image.fromarray(out[y0b - y0:y1b - y0, x0b - x0:x1b - x0])
    im.save(f"{OUT}/{name}")
    return {"name": name, "frame_bbox": [int(x0b), int(y0b), int(x1b), int(y1b)],
            "w_px": im.size[0], "h_px": im.size[1]}


info_l = extract_doodle(588, 318, 674, 375, "doodle_008_L.png")
info_r = extract_doodle(764, 318, 855, 370, "doodle_008_R.png")

# --- measure tree-panel components for build coordinates ---
def color_bbox(x0, y0, x1, y1, pred):
    reg = a[y0:y1, x0:x1]
    m = pred(reg)
    ys, xs = np.where(m)
    if len(xs) == 0:
        return None
    return [int(x0 + xs.min()), int(y0 + ys.min()), int(x0 + xs.max() + 1), int(y0 + ys.max() + 1)]


red_fill = lambda r: (r[:, :, 0] > 130) & (r[:, :, 1] < 90) & (r[:, :, 2] < 90)
green_fill = lambda r: (r[:, :, 1] > 110) & (r[:, :, 0] < 90) & (r[:, :, 2] < 110)
blue_ink = lambda r: (r[:, :, 2] > 140) & (r[:, :, 0] < 100) & (r[:, :, 1] < 130)
print(json.dumps({
    "frac": info_frac, "worked": info_worked, "brace": info_brace,
    "doodle_L": info_l, "doodle_R": info_r,
    "tree_red_circles": color_bbox(536, 290, 882, 502, red_fill),
    "tree_green_circles": color_bbox(536, 290, 882, 502, green_fill),
    "tree_blue_arrows": color_bbox(536, 290, 882, 502, blue_ink),
}, indent=1))
