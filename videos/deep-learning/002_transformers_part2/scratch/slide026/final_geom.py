#!/usr/bin/env python3
"""Final geometry pass for slide_026 build."""
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg').convert('RGB')
W, H = im.size
px = im.load()

# 1. 24V gray box bbox
minx = miny = 99999; maxx = maxy = -1
for y in range(412, 460):
    for x in range(380, 425):
        c = px[x, y]
        if abs(c[0]-215) < 16 and abs(c[1]-215) < 16 and abs(c[2]-213) < 16:
            minx = min(minx, x); maxx = max(maxx, x)
            miny = min(miny, y); maxy = max(maxy, y)
print("24V gray box bbox:", (minx, miny, maxx, maxy))

# 2. sub-box 2 bottom / 3 top: dash rows y 335-360
print("--- dash rows y335..360 (dark sum<420, x455..595) ---")
for y in range(335, 361):
    xs = [x for x in range(455, 596) if sum(px[x, y]) < 420]
    if len(xs) >= 8:
        print(f"y={y}: n={len(xs)} x {min(xs)}..{max(xs)}")

# 3. fan labels: dark rows x692..732, y285..378
print("--- fan label rows x692..732 y285..378 ---")
for y in range(285, 379):
    xs = [x for x in range(692, 733) if sum(px[x, y]) < 400]
    if len(xs) >= 2:
        print(f"y={y}: x {min(xs)}..{max(xs)} n={len(xs)}")

# 4. cable/encoder/motor: gray map x725..856 y288..432 (coarse)
print("--- gray/white map x725..856 y288..432 (2px step) ---")
for y in range(288, 433, 4):
    row = ''
    for x in range(725, 857, 2):
        c = px[x, y]
        r, g, b = c
        if r > 243 and g > 243 and b > 240: k = '.'
        elif r < 90 and g < 90 and b < 90: k = '#'
        elif abs(r-g) < 18 and abs(g-b) < 18 and 110 < r < 210: k = 'm'
        elif r > 225 and 180 < g < 235 and 150 < b < 215: k = 'p'
        else: k = '?'
        row += k
    print(f"{y:3d} {row}")

# 5. diff box text rows
print("--- diff box text rows x700..828 y248..282 ---")
for y in range(248, 283):
    xs = [x for x in range(700, 829) if sum(px[x, y]) < 400]
    if len(xs) >= 3:
        print(f"y={y}: x {min(xs)}..{max(xs)} n={len(xs)}")

# 6. cap heights: title S stem, subtitle, caption
def col_profile(x0, x1, y0, y1, pred):
    rows = [y for y in range(y0, y1) if any(pred(px[x, y]) for x in range(x0, x1))]
    return (min(rows), max(rows)) if rows else None

isredd = lambda c: c[0] > 120 and c[1] < 90 and c[2] < 90
print("title 'S' (x372-390) band:", col_profile(372, 391, 50, 85, isredd))
print("caption1 'E' (x335-347) band:", col_profile(335, 348, 475, 495, isredd))
print("arrowlabel 'P' (x144-156) band:", col_profile(144, 157, 318, 340, isredd))
isnavy = lambda c: c[2] > 100 and c[2]-c[0] > 40 and c[0] < 150
print("subtitle '(' (x208-220) band:", col_profile(208, 221, 78, 105, isnavy))

# 7. wires connector->panel gap (bg gray panel): x667..684
print("--- gap rows x667..684 y250..400 (non-bg) ---")
for y in range(250, 401):
    xs = [x for x in range(667, 685) if not (abs(px[x,y][0]-233)<14 and abs(px[x,y][1]-233)<14 and abs(px[x,y][2]-231)<16)]
    if len(xs) >= 3:
        print(f"y={y}: x {min(xs)}..{max(xs)} n={len(xs)}")
