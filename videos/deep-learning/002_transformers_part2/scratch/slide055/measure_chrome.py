#!/usr/bin/env python3
"""Slide 055 frame landmark measurement (P4 pattern: re-fit THIS frame's four chrome
landmarks + badge, derive frame->slide mapping constants)."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def is_redish(p):
    r, g, b = p
    return r > 120 and g < 100 and b < 100 and (r - max(g, b)) > 50
def is_yellowish(p):
    r, g, b = p
    return r > 200 and g > 200 and b < 180
def is_purple(p):
    r, g, b = p
    return 90 <= r <= 170 and 60 <= g <= 130 and b > 150

out = {"size": [W, H]}

# 1. chrome border landmarks
col_counts = {x: sum(1 for y in range(H) if is_redish(px[x, y])) for x in range(W)}
row_counts = {y: sum(1 for x in range(W) if is_redish(px[x, y])) for y in range(H)}
weak_cols = [x for x, c in col_counts.items() if c > 60]
weak_rows = [y for y, c in row_counts.items() if c > 60]
out["weak_red_cols(>60)"] = weak_cols
out["weak_red_rows(>60)"] = weak_rows

# 2. badge: yellow/purple cluster in x 830..935, y 30..110
pts = [(x, y) for y in range(30, 110) for x in range(830, 935)
       if is_yellowish(px[x, y]) or is_purple(px[x, y])]
if pts:
    xs = sorted(set(p[0] for p in pts)); ys = sorted(set(p[1] for p in pts))
    bbox = (min(xs), min(ys), max(xs), max(ys))
    out["badge_bbox"] = bbox
    out["badge_center"] = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)

# 3. derive mapping: frame panel left/right/top/bottom <-> slide chrome 42, 919, 45, 540
if len(weak_cols) >= 2 and len(weak_rows) >= 2:
    fl, fr = min(weak_cols), max(weak_cols)
    ft = min(weak_rows)
    # bottom border: red rows near 516 (bottom stroke of panel) — strong rows sorted
    bottom_cands = [y for y in weak_rows if y > 490]
    fb = max(bottom_cands) if bottom_cands else None
    out["frame_landmarks"] = dict(left=fl, right=fr, top=ft, bottom=fb)
    # fit: frame_x = X0 + SX*slide_x with (42)->fl, (919)->fr  [slide chrome panel spans 42..918+1]
    SX = (fr - fl) / (919 - 42)
    X0 = fl - SX * 42
    SY = (fb - ft) / (540 - 45)
    out["mapping"] = dict(X0=round(X0, 3), SX=round(SX, 5), SY=round(SY, 5),
                          note="frame_x=X0+SX*slide_x; frame_y=SY*slide_y; slide_x=(fx-X0)/SX; slide_y=fy/SY")
    # cross-check badge: yellow-bbox center -> slide coords
    if "badge_center" in out:
        bx_s = (out["badge_center"][0] - X0) / SX
        by_s = out["badge_center"][1] / SY
        out["badge_to_slide"] = (round(bx_s, 1), round(by_s, 1))

print(json.dumps(out, indent=1))
