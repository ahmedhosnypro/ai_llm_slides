#!/usr/bin/env python3
"""FINAL diagram generator for slide 042 (universal measured cube-wall model).

Wall model (per column c, left edge xc, width W, main-width MW):
  front row band:  main rect [xc, Y, xc+MW, Y+FH] + bright rect [xc+MW, Y, xc+W, Y+FH]
  top band strip:  dark parallelogram [(xc,Y),(xc+MW,Y),(xc+MW+Sh,Y-BH),(xc+Sh,Y-BH)]
                   + bright parallelogram [(xc+MW,Y),(xc+W,Y),(xc+W+Sh,Y-BH),(xc+MW+Sh,Y-BH)]
  painter: rows bottom-up (upper rows' fronts hide lower rows' band tops)
Right block: 5 walls at measured per-slab x0 = [655,678,697,713,725], Y0 = 318 - 17k,
  painter back-to-front (blue first, magenta last).
"""
from PIL import Image, ImageDraw
import numpy as np
import json

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets"
SS = 4

def wall(draw, x0, Y0, cols, rows, W, MW, FH, P, BH, Sh, main, bright, band):
    for r in range(rows - 1, -1, -1):
        Y = Y0 + r * P
        for c in range(cols):
            xc = x0 + c * W
            draw.polygon([(xc, Y), ((xc + MW), Y),
                          ((xc + MW + Sh), (Y - BH)), ((xc + Sh), (Y - BH))],
                         fill=band)
            draw.polygon([((xc + MW), Y), ((xc + W), Y),
                          ((xc + W + Sh), (Y - BH)), ((xc + MW + Sh), (Y - BH))],
                         fill=bright)
        for c in range(cols):
            xc = x0 + c * W
            draw.rectangle([xc, Y, (xc + MW), (Y + FH)], fill=main)
            draw.rectangle([(xc + MW), Y, (xc + W), (Y + FH)], fill=bright)

GREEN = dict(main=(88, 192, 6), bright=(137, 255, 12), band=(44, 96, 2))

# ---- LEFT STACK: 1x5, W=42, MW=26, FH=26, P=30.5, BH=15, Sh=14; frame bbox x168..211,y262..429
lw, lh = 211 - 168, 429 - 262
img = Image.new("RGB", (lw * SS, lh * SS), (255, 255, 255))
d = ImageDraw.Draw(img)
class Off:
    def __init__(s, dx, dy): s.dx, s.dy = dx, dy
    def polygon(s, pts, **k): d.polygon([((x - s.dx) * SS, (y - s.dy) * SS) for x, y in pts], **k)
    def rectangle(s, box, **k): d.rectangle([(box[0] - s.dx) * SS, (box[1] - s.dy) * SS,
                                             (box[2] - s.dx) * SS, (box[3] - s.dy) * SS], **k)
o = Off(168, 262)
wall(o, 168, 278, 1, 5, 42, 26, 26, 30.5, 15, 14, **GREEN)
img.resize((lw * 600 // 72, lh * 600 // 72), Image.LANCZOS).save(f"{OUT}/s042_left_stack.png")
json.dump(dict(frame_origin=[168, 262], frame_size=[lw, lh],
               slide=[(168 - 18.66) / 0.96055, 262 / 0.95556, lw / 0.96055, lh / 0.95556]),
          open(f"{OUT}/s042_left_meta.json", "w"))

# ---- MIDDLE GRID: 4x5, W=31, MW=26, FH=24, P=31, BH=15, Sh=14; frame bbox x379..518,y254..419
mw_, mh = 518 - 379, 419 - 254
img = Image.new("RGB", (mw_ * SS, mh * SS), (255, 255, 255))
d = ImageDraw.Draw(img)
o = Off(379, 254)
wall(o, 379, 270, 4, 5, 31, 26, 24, 31, 15, 14, **GREEN)
img.resize((mw_ * 600 // 72, mh * 600 // 72), Image.LANCZOS).save(f"{OUT}/s042_mid_grid.png")
json.dump(dict(frame_origin=[379, 254], frame_size=[mw_, mh],
               slide=[(379 - 18.66) / 0.96055, 254 / 0.95556, mw_ / 0.96055, mh / 0.95556]),
          open(f"{OUT}/s042_mid_meta.json", "w"))

# ---- RIGHT BLOCK: 5 walls, per-slab x0, Y0 = 318-17k
SLABS = [
    dict(main=(158, 0, 164), bright=(221, 0, 234), band=(84, 0, 91)),    # magenta (front)
    dict(main=(133, 255, 10), bright=(170, 255, 70), band=(85, 93, 5)),  # green
    dict(main=(234, 122, 10), bright=(250, 165, 60), band=(105, 50, 6)), # orange
    dict(main=(250, 255, 13), bright=(255, 255, 100), band=(135, 145, 6)),  # yellow
    dict(main=(94, 125, 157), bright=(150, 180, 205), band=(41, 55, 64)),   # blue (back)
]
X0S = [655, 678, 697, 713, 725]
Y0S = [318 - 17 * k for k in range(5)]
RW, MW_R, FH_R, P_R, BH_R, Sh_R = 31, 24, 27, 31.25, 15, 14
bx0, by0 = 640, 228  # canvas origin (frame px)
bw_, bh_ = 876 - bx0, 478 - by0
img = Image.new("RGB", (bw_ * SS, bh_ * SS), (255, 255, 255))
d = ImageDraw.Draw(img)
o = Off(bx0, by0)
for k in range(4, -1, -1):
    wall(o, X0S[k], Y0S[k], 4, 5, RW, MW_R, FH_R, P_R, BH_R, Sh_R, **SLABS[k])
img.resize((bw_ * 600 // 72, bh_ * 600 // 72), Image.LANCZOS).save(f"{OUT}/s042_right_block.png")
json.dump(dict(frame_origin=[bx0, by0], frame_size=[bw_, bh_], slab_x0=X0S, slab_Y0=Y0S,
               slide=[(bx0 - 18.66) / 0.96055, by0 / 0.95556, bw_ / 0.96055, bh_ / 0.95556]),
          open(f"{OUT}/s042_right_meta.json", "w"))
print("final PNGs written")

# quick class-agreement stats for the right block
orig = np.asarray(Image.open(FR).convert("RGB")).astype(int)
ren = np.asarray(Image.open(f"{OUT}/s042_right_block.png").resize((bw_, bh_), Image.LANCZOS)).astype(int)
reg = orig[by0:by0 + bh_, bx0:bx0 + bw_]
def cls3(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    out = np.full(a.shape[:2], 8, np.uint8)
    m = (r > 235) & (g > 235) & (b > 230); out[m] = 0
    m = (r > 95) & (b > 95) & (g < 115) & (r - g > 40); out[m] = 1
    m = (g > 140) & (g - r > 30) & (g - b > 60); out[m] = 2
    m = (g > 55) & (g - r > 8) & (g - b > 15); out[m] = 2
    m = (r > 135) & (g > 45) & (g < 195) & (b < 95) & (r - g > 30); out[m] = 3
    m = (r > 165) & (g > 165) & (b < 145); out[m] = 4
    m = (b > 75) & (b - r > 8); out[m] = 5
    m = (r < 115) & (g < 115) & (b < 115); out[m] = 6
    m = (r > 110) & (r - g > 45) & (r - b > 45) & (g < 130); out[m] = 8
    return out
ca, cb = cls3(reg), cls3(ren)
v = (ca != 8)
dis = (ca != cb) & v
print(f"right block class agreement: {100*(1 - dis.sum()/v.sum()):.1f}% ({dis.sum()}/{v.sum()})")
