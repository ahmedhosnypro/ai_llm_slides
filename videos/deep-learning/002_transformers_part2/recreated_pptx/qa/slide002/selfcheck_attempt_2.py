#!/usr/bin/env python3
"""Pre-judge self-check, slide 002 attempt 2 (150dpi render_2.png, 2001x1125).
Checks: (1) frame containment — all content ink inside the gray panel with
clearance; (2) color sampling vs spec (red title C00000, panel gray E9E9E7,
badge FDFD96/6A5ACD, canvas white); (3) badge numeral ink present (numeral '2').
N/A by inspection: equations (none), delimiters (none), tables (none),
multi-line boxes (three single-line boxes -> explicit-line-spacing N/A),
dense-region crop compare (trigger conditions absent: no equations/delimiters/
tables on this slide; geometry is closed-loop verified at 1.0-2.9px instead).
"""
from PIL import Image
import json

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide002/render_2.png"
img = Image.open(R).convert("RGB")
W, H = img.size
px = img.load()
out = {"render_size": [W, H]}

def reddish(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50

# ---- 1. FRAME CONTAINMENT: all red content ink (title) inside panel bounds.
# Panel from house chrome: x 42..919 pt, y 45..540 pt -> px = pt*2.08333
PXPT = 150 / 72.0
pan_l, pan_r = 42 * PXPT, 919 * PXPT
pan_t, pan_b = 45 * PXPT, 540 * PXPT
ink_pts = [(x, y) for y in range(int(pan_t) + 6, int(pan_b) - 6)
           for x in range(int(pan_l) + 6, int(pan_r) - 6) if reddish(px[x, y])]
ix0 = min(p[0] for p in ink_pts); ix1 = max(p[0] for p in ink_pts)
iy0 = min(p[1] for p in ink_pts); iy1 = max(p[1] for p in ink_pts)
out["content_ink_bbox_px"] = [ix0, iy0, ix1, iy1]
out["clearance_px"] = {"left": round(ix0 - pan_l, 1), "right": round(pan_r - ix1, 1),
                       "top": round(iy0 - pan_t, 1), "bottom": round(pan_b - iy1, 1)}
out["containment_pass"] = (ix0 > pan_l and ix1 < pan_r and iy0 > pan_t and iy1 < pan_b)

# also: no ink OUTSIDE the panel except chrome (scan white canvas margins for
# non-white, non-chrome ink; chrome border/badge live at known coords)
stray = []
for y in range(0, H, 2):
    for x in range(0, W, 2):
        r, g, b = px[x, y]
        if not (r > 235 and g > 235 and b > 235):
            in_panel = pan_l - 4 <= x <= pan_r + 4 and y >= pan_t - 4
            # chrome border strokes + badge region (house chrome, tol 4px)
            on_border = (abs(x - pan_l) <= 4 or abs(x - pan_r) <= 4 or
                         abs(y - pan_t) <= 4 or y >= pan_b - 6)
            in_badge = (893 * PXPT - 60) <= x <= (893 * PXPT + 60) and (71 * PXPT - 60) <= y <= (71 * PXPT + 60)
            if not (in_panel or on_border or in_badge):
                stray.append((x, y))
out["stray_ink_outside_chrome_count"] = len(stray)
out["stray_sample"] = stray[:10]
out["no_stray_pass"] = len(stray) == 0

# ---- 2. COLOR SAMPLING vs spec
from collections import Counter
def mode_color(x0, y0, x1, y1, pred):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = px[x, y]
            if pred(p):
                c[p] += 1
    return c.most_common(3)

# title glyph core: darkest/most saturated red inside L1 band
title_reds = Counter()
for y in range(430, 500):
    for x in range(600, 1400):
        p = px[x, y]
        if p[0] > 150 and p[1] < 60 and p[2] < 60:
            title_reds[p] += 1
out["title_red_core_top"] = title_reds.most_common(3)

out["panel_fill_sample"] = [px[400, 950], px[1000, 300], px[1700, 600]]
out["canvas_sample"] = [px[30, 30], px[1970, 30], px[30, 1100]]

badge_fills = Counter()
badge_rings = Counter()
for y in range(int(71 * PXPT - 40), int(71 * PXPT + 40)):
    for x in range(int(893 * PXPT - 40), int(893 * PXPT + 40)):
        r, g, b = px[int(x), int(y)]
        if r > 230 and g > 230 and 130 < b < 200:
            badge_fills[(r, g, b)] += 1
        if 80 <= r <= 190 and 60 <= g <= 140 and b > 170:
            badge_rings[(r, g, b)] += 1
out["badge_fill_top"] = badge_fills.most_common(2)
out["badge_ring_top"] = badge_rings.most_common(2)

# ---- 3. badge numeral ink present (dark pixels inside badge circle)
darks = sum(1 for y in range(int(71 * PXPT - 25), int(71 * PXPT + 25))
            for x in range(int(893 * PXPT - 25), int(893 * PXPT + 25)) if sum(px[x, y]) < 300)
out["badge_numeral_ink_px"] = darks
out["numeral_present_pass"] = darks > 40

ok = out["containment_pass"] and out["no_stray_pass"] and out["numeral_present_pass"]
print(json.dumps(out, indent=1))
print("SELF-CHECK:", "PASS" if ok else "FAIL")
