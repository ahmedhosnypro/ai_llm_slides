#!/usr/bin/env python3
"""Forensics pass 2d — dotted connector line true color/pattern + ends, top-strip crops."""
import numpy as np
from PIL import Image

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
im = Image.open(ORIG).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

# find the line row: pinkish-magenta = R-G>60 and R-B in -20..40 (fill 243,148,248 has B>R!)
# sample-based: pinkish magenta family (243,148,248) OR (224,136,224): R>180, G 100..190, B 190..255
line = (R > 175) & (G > 95) & (G < 200) & (B > 185)
seg = line[100:122, 130:610]
rp = seg.sum(axis=1)
print("== connector rows (pinkish-magenta mask, x130..610) ==")
print({100 + i: int(n) for i, n in enumerate(rp) if n > 0})
rowy = 100 + int(np.argmax(rp))
xs = np.where(line[rowy, 130:610])[0] + 130
diffs = np.diff(xs)
uh, uc = np.unique(diffs, return_counts=True)
print(f"row y{rowy}: {len(xs)} dots x{xs.min()}..{xs.max()}")
print("gaps:", dict(zip(map(int, uh), map(int, uc))))
print("dot xs:", list(map(int, xs)))
# vertical thickness at a dot
xd = int(xs[len(xs) // 2])
print(f"column x{xd} y100..122:", [f"y{y}:{tuple(int(v) for v in a[y, xd])}" for y in range(106, 116)])

# raw scan along candidate rows to see everything (no mask)
print("\n== raw non-background pixels y104..116, x130..200 (left segment) ==")
bg = (abs(R - 232) < 12) & (abs(G - 232) < 12) & (abs(B - 232) < 12)
for y in range(104, 117):
    runs = []
    inr = False
    for x in range(128, 210):
        isink = not bg[y, x]
        if isink and not inr:
            s = x; inr = True
        elif not isink and inr:
            runs.append((s, x - 1, tuple(int(v) for v in a[y, (s + x - 1) // 2]))); inr = False
    if runs:
        print(f"  y{y}: {runs}")

print("\n== raw non-background pixels y104..116, x585..612 (right segment) ==")
for y in range(104, 117):
    runs = []
    inr = False
    for x in range(585, 613):
        isink = not bg[y, x]
        if isink and not inr:
            s = x; inr = True
        elif not isink and inr:
            runs.append((s, x - 1, tuple(int(v) for v in a[y, (s + x - 1) // 2]))); inr = False
    if runs:
        print(f"  y{y}: {runs}")

# ---- zoom crops of the top strip ----
im2 = Image.open(ORIG).convert("RGB")
# full strip 4x
strip = im2.crop((50, 80, 690, 132)).resize((640 * 3, 52 * 3), Image.NEAREST)
strip.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide025/z_topstrip_3x.png")
# input box 5x
ib = im2.crop((52, 88, 140, 132)).resize((88 * 5, 44 * 5), Image.NEAREST)
ib.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide025/z_inputbox_5x.png")
# sample label box 5x
sb = im2.crop((598, 80, 675, 126)).resize((77 * 5, 46 * 5), Image.NEAREST)
sb.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide025/z_samplelabel_5x.png")
# line right end 8x (arrowhead check)
re_ = im2.crop((585, 100, 615, 120)).resize((30 * 8, 20 * 8), Image.NEAREST)
re_.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide025/z_line_rightend_8x.png")
# line left end 8x
le_ = im2.crop((124, 100, 154, 120)).resize((30 * 8, 20 * 8), Image.NEAREST)
le_.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide025/z_line_leftend_8x.png")
print("crops saved")
