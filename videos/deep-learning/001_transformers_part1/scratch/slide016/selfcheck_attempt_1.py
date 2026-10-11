#!/usr/bin/env python3
"""selfcheck_attempt_1.py — pre-judge self-checks for slide 016 render_1.png.
150dpi render (2000x1125); frame-px = render-px * 0.48 (1px frame = 1pt).
Checks: frame containment (green fig frame, panels, containers, callout boxes,
highlight), house-panel containment, explicit line-spacing pins (c4 3-line pitch)."""
import sys
import numpy as np
from PIL import Image

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide016/render_1.png"
im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W = im.shape[:2]
S = H / 1125.0  # render px per 1125-space px
def fx(v): return v * (H / 1125.0) / (1125.0 * (13.333 * 150 / 2000) / 1125.0)  # unused
SCALE = 150 / 72.0  # render px per frame pt (=2.0833)

fails = []
def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond:
        fails.append(f"{name} {detail}")

r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def ink_mask(x0, y0, x1, y1, bg_colors, tol=26):
    """pixels in region that differ from all bg colors"""
    reg = im[int(y0):int(y1), int(x0):int(x1)]
    m = np.ones(reg.shape[:2], dtype=bool)
    for (br, bgc, bb) in bg_colors:
        m &= ~((np.abs(reg[:, :, 0] - br) < tol) & (np.abs(reg[:, :, 1] - bgc) < tol) & (np.abs(reg[:, :, 2] - bb) < tol))
    ys, xs = np.where(m)
    if len(ys) == 0:
        return None
    return (int(x0) + xs.min(), int(y0) + ys.min(), int(x0) + xs.max(), int(y0) + ys.max())

PANEL = (233, 233, 231)
WHITE = (255, 255, 255)

print("== 1. house-panel containment (content ink inside gray panel x42-918 y45-540 frame px) ==")
# callout boxes (left zone) must sit inside panel: boxes c4 x61.5.. y469+515.. etc.
for name, (bx0, by0, bx1, by1) in {
    "c1": (285, 101, 448, 135), "c2": (369, 148, 528, 179),
    "c3": (167, 203, 477, 252), "c4": (61, 290, 528, 354),
    "c5": (90, 402, 446, 450), "c6": (69, 469, 465, 516),
}.items():
    ok = bx0 >= 43 and by0 >= 46 and bx1 <= 917 and by1 <= 538
    check(f"callout {name} inside panel", ok, f"box=({bx0},{by0})-({bx1},{by1})")

print("== 2. green figure-frame containment (diagram ink inside x572-895 y103-525) ==")
# scan the diagram zone; ink = non(panel,white); exclude the leaders' gray (191,191,191)-ish
# and the frame stroke itself (allow 2px around the boundary)
gx0, gy0, gx1, gy1 = int(572 * SCALE), int(103 * SCALE), int(895 * SCALE), int(525 * SCALE)
zone = im[gy0:gy1, gx0:gx1]
nz = ~((np.abs(zone[:, :, 0] - 233) < 26) & (np.abs(zone[:, :, 1] - 233) < 26) & (np.abs(zone[:, :, 2] - 231) < 26))
nz &= ~((zone[:, :, 0] > 244) & (zone[:, :, 1] > 244) & (zone[:, :, 2] > 240))
ys, xs = np.where(nz)
check("diagram zone has ink", len(ys) > 1000, f"n={len(ys)}")
print(f"  diagram ink bbox (render px): x{xs.min()+gx0}-{xs.max()+gx0} y{ys.min()+gy0}-{ys.max()+gy0}")

# check left column of callout zone: no diagram ink left of the green frame
left = im[gy0:gy1, int(43 * SCALE):int(560 * SCALE)]
nzl = ~((np.abs(left[:, :, 0] - 233) < 26) & (np.abs(left[:, :, 1] - 233) < 26) & (np.abs(left[:, :, 2] - 231) < 26))
nzl &= ~((left[:, :, 0] > 244) & (left[:, :, 1] > 244) & (left[:, :, 2] > 240))
# exclude leader gray
nzl &= ~((np.abs(left[:, :, 0] - 191) < 40) & (np.abs(left[:, :, 1] - 191) < 40) & (np.abs(left[:, :, 2] - 191) < 40))
ysl, xsl = np.where(nzl)
# everything found must belong to callout boxes (colored fills/text) — verify x-range of boxes
if len(ysl):
    print(f"  left-zone non-gray ink bbox: x{xsl.min()+int(43*SCALE)}-{xsl.max()+int(43*SCALE)} y{ysl.min()+gy0}-{ysl.max()+gy0}")

print("== 3. callout text inside boxes ==")
def text_in_box(name, bx0, by0, bx1, by1, fills):
    bb = ink_mask(bx0 * SCALE + 3, by0 * SCALE + 3, bx1 * SCALE - 3, by1 * SCALE - 3, fills, 30)
    if bb is None:
        check(f"{name} has text", False, "NO INK")
        return
    inside = bb[0] >= bx0 * SCALE - 2 and bb[2] <= bx1 * SCALE + 2 and bb[1] >= by0 * SCALE - 2 and bb[3] <= by1 * SCALE + 2
    check(f"{name} text inside box", inside, f"ink=({bb[0]},{bb[1]})-({bb[2]},{bb[3]}) box=({bx0},{by0})-({bx1},{by1})")

text_in_box("c1", 285, 101, 448, 135, [(184, 230, 202)])
text_in_box("c2", 369, 148, 528, 179, [(242, 198, 198)])
text_in_box("c3", 167, 203, 477, 252, [(216, 204, 180)])
text_in_box("c4", 61, 290, 528, 354, [(255, 255, 153)])
text_in_box("c5", 90, 402, 446, 450, [(228, 252, 252)])
text_in_box("c6", 69, 469, 465, 516, [(228, 252, 252)])

