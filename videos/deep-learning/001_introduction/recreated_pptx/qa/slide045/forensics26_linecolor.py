#!/usr/bin/env python3
"""forensics26: connector A line true color; corridor B ultra-low-threshold scan."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
org = np.asarray(Image.open(VID + "/unique_slides/slide_045.jpg").convert("RGB")).astype(int)

print("== connector A line pixel colors (sampled along the diagonal) ==")
for (x, y) in [(708, 357), (711, 359), (714, 362), (717, 364), (720, 367), (723, 369), (726, 371), (729, 373), (732, 375)]:
    print(f"  ({x},{y}) = {tuple(org[y, x])}   neighbors: {tuple(org[y-1, x])} {tuple(org[y+1, x])}")

print("== arrowhead red pixels true colors ==")
for (x, y) in [(704, 350), (705, 352), (695, 348), (693, 346), (703, 353)]:
    print(f"  ({x},{y}) = {tuple(org[y, x])}")

print("== corridor B ultra-faint scan x680..734 y425..470 (delta>10 from bg) ==")
r, g, b = org[:, :, 0], org[:, :, 1], org[:, :, 2]
f10 = (r < 223) & ~((abs(r - 233) < 8) & (abs(g - 233) < 8) & (abs(b - 231) < 8))
hits = 0
for y in range(425, 470):
    cols = [c for c in np.where(f10[y, 680:735])[0] + 680 if c > 703]
    if cols:
        hits += len(cols)
        print(f"  y{y}: {cols}")
print(f"  total (excl border cols <=703): {hits}")

print("== corridor B inside-panel x677..696 y450..480 (any ink, delta>10) ==")
for y in range(450, 480):
    cols = list(np.where(f10[y, 677:697])[0] + 677)
    if cols:
        print(f"  y{y}: {cols}")

print("== eq(c) row: where exactly does x_{r-i,c-j} end? dark mask x615..700 y455..478 ==")
dark = (r < 110) & (g < 110) & (b < 110)
for y in range(455, 478):
    cols = list(np.where(dark[y, 615:700])[0] + 615)
    if cols:
        print(f"  y{y}: {cols}")
