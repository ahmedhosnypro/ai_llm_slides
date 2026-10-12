#!/usr/bin/env python3
"""Sample the frame's actual colors: dominant colors + point samples."""
from PIL import Image
import numpy as np
from collections import Counter
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg"
img = Image.open(SRC).convert("RGB")
A = np.asarray(img).astype(int)
H, W, _ = A.shape

def top_colors(x0, y0, x1, y1, n=8, q=24):
    reg = A[y0:y1, x0:x1]
    # quantize to reduce JPEG noise
    qd = (reg // q) * q
    flat = qd.reshape(-1, 3)
    c = Counter(map(tuple, flat))
    return c.most_common(n)

out = {}
# big pink panel interior — pick clear areas: between elements
out["panel_mid(480,120)"] = top_colors(470, 110, 500, 135)      # between title and boxes
out["panel_topright(760,150)"] = top_colors(750, 140, 800, 165)
out["panel_botleft(90,440)"] = top_colors(80, 430, 130, 455)
# known boxes (from earlier palepink/nearwhite comps):
out["box_384_189_412_386 (scaling col)"] = top_colors(390, 200, 410, 380, 4)
out["box_748_216_831_389 (right zone)"] = top_colors(760, 230, 820, 380, 4)
out["box_75_279_156_382 (left W_k zone)"] = top_colors(80, 290, 150, 375, 5)
out["box_192_455_489_498 (bottom container)"] = top_colors(200, 460, 300, 495, 5)
out["mask_zone(530,220,613,315)"] = top_colors(535, 225, 610, 310, 6)
out["dotprod_zone(604,212,705,367)"] = top_colors(610, 220, 700, 360, 6)
out["sum_zone(542,189,670,210)"] = top_colors(545, 190, 665, 208, 4)
# title
out["title_zone(80,60,500,95)"] = top_colors(80, 60, 500, 95, 6)
# legend top-right
out["legend_zone(700,55,900,95)"] = top_colors(700, 55, 900, 95, 8)
# look-ahead ellipse below mask (~ y 320-360?)
out["below_mask(530,320,640,370)"] = top_colors(530, 320, 640, 370, 6)
# W_q / q2 bottom middle
out["wq_zone(255,415,345,455)"] = top_colors(255, 415, 345, 455, 6)
# bottom-right legend
out["br_legend(700,420,890,510)"] = top_colors(700, 420, 890, 510, 8)
print(json.dumps({k: [[list(c), n] for c, n in v] for k, v in out.items()}, default=str))
