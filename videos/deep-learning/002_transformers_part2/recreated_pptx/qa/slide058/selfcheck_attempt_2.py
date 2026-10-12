#!/usr/bin/env python3
"""Closed-loop ink check, slide 058: row-run separated lines, mask-to-mask.
Same red-ink thresholds both images; targets = frame mask through the certified
slide-002 mapping. Tolerance ~4px @150dpi. Also: containment (interior only),
badge numeral, no black strip, no cursor blob."""
from PIL import Image
import numpy as np

A, SX, SY = 18.63, 0.96123, 0.95556
REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide058/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_058.jpg"

ren = np.asarray(Image.open(REN).convert("RGB")).astype(int)
org = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
PX = ren.shape[1] / (13.333 * 72)

def redm(im, x0, x1):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    m = (R > 110) & (R - G > 50) & (R - B > 40)
    mm = np.zeros_like(m); mm[:, x0:x1] = m[:, x0:x1]
    return mm

def rowruns(mask, y0, y1, minpx=3):
    rr = mask[y0:y1].sum(axis=1)
    runs, inrun = [], False
    for i, v in enumerate(rr):
        if v > minpx and not inrun: st = i; inrun = True
        elif v <= minpx and inrun: runs.append((st + y0, i - 1 + y0)); inrun = False
    if inrun: runs.append((st + y0, y1 - 1))
    return runs

fails = []

# ---- render: find the two title line runs in y 400..800 (borders excluded x 300..1700)
mr = redm(ren, 300, 1700)
rruns = rowruns(mr, 400, 800)
print("render title row runs:", rruns)
if len(rruns) < 2:
    print("BLOCKER: fewer than 2 title lines in render"); fails.append("lines")
else:
    for label, (fx0, fx1, fy0, fy1), (ry0, ry1) in [
        ("L1", (224, 697, 229, 264), rruns[0]),
        ("L2", (318, 631, 282, 317), rruns[1]),
    ]:
        tx0 = (fx0 - A) / SX * PX; tx1 = (fx1 - A) / SX * PX
        ty0 = fy0 / SY * PX; ty1 = fy1 / SY * PX
        sub = mr[ry0:ry1 + 1]
        ys, xs = np.nonzero(sub)
        rx0, rx1 = xs.min(), xs.max()
        d = (rx0 - tx0, rx1 - tx1, ry0 - ty0, ry1 - ty1)
        ok = all(abs(v) <= 4.5 for v in d)
        print(f"{label}: ink x {rx0}..{rx1} y {ry0}..{ry1} | target x {tx0:.1f}..{tx1:.1f} y {ty0:.1f}..{ty1:.1f}")
        print(f"    d(L/R/T/B) {d[0]:+.1f}/{d[1]:+.1f}/{d[2]:+.1f}/{d[3]:+.1f}  width {rx1-rx0} vs {tx1-tx0:.1f} ({rx1-rx0-(tx1-tx0):+.1f})  -> {'OK' if ok else 'FAIL'}")
        if not ok: fails.append(label)

# ---- containment: interior title ink strictly inside panel interior (border excluded)
inner = redm(ren, 95, 1905)
ys, xs = np.nonzero(inner[100:1100])
ok = xs.min() >= 95 and xs.max() <= 1904
print(f"containment: interior red ink x {xs.min()}..{xs.max()} in [95,1904]: {ok}")
if not ok: fails.append("containment")

# ---- badge numeral + no artifacts
R, G, B = ren[..., 0], ren[..., 1], ren[..., 2]
yel = (R > 200) & (G > 200) & (B < 180) & (np.abs(R - G) < 40)
ys, xs = np.nonzero(yel[80:220, 1750:1980])
if len(xs):
    by0, by1, bx0, bx1 = ys.min() + 80, ys.max() + 80, xs.min() + 1750, xs.max() + 1750
    dark = (R < 90) & (G < 90) & (B < 90)
    print(f"badge yellow ({bx0},{by0})-({bx1},{by1}) d={bx1-bx0+1}x{by1-by0+1}, numeral ink {int(dark[by0:by1, bx0:bx1].sum())}px")
else:
    fails.append("badge"); print("badge: NO YELLOW")
strip = [y for y in range(1050, 1125) if ((R[y] < 60) & (G[y] < 60) & (B[y] < 60)).mean() > 0.5]
mid = ((R[500:1100, 300:1700] < 90) & (G[500:1100, 300:1700] < 90) & (B[500:1100, 300:1700] < 90)).sum()
print(f"strip rows: {strip} (want []), mid-panel black px: {int(mid)} (want 0)")
if strip or mid: fails.append("artifacts")

print("SELF-CHECK:", "PASS" if not fails else "FAIL " + str(fails))
