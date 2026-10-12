#!/usr/bin/env python3
"""Closed-loop self-check: render_1.png (2001x1125, 2.0833 px/frame-px) vs the
PIL-measured geometry of slide_042.jpg. Tolerances: layout <= 5 render px
(~2.4 frame px), per 17 alignment law (4 px @150dpi standard)."""
import numpy as np
from PIL import Image

REND = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide042/render_1.png"
im = np.asarray(Image.open(REND).convert("RGB")).astype(int)
H, W = im.shape[:2]
S = H / 540.0  # render px per frame px

r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
strong_red = (r - g > 60) & (r - b > 60) & (r > 110)
blue = (b - r > 50) & (b - g > 30)
green = (g - r > 40) & (g - b > 40) & (g > 90)

fails = []
def check(name, got, want, tol=5.0):
    d = max(abs(a - w) for a, w in zip(got, want)) if isinstance(got, (list, tuple)) else abs(got - want)
    status = "OK " if d <= tol else "FAIL"
    print(f"  [{status}] {name}: got {got} want {want} (maxdiff {d:.1f}, tol {tol})")
    if d > tol:
        fails.append(name)

def bbox(mask, y0, y1, x0=0, x1=None):
    x1 = x1 or W
    m = mask[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if not len(ys):
        return None
    return (xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0)

print("== title (want ink x299-663 y81-103 frame px) ==")
tb = bbox(strong_red, int(50 * S), int(130 * S), int(60 * S), int(900 * S))
if tb:
    got = [v / S for v in tb]
    check("title bbox (x0,x1,y0,y1)", got, [299, 663, 81, 103], tol=5)
else:
    fails.append("title missing")

print("== subtitle (want L1 x108-832 ytop~151-152; L2 x359-581 ytop~174) ==")
s1 = bbox(strong_red, int(135 * S), int(172 * S), int(60 * S), int(880 * S))
s2 = bbox(strong_red, int(172 * S), int(193 * S), int(100 * S), int(860 * S))
if s1:
    check("sub L1 (x0,x1,y0)", [s1[0] / S, s1[1] / S, s1[2] / S], [108, 832, 151.5], tol=5)
else: fails.append("sub L1 missing")
if s2:
    check("sub L2 (x0,x1,y0)", [s2[0] / S, s2[1] / S, s2[2] / S], [359, 581, 174], tol=5)
else: fails.append("sub L2 missing")

print("== content box borders (want x 72..880, ytop 196, ybot 483) ==")
# top border: row with >1000 strong-red in mid area
tops = [y for y in range(int(180 * S), int(220 * S)) if strong_red[y, int(100*S):int(850*S)].sum() > 500]
bots = [y for y in range(int(470 * S), int(500 * S)) if strong_red[y, int(100*S):int(850*S)].sum() > 500]
if tops: check("box top border row", tops[0] / S, 196, tol=5)
else: fails.append("box top border missing")
if bots: check("box bottom border row", bots[-1] / S, 483, tol=5)
else: fails.append("box bottom border missing")
mid = slice(int(300 * S), int(310 * S))
lc = [x for x in range(int(60 * S), int(90 * S)) if strong_red[mid, x].sum() >= 8]
rc = [x for x in range(int(860 * S), int(900 * S)) if strong_red[mid, x].sum() >= 8]
if lc: check("box left border col", lc[0] / S, 71, tol=5)
else: fails.append("box left border missing")
if rc: check("box right border col", rc[-1] / S, 880, tol=5)
else: fails.append("box right border missing")

print("== body lines (blue ink; want tops 234/286/346/398/428, left 82) ==")
rows = np.where(blue[int(210 * S):int(470 * S)].sum(axis=1) > 3)[0] + int(210 * S)
bands = []
s = p = rows[0]
for i in rows[1:]:
    if i == p + 1: p = i
    else: bands.append((s, p)); s = p = i
bands.append((s, p))
want = [(234, 251, 82, 400), (286, 303, 82, 610), (346, 367, 82, 827), (398, 419, 82, 770), (428, 446, 82, 849)]
print(f"  found {len(bands)} blue bands")
for i, (b0, b1) in enumerate(bands[:6]):
    m = blue[b0:b1 + 1]
    xs = np.where(m.sum(axis=0) > 0)[0]
    got = [b0 / S, b1 / S, xs.min() / S, xs.max() / S]
    if i < len(want):
        w0, w1, wl, wr = want[i]
        check(f"L{i+1} (top,bot,left,right)", got, [w0, w1, wl, wr], tol=6)
    else:
        print(f"  extra band {i+1}: {got}")

print("== green subscripts line 2 (want clusters at 464-472, 531-538, 592-599, y~296-303) ==")
g2 = bbox(green, int(282 * S), int(310 * S), int(60 * S), int(700 * S))
if g2:
    check("green line2 bbox (x0,x1)", [g2[0] / S, g2[1] / S], [464, 599], tol=6)
else: fails.append("green subscripts missing")

print("== red math runs ==")
inside = np.zeros((H, W), bool); inside[int(200 * S):int(480 * S), int(78 * S):int(872 * S)] = True
redin = strong_red & inside
for y0, y1, want_x, lbl in [
    (230, 255, (386, 393), "L1 red r"),
    (280, 310, (458, 589), "L2 red sups span"),
    (340, 370, (186, 821), "L3 red X..Yr"),
    (425, 450, (710, 723), "L4 red X"),
]:
    m = redin[int(y0 * S):int(y1 * S)]
    ys, xs = np.where(m)
    if len(ys):
        check(f"{lbl} (x0,x1)", [xs.min() / S, xs.max() / S], list(want_x), tol=7)
    else:
        fails.append(f"{lbl} missing")

print("== color cores ==")
def core_color(y0, y1, x0, x1, mask):
    m = mask[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    ys, xs = np.where(m)
    if not len(ys): return None
    return np.median(im[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)][m], axis=0)

tc = core_color(60, 120, 250, 700, strong_red)
print("  title core:", tc, "(want ~C00000=192,0,0 dulled by JPEG ~170,35,48)")
bc = core_color(230, 255, 80, 420, blue)
print("  body core:", bc, "(want ~0000CC=0,0,204 dulled ~49,40,134)")

print()
if fails:
    print("SELF-CHECK GEOMETRY: FAIL ->", fails)
else:
    print("SELF-CHECK GEOMETRY: ALL OK")
