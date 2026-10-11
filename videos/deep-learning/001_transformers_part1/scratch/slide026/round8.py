#!/usr/bin/env python3
import numpy as np
from PIL import Image

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
IM2 = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_002.jpg").convert("RGB")
B = np.asarray(IM2).astype(int)

print("== chrome border comparison: col medians y300..360 ==")
for nm, M in (("s26", A), ("s02", B)):
    for x in list(range(34, 56)):
        c = np.median(M[300:360, x], axis=0).astype(int)
        print(f"  {nm} x={x}: #{c[0]:02X}{c[1]:02X}{c[2]:02X}", end="")
        if x == 45: print()
    print()
    for x in list(range(912, 928)):
        c = np.median(M[300:360, x], axis=0).astype(int)
        print(f"  {nm} x={x}: #{c[0]:02X}{c[1]:02X}{c[2]:02X}", end="")
    print()

print("\n== right-side tint check s26 ==")
for y in (150, 250, 350, 430, 500):
    for x in (880, 900, 915):
        c = A[y, x]
        print(f"  ({x},{y}) #{c[0]:02X}{c[1]:02X}{c[2]:02X}", end="")
    print()

print("\n== line continuity (rows y245..248 etc, x490..766) ==")
PEACH = np.array([247, 227, 206])
for y0 in (245, 286, 327, 371):
    band = A[y0:y0+3, 490:766]
    ink = (np.abs(band - PEACH).sum(axis=2) > 35).any(axis=0)
    xs = np.where(ink)[0]
    if len(xs):
        # find gaps > 6
        gaps, prev = [], xs[0]
        for v in xs[1:]:
            if v > prev + 6: gaps.append((490 + prev, 490 + v))
            prev = v
        print(f"  y~{y0+1}: x{490+xs.min()}..{490+xs.max()} gaps={gaps}")
    else:
        print(f"  y~{y0+1}: none")

print("\n== fills ==")
def fmed(nm, x0, y0, x1, y1, M=A):
    sub = M[y0:y1, x0:x1].reshape(-1, 3)
    m = np.median(sub, axis=0).astype(int)
    print(f"  {nm:26s} #{m[0]:02X}{m[1]:02X}{m[2]:02X} {tuple(m)}")
fmed("peach", 700, 440, 850, 465)
fmed("left_stack_fill", 61, 260, 66, 275)
fmed("strip_fill", 158, 482, 170, 510)
fmed("softmax_bar", 462, 210, 484, 260)
fmed("dotproduct_box", 258, 240, 270, 268)
fmed("sigma_box", 525, 200, 570, 214)
fmed("X2_fill", 278, 486, 322, 500)
fmed("red_block_arrow", 268, 512, 284, 524)
fmed("ybox_b1", 554, 128, 574, 138)
fmed("ybox_b2", 566, 128, 586, 138)
fmed("ybox_b3", 592, 128, 610, 138)
fmed("right_panel_zone", 880, 400, 915, 460)

print("\n== X2 border ring ==")
ring = np.concatenate([A[473:476, 262:336].reshape(-1,3), A[504:507, 262:336].reshape(-1,3),
                       A[476:504, 261:265].reshape(-1,3), A[476:504, 332:336].reshape(-1,3)])
sat = ring[(ring[:, 0] > 110) & (ring[:, 0] - ring[:, 1] > 40)]
print(f"  n={len(sat)} med={np.median(sat, axis=0) if len(sat) else 'none'}")

print("\n== W label row prints x490..520 ==")
def cls(c):
    r, g, b = c
    if r < 165 and g < 165 and b < 200: return "k"
    if b - r > 25: return "B"
    if abs(r-247)+abs(g-227)+abs(b-206) <= 40: return "."
    if r > 240 and g > 240: return "w"
    return "?"
for y in range(226, 238):
    print(f"  y{y}: " + "".join(cls(A[y, x]) for x in range(490, 520)))

print("\n== query arrow + block arrow ==")
def cls2(c):
    r, g, b = c
    if r < 170 and g < 130: return "R"
    if abs(r-247)+abs(g-227)+abs(b-206) <= 40: return "."
    if r > 240 and g > 240: return "w"
    if g - r > 15: return "G"
    return "?"
print("  block arrow region x262..292, y505..532:")
for y in range(505, 533):
    print(f"  y{y}: " + "".join(cls2(A[y, x]) for x in range(260, 296)))
print("  query arrow x292..304, y400..480 col ink:")
sub = A[400:480, 290:306]
m = (sub[:, :, 0] - sub[:, :, 1] > 35) & (sub[:, :, 0] > 120)
ys, xs = np.where(m)
print(f"    n={len(xs)} x{290+xs.min()}..{290+xs.max()} y{400+ys.min()}..{400+ys.max()}" if len(xs) else "    none")

print("\n== subtitle full ink map (red vs black) ==")
sub = A[78:103, 180:812]
red = (sub[:, :, 0] - sub[:, :, 1] > 60) & (sub[:, :, 0] > 120)
blk = (sub.sum(axis=2) < 330) & ~red
ys, xs = np.where(red)
print(f"  red tokens bbox x{180+xs.min()}..{180+xs.max()}")
L = np.zeros(sub.shape[:2], dtype=int)
cols_red = red.sum(axis=0); cols_blk = blk.sum(axis=0)
runs, s = [], None
for i, v in enumerate(cols_red >= 1):
    if v and s is None: s = i
    if not v and s is not None:
        runs.append((180 + s, 180 + i - 1)); s = None
print("  red col runs:", runs)
print("  blk col extent:", 180 + int(np.where(cols_blk >= 1)[0].min()), "..", 180 + int(np.where(cols_blk >= 1)[0].max()))

print("\n== title line1 ink (excl badge) ==")
sub = A[50:80, 60:860]
m = sub.sum(axis=2) < 340
ys, xs = np.where(m)
print(f"  x{60+xs.min()}..{60+xs.max()} y{50+ys.min()}..{50+ys.max()}")
# words: column runs
cols = m.sum(axis=0)
runs, s = [], None
for i, v in enumerate(cols >= 1):
    if v and s is None: s = i
    if not v and s is not None:
        if i - s >= 2: runs.append((60 + s, 60 + i - 1)); s = None
        else: s = None
if s is not None: runs.append((60 + s, 60 + len(cols) - 1))
print("  word runs:", runs)
