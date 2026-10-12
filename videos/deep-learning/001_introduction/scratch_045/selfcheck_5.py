#!/usr/bin/env python3
"""selfcheck_1.py — closed-loop comparator: render_5.png (150dpi) vs slide_045.jpg (960x540).
Same masks on both; all numbers reported in FRAME px (1px = 1pt); tol ~4 frame px.
Banked to qa/slide045/selfcheck_1_out.txt"""
import sys
import numpy as np
from PIL import Image

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045/render_5.png"
ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg"

def load(p):
    im = np.asarray(Image.open(p).convert("RGB")).astype(int)
    return im

ren = load(REN); org = load(ORG)
s = ren.shape[0] / 540.0  # render px per frame px (~2.083)

def to_frame(v):
    return v / s

def mask_ink(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    lum = (r + g + b) / 3
    reddish = (r - g > 30) & (r - b > 20)
    return (lum < 205) & (~reddish)

def mask_red(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return (r - g > 30) & (r - b > 20) & (r > 100)

def mask_yellow(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return (r > 225) & (g > 225) & (r - b > 25) & (b < 225)

def mask_blue(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return (b - r > 30) & (b - g > 25) & (b > 110)

def bbox_in(mask, fx0, fx1, fy0, fy1, img_is_render):
    """ink bbox within a frame-px window; returns frame-px (x0,x1,y0,y1) or None"""
    if img_is_render:
        win = mask[int(fy0 * s):int(fy1 * s) + 1, int(fx0 * s):int(fx1 * s) + 1]
        ox, oy = int(fx0 * s), int(fy0 * s)
    else:
        win = mask[int(fy0):int(fy1) + 1, int(fx0):int(fx1) + 1]
        ox, oy = int(fx0), int(fy0)
    ys, xs = np.where(win)
    if len(ys) == 0:
        return None
    return (xs.min() / (s if img_is_render else 1) + ox / (s if img_is_render else 1),
            xs.max() / (s if img_is_render else 1) + ox / (s if img_is_render else 1),
            ys.min() / (s if img_is_render else 1) + oy / (s if img_is_render else 1),
            ys.max() / (s if img_is_render else 1) + oy / (s if img_is_render else 1))

def cmp(name, tgt, tol=4.0):
    # tgt: (fx0,fx1,fy0,fy1, which) — measure both, print diff vs original
    fx0, fx1, fy0, fy1, m = tgt
    o = bbox_in(m["org"], fx0, fx1, fy0, fy1, False)
    r = bbox_in(m["ren"], fx0, fx1, fy0, fy1, True)
    if o is None or r is None:
        print(f" {name:22s} org={o} ren={r}  <-- MISSING INK")
        return
    d = [r[i] - o[i] for i in range(4)]
    bad = any(abs(x) > tol for x in d)
    print(f" {name:22s} org=({o[0]:6.1f},{o[1]:6.1f},{o[2]:6.1f},{o[3]:6.1f}) "
          f"ren=({r[0]:6.1f},{r[1]:6.1f},{r[2]:6.1f},{r[3]:6.1f}) "
          f"d=({d[0]:+5.1f},{d[1]:+5.1f},{d[2]:+5.1f},{d[3]:+5.1f}){'  <-- CHECK' if bad else ''}")

mI = {"org": mask_ink(org), "ren": mask_ink(ren)}
mR = {"org": mask_red(org), "ren": mask_red(ren)}
mY = {"org": mask_yellow(org), "ren": mask_yellow(ren)}
mB = {"org": mask_blue(org), "ren": mask_blue(ren)}

print("== TITLE (target ink x199..767 y69..99) ==")
cmp("title-band", (150, 790, 60, 104, mI))

print("== DEFBORDER boxes (blue strokes) ==")
cmp("defbox-top", (100, 800, 108, 122, mB))
cmp("defbox-bottom", (100, 800, 200, 216, mB))
cmp("legend-top", (90, 240, 348, 362, mB))
cmp("legend-bottom", (90, 240, 428, 442, mB))
cmp("calloutW-top", (750, 880, 358, 372, mB))
cmp("calloutI-top", (750, 870, 416, 430, mB))

print("== RED box borders ==")
cmp("eqpanel-top", (320, 680, 285, 299, mR))
cmp("eqpanel-bottom", (320, 680, 494, 508, mR))
cmp("remember-bottom", (100, 800, 270, 283, mR))

print("== TEXT bands (ink) ==")
cmp("def-L1", (78, 880, 116, 149, mI))
cmp("def-L2", (78, 880, 149, 175, mI))
cmp("def-L3", (78, 880, 176, 207, mI))
cmp("rem-L1", (74, 880, 229, 250, mR))
cmp("rem-L2", (74, 880, 250, 274, mR))
cmp("leg-L1", (72, 260, 355, 376, mI))
cmp("leg-L2", (72, 260, 376, 395, mI))
cmp("leg-L3", (72, 260, 395, 413, mI))
cmp("leg-L4", (72, 260, 413, 433, mI))
cmp("b1-label", (312, 470, 294, 312, mI))
cmp("b2-label", (312, 680, 372, 395, mI))
cmp("b3-label", (312, 680, 420, 445, mI))
cmp("calloutW-text", (737, 894, 365, 391, mI))
cmp("calloutI-text", (736, 877, 423, 449, mI))

print("== BULLET circles (dark ring) ==")
for i, (cy) in enumerate([304, 382.5, 428.5]):
    cmp(f"bullet{i+1}", (294, 315, cy - 8, cy + 8, mI))

print("== EQUATION tokens (target boxes from manifest) ==")
import json
MAN = json.load(open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/eq_045_manifest.json"))
for name, tok in MAN.items():
    L, T = tok["place_left"], tok["place_top"]
    w, h = tok["target_w"], tok["target_h"]
    cmp(f"tok-{name}", (L - 3, L + w + 6, T - 3, T + h + 6, mI))

print("== EQUATIONS whole-region ink ==")
cmp("eq(a)-all", (465, 696, 296, 375, mI))
cmp("eq(b)-all", (510, 655, 386, 418, mI))
cmp("eq(c)-all", (420, 695, 418, 497, mI))

print("== STARBURST ==")
cmp("star-yellow", (770, 910, 44, 160, mY))
cmp("star-red", (770, 910, 44, 160, mR))

print("== ARROW ==")
cmp("arrow-shaft", (600, 712, 342, 360, mR))
cmp("arrow-head", (604, 626, 342, 362, mR))

print("== FRAME CONTAINMENT (content ink vs chrome panel x42..918 y45..538) ==")
ink_r = mI["ren"]
ys, xs = np.where(ink_r)
print(f" render ink extent (frame px): x {to_frame(xs.min()):.1f}..{to_frame(xs.max()):.1f}  y {to_frame(ys.min()):.1f}..{to_frame(ys.max()):.1f}")
ok = to_frame(xs.min()) >= 42 - 2 and to_frame(xs.max()) <= 918 + 2 and to_frame(ys.min()) >= 45 - 2 and to_frame(ys.max()) <= 538 + 2
print(f" containment: {'OK' if ok else 'VIOLATION'}")
# eqpanel interior containment: eq ink inside x292..699 y291..500
for (nm, X0, X1, Y0, Y1) in [("eq(a)", 465, 696, 296, 375), ("eq(b)", 510, 655, 386, 418), ("eq(c)", 420, 695, 418, 497)]:
    r = bbox_in(mI["ren"], X0, X1, Y0, Y1, True)
    if r:
        inside = r[0] >= 292 + 1.5 and r[1] <= 699 - 1.5 and r[2] >= 291 + 1.5 and r[3] <= 500 - 1.5
        print(f" {nm} inside eqpanel: {'OK' if inside else 'VIOLATION ' + str(r)}")
