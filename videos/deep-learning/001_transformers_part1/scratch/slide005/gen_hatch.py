#!/usr/bin/env python3
"""Generate the hatched bottom-arrow PNG for slide 005 (8x supersampled) +
final tri2 raw check + hatch stripe direction check."""
import numpy as np
from PIL import Image, ImageDraw

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/slide005_hatch_arrow.png"

im = np.asarray(Image.open(SRC).convert("RGB")).astype(int)

# --- tri2 final raw check: gap1 y330-465, print min deviation per 10px row band
print("=== tri2 zone raw check (x246-306) ===")
for y0 in range(330, 460, 10):
    devs = []
    for y in range(y0, y0 + 10):
        for x in range(246, 307):
            px = im[y, x]
            d = min(abs(int(px[0]) - 233) + abs(int(px[1]) - 233) + abs(int(px[2]) - 231),
                    abs(int(px[0]) - 167) + abs(int(px[1]) - 175) + abs(int(px[2]) - 184))
            if d > 20:
                devs.append((x, y, tuple(int(v) for v in px)))
    print(f"y{y0}-{y0+9}: {len(devs)} dev px", devs[:6] if devs else "")

# --- hatch stripe direction: stripe x-positions at y480 vs y487 in a clean zone (x250-330)
def stripe_centers(y, xa=250, xb=340):
    row = im[y, xa:xb]
    dark = [x + xa for x, px in enumerate(row) if px[0] < 240 and px[1] < 225]
    runs = []
    s = p = None
    for x in dark:
        if s is None:
            s = p = x
        elif x == p + 1:
            p = x
        else:
            runs.append((s + p) / 2); s = p = x
    if s is not None:
        runs.append((s + p) / 2)
    return runs

c480 = stripe_centers(480)
c487 = stripe_centers(487)
print(f"\nstripe centers y480: {[round(v,1) for v in c480]}")
print(f"stripe centers y487: {[round(v,1) for v in c487]}")
if len(c480) > 1 and len(c487) > 1:
    print(f"drift over +7 rows: {c487[0]-c480[0]:+.1f}px (positive => stripes lean like '/' mirrored... i.e. as y increases stripe moves right = '\\\\')")

# --- generate the arrow PNG at 8x scale
S = 8
# original-frame geometry (px): bbox x176..815, y470..497 -> local 639x27
W, H = 639, 27
body_y0, body_y1 = 7, 20        # y477-470=7 .. y490-470=20 (band incl.)
head_back_x = 782 - 176          # 606
tip_x = 815 - 176                # 639
tip_y = 13.5
img = Image.new("RGBA", (W * S, H * S), (233, 233, 231, 255))  # opaque panel bg (alpha blending dimmed white in LO)
d = ImageDraw.Draw(img)

# arrow path (body + head) polygon
path = [
    (0, body_y0 * S),
    (head_back_x * S, body_y0 * S),
    (head_back_x * S, 0),
    (tip_x * S, tip_y * S),
    (head_back_x * S, H * S),
    (head_back_x * S, body_y1 * S),
    (0, body_y1 * S),
]
# white fill inside path
d.polygon(path, fill=(255, 255, 255, 255))

# diagonal hatch stripes clipped to the path: draw wide diagonal lines with mask
stripe_layer = Image.new("L", (W * S, H * S), 0)
ds = ImageDraw.Draw(stripe_layer)
RED = (192, 0, 0)
# 45 deg "\" stripes: measured drift +2.5px per +3 rows (down-right); along-x pitch 5.4px,
# stroke ~2px perpendicular (original-frame px) — fine light-diagonal hatch.
pitch = 5.4 * S
width = int(2 * S)
# lines: y = x + c  ("\" direction) or y = -x + c ("/") — decided by drift check printed above;
# default "\" (down-right): draw long diagonals covering canvas
n = int((W + H) * S // pitch) + 2
for k in range(-n, n):
    c = k * pitch
    ds.line([( -H * S + c, 0), (c, H * S)], fill=255, width=width)  # y = x - c family ("\")

mask = Image.new("L", (W * S, H * S), 0)
dm = ImageDraw.Draw(mask)
dm.polygon(path, fill=255)
# white body inside the path (over the opaque panel bg), then red stripes clipped to it
d.polygon(path, fill=(255, 255, 255, 255))
stripe_layer = Image.composite(stripe_layer, Image.new("L", stripe_layer.size, 0), mask)
red_layer = Image.new("RGBA", stripe_layer.size, RED + (255,))
img.paste(red_layer, (0, 0), stripe_layer)

# outline the path
d.line(path + [path[0]], fill=RED + (255,), width=2 * S)

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT)
print(f"\nwrote {OUT} ({W*S}x{H*S}px, embed at {W/72:.4f} x {H/72:.4f} in @ x=2.4444 y=6.5278)")
