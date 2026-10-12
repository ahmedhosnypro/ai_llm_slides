#!/usr/bin/env python3
"""Closed-loop PIL ink check: render (150dpi -> 960x540 slide space) vs the original
frame (resampled into slide coords). Per-element ink-band bboxes; pass tolerance
~4px @150dpi = 1.92pt in this 960x540 space."""
from PIL import Image, ImageChops
import json, sys

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide015"
rend = Image.open(f"{SCR}/render2/r-1.png").convert("RGB")
if rend.size != (960, 540):
    rend = rend.resize((960, 540), Image.LANCZOS)
rend.save(f"{SCR}/render_960.png")
orig = Image.open(f"{SCR}/frame_in_slide_coords.png").convert("RGB")

TOL = 2.0  # pt (~4px @150dpi)

def ink_bbox(img, x0, y0, x1, y1, pred):
    px = img.load()
    pts = [(x, y) for y in range(int(y0), int(y1)) for x in range(int(x0), int(x1)) if pred(px[x, y])]
    if not pts:
        return None
    return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))

def cmp(name, x0, y0, x1, y1, pred, tol=TOL):
    a = ink_bbox(rend, x0, y0, x1, y1, pred)
    b = ink_bbox(orig, x0, y0, x1, y1, pred)
    if a is None or b is None:
        print(f"  {name:24s} render={a} orig={b}  -> {'MISSING INK' if a is None else 'ok(no ink in orig?)'}")
        return False
    d = [abs(u - v) for u, v in zip(a, b)]
    ok = all(t <= tol for t in d)
    print(f"  {name:24s} render={a} orig={b}  d={d}  {'OK' if ok else 'OFF > %.1f' % tol}")
    return ok

dark = lambda p: sum(p) < 330
red = lambda p: p[0] > 140 and p[0] - p[1] > 60 and p[0] - p[2] > 60
salmon = lambda p: abs(p[0] - 241) < 24 and abs(p[1] - 139) < 26 and abs(p[2] - 150) < 26
lav = lambda p: abs(p[0] - 197) < 20 and abs(p[1] - 193) < 20 and abs(p[2] - 244) < 20
yel = lambda p: p[0] > 235 and p[1] > 235 and p[2] < 200
mint = lambda p: abs(p[0] - 212) < 22 and p[1] > 235 and abs(p[2] - 229) < 22
peach = lambda p: p[0] > 235 and abs(p[1] - 226) < 24 and abs(p[2] - 205) < 26
navyblue = lambda p: p[2] > 120 and p[2] - p[0] > 40 and p[2] - p[1] > 30 and sum(p) < 620
greenink = lambda p: p[1] > 120 and p[1] - p[0] > 40 and p[1] - p[2] > 30

checks = [
    ("card_h1_salmon", 60, 160, 410, 470, salmon),
    ("card_h2_lavender", 600, 130, 720, 200, lav),
    ("card_h3_yellow", 560, 120, 760, 175, yel),
    ("card_h4_mint", 700, 110, 800, 170, mint),
    ("card_h5_peach", 740, 95, 830, 145, peach),
    ("oval_h1", 585, 183, 640, 212, dark),
    ("oval_h5", 765, 98, 825, 132, dark),
    ("pill_zone_h1", 230, 180, 520, 208, lambda p: sum(p) > 690 and p[0] > 240),
    ("chain_rust", 405, 145, 505, 178, red),
    ("chain_tan", 580, 68, 675, 98, peach),
    ("swoosh_band", 580, 230, 830, 390, red),
    ("hlabel_blue", 775, 258, 850, 298, navyblue),
    ("title_ink", 310, 470, 700, 510, dark),
    ("title_red", 310, 470, 700, 510, lambda p: red(p) and sum(p) < 560),
    ("dots_blue", 230, 230, 300, 350, navyblue),
    ("dotprod_box", 222, 200, 295, 360, lambda p: abs(p[0]-216)<18 and abs(p[1]-192)<18 and abs(p[2]-180)<18),
    ("scale_pill", 306, 205, 342, 360, lambda p: abs(p[0]-246)<16 and abs(p[1]-204)<18 and abs(p[2]-208)<18),
    ("soft_pill", 360, 205, 395, 360, lambda p: p[0]>238 and abs(p[1]-210)<20 and p[2]>235),
    ("sigma_box", 400, 205, 505, 232, lambda p: abs(p[0]-220)<18 and p[1]>235 and p[2]>235),
    ("mult_nodes", 405, 236, 495, 345, lambda p: p[0]>150 and p[0]-p[1]>60 and sum(p)<600),
    ("wv_boxes", 532, 235, 562, 345, lambda p: abs(p[0]-198)<26 and abs(p[1]-240)<18 and abs(p[2]-230)<20),
    ("qrow_fill", 165, 395, 400, 440, lambda p: abs(p[0]-236)<14 and p[1]>243 and abs(p[2]-222)<16),
    ("x2_magenta", 228, 400, 290, 434, lambda p: p[0]>180 and p[2]>150 and p[1]<160),
    ("orange_zone", 85, 225, 205, 375, lambda p: p[0]>200 and 100<p[1]<200 and p[2]<140),
    ("green_ell", 178, 226, 240, 350, greenink),
    ("wk_boxes", 158, 235, 192, 345, lambda p: abs(p[0]-230)<22 and abs(p[1]-182)<24 and abs(p[2]-108)<30),
    ("chip_c1_q", 600, 365, 640, 392, lambda p: sum(p) > 640 and p[0] > 235),
    ("chip_c5_q", 778, 290, 816, 322, lambda p: sum(p) > 640 and p[0] > 235),
    ("cont_h1", 570, 228, 638, 358, lambda p: abs(p[0]-166)<40 and abs(p[1]-169)<40 and abs(p[2]-143)<40 and p[1]-p[2]>8),
    ("cont_h5", 762, 143, 812, 268, greenink),
    ("frac_zone_ink", 340, 205, 370, 240, dark),
    ("kq_label", 286, 206, 318, 228, lambda p: red(p) and sum(p) < 450),
    ("plane_zone", 130, 80, 420, 200, lambda p: max(abs(p[0]-p[1]), abs(p[1]-p[2])) < 16 and 192 <= sum(p)//3 <= 226),
]
ok_all = True
print("closed-loop ink check (render vs original, slide-pt space):")
for c in checks:
    ok_all = cmp(*c) and ok_all
print("ALL OK" if ok_all else "SOME CHECKS OFF")
