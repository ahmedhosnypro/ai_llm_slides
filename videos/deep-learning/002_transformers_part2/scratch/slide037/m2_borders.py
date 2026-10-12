#!/usr/bin/env python3
"""Probe the thin red vertical border strokes with a looser test + column profiles."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

out = {}
# raw column profiles near expected borders
def profile(x0, x1, ys):
    res = {}
    for x in range(x0, x1):
        col = [px[x, y] for y in ys]
        res[x] = col
    return res

# left border candidate region x48..62, sample rows spread over full height
ys = list(range(60, 510, 25))
out["left_profile"] = {x: [px[x,y] for y in ys] for x in range(48, 64)}
out["right_profile"] = {x: [px[x,y] for y in ys] for x in range(893, 908)}
# top border candidate rows y40..50 at x=300..320
out["top_profile"] = {y: [px[x,y] for x in range(300, 320, 4)] for y in range(38, 52)}
# bottom stroke rows 513..519 at x=300..320
out["bottom_profile"] = {y: [px[x,y] for x in range(300, 320, 4)] for y in range(512, 520)}

# count reddish-ish px per column with a very loose test over full height
def loose_red(p):
    r,g,b = p
    return (r-g) > 35 and (r-b) > 35 and r > 110
cols = []
for x in range(W):
    c = sum(1 for y in range(46, 517) if loose_red(px[x, y]))
    if c > 150: cols.append((x, c))
out["loose_red_cols"] = cols
print(json.dumps(out, indent=0, default=str))
