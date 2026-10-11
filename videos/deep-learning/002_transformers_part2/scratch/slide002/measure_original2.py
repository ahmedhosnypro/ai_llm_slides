#!/usr/bin/env python3
"""Second-pass measurement: scanlines, looser thresholds, crops."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_002.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide002"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def reddish(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50

out = {}

# scanline across middle: report color CHANGE points
def scan_h(y):
    prev = None; changes = []
    for x in range(W):
        p = px[x, y]
        key = (p[0] // 24, p[1] // 24, p[2] // 24)
        if key != prev:
            changes.append((x, p))
            prev = key
    return changes

def scan_v(x):
    prev = None; changes = []
    for y in range(H):
        p = px[x, y]
        key = (p[0] // 24, p[1] // 24, p[2] // 24)
        if key != prev:
            changes.append((y, p))
            prev = key
    return changes

out["scan_h_y300_changes"] = scan_h(300)[:40]
out["scan_v_x480_changes"] = scan_v(480)[:50]

# red border with looser threshold: columns/rows with many reddish px
red_cols = [(x, sum(1 for y in range(0, H, 2) if reddish(px[x, y]))) for x in range(W)]
red_cols = [c for c in red_cols if c[1] > 40]
red_rows = [(y, sum(1 for x in range(0, W, 2) if reddish(px[x, y]))) for y in range(H)]
red_rows = [r for r in red_rows if r[1] > 60]
out["reddish_cols>40"] = red_cols[:20]
out["reddish_rows>60"] = red_rows[:40]

# black strip horizontal extent at y=530
blk = [x for x in range(W) if sum(px[x, 530]) < 150]
out["black_strip_y530_extent"] = (min(blk), max(blk)) if blk else None
blk_top = [y for y in range(H) if sum(px[480, y]) < 150 and sum(px[200, y]) < 150 and sum(px[700, y]) < 150]
out["black_strip_full_rows"] = (min(blk_top), max(blk_top)) if blk_top else None

# top rows: what's at the very top?
out["row0_sample"] = [px[x, 0] for x in (5, 200, 480, 800, 955)]
out["row5_sample"] = [px[x, 5] for x in (5, 200, 480, 800, 955)]
out["row44_sample"] = [px[x, 44] for x in (5, 50, 200, 480, 800, 950)]
out["row46_sample"] = [px[x, 46] for x in (5, 50, 200, 480, 800, 950)]
out["col0_sample"] = [px[0, y] for y in (5, 100, 300, 500, 535)]
out["col5_sample"] = [px[5, y] for y in (5, 100, 300, 500, 535)]
out["col30_sample"] = [px[30, y] for y in (5, 100, 300, 500, 535)]
out["col45_sample"] = [px[45, y] for y in (5, 100, 300, 500, 535)]
out["col950_sample"] = [px[950, y] for y in (5, 100, 300, 500, 535)]
out["col930_sample"] = [px[930, y] for y in (5, 100, 300, 500, 535)]
out["col915_sample"] = [px[915, y] for y in (5, 100, 300, 500, 535)]
out["col919_sample"] = [px[919, y] for y in (5, 100, 300, 500, 535)]

# badge: all non-panel, non-white px in x 820..960, y 30..130
pts = []
for y in range(30, 130):
    for x in range(820, 960):
        r, g, b = px[x, y]
        # not gray panel (~233) and not white
        if not (abs(r - 233) < 18 and abs(g - 233) < 18 and abs(b - 231) < 18) and not (r > 242 and g > 242 and b > 242):
            pts.append((x, y))
if pts:
    bx0, by0 = min(p[0] for p in pts), min(p[1] for p in pts)
    bx1, by1 = max(p[0] for p in pts), max(p[1] for p in pts)
    out["badge_full_bbox"] = (bx0, by0, bx1, by1)
    out["badge_center"] = ((bx0 + bx1) / 2, (by0 + by1) / 2)
    out["badge_w_h"] = (bx1 - bx0 + 1, by1 - by0 + 1)
    # numeral: dark px
    dark = [(x, y) for (x, y) in pts if sum(px[x, y]) < 330]
    if dark:
        out["numeral_bbox"] = (min(d[0] for d in dark), min(d[1] for d in dark),
                               max(d[0] for d in dark), max(d[1] for d in dark))

# title lines with looser reddish: per-line tight bboxes + per-line column profiles
rows = {}
for y in range(180, 360):
    xs = [x for x in range(50, 910) if reddish(px[x, y])]
    if xs:
        rows[y] = (min(xs), max(xs))
lines = []
cur = None
for y in sorted(rows):
    if cur and y <= cur[1] + 2:
        cur[1] = y; cur[2].append(rows[y])
    else:
        if cur: lines.append(cur)
        cur = [y, y, [rows[y]]]
if cur: lines.append(cur)
out["title_lines_loose"] = []
for y0, y1, segs in lines:
    out["title_lines_loose"].append({
        "y0": y0, "y1": y1, "h": y1 - y0 + 1,
        "x0": min(s[0] for s in segs), "x1": max(s[1] for s in segs),
        "cx": (min(s[0] for s in segs) + max(s[1] for s in segs)) / 2,
    })
    # row heights within: per-row red count for cap-height analysis
    prof = []
    for y in range(y0, y1 + 1):
        cnt = sum(1 for x in range(50, 910) if reddish(px[x, y]))
        prof.append((y, cnt))
    out["title_lines_loose"][-1]["row_profile"] = prof

# title core color mode
from collections import Counter
cores = Counter()
for y0, y1, segs in lines:
    for y in range(y0, y1 + 1):
        for x in range(50, 910):
            p = px[x, y]
            if p[0] > 150 and p[1] < 80 and p[2] < 80:
                cores[p] += 1
out["title_core_colors"] = cores.most_common(5)

# cursor region colors
cc = Counter()
for y in range(355, 380):
    for x in range(430, 460):
        p = px[x, y]
        if sum(p) < 600:
            cc[p] += 1
out["cursor_colors"] = cc.most_common(8)

print(json.dumps(out, indent=1, default=str))

# crops for visual inspection
img.crop((820, 30, 960, 130)).resize((420, 300), Image.NEAREST).save(f"{OUT}/crop_badge.png")
img.crop((250, 190, 720, 360)).save(f"{OUT}/crop_title.png")
img.crop((0, 480, 960, 540)).save(f"{OUT}/crop_bottom.png")
img.crop((400, 340, 500, 395)).resize((400, 220), Image.NEAREST).save(f"{OUT}/crop_cursor.png")
img.crop((0, 0, 120, 120)).resize((360, 360), Image.NEAREST).save(f"{OUT}/crop_topleft.png")
img.crop((840, 0, 960, 120)).resize((360, 360), Image.NEAREST).save(f"{OUT}/crop_topright.png")
print("crops saved")
