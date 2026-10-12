#!/usr/bin/env python3
"""m3: left-input zone of 011 (x55..265, y195..395) — dashed X column, W_v boxes,
K boxes, arrows. Also the green ellipse/orange ellipses if present."""
from PIL import Image
import json
from collections import Counter

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
im = Image.open(f"{SCR}/frame11_slide.png").convert("RGB")
px = im.load()

def near(p, t, tol):
    return all(abs(p[i] - t[i]) <= tol for i in range(3))

out = {}

# 1) green dashes (2E8B57=(46,139,87) family incl. 22AA44=(34,170,68))
gpts = [(x, y) for y in range(195, 400) for x in range(55, 270)
        if near(px[x, y], (46, 139, 87), 45) and px[x, y][1] - px[x, y][0] > 40]
out["green_pts_bbox"] = (min(p[0] for p in gpts), min(p[1] for p in gpts),
                         max(p[0] for p in gpts), max(p[1] for p in gpts)) if gpts else None
# green column histogram -> vertical dashed borders of X boxes
colc = Counter(x for x, _ in gpts)
out["green_cols>30"] = sorted(c for c, n in colc.items() if n > 30)
rowc = Counter(y for _, y in gpts)
out["green_rows>25"] = sorted(r for r, n in rowc.items() if n > 25)

# 2) white boxes w/ red text (W_v): find red text pixels x 140..220
rpts = [(x, y) for y in range(200, 395) for x in range(130, 230)
        if near(px[x, y], (204, 34, 34), 60) and px[x, y][0] - px[x, y][1] > 90]
if rpts:
    xs = [p[0] for p in rpts]; ys = [p[1] for p in rpts]
    out["red_text_bbox"] = (min(xs), min(ys), max(xs), max(ys))
    rowc2 = Counter(y for _, y in rpts)
    # cluster rows into label bands
    bands = []
    ys_sorted = sorted(set(y for _, y in rpts))
    s = e = ys_sorted[0]
    for y in ys_sorted[1:]:
        if y - e <= 3: e = y
        else: bands.append((s, e)); s = e = y
    bands.append((s, e))
    out["red_text_row_bands"] = bands

# 3) vertical scan at several x to map the zone's horizontal bands
def scan_v(x, y0, y1):
    prev = None; ch = []
    for y in range(y0, y1):
        p = px[x, y]
        key = (p[0] // 24, p[1] // 24, p[2] // 24)
        if key != prev: ch.append((y, p)); prev = key
    return ch
for x in (100, 150, 175, 205):
    out[f"scanv_x{x}"] = scan_v(x, 210, 390)[:40]

# 4) orange ellipse check (E8843C / EABC78 family)
opts = [(x, y) for y in range(200, 400) for x in range(60, 200)
        if near(px[x, y], (232, 132, 60), 40) or near(px[x, y], (234, 188, 120), 30)]
out["orange_n"] = len(opts)
if opts:
    xs = [p[0] for p in opts]; ys = [p[1] for p in opts]
    out["orange_bbox"] = (min(xs), min(ys), max(xs), max(ys))

print(json.dumps(out, indent=1, default=str))
