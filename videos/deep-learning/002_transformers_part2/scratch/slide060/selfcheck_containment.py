#!/usr/bin/env python3
"""Self-check #2: FRAME CONTAINMENT on render_3 — no content ink outside the content box
interior / house panel; no ink touching the box border stroke."""
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide060/render_3.png"
img = Image.open(R).convert("RGB")
W, H = img.size
px = img.load()

def reddish(p):
    r, g, b = p
    return r > 140 and r - g > 60 and r - b > 60

def blueish(p):
    r, g, b = p
    return b > 90 and b - r > 40 and b - g > 30

# box border stroke outer edges (measured attempt-1: left ~132-137, right ~1860-1865,
# top ~251-256, bottom ~1049-1054). Content box interior for text: [140, 1857] x [259, 1046].
# House panel interior (chrome borders excluded): x [90, 1912], y [96, 1123].
viol = []
for y in range(96, H - 2):
    for x in range(90, min(W - 2, 1913)):
        if reddish(px[x, y]) or blueish(px[x, y]):
            inside_box = (140 <= x <= 1857 and 259 <= y <= 1046)
            is_border = (131 <= x <= 139 or 1858 <= x <= 1867 or 250 <= y <= 258 or 1047 <= y <= 1055)
            is_title = (400 <= x <= 1500 and 135 <= y <= 210)  # title band (above box, inside panel)
            is_badge = x >= 1750 and y <= 200  # badge numeral zone (chrome)
            if not (inside_box or is_border or is_title or is_badge):
                viol.append((x, y, px[x, y]))
print("containment violations (content ink outside allowed zones):", len(viol))
for v in viol[:20]:
    print("  ", v)
# also: ink must not TOUCH the border stroke interior edges (>=2px clearance)
touch = []
for y in range(259, 1046):
    for x in (140, 141, 1856, 1857):
        if reddish(px[x, y]) or blueish(px[x, y]):
            touch.append((x, y))
    for x in range(140, 1858):
        if y in (259, 260, 1045, 1046) and (reddish(px[x, y]) or blueish(px[x, y])):
            touch.append((x, y))
print("ink within 2px of box border interior:", len(touch), touch[:10])
print("PASS" if not viol and not touch else "FAIL")
