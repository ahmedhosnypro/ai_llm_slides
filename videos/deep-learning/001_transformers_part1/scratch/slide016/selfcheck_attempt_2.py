#!/usr/bin/env python3
"""selfcheck_attempt_2.py — pre-judge self-checks for slide 016 render_2.png.
150dpi render (2000x1125); frame-px = render-px / SCALE (1px frame = 1pt).
Attempt-2 additions: dec-top no-overlap (MAJOR 1 fix), enc sub-block outlines
(MAJOR 2 fix), Nx arrow ink, sine glyph ink. Re-runs all attempt-1 checks."""
import sys
import numpy as np
from PIL import Image

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide016/render_2.png"
im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W = im.shape[:2]
SCALE = 150 / 72.0  # render px per frame pt

fails = []
def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond:
        fails.append(f"{name} {detail}")

def ink_mask(x0, y0, x1, y1, bg_colors, tol=26):
    reg = im[int(y0):int(y1), int(x0):int(x1)]
    m = np.ones(reg.shape[:2], dtype=bool)
    for (br, bgc, bb) in bg_colors:
        m &= ~((np.abs(reg[:, :, 0] - br) < tol) & (np.abs(reg[:, :, 1] - bgc) < tol) & (np.abs(reg[:, :, 2] - bb) < tol))
    ys, xs = np.where(m)
    if len(ys) == 0:
        return None
    return (int(x0) + xs.min(), int(y0) + ys.min(), int(x0) + xs.max(), int(y0) + ys.max())

PANEL = (233, 233, 231)

print("== 1. house-panel containment (callout boxes inside gray panel) ==")
for name, (bx0, by0, bx1, by1) in {
    "c1": (285, 101, 448, 135), "c2": (369, 148, 528, 179),
    "c3": (167, 203, 477, 252), "c4": (61, 290, 528, 354),
    "c5": (90, 402, 446, 450), "c6": (69, 469, 465, 516),
}.items():
    ok = bx0 >= 43 and by0 >= 46 and bx1 <= 917 and by1 <= 538
    check(f"callout {name} inside panel", ok, f"box=({bx0},{by0})-({bx1},{by1})")

print("== 2. green figure-frame containment (diagram ink inside x572-895 y103-525) ==")
gx0, gy0, gx1, gy1 = int(572 * SCALE), int(103 * SCALE), int(895 * SCALE), int(525 * SCALE)
zone = im[gy0:gy1, gx0:gx1]
nz = ~((np.abs(zone[:, :, 0] - 233) < 26) & (np.abs(zone[:, :, 1] - 233) < 26) & (np.abs(zone[:, :, 2] - 231) < 26))
nz &= ~((zone[:, :, 0] > 244) & (zone[:, :, 1] > 244) & (zone[:, :, 2] > 240))
ys, xs = np.where(nz)
check("diagram zone has ink", len(ys) > 1000, f"n={len(ys)}")
bb_diag = (xs.min() + gx0, ys.min() + gy0, xs.max() + gx0, ys.max() + gy0)
inside_frame = bb_diag[0] >= gx0 - 2 and bb_diag[2] <= gx1 + 2 and bb_diag[1] >= gy0 - 2 and bb_diag[3] <= gy1 + 2
check("diagram ink inside green frame", inside_frame,
      f"bbox=({bb_diag[0]},{bb_diag[1]})-({bb_diag[2]},{bb_diag[3]}) frame=({gx0},{gy0})-({gx1},{gy1})")

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
bb = ink_mask(631 * SCALE, 269 * SCALE, 725 * SCALE, 407 * SCALE, [(200, 168, 136), (185, 163, 130), (191, 158, 104)], 26)
if bb:
    inside = bb[0] >= 629 * SCALE - 3 and bb[2] <= 727 * SCALE + 3 and bb[1] >= 267 * SCALE - 3 and bb[3] <= 409 * SCALE + 3
    check("enc container ink inside", inside, f"ink=({bb[0]/SCALE:.0f},{bb[1]/SCALE:.0f})-({bb[2]/SCALE:.0f},{bb[3]/SCALE:.0f}) frame-px")