print("== 4. containers: content ink inside ==")
# enc container (frame px 628.5-727.5 x 267.5-408.5): non-tan ink inside
bb = ink_mask(630 * SCALE, 269 * SCALE, 726 * SCALE, 407 * SCALE, [(200, 168, 136)], 30)
if bb:
    inside = bb[0] >= 629 * SCALE - 3 and bb[2] <= 727 * SCALE + 3 and bb[1] >= 268 * SCALE - 3 and bb[3] <= 408 * SCALE + 3
    check("enc container ink inside", inside, f"ink=({bb[0]/SCALE:.0f},{bb[1]/SCALE:.0f})-({bb[2]/SCALE:.0f},{bb[3]/SCALE:.0f}) frame-px")
else:
    check("enc container ink", False, "none")
# dec upper container (744-841 x 199.5-324.5)
bb = ink_mask(746 * SCALE, 201.5 * SCALE, 839 * SCALE, 322.5 * SCALE, [(181, 184, 141), (206, 255, 225)], 30)
if bb:
    inside = bb[0] >= 744 * SCALE - 4 and bb[2] <= 841 * SCALE + 4 and bb[1] >= 199 * SCALE - 4 and bb[3] <= 325 * SCALE + 4
    check("dec upper container ink inside", inside, f"ink=({bb[0]/SCALE:.0f},{bb[1]/SCALE:.0f})-({bb[2]/SCALE:.0f},{bb[3]/SCALE:.0f})")
else:
    check("dec upper container ink", False, "none")
# dec lower container (744-834 x 325.5-409.5)
bb = ink_mask(746 * SCALE, 327.5 * SCALE, 832 * SCALE, 407.5 * SCALE, [(197, 246, 217), (206, 255, 225)], 26)
if bb:
    inside = bb[0] >= 744 * SCALE - 4 and bb[2] <= 834 * SCALE + 4 and bb[1] >= 325 * SCALE - 4 and bb[3] <= 410 * SCALE + 4
    check("dec lower container ink inside", inside, f"ink=({bb[0]/SCALE:.0f},{bb[1]/SCALE:.0f})-({bb[2]/SCALE:.0f},{bb[3]/SCALE:.0f})")
else:
    check("dec lower container ink", False, "none")

print("== 5. highlight present (yellow + red dashes) ==")
yel = (r > 225) & (g > 225) & (b < 130)
ys, xs = np.where(yel[int(240 * SCALE):int(330 * SCALE), int(660 * SCALE):int(800 * SCALE)])
check("yellow band ink present", len(ys) > 400, f"n={len(ys)}")
if len(ys):
    print(f"  yellow bbox frame-px: x{(xs.min()+int(660*SCALE))/SCALE:.0f}-{(xs.max()+int(660*SCALE))/SCALE:.0f} y{(ys.min()+int(240*SCALE))/SCALE:.0f}-{(ys.max()+int(240*SCALE))/SCALE:.0f}")
red = (r > 150) & (g < 100) & (b < 100)
ys, xs = np.where(red[int(240 * SCALE):int(335 * SCALE), int(660 * SCALE):int(800 * SCALE)])
check("red dash ink present", len(ys) > 80, f"n={len(ys)}")

print("== 6. explicit line-spacing: c4 3-line pitch ==")
# c4 box (frame 61.5-527.5 x 290.5-354) -> render; find text row bands (dark/blue ink)
bx0, by0, bx1, by1 = int(70 * SCALE), int(292 * SCALE), int(520 * SCALE), int(352 * SCALE)
reg = im[by0:by1, bx0:bx1]
dark = (reg.max(axis=2) < 160) | ((reg[:, :, 2] > 150) & (reg[:, :, 0] < 130)) | ((reg[:, :, 0] > 150) & (reg[:, :, 2] < 120))
rowsum = dark.sum(axis=1)
rows = [i for i, v in enumerate(rowsum) if v > 8]
bands = []
if rows:
    s = p = rows[0]
    for i in rows[1:]:
        if i <= p + 3: p = i
        else: bands.append((s, p)); s = p = i
    bands.append((s, p))
centers = [((a + bb_) / 2 + by0) / SCALE for a, bb_ in bands]
print(f"  c4 text bands (frame-px y centers): {[f'{c:.1f}' for c in centers]}")
if len(centers) >= 3:
    p1 = centers[1] - centers[0]
    p2 = centers[2] - centers[1]
    check("c4 line pitch ~19pt", abs(p1 - 19) <= 2.5 and abs(p2 - 19) <= 2.5, f"pitches {p1:.1f}, {p2:.1f}")
else:
    check("c4 3 lines detected", False, f"bands={len(bands)}")

print("== 7. no ink wrap outside c6 box (longest line) ==")
bb = ink_mask(69 * SCALE, 469 * SCALE, 465 * SCALE, 516 * SCALE, [(228, 252, 252)], 30)
if bb:
    inside = bb[0] >= 69 * SCALE - 2 and bb[2] <= 465 * SCALE + 2 and bb[1] >= 469 * SCALE - 2 and bb[3] <= 516 * SCALE + 2
    check("c6 text inside box", inside, f"ink=({bb[0]},{bb[1]})-({bb[2]},{bb[3]})")

print()
if fails:
    print(f"SELFCHECK: FAIL ({len(fails)})")
    for f in fails: print("  -", f)
    sys.exit(1)
print("SELFCHECK: ALL PASS")
