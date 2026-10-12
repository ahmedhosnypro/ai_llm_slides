#!/usr/bin/env python3
"""Pass 6: definitive token-box anatomy — per-column color medians across box1 & box7
(Y and X rows), label ink bboxes per box, arrow geometry summary, caption/gutter colors."""
import numpy as np
from PIL import Image

P = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_036.jpg"
im = np.asarray(Image.open(P).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

boxes = [(176, 213), (248, 286), (321, 359), (394, 432), (467, 505), (540, 578), (731, 771), (803, 842)]

print("=== per-column median color, cell band rows ===")
for tag, (y0, y1) in [("Y", (361, 375)), ("X", (465, 478))]:
    for bi in (0, 6):
        x0, x1 = boxes[bi]
        cols = []
        for x in range(x0 - 2, x1 + 3):
            seg = im[y0:y1, x]
            cols.append((x, tuple(np.median(seg, axis=0).astype(int))))
        print(f"  {tag} box{bi+1} (x{x0}..{x1}):")
        line = " ".join(f"{x}:{c[0]},{c[1]},{c[2]}" for x, c in cols)
        print("   ", line)

print("=== label ink bbox per box (red mask rows 356..382 / 460..486) ===")
red = (r > 120) & (g < 110) & (b < 110)
for tag, (y0, y1) in [("Y", (356, 382)), ("X", (460, 486))]:
    for bi, (x0, x1) in enumerate(boxes):
        sub = red[y0:y1, x0:x1 + 1]
        ys, xs = np.where(sub)
        if len(xs):
            print(f"  {tag} box{bi+1}: label ink x {x0+xs.min()}..{x0+xs.max()} y {y0+ys.min()}..{y0+ys.max()} (off {xs.min()}..{xs.max()} of {x1-x0+1})")

print("=== arrow geometry summary (outline mask) ===")
db = (b > 110) & (b < 205) & (r < 90) & (g < 90)
bright = (b > 205) & (r < 90) & (g < 90)
anym = db | bright
print("  below-banner arrows (rows 445..461): per-arrow x-centers")
cols = anym[446:460, :].sum(axis=0)
runs, s = [], None
for x in range(150, 900):
    if cols[x] > 0 and s is None: s = x
    elif cols[x] == 0 and s is not None:
        if x - s > 3: runs.append((s, x - 1))
        s = None
print("   ", runs)
print("  above-banner arrows (rows 378..392):")
cols = anym[379:392, :].sum(axis=0)
runs, s = [], None
for x in range(150, 900):
    if cols[x] > 0 and s is None: s = x
    elif cols[x] == 0 and s is not None:
        if x - s > 3: runs.append((s, x - 1))
        s = None
print("   ", runs)
# vertical extent of one arrow (x 273..284)
sub = anym[440:466, 270:288]
ys, xs = np.where(sub)
print(f"  below arrow2 y-extent {440+ys.min()}..{440+ys.max()}, x {270+xs.min()}..{270+xs.max()}")
sub = anym[374:396, 342:360]
ys, xs = np.where(sub)
print(f"  above arrow3 y-extent {374+ys.min()}..{374+ys.max()}, x {342+xs.min()}..{342+xs.max()}")

print("=== caption text + gutter colors (dark cores) ===")
def cores(y0, y1, x0, x1, tag, pct=30):
    sub = im[y0:y1, x0:x1].reshape(-1, 3)
    s = sub.sum(axis=1)
    sel = sub[s < np.percentile(s, pct)]
    print(f"  {tag}: n={len(sel)} median {np.median(sel, axis=0)}")
cores(486, 504, 288, 578, "caption text cores")
cores(360, 394, 66, 160, "upper gutter ink cores")
cores(444, 480, 60, 160, "lower gutter ink cores")
cores(78, 98, 306, 712, "title cores")
cores(119, 130, 104, 160, "Input: header cores")
cores(137, 152, 180, 700, "body line1 cores")
print("=== panel border color (col 95 core, rows 150..300) ===")
sub = im[150:300, 94:97].reshape(-1, 3)
s = sub.sum(axis=1)
sel = sub[s < np.percentile(s, 25)]
print(f"  n={len(sel)} median {np.median(sel, axis=0)}")
print("=== info panel text right edges (excluding border cols 95/861) ===")
blue = (b > 120) & (r < 110) & (g < 110)
for (a, bb) in [(119, 129), (137, 152), (156, 167), (196, 207), (215, 228), (256, 266), (274, 289), (293, 304), (312, 327)]:
    sub = blue[a:bb + 1, 100:858]
    ys, xs = np.where(sub)
    if len(xs):
        print(f"  line {a}..{bb}: x {100+xs.min()}..{100+xs.max()}")
