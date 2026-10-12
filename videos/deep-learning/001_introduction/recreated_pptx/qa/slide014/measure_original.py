#!/usr/bin/env python3
"""PIL-measure ground truth frame slide_014.jpg (960x540, 1px = 1pt = 1/72 in).

Measures: title band, flowchart panel (white + blue border), the five node boxes,
arrow regions, bottom black bar, red frame lines, takeaway sentence.
"""
import json
from PIL import Image

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_014.jpg"
img = Image.open(IM).convert("RGB")
W, H = img.size
px = img.load()

def is_red(p, tol=90):
    r, g, b = p
    return r > 150 and g < 90 and b < 90

def is_black(p, tol=60):
    r, g, b = p
    return r < tol and g < tol and b < tol

def is_blue(p):
    r, g, b = p
    return b > 140 and b - r > 60 and b - g > 40

def is_white(p, tol=40):
    r, g, b = p
    return r > 255 - tol and g > 255 - tol and b > 255 - tol

out = {}

# --- 1. Global row profile: red pixels per row (frame lines, title, takeaway) ---
red_rows = {}
for y in range(H):
    c = 0
    for x in range(W):
        if is_red(px[x, y]):
            c += 1
    if c > 5:
        red_rows[y] = c

# Print red row bands
bands = []
cur = None
for y in range(H):
    if y in red_rows:
        if cur is None:
            cur = [y, y, red_rows[y]]
        else:
            cur[1] = y
            cur[2] = max(cur[2], red_rows[y])
    else:
        if cur is not None:
            bands.append(cur)
            cur = None
if cur:
    bands.append(cur)
out["red_row_bands_(y0,y1,maxcount)"] = bands

# --- 2. Bottom black bar ---
for y in range(H - 1, -1, -1):
    cnt = sum(1 for x in range(0, W, 4) if is_black(px[x, y]))
    if cnt < W // 8:
        out["black_bar_top_y"] = y + 1
        break
# bar x extent at its middle
yb = out.get("black_bar_top_y", H - 5) + 8
xs = [x for x in range(W) if is_black(px[x, min(yb, H - 1)])]
out["black_bar_x_range"] = (min(xs), max(xs)) if xs else None

# --- 3. White flowchart panel: rows where many white pixels ---
white_rows = {}
for y in range(45, H - 30):
    c = sum(1 for x in range(0, W, 2) if is_white(px[x, y]))
    white_rows[y] = c
# find the band with the max white count
band_white = [y for y, c in white_rows.items() if c > 250]
if band_white:
    out["white_panel_y_range"] = (min(band_white), max(band_white))
# panel x range: columns white in the panel middle
ymid = (min(band_white) + max(band_white)) // 2
xs_white = [x for x in range(W) if is_white(px[x, ymid])]
out["panel_white_x_at_ymid"] = (min(xs_white), max(xs_white)) if xs_white else None

# --- 4. Blue border of panel: blue pixel columns/rows ---
blue_pts = [(x, y) for y in range(30, H - 20, 2) for x in range(0, W, 2) if is_blue(px[x, y])]
if blue_pts:
    xsb = [p[0] for p in blue_pts]
    ysb = [p[1] for p in blue_pts]
    out["blue_extent_sampled"] = (min(xsb), max(xsb), min(ysb), max(ysb))

# --- 5. Node boxes: scan the panel interior for the distinct fill colors ---
def color_bands(target, tol):
    """Return list of (y0,y1,x0,x1) bounding boxes of connected-ish regions of a color."""
    pts = []
    for y in range(100, 520):
        for x in range(60, 900):
            r, g, b = px[x, y]
            tr, tg, tb = target
            if abs(r - tr) < tol and abs(g - tg) < tol and abs(b - tb) < tol:
                pts.append((x, y))
    return pts

# sample colors first: print modal colors inside panel at a few rows
print("panel ymid row sample:", [px[x, ymid] for x in range(100, 900, 100)])

# green box
gp = color_bands((0, 128, 0), 70)
if gp:
    gx = [p[0] for p in gp]; gy = [p[1] for p in gp]
    out["green_node_bbox"] = (min(gx), max(gx), min(gy), max(gy))

# dark red box (A50021-ish)
dp = color_bands((165, 0, 33), 80)
if dp:
    dx = [p[0] for p in dp]; dy = [p[1] for p in dp]
    out["darkred_node_bbox"] = (min(dx), max(dx), min(dy), max(dy))

# light blue box (CCECFF)
lb = color_bands((204, 236, 255), 40)
if lb:
    lx = [p[0] for p in lb]; ly = [p[1] for p in lb]
    out["lightblue_node_bbox"] = (min(lx), max(lx), min(ly), max(ly))

# tan box (F5DEB3)
tp = color_bands((245, 222, 179), 40)
if tp:
    tx = [p[0] for p in tp]; ty = [p[1] for p in tp]
    out["tan_node_bbox"] = (min(tx), max(tx), min(ty), max(ty))

# light yellow box (FFFFCC)
yp = color_bands((255, 255, 204), 35)
if yp:
    yx2 = [p[0] for p in yp]; yy2 = [p[1] for p in yp]
    out["lightyellow_node_bbox"] = (min(yx2), max(yx2), min(yy2), max(yy2))

print(json.dumps(out, indent=1))