else:
    check("enc container ink", False, "none")
bb = ink_mask(746 * SCALE, 201.5 * SCALE, 839 * SCALE, 322.5 * SCALE, [(181, 184, 141), (206, 255, 225)], 30)
if bb:
    inside = bb[0] >= 744 * SCALE - 4 and bb[2] <= 841 * SCALE + 4 and bb[1] >= 199 * SCALE - 4 and bb[3] <= 325 * SCALE + 4
    check("dec upper container ink inside", inside, f"ink=({bb[0]/SCALE:.0f},{bb[1]/SCALE:.0f})-({bb[2]/SCALE:.0f},{bb[3]/SCALE:.0f})")
else:
    check("dec upper container ink", False, "none")
bb = ink_mask(746 * SCALE, 327.5 * SCALE, 832 * SCALE, 407.5 * SCALE, [(197, 246, 217), (206, 255, 225)], 26)
if bb:
    inside = bb[0] >= 744 * SCALE - 4 and bb[2] <= 834 * SCALE + 4 and bb[1] >= 325 * SCALE - 4 and bb[3] <= 410 * SCALE + 4
    check("dec lower container ink inside", inside, f"ink=({bb[0]/SCALE:.0f},{bb[1]/SCALE:.0f})-({bb[2]/SCALE:.0f},{bb[3]/SCALE:.0f})")
else:
    check("dec lower container ink", False, "none")

print("== 5. MAJOR-1 fix: dec-top 'Output'/'Probabilities' vs 'Decoder' separation ==")
# zone: dec panel top (frame x740-895, y108-142) on dec-panel bg (206,255,225)
zx0, zy0, zx1, zy1 = int(742 * SCALE), int(109 * SCALE), int(893 * SCALE), int(142 * SCALE)
reg = im[zy0:zy1, zx0:zx1]
darkgreen = (reg[:, :, 0] < 180) & (reg[:, :, 1] < 215) & (reg[:, :, 2] < 200)
ys2, xs2 = np.where(darkgreen)
if len(ys2) < 40:
    check("dec-top text ink present", False, f"n={len(ys2)}")
else:
    # cluster columns into glyph groups (gap > 8 render px splits)
    cols = np.zeros(zx1 - zx0, dtype=bool)
    for x in xs2: cols[x] = True
    groups = []
    s = p = None
    for i, v in enumerate(cols):
        if v:
            if s is None: s = p = i
            elif i <= p + 8: p = i
            else: groups.append((s, p)); s = p = i
    if s is not None: groups.append((s, p))
    g = [(a / SCALE + 742, b / SCALE + 742) for a, b in groups]
    print(f"    glyph x-clusters (frame-px): {[f'{a:.0f}-{b:.0f}' for a, b in g]}")
    # expect: Output ~769-800, Probabilities ~756-813 (below), Decoder ~823-888
    left = [t for t in g if t[1] < 815]
    right = [t for t in g if t[0] > 816]
    check("left cluster (Output Probabilities) present", len(left) >= 1, f"{left}")
    check("right cluster (Decoder) present", len(right) >= 1, f"{right}")
    if left and right:
        gap = min(t[0] for t in right) - max(t[1] for t in left)
        check("no overprint: gap > 8 frame-px", gap > 8, f"gap={gap:.1f}")
    # vertical: two bands on the left (Output above Probabilities)
    rowsum = darkgreen.sum(axis=1)
    rows = [i for i, v in enumerate(rowsum) if v > 3]
    bands = []
    if rows:
        s = p = rows[0]
        for i in rows[1:]:
            if i <= p + 2: p = i
            else: bands.append((s, p)); s = p = i
        bands.append((s, p))
    bcent = [((a + b) / 2 / SCALE + 109) for a, b in bands]
    print(f"    text y-bands (frame-px centers): {[f'{c:.1f}' for c in bcent]}")
    check("two stacked lines present", len(bands) >= 2, f"bands={len(bands)}")

