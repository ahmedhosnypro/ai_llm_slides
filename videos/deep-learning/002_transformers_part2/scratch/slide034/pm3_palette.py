#!/usr/bin/env python3
"""pm3_palette.py — slide 034 ink census: palette hexes per region.

For each named region: top exact colors by count (census), plus a "core" estimate
(mean of the most extreme 10% of pixels — darkest for ink/line classes, most-saturated
for fill classes). JPEG-blend law: cores are what the P2 family draws; census modes
are what the eye sees.

Output: pm3_palette_output.txt
"""
import numpy as np
from PIL import Image
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
OUT = os.path.join(HERE, "pm3_palette_output.txt")

img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = img[..., 0], img[..., 1], img[..., 2]
lines = []
def say(s=""):
    lines.append(s)
    print(s)

def hx(c):
    return "#%02X%02X%02X" % tuple(int(v) for v in c)

def census(name, y0, y1, x0, x1, mask_fn=None, core="dark"):
    win = img[y0:y1, x0:x1]
    m = np.ones(win.shape[:2], dtype=bool) if mask_fn is None else mask_fn(win)
    px = win[m]
    if len(px) == 0:
        say(f"  {name:34s} EMPTY")
        return
    cnt = Counter(map(tuple, px))
    top = ", ".join(f"{hx(c)}x{n}" for c, n in cnt.most_common(6))
    # core: extreme 10% by the criterion
    if core == "dark":
        key = px.sum(axis=1)
        sel = px[key <= np.percentile(key, 10)]
    elif core == "sat":  # most colorful = farthest from gray of its own luminance
        sat = px.max(axis=1) - px.min(axis=1)
        sel = px[sat >= np.percentile(sat, 90)]
    elif core == "light":
        key = px.sum(axis=1)
        sel = px[key >= np.percentile(key, 90)]
    say(f"  {name:34s} n={len(px):6d}  core({core})={hx(sel.mean(axis=0))}  top: {top}")

say("== PALETTE CENSUS (frame px regions) ==")

say("\n-- title / subtitle --")
census("title red glyphs", 56, 98, 270, 485, lambda w: (w[..., 0] - np.maximum(w[..., 1], w[..., 2]) > 45))
census("title blue glyphs", 56, 98, 488, 700, lambda w: (w[..., 2] - w[..., 0] > 30) & (w[..., 2] > 70))
census("subtitle red glyphs", 96, 124, 270, 660, lambda w: (w[..., 0] - np.maximum(w[..., 1], w[..., 2]) > 45))

say("\n-- left labels --")
census("lab1 blue ('Position Information' + paren)", 137, 195, 63, 165, lambda w: (w[..., 2] - w[..., 0] > 25) & (w[..., 2] > 60))
census("lab2 red italic ('Positional Embedding')", 215, 253, 66, 168, lambda w: (w[..., 0] - np.maximum(w[..., 1], w[..., 2]) > 40))
census("lab2 blue ('(Trained on Position Values)')", 253, 275, 63, 170, lambda w: (w[..., 2] - w[..., 0] > 25) & (w[..., 2] > 60))

say("\n-- lane1 / token row --")
census("lane1 fill (x340..360 between boxes)", 146, 162, 336, 358, None, "sat")
census("lane1 dash top row (y135..138)", 135, 138, 200, 850, lambda w: (w[..., 2] - w[..., 0] > 20) & (w.sum(axis=2) < 600))
census("token box border (box1 edges x180/x239)", 146, 164, 178, 242, lambda w: (w.sum(axis=2) < 640) & (np.abs(w[..., 0] - w[..., 2]) < 90))
census("token box interior fill (box1 center)", 150, 160, 200, 225, None, "light")
census("digit ink (box1 '0' zone)", 144, 168, 195, 230, lambda w: (w.sum(axis=2) < 420))
census("dots zone (x620..725 y146..170, non-fill)", 146, 170, 620, 725,
       lambda w: (w.sum(axis=2) < 660) & (np.abs(w[..., 0] - w[..., 2]) < 70))

say("\n-- arrows --")
census("arrow1 red", 178, 212, 505, 545, lambda w: (w[..., 0] - np.maximum(w[..., 1], w[..., 2]) > 40))
census("arrow2 red", 254, 288, 505, 545, lambda w: (w[..., 0] - np.maximum(w[..., 1], w[..., 2]) > 40))

say("\n-- purple bar --")
census("bar fill (quiet right end)", 220, 248, 800, 860, None, "sat")
census("bar yellow words", 222, 250, 305, 600, lambda w: (w[..., 0] > 200) & (w[..., 1] > 190) & (w[..., 2] < 180), "light")
census("bar white words", 222, 250, 600, 800, lambda w: (w.min(axis=2) > 190), "light")

say("\n-- lane3 / vector row --")
census("lane3 fill (gap x630..710 y295..320)", 296, 320, 630, 710, None, "sat")
census("lane3 dash top row (y289..292)", 289, 293, 200, 850, lambda w: (w.sum(axis=2) < 620))
census("vector box border (box1 edges)", 296, 322, 176, 242, lambda w: (w.sum(axis=2) < 640) & (w[..., 0] - w[..., 2] > 10))
census("vector box interior fill (box1 center)", 300, 318, 200, 225, None, "light")
census("vector label ink (box1 'Vector' zone)", 298, 324, 185, 235, lambda w: (w.sum(axis=2) < 430))
census("vector labels RED check (all boxes, red px)", 296, 324, 170, 890, lambda w: (w[..., 0] - np.maximum(w[..., 1], w[..., 2]) > 45))

say("\n-- brace / summary --")
census("brace red", 332, 356, 175, 875, lambda w: (w[..., 0] - np.maximum(w[..., 1], w[..., 2]) > 40))
census("summary border (top+bottom rows)", 360, 366, 300, 700, lambda w: (w[..., 1] - np.maximum(w[..., 0], w[..., 2]) > 15))
census("summary border right col (x823..827)", 365, 500, 822, 828, lambda w: (w[..., 1] - np.maximum(w[..., 0], w[..., 2]) > 15))
census("line1/2/5 black ink", 368, 410, 240, 810, lambda w: (w.sum(axis=2) < 330))
census("line5 black ink", 470, 496, 240, 810, lambda w: (w.sum(axis=2) < 330))
census("line3/4 red ink", 410, 456, 240, 810, lambda w: (w[..., 0] - np.maximum(w[..., 1], w[..., 2]) > 40))
census("highlight yellow (line3 'N-1')", 408, 436, 425, 500, lambda w: (w[..., 0] > 205) & (w[..., 1] > 195) & (w[..., 2] < 180), "light")

say("\n-- chrome / artifacts --")
census("letterbox black (y520..538)", 520, 538, 150, 800, None, "dark")
census("badge yellow", 55, 88, 858, 894, lambda w: (w[..., 0] > 200) & (w[..., 1] > 200) & (w[..., 2] < 190), "light")
census("badge ring purple-ish", 50, 92, 850, 900, lambda w: (w[..., 2] > 140) & (w[..., 2] - w[..., 1] > 25) & (w[..., 0] > 70) & (w[..., 0] < 200))
census("panel gray", 300, 310, 480, 500, None, "light")
census("canvas white (x30..40)", 300, 400, 25, 40, None, "light")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"\nwrote {OUT}")
