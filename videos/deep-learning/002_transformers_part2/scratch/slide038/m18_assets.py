#!/usr/bin/env python3
"""Slide 038 — generate diagram PNG assets: spiral-hatched navy block arrow + orange
residual curve. Drawn at 10 px/pt (720 dpi-equivalent), placed at exact pt/72 sizes."""
from PIL import Image, ImageDraw
import math

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/"
S = 10  # px per pt

# ---------------- 1. navy outlined UP block-arrow with spiral hatching ----------------
# Placed size: 10.5pt x 20pt  -> canvas 105x200 pt *10 = 1050x2000?? too big; use 4 px/pt.
S = 4
W, H = int(10.5 * S), int(20 * S)
im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
NAVY = (0, 0, 150, 255)  # 000096-ish outline (0000CC washed per frame reads)
lw = max(2, int(0.9 * S))
# head: triangle tip top-center; shaft below
tip = (W / 2, 1)
hb_l, hb_r = (0.6 * S, 0.52 * H)      # head base y = 52% height
sh_l, sh_r = (W * 0.33, W * 0.67)     # shaft width ~34%
poly = [
    (W / 2, 1), (hb_r, hb_y := 0.52 * H), (sh_r, hb_y),
    (sh_r, H - 1), (sh_l, H - 1), (sh_l, hb_y), (hb_l, hb_y),
]
d.polygon(poly, fill=(255, 255, 255, 255), outline=NAVY, width=lw)
# spiral (Archimedean) inside the shaft
cx, cy = W / 2, (hb_y + H) / 2
rmax = min(sh_r - sh_l, H - hb_y) / 2 - 1.2 * S
pts = []
for i in range(0, 260):
    t = i / 260 * 2.6 * 2 * math.pi
    r = rmax * (i / 260)
    pts.append((cx + r * math.cos(t), cy + r * math.sin(t) * 0.9))
d.line(pts, fill=NAVY, width=max(2, int(0.55 * S)), joint="curve")
im.save(OUT + "s038_blkarrow.png")
print("s038_blkarrow.png", im.size)

# ---------------- 2. orange curved residual arrow (per column) ----------------
# Canvas in slide-pt space: x from (cx-52) to (cx+2) -> w 54pt; y 351..500 -> h 149pt
S = 6
w_pt, h_pt = 54.0, 149.0
W, H = int(w_pt * S), int(h_pt * S)
im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
ORANGE = (227, 108, 9, 255)  # E36C09
lw = max(3, int(1.4 * S))
# measured path (rel pt; canvas origin = (cx-52, y351)):
# (17.4,147.1) start -> (1.0,79) -> (1.0,55) -> (7.4,38.3) -> (14.7,21.6)
#  -> (22.0,13.2) -> (29.8,9.0) -> (35.6,4.8) -> tip (50.1,1.5)
import numpy as np
P = [(17.4, 147.1), (8.4, 134.6), (1.0, 110.0), (1.0, 79.0), (1.0, 55.0),
     (7.4, 38.3), (14.7, 21.6), (22.0, 13.2), (29.8, 9.0), (35.6, 4.8), (46.0, 2.2)]
# Catmull-Rom smoothing
def cr(points, n=24):
    pts = [points[0]] + points + [points[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = (np.array(pts[j], float) for j in (i - 1, i, i, i + 1)), None, None, None
        p0 = np.array(pts[i - 1], float); p1 = np.array(pts[i], float)
        p2 = np.array(pts[i + 1], float); p3 = np.array(pts[i + 2], float)
        for t in np.linspace(0, 1, n):
            t2, t3 = t * t, t * t * t
            pt = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)
            out.append(pt)
    out.append(np.array(points[-1], float))
    return out
smooth = cr(P)
px = [(x * S, y * S) for x, y in smooth]
d.line(px, fill=ORANGE, width=lw, joint="curve")
# arrowhead at the end: direction from last two smoothed points
import math
(x1, y1), (x2, y2) = px[-3], px[-1]
ang = math.atan2(y2 - y1, x2 - x1)
hlen, hwid = 5.2 * S, 3.4 * S
tip = (x2 + 0.8 * S, y2)
b1 = (tip[0] - hlen * math.cos(ang - 0.45), tip[1] - hlen * math.sin(ang - 0.45))
b2 = (tip[0] - hlen * math.cos(ang + 0.45), tip[1] - hlen * math.sin(ang + 0.45))
d.polygon([tip, b1, b2], fill=ORANGE)
im.save(OUT + "s038_orangearrow.png")
print("s038_orangearrow.png", im.size)