print("== 6. MAJOR-2 fix: enc sub-block outlines + fills present ==")
# sub-block 2 fill (191,158,104) present in y343-383 x655-718
def fill_present(x0, y0, x1, y1, rgb, tol=18, minpx=400):
    reg = im[int(y0 * SCALE):int(y1 * SCALE), int(x0 * SCALE):int(x1 * SCALE)]
    m = (np.abs(reg[:, :, 0] - rgb[0]) < tol) & (np.abs(reg[:, :, 1] - rgb[1]) < tol) & (np.abs(reg[:, :, 2] - rgb[2]) < tol)
    return m.sum()
n = fill_present(656, 344, 717, 381, (191, 158, 104))
check("enc sub-block 2 fill (BF9E68) present", n > 400, f"n={n}")
n = fill_present(656, 293, 717, 314, (185, 163, 130))
check("enc FF cell fill (B9A382) present", n > 300, f"n={n}")
# border rows: dark ink across x655-718 at y274, 290.5, 316.5, 341.5, 383.5
for yy in [274, 286.5, 290.5, 316.5, 341.5, 357.5, 383.5]:
    band = im[int((yy - 1.2) * SCALE):int((yy + 1.2) * SCALE), int(655 * SCALE):int(718 * SCALE)]
    dark = band.max(axis=2) < 150
    check(f"enc border row y={yy}", dark.sum() > 30, f"darkpx={dark.sum()}")

print("== 7. Nx arrow ink (minor-4 fix) ==")
zx0, zy0, zx1, zy1 = int(577 * SCALE), int(338 * SCALE), int(590 * SCALE), int(346 * SCALE)
reg = im[zy0:zy1, zx0:zx1]
grayink = (np.abs(reg[:, :, 0] - 143) < 60) & (np.abs(reg[:, :, 1] - 143) < 60) & (np.abs(reg[:, :, 2] - 143) < 60)
grayink &= reg.max(axis=2) < 200
check("Nx arrow ink present", grayink.sum() > 15, f"n={grayink.sum()}")

print("== 8. sine glyph ink at PE icons (minor-3 fix) ==")
# enc PE sine zone (frame x674-698 y424-432): dark ink on panel
zx0, zy0, zx1, zy1 = int(674 * SCALE), int(422 * SCALE), int(698 * SCALE), int(434 * SCALE)
reg = im[zy0:zy1, zx0:zx1]
dark = reg.max(axis=2) < 140
check("enc sine ink present", dark.sum() > 25, f"n={dark.sum()}")
# dec PE sine zone (frame x806-820 y414-425)
zx0, zy0, zx1, zy1 = int(805 * SCALE), int(412 * SCALE), int(821 * SCALE), int(426 * SCALE)
reg = im[zy0:zy1, zx0:zx1]
dark = reg.max(axis=2) < 140
check("dec sine ink present", dark.sum() > 15, f"n={dark.sum()}")

print("== 9. highlight present (yellow + red dashes) ==")
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
yel = (r > 225) & (g > 225) & (b < 130)
ys3, xs3 = np.where(yel[int(240 * SCALE):int(330 * SCALE), int(660 * SCALE):int(800 * SCALE)])
check("yellow band ink present", len(ys3) > 400, f"n={len(ys3)}")
red = (r > 150) & (g < 100) & (b < 100)
ys4, xs4 = np.where(red[int(240 * SCALE):int(335 * SCALE), int(660 * SCALE):int(800 * SCALE)])
check("red dash ink present", len(ys4) > 80, f"n={len(ys4)}")

print("== 10. explicit line-spacing: c4 3-line pitch ==")
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

print("== 11. no ink wrap outside c6 box ==")
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
