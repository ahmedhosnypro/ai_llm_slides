#!/usr/bin/env python3
"""Locate color families in slide_013.jpg: bbox + 24x14 occupancy grid per family."""
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_013.jpg').convert('RGB')
W, H = im.size
px = im.load()

FAMILIES = {
    'panel_peach_F7E2CD': lambda r, g, b: 243 <= r <= 252 and 222 <= g <= 231 and 200 <= b <= 210,
    'mint_green_85FFA7': lambda r, g, b: 115 <= r <= 160 and g >= 235 and 140 <= b <= 185,
    'bluegray_B7C1CB': lambda r, g, b: 170 <= r <= 195 and 185 <= g <= 205 and 195 <= b <= 215,
    'container_green_border': lambda r, g, b: 60 <= r <= 100 and 110 <= g <= 140 and 65 <= b <= 95,
    'yellow_band_F7F96B': lambda r, g, b: 240 <= r <= 255 and 240 <= g <= 255 and 90 <= b <= 130,
    'dp_box_DBCBBB': lambda r, g, b: 210 <= r <= 228 and 195 <= g <= 212 and 175 <= b <= 195,
    'softmax_F8DEFB': lambda r, g, b: 243 <= r <= 255 and 214 <= g <= 228 and 243 <= b <= 255,
    'sigma_EAFEFC': lambda r, g, b: 228 <= r <= 240 and 248 <= g <= 255 and 246 <= b <= 255,
    'pill_FFFFE3': lambda r, g, b: 250 <= r <= 255 and 248 <= g <= 255 and 200 <= b <= 235,
    'red_C00000_ink': lambda r, g, b: 140 <= r <= 210 and g <= 60 and b <= 60,
    'dark_red_border': lambda r, g, b: 90 <= r <= 140 and g <= 60 and 20 <= b <= 80,
    'navy_text': lambda r, g, b: r <= 60 and g <= 60 and b >= 90,
    'black_text': lambda r, g, b: r <= 70 and g <= 70 and b <= 70,
    'green_text_0E9B4C': lambda r, g, b: r <= 90 and 130 <= g <= 190 and b <= 110,
    'white_boxes': lambda r, g, b: r >= 248 and g >= 248 and b >= 248,
}

def grid(mask_name, coords):
    if not coords:
        print(mask_name + ': EMPTY')
        return
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    print('%s: n=%d bbox x %d..%d y %d..%d' % (mask_name, len(coords), x0, x1, y0, y1))
    # 48x28 occupancy grid
    gw, gh = 48, 28
    g = [[0] * gw for _ in range(gh)]
    for x, y in coords:
        gx = min(gw - 1, (x - x0) * gw // max(1, (x1 - x0 + 1)))
        gy = min(gh - 1, (y - y0) * gh // max(1, (y1 - y0 + 1)))
        g[gy][gx] += 1
    for row in g:
        print(''.join('#' if v > 8 else ('+' if v > 2 else ('.' if v > 0 else ' ')) for v in row))

import sys
sel = sys.argv[1:] if len(sys.argv) > 1 else FAMILIES.keys()
for name in sel:
    fn = FAMILIES[name]
    coords = []
    for y in range(46, 517):
        for x in range(59, 901):
            r, g, b = px[x, y]
            if fn(r, g, b):
                coords.append((x, y))
    grid(name, coords)
    print()
