#!/usr/bin/env python3
"""pm2_structure.py — slide 034 global structure: ink bands + per-element ink bboxes.

Ink = pixel differing from the panel background (gray E9E9E7 / white canvas FFFFFF).
Outputs the row-band table for the whole content column, then a named-element table
(title, subtitle, left labels, lanes, boxes, bar, arrows, brace, summary box, lines).

Output: pm2_structure_output.txt
"""
import numpy as np
from PIL import Image
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
OUT = os.path.join(HERE, "pm2_structure_output.txt")

AX, SX, SY = 17.891, 0.962062, 0.955556
def FX(fx): return (fx - AX) / SX
def FY(fy): return fy / SY

img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = img.shape
r, g, b = img[..., 0], img[..., 1], img[..., 2]
lines = []
def say(s=""):
    lines.append(s)
    print(s)

bg_gray = (np.abs(r - 233) < 12) & (np.abs(g - 233) < 12) & (np.abs(b - 231) < 14)
bg_white = (r > 243) & (g > 243) & (b > 243)
ink = ~(bg_gray | bg_white)
# exclude the letterbox rows and the chrome border columns from the content scan
XL, XR, YT = 63, 899, 47   # inside the panel border strokes

def bbox_of(mask, x0, x1, y0, y1):
    m = mask[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if len(xs) == 0:
        return None
    return (int(xs.min() + x0), int(x1 and xs.max() + x0), int(ys.min() + y0), int(ys.max() + y0), int(m.sum()))

def fmt(bb):
    if bb is None:
        return "NONE"
    x0, x1, y0, y1, n = bb
    return f"x[{x0},{x1}] y[{y0},{y1}] npx={n}"

# --- row band table ---
say("== ROW BAND TABLE (ink px per row, x 63..899; runs >=2 rows with >=8 ink px) ==")
counts = ink[:, XL:XR].sum(axis=1)
bands = []
y = YT
while y < 516:
    if counts[y] >= 8:
        y0 = y
        while y < 516 and counts[y] >= 3:
            y += 1
        y1 = y - 1
        if y1 - y0 >= 1:
            bands.append((y0, y1))
    y += 1
for y0, y1 in bands:
    bb = bbox_of(ink, XL, XR, y0, y1 + 1)
    x0, x1, _, _, n = bb
    say(f"  band y[{y0},{y1}] h={y1-y0+1}  ink-x[{x0},{x1}]  slide-y {FY(y0):.1f}..{FY(y1):.1f}  npx={n}")

# --- named elements (windows hand-placed from the band table) ---
say("\n== ELEMENT INK BBOXES (frame px; slide-pt conversion via adopted mapping) ==")
els = [
    ("title+badge row (y47..95)", 250, 910, 47, 95),
    ("title ink only (x<840)", 250, 840, 47, 100),
    ("subtitle", 250, 760, 95, 125),
    ("left label block1 (blue)", 63, 165, 130, 195),
    ("lane1 (token row, incl dashes)", 150, 900, 128, 180),
    ("token boxes band", 160, 890, 138, 172),
    ("dots gap region (x615..725)", 615, 725, 140, 175),
    ("arrow1", 490, 560, 176, 216),
    ("bar (purple)", 150, 900, 210, 258),
    ("bar text ink (non-purple inside bar)", 165, 885, 216, 254),
    ("left label block2 (red+blue)", 63, 168, 210, 275),
    ("arrow2", 490, 560, 252, 292),
    ("lane3 (vector row, incl dashes)", 150, 900, 283, 334),
    ("vector boxes band", 160, 890, 293, 328),
    ("brace", 150, 900, 330, 365),
    ("summary box", 200, 850, 355, 512),
    ("summary line1", 220, 830, 368, 390),
    ("summary line2", 220, 830, 390, 410),
    ("summary line3", 220, 830, 410, 432),
    ("summary line4", 220, 830, 432, 455),
    ("summary line5", 220, 830, 470, 495),
]
for name, x0, x1, y0, y1 in els:
    bb = bbox_of(ink, x0, x1, y0, y1)
    if bb:
        bx0, bx1, by0, by1, n = bb
        say(f"  {name:42s} frame x[{bx0},{bx1}] y[{by0},{by1}] npx={n}  | slide x {FX(bx0):.1f}..{FX(bx1):.1f} y {FY(by0):.1f}..{FY(by1):.1f}")
    else:
        say(f"  {name:42s} NONE")

# --- color-class sub-bboxes for key elements ---
say("\n== COLOR-CLASS BBOXES ==")
blue = (b - r > 30) & (b > 70)
red = (r - np.maximum(g, b) > 45)
yellow = (r > 205) & (g > 195) & (b < 170)
green = (g - np.maximum(r, b) > 25) & (g > 90)
purple = (r > 90) & (r < 210) & (g < 75) & (b > 95) & (b < 215)
dark = (r + g + b < 420)
classes = [("red-ish", red), ("blue-ish", blue), ("yellow", yellow), ("green-ish", green), ("purple", purple), ("dark ink", dark)]
for name, cm in classes:
    say(f"  -- {name} --")
    for label, x0, x1, y0, y1 in [
        ("title", 250, 840, 47, 100), ("subtitle", 250, 760, 95, 125),
        ("lab1", 63, 165, 130, 195), ("lab2", 63, 168, 210, 275),
        ("lane1 band", 150, 900, 128, 180), ("bar band", 150, 900, 210, 258),
        ("lane3 band", 150, 900, 283, 334), ("brace band", 150, 900, 330, 365),
        ("summary", 200, 850, 355, 512),
    ]:
        bb = bbox_of(cm, x0, x1, y0, y1)
        if bb:
            bx0, bx1, by0, by1, n = bb
            say(f"    {label:12s} frame x[{bx0},{bx1}] y[{by0},{by1}] npx={n}")

# --- lane dash detection: top/bottom dash rows of lane1 and lane3 ---
say("\n== LANE DASH ROWS (dark-navy px in lane1 / slate-teal px in lane3) ==")
navy = (b - r > 25) & (b > 60) & (r + g + b < 560)
teal = (np.abs(r - 95) < 45) & (np.abs(g - 115) < 45) & (np.abs(b - 130) < 45) & (b > r)
for label, cm, y0, y1 in [("lane1 dashes", navy, 128, 182), ("lane3 dashes", teal, 283, 336)]:
    rows = cm[y0:y1, XL:XR].sum(axis=1)
    hits = [f"{y0+i}:{v}" for i, v in enumerate(rows) if v > 40]
    say(f"  {label}: " + "  ".join(hits))

# --- empty-gap proof: ink between token box 6 right edge and box 7 left edge ---
say("\n== GAP CHECKS ==")
say(f"  token-gap x615..727, y142..170 ink bbox (excl dots): see dots line below")
dbb = bbox_of(ink, 612, 730, 140, 172)
say(f"  dots-window ink bbox: {fmt(dbb)}")
vgap = bbox_of(ink, 615, 725, 293, 328)
say(f"  vector-gap x615..725 y293..328 ink bbox: {fmt(vgap)}")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"\nwrote {OUT}")
