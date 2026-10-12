#!/usr/bin/env python3
"""Pre-judge self-check attempt 1 (resume worker, 2026-10-12):
inheritance diff — 002 slide_017 render_1.png vs 001 slide_043 certified render_2.png.
The render inherits the parent component wholesale except the 4 measured delta zones;
the pixel diff must be CONFINED to: title zone (line 2 removed + numeral 17),
ff_left (gold W_k panel + shifted K strips), ff_right (gold W_v panel + shifted V bars),
swoosh label («"H" Heads»). 1 slide-pt = 2001/960 px at 150dpi.
"""
from PIL import Image
import numpy as np

R = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide017/render_1.png").convert("RGB"), dtype=int)
P = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide043/render_2.png").convert("RGB"), dtype=int)
print("render", R.shape, "parent", P.shape)
H = min(R.shape[0], P.shape[0]); W = min(R.shape[1], P.shape[1])
R, P = R[:H, :W], P[:H, :W]
S = 2001 / 960.0  # px per slide-pt

def zone(x0, y0, x1, y1):
    return (int(y0 * S), int(y1 * S), int(x0 * S), int(x1 * S))

ZONES = {
    "title+numeral": zone(480, 40, 915, 110),
    "ff_left":       zone(88, 294, 196, 450),
    "ff_right":      zone(414, 294, 612, 450),
    "swoosh_label":  zone(598, 378, 722, 442),
}
mask = np.zeros((H, W), dtype=bool)
for name, (y0, y1, x0, x1) in ZONES.items():
    mask[y0:y1, x0:x1] = True

d = np.abs(R - P).sum(axis=2)
changed = d > 40  # significant channel-sum diff
out = changed & ~mask
print(f"changed px total: {changed.sum()}  inside delta zones: {(changed & mask).sum()}  OUTSIDE: {out.sum()}")
per = {n: int(changed[z0:z1, x0:x1].sum()) for n, (z0, z1, x0, x1) in ZONES.items()}
print("per-zone changed px:", per)
if out.sum():
    ys, xs = np.where(out)
    # cluster outside-ink into coarse slide-pt boxes
    boxes = {}
    for y, x in zip(ys, xs):
        key = (y // 40 * 40, x // 40 * 40)
        boxes[key] = boxes.get(key, 0) + 1
    print("outside-diff clusters (render px grid 40):")
    for (y, x), n in sorted(boxes.items(), key=lambda kv: -kv[1])[:12]:
        print(f"  y~{y}-{y+40} x~{x}-{x+40}  n={n}  (slide pt y~{y/S:.0f} x~{x/S:.0f})")
print("SELF-CHECK INHERITANCE:", "PASS" if out.sum() < 2000 else "CHECK CLUSTERS")
