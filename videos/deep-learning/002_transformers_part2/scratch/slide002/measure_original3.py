#!/usr/bin/env python3
"""Third pass: clean title-line bboxes (exclude borders), badge bbox, mapping to slide coords."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_002.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def reddish(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50

# clean title scan: x 75..885 (borders at 59, 902 excluded), y 150..400
rows = {}
for y in range(150, 400):
    xs = [x for x in range(75, 886) if reddish(px[x, y])]
    if xs:
        rows[y] = (min(xs), max(xs))
lines = []
cur = None
for y in sorted(rows):
    if cur and y <= cur[1] + 3:
        cur[1] = y; cur[2].append(rows[y])
    else:
        if cur: lines.append(cur)
        cur = [y, y, [rows[y]]]
if cur: lines.append(cur)

# frame->slide mapping (fitted from border landmarks)
SH, DH = 0.96123, 18.63   # frame_x = DH + SH * slide_x
SV, DV = 0.95556, 0.0     # frame_y = DV + SV * slide_y
def to_slide(fx, fy):
    return ((fx - DH) / SH, (fy - DV) / SV)

out = {"mapping": {"SH": SH, "DH": DH, "SV": SV, "DV": DV}}
out["title_lines"] = []
for y0, y1, segs in lines:
    fx0 = min(s[0] for s in segs); fx1 = max(s[1] for s in segs)
    sx0, sy0 = to_slide(fx0, y0); sx1, sy1 = to_slide(fx1, y1)
    out["title_lines"].append({
        "frame": {"y0": y0, "y1": y1, "h": y1 - y0 + 1, "x0": fx0, "x1": fx1, "w": fx1 - fx0 + 1,
                  "cx": (fx0 + fx1) / 2},
        "slide": {"y0": round(sy0, 1), "y1": round(sy1, 1), "h": round(sy1 - sy0, 1),
                  "x0": round(sx0, 1), "x1": round(sx1, 1), "w": round(sx1 - sx0, 1),
                  "cx": round((sx0 + sx1) / 2, 1)},
    })

# cap-height of line1 via column profile of 'T' (leftmost glyph): dense rows
if lines:
    y0, y1, segs = lines[0]
    fx0 = min(s[0] for s in segs)
    # column ink profile at line1's left edge glyph
    col = [(y, 1) for y in range(y0, y1 + 1) if any(reddish(px[xx, y]) for xx in range(fx0, fx0 + 18))]
    if col:
        out["line1_left_glyph_frame_rows"] = (col[0][0], col[-1][0])

# badge clean: yellowish fill only, region x 840..920, y 40..110, excluding border row/col
ypts = [(x, y) for y in range(46, 110) for x in range(840, 900)
        if px[x, y][0] > 235 and px[x, y][1] > 235 and 130 < px[x, y][2] < 210]
if ypts:
    bx0, by0 = min(p[0] for p in ypts), min(p[1] for p in ypts)
    bx1, by1 = max(p[0] for p in ypts), max(p[1] for p in ypts)
    out["badge_yellow_bbox_frame"] = (bx0, by0, bx1, by1)
    out["badge_yellow_center_frame"] = ((bx0 + bx1) / 2, (by0 + by1) / 2)
    sb = to_slide((bx0 + bx1) / 2, (by0 + by1) / 2)
    out["badge_yellow_center_slide"] = (round(sb[0], 1), round(sb[1], 1))

# numeral: dark px within badge bbox
dark = [(x, y) for y in range(46, 110) for x in range(840, 900) if sum(px[x, y]) < 300]
if dark:
    out["numeral_dark_bbox_frame"] = (min(d[0] for d in dark), min(d[1] for d in dark),
                                      max(d[0] for d in dark), max(d[1] for d in dark))

# cursor bbox (for the record; omitted from build)
cpts = [(x, y) for y in range(345, 395) for x in range(400, 500) if sum(px[x, y]) < 520]
if cpts:
    out["cursor_bbox_frame"] = (min(c[0] for c in cpts), min(c[1] for c in cpts),
                                max(c[0] for c in cpts), max(c[1] for c in cpts))

# black strip rows/extent (for the record; omitted from build - below slide bottom)
out["black_strip_frame"] = {"rows": "517-539", "x_extent_y530": [38, 921],
                            "slide_y_of_row517": round(517 / SV, 1)}

print(json.dumps(out, indent=1))
