#!/usr/bin/env python3
import numpy as np
from PIL import Image

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
PEACH = np.array([247, 227, 206]); GRAY = np.array([233, 233, 231])

def cls(c):
    r, g, b = c
    if r < 165 and g < 165: return "k"
    if r - g > 45 and r > 150: return "R"
    if r > 240 and g > 240 and b < 228: return "Y"
    if b - r > 25 and b > 200: return "L"
    if r > 225 and 120 < g < 215 and b > 185 and r - g > 25: return "P"
    if g - r > 12 and g - b > 12 and g > 170 and r < 235: return "G"
    if g > r and g > b and g > 230 and r > 200: return "m"
    if r > 240 and g > 240 and b > 240: return "w"
    if abs(r-247)+abs(g-227)+abs(b-206) <= 40: return "."
    if abs(r-233)+abs(g-233)+abs(b-231) <= 22: return ","
    if r > 200 and g > 180 and b > 160 and r - b > 25: return "t"
    return "?"

def amap1(name, x0, x1, y0, y1):
    print(f"== {name} x{x0}..{x1-1} y{y0}..{y1-1} ==")
    for y in range(y0, y1):
        print(f"{y:3d} " + "".join(cls(A[y, x]) for x in range(x0, x1)))

amap1("BOTTOM-LEFT band", 30, 190, 385, 470)
amap1("BOTTOM-RIGHT band", 780, 928, 375, 470)

print("\n== line continuity x490..766 ==")
for y in (246, 287, 328, 372):
    row = A[y, 490:766]
    ink = (np.abs(row - PEACH).sum(axis=1) > 30)
    runs, s = [], None
    for i, v in enumerate(ink):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= 1: runs.append((490 + s, 490 + i - 1))
            s = None
    if s is not None: runs.append((490 + s, 765))
    print(f"  y={y}: {runs}")

print("\n== fills (medians) ==")
def fmed(nm, x0, y0, x1, y1):
    sub = A[y0:y1, x0:x1].reshape(-1, 3)
    m = np.median(sub, axis=0).astype(int)
    print(f"  {nm:26s} #{m[0]:02X}{m[1]:02X}{m[2]:02X} {tuple(m)}")
fmed("peach_canvas", 700, 440, 850, 465)
fmed("left_stack_fill", 62, 260, 66, 275)
fmed("right_stack_fill", 838, 260, 842, 275)
fmed("strip_fill", 160, 480, 172, 510)
fmed("softmax_bar", 462, 210, 484, 260)
fmed("dotproduct_box", 260, 240, 272, 270)
fmed("sigma_box", 525, 200, 570, 214)
fmed("X2_fill", 280, 486, 320, 500)
fmed("red_block_arrow", 268, 512, 284, 524)
fmed("ybox_b1", 553, 128, 574, 138)
fmed("ybox_b2", 566, 128, 588, 138)
fmed("ybox_b3", 596, 128, 610, 138)
fmed("title_ink_core", 250, 60, 480, 72)

print("\n== X2 border ring colors ==")
ring = []
for x in range(263, 335):
    ring.append(A[474, x]); ring.append(A[505, x])
for y in range(474, 506):
    ring.append(A[263, y] if y < A.shape[0] else GRAY)
    ring.append(A[334, y])
ring = np.array(ring)
sat = ring[(ring[:, 0] > 120) & (ring[:, 0] - ring[:, 1] > 30)]
print(f"  ring n={len(sat)} med={np.median(sat, axis=0) if len(sat) else 'none'}")

print("\n== W label wide scan ==")
sub = A[222:242, 488:520]
m = (sub[:, :, 2] - sub[:, :, 0] > 25) & (sub.sum(axis=2) < 620)
ys, xs = np.where(m)
print(f"  n={len(xs)} x{488+xs.min()}..{488+xs.max()} y{222+ys.min()}..{222+ys.max()}" if len(xs) else "  none")
for y in range(224, 240):
    print(f"  y{y}: " + "".join(cls(A[y, x]) for x in range(490, 518)))
