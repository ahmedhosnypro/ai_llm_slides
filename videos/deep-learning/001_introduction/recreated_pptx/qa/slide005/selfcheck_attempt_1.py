#!/usr/bin/env python3
# selfcheck_attempt_1.py (v3, paired-window) — closed-loop PIL geometry check.
# For every feature, measure the ink bbox in the SAME window on BOTH images
# (original 960x540 and 150dpi render 2001x1125), convert render to frame px
# (scale 2001/960), and compare. Tolerance ~4 render-px = 1.92 frame px.
from PIL import Image
import numpy as np
import sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide005/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_005.jpg"
S = 2001 / 960.0

ren = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
org = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
fails = []

def masks(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    dark_ink = a.max(axis=2) < 150
    red = (r > 110) & (r - g > 45) & (r - b > 35)
    blue = (b > 105) & (b - r > 55) & (b - g > 55)
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
    ds = []
    for i, lab in enumerate(labels):
        d = abs(fr[i] - fo[i])
        ds.append(d)
        ok = d <= tol_f
        if not ok:
            fails.append(f"{name} {lab}: render {fr[i]:.1f} vs orig {fo[i]:.1f} (d={d:.1f}fp)")
        print(f"{'PASS' if ok else 'FAIL'} {name}.{lab}: render={fr[i]:.1f} orig={fo[i]:.1f} d={d:.1f}fp (tol {tol_f:.1f}fp)")

print("== title (red) ==")
cmp("title", red_r, red_o, 200, 780, 78, 128, 5)

print("== header (red) ==")
cmp("header", red_r, red_o, 96, 400, 148, 190, 5)

print("== box borders (red, excluding text zones) ==")
cmp("box.top", red_r, red_o, 400, 700, 130, 146, 4)
cmp("box.bottom", red_r, red_o, 400, 700, 495, 512, 4)
cmp("box.left", red_r, red_o, 82, 97, 300, 450, 4)
cmp("box.right", red_r, red_o, 868, 883, 300, 450, 5)

print("== bar (dark) ==")
bar_r = ren.max(axis=2) < 80
bar_o = org.max(axis=2) < 80
cmp("bar", bar_r, bar_o, 30, 930, 512, 540, 4)

print("== bullet lines (all-ink: black|red|blue) — x window skips dots (>=125) ==")
LINES = [
    ("b1l1", 125, 860, 194, 224),
    ("b1l2", 125, 860, 225, 252),
    ("b2l1", 125, 860, 263, 291),
    ("b2l2", 125, 300, 293, 319),
    ("b3l1", 125, 860, 331, 358),
    ("b3l2", 125, 860, 360, 388),
]
for name, x0, x1, y0, y1 in LINES:
    cmp(name, ink_r, ink_o, x0, x1, y0, y1, 6)

print("== bullet dots (dark ink) ==")
for name, cy in [("dot1", 206.5), ("dot2", 274.5), ("dot3", 343.5)]:
    cmp(name, dark_r, dark_o, 103, 125, cy - 9, cy + 9, 4)

print("== colors (modal of saturated cores) ==")
def modal(a, mask):
    px = a[mask]
    if not len(px):
        return None
    vals, counts = np.unique(px, axis=0, return_counts=True)
    return tuple(int(v) for v in vals[counts.argmax()])

bl_r = blue_r[int(196*S):int(390*S), int(130*S):int(900*S)]
bl_o = blue_o[196:390, 130:900]
print("render blue modal:", modal(ren[int(196*S):int(390*S), int(130*S):int(900*S)], bl_r), "| orig:", modal(org[196:390, 130:900], bl_o))
print("render body black modal:", modal(ren[int(198*S):int(222*S), int(140*S):int(300*S)], dark_r[int(198*S):int(222*S), int(140*S):int(300*S)]), "| orig:", modal(org[198:222, 140:300], dark_o[198:222, 140:300]))
tr_r = red_r[int(80*S):int(130*S), int(250*S):int(710*S)]
print("render title red modal:", modal(ren[int(80*S):int(130*S), int(250*S):int(710*S)], tr_r), "| orig:", modal(org[80:130, 250:710], red_o[80:130, 250:710]))

print("== frame containment (render ink inside chrome panel 42..918 x 45..537) ==")
sub = ink_r[int(60*S):int(512*S), int(45*S):int(915*S)]
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
