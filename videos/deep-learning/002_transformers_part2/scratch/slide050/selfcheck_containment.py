#!/usr/bin/env python3
"""Self-check: frame containment + no stray ink on the slide-050 render.

Checks:
 1. Title ink sits fully inside the house panel (clearance on all four sides).
 2. No content ink ANYWHERE on the panel except the title band and the badge
    (single-element divider — spec step 8).
 3. Badge ink is confined to the badge circle area.
"""
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide050/render_2.png").convert("RGB")
W, H = im.size
px = im.load()

PANEL = (89, 95, 1913, H)          # x0,y0,x1,y1 (chrome check measured)
BADGE = (1815, 105, 1905, 195)     # house badge zone @150dpi: cx 893*150/72=1860.4, cy 71*150/72=147.9, d 75
TITLE_BAND = (400, 540, 1600, 710) # generous title zone

def is_red(c):
    r, g, b = c
    return r > 90 and r - max(g, b) > 50

def is_ink(c):
    r, g, b = c
    gray = abs(r - g) < 14 and abs(g - b) < 14
    return not gray  # any non-gray pixel = content ink (red text, dark numeral)

# panel interior strictly inside the border stroke (avoid the border itself)
ix0, iy0, ix1, iy1 = PANEL[0] + 5, PANEL[1] + 5, PANEL[2] - 5, PANEL[3] - 5

stray = []
title_out = []
for y in range(iy0, iy1):
    for x in range(ix0, ix1):
        if is_ink(px[x, y]):
            in_title = TITLE_BAND[0] <= x <= TITLE_BAND[2] and TITLE_BAND[1] <= y <= TITLE_BAND[3]
            in_badge = BADGE[0] <= x <= BADGE[2] and BADGE[1] <= y <= BADGE[3]
            if not in_title and not in_badge:
                stray.append((x, y, px[x, y]))
            elif in_title and not (476 <= x <= 1500 and 587 <= y <= 664):
                # bbox +1px antialias halo; anything outside is genuine stray ink
                title_out.append((x, y, px[x, y]))

print(f"stray ink px outside title+badge zones: {len(stray)}")
if stray[:8]:
    print("  samples:", stray[:8])
print(f"ink px in title zone but outside measured title bbox: {len(title_out)}")
if title_out[:8]:
    print("  samples:", title_out[:8])

# containment clearances of the measured title bbox vs panel edges
t = dict(x0=476, x1=1500, y0=589, y1=663)
cl = dict(left=t['x0'] - PANEL[0], right=PANEL[2] - t['x1'], top=t['y0'] - PANEL[1], bottom=PANEL[3] - t['y1'])
print("title clearance vs panel edges (px):", cl)
ok = len(stray) == 0 and len(title_out) == 0 and all(v > 20 for v in cl.values())
print("CONTAINMENT/STRAY-INK:", "PASS" if ok else "FAIL")
