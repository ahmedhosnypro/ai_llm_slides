#!/usr/bin/env python3
"""Per-region alignment: find (dx,dy) in [-10..10] minimizing mean |diff| between
base_960.png (imported 001:19 composition, slide space) and slide037_slide_space.png
(my frame warped to slide space). Tells which inherited blocks align at (0,0)."""
from PIL import Image
import json

base = Image.open("base_960.png").convert("RGB")
mine = Image.open("slide037_slide_space.png").convert("RGB")
W, H = base.size
pb, pm = base.load(), mine.load()

REGIONS = {
    "left_inset_full":   (55, 260, 200, 500),
    "left_matmul_top":   (100, 285, 180, 330),
    "left_softmax":      (75, 325, 145, 350),
    "left_circles":      (80, 458, 185, 492),
    "center_inset_full": (295, 240, 515, 520),
    "center_sdpa":       (300, 348, 480, 400),
    "center_linear_row": (300, 395, 480, 450),
    "center_circles":    (315, 485, 460, 515),
    "fig_frame_tl":      (560, 95, 590, 115),
    "fig_frame_br":      (885, 515, 905, 535),
    "panels_top":        (575, 105, 900, 118),
    "label_encoder":     (575, 105, 665, 135),
    "label_decoder":     (805, 105, 895, 135),
    "dec_top":           (740, 105, 845, 200),
    "dec_base":          (735, 480, 855, 525),
    "feedback_band":     (845, 150, 900, 500),
    "enc_base_inputs":   (640, 478, 725, 515),
    "dec_nx":            (833, 288, 878, 330),
    "enc_nx_area":       (588, 318, 632, 362),
    "badge":             (855, 45, 910, 95),
}

def score(x0, y0, x1, y1, dx, dy):
    tot = 0; n = 0
    for y in range(y0, y1, 2):
        yy = y + dy
        if yy < 0 or yy >= H: return 1e9
        for x in range(x0, x1, 2):
            xx = x + dx
            if xx < 0 or xx >= W: return 1e9
            a, b = pb[x, y], pm[xx, yy]
            tot += abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])
            n += 1
    return tot / max(n, 1)

out = {}
for name, (x0, y0, x1, y1) in REGIONS.items():
    best = None
    grid = {}
    for dx in range(-10, 11):
        for dy in range(-10, 11):
            s = score(x0, y0, x1, y1, dx, dy)
            grid[(dx, dy)] = s
            if best is None or s < best[0]:
                best = (s, dx, dy)
    s0 = grid[(0, 0)]
    out[name] = {"best": best, "score_at_0_0": round(s0, 1),
                 "gain_pct": round(100 * (s0 - best[0]) / s0, 1) if s0 else 0}
    print(f"{name:18s} best d=({best[1]:+d},{best[2]:+d}) score {best[0]:6.1f} | at(0,0) {s0:6.1f} | gain {out[name]['gain_pct']:5.1f}%")

json.dump(out, open("m19_align_out.json", "w"), indent=1)
print("wrote m19_align_out.json")
