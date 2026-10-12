#!/usr/bin/env python3
"""Targeted geometry scans for slide_031.jpg — precise bounds, colors, profiles."""
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def c(x, y): return px[x, y]

print("=== A. GLOBAL STRIP SAMPLES (colors along key rows/cols) ===")
print("row y=92 (above panels):", [c(x, 92) for x in range(40, 960, 80)])
print("row y=305 (between Q and K):", [(x, c(x, 305)) for x in range(44, 960, 64)])
print("col x=50 (left strip):", [(y, c(50, y)) for y in range(90, 540, 40)])
print("col x=472 (between panels):", [(y, c(472, y)) for y in range(100, 540, 40)])
print("col x=900 (right strip):", [(y, c(900, y)) for y in range(90, 540, 40)])
print("peach core samples:", c(500, 400), c(700, 350), c(60, 480), c(910, 300), c(300, 530))

print("\n=== B. Q/V/K PANEL BORDER SCANS ===")
# border = strongly-colored pixel rows/cols; print exact strokes with mean color
def stroke_rows(x0, x1, y0, y1, pred, label):
    for y in range(y0, y1):
        xs = [x for x in range(x0, x1) if pred(c(x, y))]
        if len(xs) >= (x1 - x0) * 0.5:
            mc = tuple(round(sum(cc[i] for cc in (c(x, y) for x in xs)) / len(xs)) for i in range(3))
            print(f"  {label} row y={y}: n={len(xs)} mean={mc}")

def stroke_cols(y0, y1, x0, x1, pred, label):
    for x in range(x0, x1):
        ys = [y for y in range(y0, y1) if pred(c(x, y))]
        if len(ys) >= (y1 - y0) * 0.5:
            mc = tuple(round(sum(cc[i] for cc in (c(x, y) for y in ys)) / len(ys)) for i in range(3))
            print(f"  {label} col x={x}: n={len(ys)} mean={mc}")

pred_red = lambda cc: cc[0] > 130 and cc[0] - cc[1] > 55 and cc[0] - cc[2] > 55
pred_blue = lambda cc: cc[2] > 120 and cc[2] - cc[0] > 50 and cc[2] - cc[1] > 40
pred_grn = lambda cc: cc[1] > 90 and cc[1] - cc[0] > 25 and cc[1] - cc[2] > 25
pred_dark = lambda cc: sum(cc) < 330

print("-- Q panel (red) --")
stroke_rows(70, 450, 90, 110, pred_red, "Qtop")
stroke_rows(70, 450, 290, 312, pred_red, "Qbot")
stroke_cols(110, 290, 50, 70, pred_red, "Qleft")
stroke_cols(110, 290, 458, 478, pred_red, "Qright")
print("-- V panel (blue) --")
stroke_rows(490, 870, 90, 110, pred_blue, "Vtop")
stroke_rows(490, 870, 290, 312, pred_blue, "Vbot")
stroke_cols(110, 290, 470, 490, pred_blue, "Vleft")
stroke_cols(110, 290, 878, 898, pred_blue, "Vright")
print("-- K panel (green or dark?) --")
stroke_rows(70, 450, 302, 325, pred_grn, "Ktop-grn")
stroke_rows(70, 450, 302, 325, pred_dark, "Ktop-dark")
stroke_rows(70, 450, 518, 535, pred_grn, "Kbot-grn")
stroke_rows(70, 450, 518, 535, pred_dark, "Kbot-dark")
stroke_cols(320, 510, 50, 70, pred_grn, "Kleft-grn")
stroke_cols(320, 510, 458, 478, pred_grn, "Kright-grn")
print("  K border candidate samples:", c(200, 311), c(200, 312), c(200, 313), c(57, 400), c(58, 400), c(59, 400), c(466, 400), c(467, 400), c(468, 400))

print("\n=== C. TITLE / SUBTITLE ===")
def ink_bbox(x0, y0, x1, y1, pred):
    xs = []; ys = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(c(x, y)):
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys), len(xs)) if xs else None
pred_black = lambda cc: sum(cc) < 200
print("title ink (black, y44..70):", ink_bbox(50, 44, 940, 70, pred_black))
pred_yel = lambda cc: cc[0] > 235 and cc[1] > 210 and cc[2] < 170
print("title highlight (yellow):", ink_bbox(50, 40, 940, 78, pred_yel))
# subtitle: colored + black ink
print("subtitle red ink:", ink_bbox(50, 71, 940, 92, pred_red))
print("subtitle blue ink:", ink_bbox(50, 71, 940, 92, pred_blue))
print("subtitle black ink:", ink_bbox(50, 71, 940, 92, pred_black))
print("subtitle samples: (140,80)", c(140, 80), "(300,80)", c(300, 80), "(700,80)", c(700, 80))

print("\n=== D. CALLOUTS: bounds, border color, fill ===")
# find dashed border color: sample many border-ish pixels on each callout rect
def border_color_scan(x0, y0, x1, y1, label):
    from collections import Counter
    votes = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            cc = c(x, y)
            r, g, b = cc
            if r > 120 and r - g > 50 and r - b > 50: votes["red"] += 1
            elif b > 120 and b - r > 45 and b - g > 35: votes["blue"] += 1
            elif g > 85 and g - r > 20 and g - b > 20: votes["green"] += 1
            elif sum(cc) < 330: votes["dark"] += 1
    print(f"  {label} colored-vote counts: {dict(votes)}")
# callout regions from measure4
border_color_scan(445, 272, 680, 315, "callout1")
border_color_scan(700, 305, 920, 345, "callout2")
border_color_scan(445, 332, 680, 375, "callout3")
print("  callout fill samples:", "c1", c(500, 292), c(620, 300), "c2", c(790, 320), c(860, 330), "c3", c(500, 352), c(620, 360))
# exact bboxes of any ink
pred_ink = lambda cc: sum(cc) < 660 and not (cc[0] > 244 and cc[1] > 244 and cc[2] > 244)
print("  callout1 ink bbox:", ink_bbox(440, 268, 690, 318, pred_ink))
print("  callout2 ink bbox:", ink_bbox(695, 300, 925, 348, pred_ink))
print("  callout3 ink bbox:", ink_bbox(440, 328, 690, 378, pred_ink))
