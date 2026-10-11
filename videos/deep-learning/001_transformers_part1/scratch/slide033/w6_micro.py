#!/usr/bin/env python3
"""Slide 033 pass W6: final micro-measurements before build."""
from PIL import Image
import numpy as np
from collections import Counter

IM = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg').convert('RGB')
A = np.asarray(IM).astype(int)
R, G, B = A[:, :, 0], A[:, :, 1], A[:, :, 2]

def strip(name, y, x0, x1):
    print(f"--- {name} y={y} x{x0}..{x1} ---")
    runs = []
    prev = None
    for x in range(x0, x1 + 1):
        c = tuple(A[y, x])
        if prev is None or max(abs(c[i] - prev[0][i]) for i in range(3)) > 24:
            runs.append([c, x, x])
            prev = runs[-1]
        else:
            runs[-1][2] = x
    print("  " + " ".join(f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}[{a}{'..' + str(b) if b > a else ''}]" for c, a, b in runs))

# V vector row1: vertical extent at x680
print("== V vector row1: col x=680, y224..262 ==")
print("  " + " ".join(f"y{y}:{tuple(A[y,680])}" for y in range(224, 263, 2)))
strip("V vector row1 cells", 236, 660, 700)
strip("K vector row1 cells", 236, 200, 240)
# left container widget row1: full cell run
strip("L container row1 cells", 245, 58, 142)
# right container row1
strip("R container row1 cells", 245, 762, 848)
# sentence widget 1
strip("sentence w1 cells", 493, 184, 258)
# legend strip1 + strip2 rows
strip("legend strip1", 476, 736, 800)
strip("legend strip2", 476, 828, 884)
strip("legend W row", 487, 794, 836)
# Y2 widget cells
strip("Y2 cells", 133, 546, 622)
# emphasis circle plain-peach blend
print("\n== emphasis circle blend samples (away from label) ==")
for (x, y) in [(222, 310), (244, 312), (230, 330), (246, 326), (220, 322)]:
    print(f"  ({x},{y}): {tuple(A[y, x])}")
# line2 red token bboxes: red mask in title band
red = (R - G > 55) & (R - B > 35) & (R > 120)
sub = red[80:100, 180:860]
ys, xs = np.nonzero(sub)
if len(xs):
    cols = np.unique(xs)
    groups = []
    s = p = cols[0]
    for v in cols[1:]:
        if v <= p + 6:
            p = v
        else:
            groups.append((s, p)); s = p = v
    groups.append((s, p))
    print("\n== line2 red token x-clusters ==")
    for (a, b) in groups:
        sel = (xs >= a) & (xs <= b)
        print(f"  x {a+180}..{b+180}: y {ys[sel].min()+80}..{ys[sel].max()+80} n={sel.sum()}")
# line1 blue span end
blue = (B - R > 40) & (B > 90)
sub = blue[56:78, 180:880]
ys, xs = np.nonzero(sub)
print(f"\nline1 blue ink: x {xs.min()+180}..{xs.max()+180}, y {ys.min()+56}..{ys.max()+56}")
subk = (np.maximum.reduce([R,G,B]) < 120)[56:78, 180:880]
ys2, xs2 = np.nonzero(subk)
print(f"line1 black ink: x {xs2.min()+180}..{xs2.max()+180}")
subk2 = (np.maximum.reduce([R,G,B]) < 120)[80:100, 150:880]
ys3, xs3 = np.nonzero(subk2)
print(f"line2 black ink: x {xs3.min()+150}..{xs3.max()+150}, y {ys3.min()+80}..{ys3.max()+80}")
# DP title lines
print("\n== DP title ink rows (dark x262..336) ==")
dk = (np.maximum.reduce([R,G,B]) < 150)[192:235, 262:336]
rr = np.where(dk.sum(axis=1) > 2)[0] + 192
print("  rows:", rr.tolist())
# softmax text extent
dks = (np.maximum.reduce([R,G,B]) < 170)[240:360, 458:492]
rrs = np.where(dks.sum(axis=1) > 2)[0] + 240
print("softmax text rows:", rrs.min(), "..", rrs.max())
ccs = np.where(dks.sum(axis=0) > 2)[0] + 458
print("softmax text cols:", ccs.min(), "..", ccs.max())
# sigma glyph extent
dkz = (B - R > 40)[194:220, 516:650]
rrz = np.where(dkz.sum(axis=1) > 1)[0] + 194
ccz = np.where(dkz.sum(axis=0) > 1)[0] + 516
print("sigma glyph rows:", rrz.min(), "..", rrz.max(), " cols:", ccz.min(), "..", ccz.max())
# Y2 label extent (green ink inside widget)
dkg = (G - R > 40)[118:160, 550:620]
rrg = np.where(dkg.sum(axis=1) > 1)[0] + 118
ccg = np.where(dkg.sum(axis=0) > 1)[0] + 550
print("Y2 label rows:", rrg.min(), "..", rrg.max(), " cols:", ccg.min(), "..", ccg.max())
# pill text bboxes (blue)
bluep = (B - R > 25) & (B - G > 12)
for nm, (x0, x1) in [("S", (262, 345)), ("P", (420, 522)), ("W", (590, 700))]:
    sub = bluep[162:186, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs):
        print(f"pill {nm} text: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+162}..{ys.max()+162} n={len(xs)}")
# W_q label + K label caps for font size
print("\nW_q box text ink rows (dark x280..318):")
dkq = (np.maximum.reduce([R,G,B]) < 180)[432:465, 280:318]
rrq = np.where(dkq.sum(axis=1) > 1)[0] + 432
ccq = np.where(dkq.sum(axis=0) > 1)[0] + 280
print("  rows:", rrq.min(), "..", rrq.max(), " cols:", ccq.min(), "..", ccq.max())
print("W_k box1 text ink (dark x158..196):")
dkw = (np.maximum.reduce([R,G,B]) < 180)[232:262, 158:196]
rrw = np.where(dkw.sum(axis=1) > 1)[0] + 232
ccw = np.where(dkw.sum(axis=0) > 1)[0] + 158
print("  rows:", rrw.min(), "..", rrw.max(), " cols:", ccw.min(), "..", ccw.max())
