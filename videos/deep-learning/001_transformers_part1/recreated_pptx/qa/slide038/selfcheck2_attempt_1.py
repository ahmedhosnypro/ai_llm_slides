#!/usr/bin/env python3
"""selfcheck2_attempt_1: corrected coordinate handling (frame px vs 150dpi px).
 - scaling box solid-yellow core, render vs frame
 - fraction bar row (wide red run) render vs parent's certified render
 - panel border columns/rows profile, render vs frame
 - box border bands, render vs frame
"""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
S = 2000 / 960.0
mine = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide038/render_1.png").convert("RGB")).astype(int)
par = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide037/render_1.png").convert("RGB")).astype(int)
orig = np.asarray(Image.open(f"{V}/unique_slides/slide_038.jpg").convert("RGB")).astype(int)

def yel_core(img):
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    return (R > 225) & (G > 215) & (B < 140) & (R - B > 90)

for tag, img, x, scale in [("render", mine, int(395 * S), 1.0), ("frame", orig, 395, S)]:
    yel = yel_core(img)
    col = np.where(yel[:int(460 * scale), x])[0]
    print(f"[scaling] {tag} solid-yellow run at col {x}: y[{col.min() / scale:.1f}..{col.max() / scale:.1f}] (frame px)")

def red_bar_row(img, scale):
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    red = (R > 130) & (R - G > 60) & (R - B > 50)
    best = None
    for y in range(int(195 * scale), int(215 * scale)):
        xs = np.where(red[y, int(410 * scale):int(460 * scale)])[0]
        if len(xs) > 20:
            w = xs.max() - xs.min()
            if best is None or w > best[1]:
                best = (y, w)
    return best

b_m = red_bar_row(mine, 1.0); b_o = red_bar_row(orig, S); b_p = red_bar_row(par, 1.0)
print(f"[frac] bar row render: y={b_m[0]} (frame {b_m[0]/S:.1f}) width150={b_m[1]}")
print(f"[frac] bar row frame : y={b_o[0]/S:.1f} width150={b_o[1]/S:.1f}  | parent-certified render: y={b_p[0]/S:.1f}")

def green_cols(img, scale, minrun):
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    g = (G > R + 25) & (G > B + 15) & (G > 80) & (G < 210) & (R < 160)
    sub = g[:int(340 * scale), int(770 * scale):int(935 * scale)]
    cols = sub.sum(axis=0)
    return [(round((x + int(770 * scale)) / scale, 1), int(c)) for x, c in enumerate(cols) if c > minrun]

print("[panel] green cols render (frame px, >100):", green_cols(mine, 1.0, 100))
print("[panel] green cols frame  (frame px, >20) :", green_cols(orig, S, 20 * S))
rows_of = lambda img, scale, minrun: None
def green_rows(img, scale, minrun):
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    g = (G > R + 25) & (G > B + 15) & (G > 80) & (G < 210) & (R < 160)
    sub = g[:int(340 * scale), int(790 * scale):int(920 * scale)]
    rr = sub.sum(axis=1)
    return [(round((y + 0) / scale, 1), int(c)) for y, c in enumerate(rr) if c > minrun]

print("[panel] green rows render (frame px, >80):", green_rows(mine, 1.0, 80))
print("[panel] green rows frame  (frame px, >18):", green_rows(orig, S, 18 * S))

# box border bands in my render (dark wide rows inside panel interior)
R, G, B = mine[:, :, 0], mine[:, :, 1], mine[:, :, 2]
ink = (R < 140) & (G < 140) & (B < 140)
sub = ink[int(120 * S):int(315 * S), int(802 * S):int(910 * S)]
rr = sub.sum(axis=1)
bands = []
inb = False
for i, c in enumerate(rr):
    y = i + int(120 * S)
    if c > 90 and not inb:
        s = y; inb = True
    elif c <= 90 and inb:
        bands.append((round(s / S, 1), round((y - 1) / S, 1))); inb = False
print("[boxes] render border bands (frame px):", bands)
print("[boxes] frame measured bands          : [(136,156),(166,185),(196,214),(225,243),(255,273)]")
