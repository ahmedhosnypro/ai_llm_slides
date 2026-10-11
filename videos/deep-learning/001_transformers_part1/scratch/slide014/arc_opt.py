#!/usr/bin/env python3
"""Optimize circular-arrow geometry vs frame red mask (IoU grid search), then render 600dpi PNG."""
import itertools
import json
import numpy as np
from PIL import Image, ImageDraw

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_014.jpg").convert("RGB")).astype(int)
R, G, B = frame[..., 0], frame[..., 1], frame[..., 2]
red = (R > 120) & (R - G > 60) & (R - B > 60)

# arc region canvas (frame px): center +/- 42
CX, CY = 450.38, 307.60
X0, Y0, S = 406, 264, 90  # canvas origin + size
tgt = red[Y0:Y0 + S, X0:X0 + S]
print("target red px:", tgt.sum())

def draw_mask(theta_tip, theta_base, theta_far, r_in, r_out, tip_r, b_lo, b_hi):
    """All angles y-up degrees. Annulus sector from theta_base CCW to theta_far; triangle head."""
    SS = 4  # supersample
    img = Image.new("L", (S * SS, S * SS), 0)
    d = ImageDraw.Draw(img)
    sc = SS

    def pt(ang, r):
        a = np.radians(ang)
        return ((CX - X0 + r * np.cos(a)) * sc, (CY - Y0 - r * np.sin(a)) * sc)

    # annulus sector via pieslice trick: outer pie minus inner pie
    d.pieslice([(CX - X0 - r_out) * sc, (CY - Y0 - r_out) * sc,
                (CX - X0 + r_out) * sc, (CY - Y0 + r_out) * sc],
               start=-theta_far, end=-theta_base, fill=255)
    d.pieslice([(CX - X0 - r_in) * sc, (CY - Y0 - r_in) * sc,
                (CX - X0 + r_in) * sc, (CY - Y0 + r_in) * sc],
               start=-theta_far - 1, end=-theta_base + 1, fill=0)
    tri = [pt(theta_tip, tip_r), pt(theta_base, b_lo), pt(theta_base, b_hi)]
    d.polygon(tri, fill=255)
    img = img.resize((S, S), Image.LANCZOS)
    return np.asarray(img) > 100

grid = list(itertools.product(
    [46, 50, 54],          # theta_tip
    [90, 96, 102],         # theta_base
    [277, 281, 285, 289],  # theta_far (other end, y-up ~ -77)
    [13.5, 14.5, 15.5],    # r_in
    [31.5, 32.5, 33.5],    # r_out
    [21, 23.5, 26],        # tip_r
    [8, 10, 12],           # base inner radius
    [36, 38, 40],          # base outer radius
))
best = None
for p in grid:
    m = draw_mask(*p)
    inter = (m & tgt).sum(); union = (m | tgt).sum()
    iou = inter / union
    if best is None or iou > best[0]:
        best = (iou, p)
print("BEST IoU=%.3f params=%s" % (best[0], best[1]))

# local refinement around best
p0 = best[1]
ref = list(itertools.product(
    [p0[0] - 2, p0[0], p0[0] + 2],
    [p0[1] - 3, p0[1], p0[1] + 3],
    [p0[2] - 2, p0[2], p0[2] + 2],
    [p0[3] - 0.75, p0[3], p0[3] + 0.75],
    [p0[4] - 0.75, p0[4], p0[4] + 0.75],
    [p0[5] - 1.5, p0[5], p0[5] + 1.5],
    [p0[6] - 1.5, p0[6], p0[6] + 1.5],
    [p0[7] - 1.5, p0[7], p0[7] + 1.5],
))
for p in ref:
    m = draw_mask(*p)
    iou = (m & tgt).sum() / max((m | tgt).sum(), 1)
    if iou > best[0]:
        best = (iou, p)
print("REFINED IoU=%.3f params=%s" % (best[0], best[1]))
json.dump({"iou": best[0], "params": list(best[1]), "canvas": [X0, Y0, S], "center": [CX, CY]},
          open(f"{VID}/scratch/slide014/arc_params.json", "w"), indent=1)

# ---- render winner at 600 dpi (8.3333 px per frame px), 4x supersampled ----
iou, (theta_tip, theta_base, theta_far, r_in, r_out, tip_r, b_lo, b_hi) = best
K = 600 / 72.0
SS = 4
W = H = int(round(S * K))
img = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

def pt600(ang, r):
    a = np.radians(ang)
    return ((CX - X0 + r * np.cos(a)) * K * SS, (CY - Y0 - r * np.sin(a)) * K * SS)

RED = (204, 0, 0, 255)
d.pieslice([(CX - X0 - r_out) * K * SS, (CY - Y0 - r_out) * K * SS,
            (CX - X0 + r_out) * K * SS, (CY - Y0 + r_out) * K * SS],
           start=-theta_far, end=-theta_base, fill=RED)
d.pieslice([(CX - X0 - r_in) * K * SS, (CY - Y0 - r_in) * K * SS,
            (CX - X0 + r_in) * K * SS, (CY - Y0 + r_in) * K * SS],
           start=-theta_far - 1, end=-theta_base + 1, fill=(0, 0, 0, 0))
d.polygon([pt600(theta_tip, tip_r), pt600(theta_base, b_lo), pt600(theta_base, b_hi)], fill=RED)
img = img.resize((W, H), Image.LANCZOS)
out = f"{VID}/recreated_pptx/build/assets/slide014_arc_cw.png"
img.save(out)
print("saved", out, img.size, "embed at", f"x={X0/72:.4f}in y={Y0/72:.4f}in w={S/72:.4f}in h={S/72:.4f}in")
