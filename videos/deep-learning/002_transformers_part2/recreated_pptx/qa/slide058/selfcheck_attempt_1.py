#!/usr/bin/env python3
"""Closed-loop ink check, slide 058 attempt 1: render vs original, mask-to-mask.
Same red-ink thresholds on both images; targets = frame mask mapped through the
certified slide-002 mapping (frame_x = 18.63 + 0.96123*slide_x, frame_y = 0.95556*slide_y).
Tolerance ~4px @150dpi (1.92 slide pt). Also checks: equation regions n/a, containment,
badge numeral ink, omitted artifacts (no black strip, no cursor in render)."""
from PIL import Image
import numpy as np

A, SX, SY = 18.63, 0.96123, 0.95556
REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide058/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_058.jpg"

ren = np.asarray(Image.open(REN).convert("RGB")).astype(int)
org = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)

def redmask(im, x0, x1):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    m = (R > 110) & (R - G > 50) & (R - B > 40)
    mm = np.zeros_like(m); mm[:, x0:x1] = m[:, x0:x1]
    return mm

def bbox(mask, y0, y1):
    sub = mask[y0:y1]
    ys, xs = np.nonzero(sub)
    if not len(xs):
        return None
    return xs.min(), xs.max(), ys.min() + y0, ys.max() + y0

# render: slide pt -> px @150dpi (2001px / 13.333in = 150.07dpi)
PX = 2001 / (13.333 * 72)  # px per slide pt
def tgt(fx0, fx1, fy0, fy1):
    x0 = (fx0 - A) / SX * PX; x1 = (fx1 - A) / SX * PX
    y0 = fy0 / SY * PX; y1 = fy1 / SY * PX
    return x0, x1, y0, y1

# render title search bands (generous, away from border strokes)
fails = []
for label, (fx0, fx1, fy0, fy1), band in [
    ("L1", (224, 697, 229, 264), (420, 640)),
    ("L2", (318, 631, 282, 317), (545, 770)),
]:
    tx0, tx1, ty0, ty1 = tgt(fx0, fx1, fy0, fy1)
    m = redmask(ren, 300, 1700)
    bb = bbox(m, band[0], band[1])
    if bb is None:
        print(f"{label}: NO INK in render band — BLOCKER"); fails.append(label); continue
    rx0, rx1, ry0, ry1 = bb
    d = dict(left=rx0 - tx0, right=rx1 - tx1, top=ry0 - ty0, bottom=ry1 - ty1)
    w_t, w_r = tx1 - tx0, rx1 - rx0
    ok = all(abs(v) <= 4.5 for v in d.values())
    print(f"{label}: render ink x {rx0}..{rx1} y {ry0}..{ry1}  target x {tx0:.1f}..{tx1:.1f} y {ty0:.1f}..{ty1:.1f}")
    print(f"    d(left/right/top/bottom) = {d['left']:+.1f}/{d['right']:+.1f}/{d['top']:+.1f}/{d['bottom']:+.1f} px  width {w_r} vs {w_t:.1f} ({w_r-w_t:+.1f})  -> {'OK' if ok else 'FAIL'}")
    if not ok: fails.append(label)

# equation regions: none on this slide (divider) — n/a
print("equations: none in spec/original — check n/a")

# containment: title ink inside panel (render panel x 89..1913, y 95..1125)
m = redmask(ren, 0, ren.shape[1])
ys, xs = np.nonzero(m[100:1100])
print(f"containment: title ink x {xs.min()}..{xs.max()} within panel 89..1913: {xs.min()>=90 and xs.max()<=1912}")

# omitted artifacts: black strip rows at bottom, cursor black blob mid-panel
R, G, B = ren[..., 0], ren[..., 1], ren[..., 2]
dark = (R < 60) & (G < 60) & (B < 60)
strip = [y for y in range(1050, 1125) if dark[y].mean() > 0.5]
print(f"bottom black strip rows in render (must be NONE): {strip}")
mid = dark[500:1100, 300:1700]
ys, xs = np.nonzero(mid)
print(f"black blob in panel (must be NONE): {len(xs)} px")

# badge numeral present
yel = (R > 200) & (G > 200) & (B < 180) & (np.abs(R - G) < 40)
ys, xs = np.nonzero(yel[80:220, 1750:1980])
if len(xs):
    bx0, bx1, by0, by1 = xs.min()+1750, xs.max()+1750, ys.min()+80, ys.max()+80
    dk = dark[by0:by1, bx0:bx1]
    print(f"badge yellow bbox ({bx0},{by0})-({bx1},{by1}), numeral ink px inside: {int(dk.sum())}")
else:
    print("badge: NO YELLOW — BLOCKER"); fails.append("badge")

print("SELF-CHECK ATTEMPT 1:", "PASS" if not fails else "FAIL " + str(fails))
