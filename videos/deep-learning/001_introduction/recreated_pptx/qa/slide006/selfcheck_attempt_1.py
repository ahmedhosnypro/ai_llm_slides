#!/usr/bin/env python3
# selfcheck_attempt_1.py — closed-loop PIL geometry check for slide 006, attempt 1.
# Same-window ink bboxes on original (960x540) vs render (2001x1125), scale S=2001/960.
# Tolerance ~4 render-px = 1.92 frame px (dispatch: closed-loop ~4px).
from PIL import Image
import numpy as np
import sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide006/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
S = 2001 / 960.0

ren = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
org = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
fails = []

def masks(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    dark_ink = a.max(axis=2) < 150
    red = (r > 110) & (r - g > 45) & (r - b > 35)
    blue = (b - r > 25) & (b - g > 25) & (b > 110) & (r < 160)
    return dark_ink | red | blue, dark_ink, red, blue

ink_r, dark_r, red_r, blue_r = masks(ren)
ink_o, dark_o, red_o, blue_o = masks(org)

def bbox(img_ink, x0, x1, y0, y1, sc):
    sub = img_ink[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        return None
    return (xs.min() / sc + x0, xs.max() / sc + x0, ys.min() / sc + y0, ys.max() / sc + y0)

def cmp(name, mask_r, mask_o, x0, x1, y0, y1, tol=4.0):
    fr = bbox(mask_r, x0, x1, y0, y1, S)
    fo = bbox(mask_o, x0, x1, y0, y1, 1.0)
    if fr is None or fo is None:
        fails.append(f"{name}: no ink (render={fr is not None}, orig={fo is not None})")
        print(f"FAIL {name}: no ink render={fr is not None} orig={fo is not None}")
        return
    tol_f = tol / S
    labels = ["left", "right", "top", "bottom"]
    for i, lab in enumerate(labels):
        d = abs(fr[i] - fo[i])
        ok = d <= tol_f
        if not ok:
            fails.append(f"{name} {lab}: render {fr[i]:.1f} vs orig {fo[i]:.1f} (d={d:.1f}fp)")
        print(f"{'PASS' if ok else 'FAIL'} {name}.{lab}: render={fr[i]:.1f} orig={fo[i]:.1f} d={d:.1f}fp (tol {tol_f:.1f}fp)")

print("== title (red) ==")
cmp("title", red_r, red_o, 100, 900, 55, 130, 5)

print("== content box borders (red, clean windows) ==")
cmp("box.top", red_r, red_o, 100, 800, 125, 140, 4)
cmp("box.bottom", red_r, red_o, 100, 800, 496, 512, 4)
cmp("box.left", red_r, red_o, 80, 96, 250, 450, 4)
cmp("box.right", red_r, red_o, 834, 852, 250, 450, 4)

print("== header lines (dark, inside box, below border) ==")
cmp("hdr.L1", dark_r, dark_o, 91, 878, 136, 163, 5)
cmp("hdr.L2", dark_r, dark_o, 91, 878, 164, 190, 5)

print("== bullet lines (all-ink; window skips dots x<195) ==")
LINES = [
    ("b1", 195, 880, 194, 220),
    ("b2", 195, 880, 220, 246),
    ("b3", 195, 880, 246, 272),
    ("b4", 195, 880, 272, 298),
    ("b5", 195, 880, 298, 325),
    ("b6", 195, 880, 325, 350),
    ("b7", 195, 880, 350, 376),
    ("b8", 195, 880, 377, 402),
    ("b9", 195, 880, 402, 428),
    ("b10", 195, 880, 428, 455),
    ("b11", 195, 880, 455, 481),
    ("b12", 195, 880, 481, 501),
]
for name, x0, x1, y0, y1 in LINES:
    cmp(name, ink_r, ink_o, x0, x1, y0, y1, 5)

print("== bullet dots (dark ink) ==")
DOTS = [203, 229, 255.5, 281, 307.5, 333.5, 360, 386, 412, 438.5, 464.5, 490.5]
for k, cy in enumerate(DOTS):
    cmp(f"dot{k+1}", dark_r, dark_o, 174, 196, cy - 9, cy + 9, 4)

print("== bar (dark) ==")
bar_r = ren.max(axis=2) < 80
bar_o = org.max(axis=2) < 80
cmp("bar", bar_r, bar_o, 30, 930, 512, 540, 4)

print("== colors (modal of saturated cores) ==")
def modal(a, mask, x0, x1, y0, y1):
    px = a[y0:y1, x0:x1][mask[y0:y1, x0:x1]]
    if not len(px):
        return None
    vals, counts = np.unique(px, axis=0, return_counts=True)
    order = np.argsort(-counts)[:3]
    return [(tuple(int(v) for v in vals[i]), int(counts[i])) for i in order]

print("render title red modal:", modal(ren, red_r, 250, 710, 80, 130), "| orig:", modal(org, red_o, 250, 710, 80, 130))
print("render bullet blue modal:", modal(ren, blue_r, 204, 570, 197, 476), "| orig:", modal(org, blue_o, 204, 570, 197, 476))
print("render b12 dark modal:", modal(ren, dark_r, 200, 345, 483, 500), "| orig:", modal(org, dark_o, 200, 345, 483, 500))

print("== diagnostic: title ink density render vs orig (weight check) ==")
tr = int(red_r[int(84 * S):int(126 * S), int(142 * S):int(834 * S)].sum())
to = int(red_o[84:126, 142:834].sum())
print(f"  title red px: render {tr} orig {to} ratio {tr/to:.2f} (crisp-vs-halo expected ~0.8-1.1 for same weight)")

print("== frame containment (render ink inside chrome panel 42..918 x 45..537) ==")
sub = ink_r[int(60 * S):int(512 * S), int(45 * S):int(915 * S)]
ys, xs = np.where(sub)
L, R = xs.min() / S + 45, xs.max() / S + 45
T, B = ys.min() / S + 60, ys.max() / S + 60
ok = L > 42 and R < 918 and T > 45 and B < 537
print(f"{'PASS' if ok else 'FAIL'} containment: ink x {L:.0f}..{R:.0f} y {T:.0f}..{B:.0f}")
if not ok:
    fails.append("containment")

print()
if fails:
    print("SELFCHECK RESULT: FAIL")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("SELFCHECK RESULT: PASS")
