#!/usr/bin/env python3
"""forensics10.py — exhaustive redness sweep for arrows + composite crop for vision check.
Banked to qa/slide045/forensics10_out.txt; composite to qa/slide045/z_arrows_composite.png"""
import numpy as np
from PIL import Image

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg"
im = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
redness = r - (g + b) / 2

print("== FULL redness sweep: any reddish px (redness>35) outside known red elements ==")
known_red = np.zeros_like(redness, dtype=bool)
# chrome border, eqpanel border, remember border, callout? (blue), starburst zone
known_red[40:48, 50:910] = True      # chrome top
known_red[:, 55:61] = True           # chrome left
known_red[:, 915:921] = True         # chrome right
known_red[288:296, 289:703] = True   # eqpanel top
known_red[497:505, 289:703] = True   # eqpanel bottom
known_red[288:505, 289:295] = True   # eqpanel left
known_red[288:505, 696:704] = True   # eqpanel right
known_red[273:280, 66:890] = True    # remember bottom
known_red[225:233, 66:890] = True    # remember top
known_red[225:280, 66:74] = True     # remember left
known_red[225:280, 879:887] = True   # remember right
known_red[40:160, 770:905] = True    # starburst zone
known_red[515:540, :] = True         # black bar zone
ys, xs = np.where((redness > 35) & (~known_red))
print(f" loose reddish px count: {len(ys)}")
if len(ys):
    import collections
    clusters = collections.Counter()
    for yy, xx in zip(ys, xs):
        clusters[(yy // 8 * 8, xx // 8 * 8)] += 1
    for (cy, cx), n in sorted(clusters.items(), key=lambda kv: -kv[1])[:40]:
        print(f"  cluster y{cy}..{cy+7} x{cx}..{cx+7}: {n}")

print("\n== ARROW1 tail zone x706..738 y338..395 redness rows ==")
for yy in range(338, 396):
    row = redness[yy, 706:739]
    if row.max() > 25:
        cxs = np.where(row > 25)[0] + 706
        print(f"  y={yy}: x{cxs.min()}..{cxs.max()} max={row.max():.0f}")

print("\n== ARROW2 low zone x676..745 y450..505 redness rows ==")
for yy in range(450, 506):
    row = redness[yy, 676:746]
    if row.max() > 25:
        cxs = np.where(row > 25)[0] + 676
        print(f"  y={yy}: x{cxs.min()}..{cxs.max()} max={row.max():.0f}")

# ---- composite crop for the vision gate: arrow1 zone + arrow2 zone, 2x ----
A = Image.open(SRC).convert("RGB").crop((575, 316, 915, 400))   # 340x84
B = Image.open(SRC).convert("RGB").crop((575, 408, 915, 500))   # 340x92
z = 2
A = A.resize((A.width * z, A.height * z), Image.LANCZOS)
B = B.resize((B.width * z, B.height * z), Image.LANCZOS)
W = max(A.width, B.width)
comp = Image.new("RGB", (W, A.height + B.height + 8), (255, 0, 0))
comp.paste(A, (0, 0))
comp.paste(B, (0, A.height + 8))
out = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045/z_arrows_composite.png"
comp.save(out)
print(f"\nsaved {out} ({comp.width}x{comp.height}); panel A = original y316..400, panel B = y408..500, both x575..915 at 2x")
