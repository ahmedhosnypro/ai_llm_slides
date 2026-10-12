#!/usr/bin/env python3
"""Measure slide_015 frame chrome landmarks -> fit frame->slide mapping.

Landmarks (per playlist chrome law): gray panel E9E9E7 spans x 42..918, y 45..bottom
in TRUE slide coords (960x540, 1px=1pt); thin C00000 border on panel left/right/top;
red bottom stroke half-visible at slide bottom (slide y ~538.5); badge circle d36 at
(893,71). The 002 capture is zoomed out ~0.958 with letterbox strips.
"""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def reddish(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50

# reddish columns/rows (panel borders + bottom stroke)
red_cols = [(x, sum(1 for y in range(0, H, 2) if reddish(px[x, y]))) for x in range(W)]
red_cols = [c for c in red_cols if c[1] > 40]
red_rows = [(y, sum(1 for x in range(0, W, 2) if reddish(px[x, y]))) for y in range(H)]
red_rows = [r for r in red_rows if r[1] > 60]

# badge: non-panel non-white px in x 800..960, y 20..140
pts = []
for y in range(20, 140):
    for x in range(800, 960):
        r, g, b = px[x, y]
        if not (abs(r - 233) < 18 and abs(g - 233) < 18 and abs(b - 231) < 18) and not (r > 242 and g > 242 and b > 242):
            pts.append((x, y))
badge = None
if pts:
    bx0, by0 = min(p[0] for p in pts), min(p[1] for p in pts)
    bx1, by1 = max(p[0] for p in pts), max(p[1] for p in pts)
    badge = {"bbox": (bx0, by0, bx1, by1), "center": ((bx0 + bx1) / 2, (by0 + by1) / 2),
             "wh": (bx1 - bx0 + 1, by1 - by0 + 1)}
    dark = [(x, y) for (x, y) in pts if sum(px[x, y]) < 330]
    if dark:
        badge["numeral_bbox"] = (min(d[0] for d in dark), min(d[1] for d in dark),
                                 max(d[0] for d in dark), max(d[1] for d in dark))

# letterbox strips: full-width dark rows / columns
dark_rows = [y for y in range(H) if sum(1 for x in range(100, 900, 25) if sum(px[x, y]) < 150) > 28]
dark_cols = [x for x in range(W) if sum(1 for y in range(60, 500, 20) if sum(px[x, y]) < 150) > 20]

out = {"reddish_cols>40": red_cols[:24], "reddish_rows>60": red_rows[:40],
       "badge": badge, "dark_rows": dark_rows, "dark_cols": dark_cols}

# scanline samples through empty areas to see white margin + panel start
def scan_h(y, x0, x1):
    prev = None; changes = []
    for x in range(x0, x1):
        p = px[x, y]
        key = (p[0] // 20, p[1] // 20, p[2] // 20)
        if key != prev:
            changes.append((x, p)); prev = key
    return changes
def scan_v(x, y0, y1):
    prev = None; changes = []
    for y in range(y0, y1):
        p = px[x, y]
        key = (p[0] // 20, p[1] // 20, p[2] // 20)
        if key != prev:
            changes.append((y, p)); prev = key
    return changes

# find a y row with only chrome (no content): try y where content likely absent - near top under badge? use y=115 maybe content; try several and report
for y in (140, 200, 320):
    out[f"scan_h_y{y}_left"] = scan_h(y, 30, 80)
    out[f"scan_h_y{y}_right"] = scan_h(y, 880, 940)
for x in (300, 700):
    out[f"scan_v_x{x}_top"] = scan_v(x, 20, 70)
    out[f"scan_v_x{x}_bot"] = scan_v(x, 495, 540)

print(json.dumps(out, indent=1, default=str))
