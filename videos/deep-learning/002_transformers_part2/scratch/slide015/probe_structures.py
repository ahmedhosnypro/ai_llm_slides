#!/usr/bin/env python3
"""Probe 002 slide_015 frame structures vs parent 001:43 block geometry.
All parent geometry is in TRUE slide coords; convert with the fitted mapping
(frame_x = 17.628 + 0.961232*slide_x, frame_y = 0.955556*slide_y).
"""
from PIL import Image
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg").convert("RGB")
W, H = img.size
px = img.load()
AX, SX, SY = 17.628, 0.961232, 0.955556
fx = lambda s: AX + SX * s
fy = lambda s: SY * s

def scanline_changes(y, x0=50, x1=910, q=16):
    prev = None; out = []
    for x in range(x0, x1):
        p = px[x, y]
        key = (p[0] // q, p[1] // q, p[2] // q)
        if key != prev:
            out.append((x, p)); prev = key
    return out

X1 = 910

def classify(p):
    r, g, b = p
    if r > 240 and g > 240 and b > 240: return "white"
    if abs(r - 233) < 15 and abs(g - 233) < 15 and abs(b - 231) < 15: return "panel"
    if r > 200 and 100 < g < 190 and 100 < b < 190: return "salmon?"
    if 180 < r < 230 and 150 < g < 200 and 220 < b < 255: return "lavender?"
    if r > 230 and g > 230 and b < 190: return "yellow?"
    if 190 < r < 230 and g > 230 and 200 < b < 240: return "mintgreen?"
    if r > 230 and 190 < g < 225 and 180 < b < 220: return "peach?"
    return f"({r},{g},{b})"

rep = {}

# 1) card staircase: scan at several y in frame coords, print long color runs
for name, fyy in [("y260(front h1?)", 260), ("y300", 300), ("y350", 350), ("y420", 420), ("y470", 470)]:
    ch = scanline_changes(fyy)
    # compress: keep runs > 8px
    runs = []
    for i, (x, p) in enumerate(ch):
        x2 = ch[i + 1][0] if i + 1 < len(ch) else X1
        if x2 - x > 8:
            runs.append((x, x2, classify(p)))
    rep[f"runs_{name}"] = runs

# 2) concat bar probe: slide y 128..151 -> frame y 122..145; scan frame y 134
ch = scanline_changes(134)
runs = []
for i, (x, p) in enumerate(ch):
    x2 = ch[i + 1][0] if i + 1 < len(ch) else X1
    if x2 - x > 6:
        runs.append((x, x2, classify(p)))
rep["runs_y134_concatbar_zone"] = runs

# 3) title zone top: slide y 48..101 -> frame 46..97. Reddish/dark ink bbox in frame y 40..100
ink = [(x, y) for y in range(40, 100) for x in range(60, 900, 1)
       if sum(px[x, y]) < 420]
rep["title_top_ink_bbox"] = (min(t[0] for t in ink), min(t[1] for t in ink),
                             max(t[0] for t in ink), max(t[1] for t in ink)) if ink else None

# 4) title zone bottom: frame y 420..480 (slide 440..502)
ink = [(x, y) for y in range(415, 490) for x in range(60, 900)
       if sum(px[x, y]) < 420]
rep["title_bottom_ink_bbox"] = (min(t[0] for t in ink), min(t[1] for t in ink),
                                max(t[0] for t in ink), max(t[1] for t in ink)) if ink else None

# 5) legend zone: slide x736..906 y468..532 -> frame x725..888 y447..508; ink?
zone = [(x, y) for y in range(447, 509) for x in range(720, 895)
        if sum(px[x, y]) < 420]
rep["legend_zone_ink_count"] = len(zone)
if zone:
    rep["legend_zone_ink_bbox"] = (min(t[0] for t in zone), min(t[1] for t in zone),
                                   max(t[0] for t in zone), max(t[1] for t in zone))

# 6) ltbox zone: slide x314..554 y90..114 -> frame 319..550 y86..109; fill probe
probe = px[int(fx(430)), int(fy(102))]
rep["ltbox_center_color"] = probe
# concatbar center
rep["concatbar_center_color"] = px[int(fx(430)), int(fy(140))]
# vecbox zone slide x400..470 y50..72 -> frame 402..469 y48..69
rep["vecbox_center_color"] = px[int(fx(435)), int(fy(60))]

# 7) big swoosh zone: slide x585..930 y325..525 -> frame x580..912 y311..502; red ink bbox
zone = [(x, y) for y in range(305, 510) for x in range(570, 900)
        if px[x, y][0] > 150 and px[x, y][0] - px[x, y][1] > 60 and px[x, y][0] - px[x, y][2] > 60]
rep["swoosh_red_ink_count"] = len(zone)
if zone:
    rep["swoosh_red_ink_bbox"] = (min(t[0] for t in zone), min(t[1] for t in zone),
                                  max(t[0] for t in zone), max(t[1] for t in zone))

# 8) W^(1..4) red boxes: spec ~62-66% width (595..634 slide), 65-78% height (351..421 slide)
#    -> frame x 590..627, y 335..402; red fill bbox
zone = [(x, y) for y in range(330, 410) for x in range(580, 640)
        if px[x, y][0] > 150 and px[x, y][0] - px[x, y][1] > 60 and px[x, y][0] - px[x, y][2] > 60]
rep["w1234_red_ink_count"] = len(zone)
if zone:
    rep["w1234_red_ink_bbox"] = (min(t[0] for t in zone), min(t[1] for t in zone),
                                 max(t[0] for t in zone), max(t[1] for t in zone))

print(json.dumps(rep, indent=1, default=str))
