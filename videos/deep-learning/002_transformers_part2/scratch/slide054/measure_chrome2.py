#!/usr/bin/env python3
"""Refined chrome measurement: thin red border, true badge circle, panel gray."""
from PIL import Image
import json
from collections import Counter

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def is_redish(p):    r,g,b = p; return r > 120 and g < 100 and b < 100 and (r - max(g,b)) > 50
def is_yellowish(p): r,g,b = p; return r > 200 and g > 200 and b < 180
def is_purple(p): r,g,b = p; return 90 <= r <= 170 and 60 <= g <= 130 and b > 150

out = {}
# 1. red border: per-column count of redish pixels (full scan)
col_counts = {x: sum(1 for y in range(H) if is_redish(px[x, y])) for x in range(W)}
strong_cols = [x for x, c in col_counts.items() if c > 150]
out["strong_red_cols(>150)"] = strong_cols[:20]
row_counts = {y: sum(1 for x in range(W) if is_redish(px[x, y])) for y in range(H)}
strong_rows = [y for y, c in row_counts.items() if c > 150]
out["strong_red_rows(>150)"] = strong_rows[:20]
# weaker strokes (1-2px wide border, may be diluted by JPEG): threshold > 60
weak_cols = [x for x, c in col_counts.items() if c > 60]
weak_rows = [y for y, c in row_counts.items() if c > 60]
out["weak_red_cols(>60)"] = weak_cols
out["weak_red_rows(>60)"] = weak_rows

# 2. border stroke sample colors near expected top border
if weak_rows:
    ytop = min(weak_rows)
    out["top_border_color_samples"] = [px[x, ytop] for x in (100, 300, 500, 700)]
if weak_cols:
    xl = min(weak_cols)
    out["left_border_color_samples"] = [px[xl, y] for y in (100, 200, 300, 400)]

# 3. panel gray detection: count gray-ish pixels per row (E9E9E7 ~ (233,233,231))
def is_gray(p): r,g,b = p; return abs(r-g) < 8 and abs(g-b) < 10 and 215 <= r <= 245
gray_rows = {}
for y in range(0, H, 10):
    cnt = sum(1 for x in range(0, W, 2) if is_gray(px[x, y]))
    gray_rows[y] = cnt
out["gray_row_profile_every10"] = gray_rows

# 4. badge isolation: yellow/purple in x 840..925, y 40..105
pts = [(x, y) for y in range(30, 110) for x in range(830, 935) if is_yellowish(px[x, y]) or is_purple(px[x, y])]
if pts:
    xs = sorted(set(p[0] for p in pts)); ys2 = sorted(set(p[1] for p in pts))
    out["badge_zone_bbox"] = (min(xs), min(ys2), max(xs), max(ys2))
    # histogram of x to split clusters
    xh = Counter(p[0] for p in pts)
    out["badge_zone_x_hist"] = {x: c for x, c in sorted(xh.items())}

print(json.dumps(out, indent=1, default=str))
