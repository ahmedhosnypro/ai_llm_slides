#!/usr/bin/env python3
"""Slide 043 round 2: callout border rect, per-line census with clean windows,
bottom-box left starts, black pixels in L3, pencil icon."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (r > 130) & (r - g > 60) & (r - b > 60) & (g < b + 35)

# callout border: strict red-text mask, window x 330..640, y 160..285
print("CALLOUT border rows (rowfrac x345..610 >0.7):")
sub = red[160:285, 345:610]
for y in range(sub.shape[0]):
    fr = sub[y].mean()
    if fr > 0.7: print("  y", 160 + y, round(fr, 2))
print("CALLOUT border cols (colfrac y178..262 >0.7):")
subv = red[178:262, 330:645]
for x in range(subv.shape[1]):
    fr = subv[:, x].mean()
    if fr > 0.7: print("  x", 330 + x, round(fr, 2))

def census(y0, y1, x0, x1, tag):
    reg = slice(y0, y1 + 1)
    rr, gg, bb = r[reg, x0:x1], g[reg, x0:x1], b[reg, x0:x1]
    blue = ((bb - rr > 40) & (bb - gg > 20) & (bb > 80))
    redc = ((rr - gg > 60) & (rr - bb > 60) & (gg < bb + 35))
    black = ((rr < 110) & (gg < 110) & (bb < 110))
    green = ((gg - rr > 30) & (gg - bb > 30) & (gg > 100))
    print(f"  {tag} y{y0}..{y1} x{x0}..{x1}: blue {blue.sum()} red {redc.sum()} black {black.sum()} green {green.sum()}")
    for name, m in [("blue", blue), ("red", redc), ("black", black), ("green", green)]:
        ys, xs = np.where(m)
        if len(xs) > 30:
            print(f"    {name}: x {xs.min()+x0}..{xs.max()+x0}")

print("CALLOUT per-line census:")
census(180, 192, 330, 640, "C-L1")
census(200, 214, 330, 640, "C-L2")
census(223, 236, 330, 640, "C-L3")
census(244, 259, 330, 640, "C-L4")
print("CALLOUT per-line x-extents (ink frac>0.04, x330..640):")
ink = (r < 170) | ((r - g > 60) & (r - b > 60)) | ((b - r > 40) & (b > 80)) | ((g - r > 30) & (g - b > 30))
for (y0, y1, tag) in [(180, 192, "C-L1"), (200, 214, "C-L2"), (223, 236, "C-L3"), (244, 259, "C-L4")]:
    cols = ink[y0:y1 + 1, 330:640].mean(axis=0)
    nz = [330 + i for i, v in enumerate(cols) if v > 0.04]
    print(f"  {tag}: x {nz[0]}..{nz[-1]}" if nz else f"  {tag}: none")

# cream fill bbox inside border (sample strict cream)
cream = (r > 240) & (g > 240) & (b > 200) & (b < 240)
ys, xs = np.where(cream[160:285, 330:645])
print("CREAM(strict) bbox x", xs.min() + 330, "..", xs.max() + 330, " y", ys.min() + 160, "..", ys.max() + 160)
print("cream sample colors:", [tuple(a[y, x]) for y, x in [(200, 360), (230, 500), (250, 580), (185, 600)]])

# bottom box lines: clean x window 90..860, ink incl colored but NOT the green border cols
ink2 = (r < 170) | ((r - g > 60) & (r - b > 60)) | ((b - r > 40) & (b > 80)) | ((g - r > 30) & (g - b > 30))
ink2[:, :90] = False; ink2[:, 860:] = False
print("BOTTOM lines x-extents + left starts:")
for (y0, y1, tag) in [(370, 383, "B-L1a"), (386, 405, "B-L1b"), (429, 447, "B-L2"), (472, 493, "B-L3")]:
    cols = ink2[y0:y1 + 1, :].mean(axis=0)
    nz = [i for i, v in enumerate(cols) if v > 0.04]
    print(f"  {tag}: x {nz[0]}..{nz[-1]}" if nz else f"  {tag}: none")
print("BOTTOM per-line census (x90..860):")
census(370, 383, 90, 860, "B-L1a")
census(386, 405, 90, 860, "B-L1b")
census(429, 447, 90, 860, "B-L2")
census(472, 493, 90, 860, "B-L3")
# black pixel locations in L3
rr, gg, bb = r[472:494, 90:860], g[472:494, 90:860], b[472:494, 90:860]
blackm = (rr < 110) & (gg < 110) & (bb < 110)
ys, xs = np.where(blackm)
if len(xs):
    print("  B-L3 black-pixel x clusters:", sorted(set((xs + 90) // 20 * 20)))
# pencil icon: gray/dark ink inside callout bottom-left (x335..390, y235..265)
penc = (r < 150) & (g < 150) & (b < 160)
ys, xs = np.where(penc[235:268, 330:400])
if len(xs):
    print("PENCIL bbox x", xs.min() + 330, "..", xs.max() + 330, " y", ys.min() + 235, "..", ys.max() + 235)
