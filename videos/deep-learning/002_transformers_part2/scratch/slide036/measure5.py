#!/usr/bin/env python3
"""Stage 5: resolve diagram panel border, box colors, arrow geometry, color cores; dump crops."""
import numpy as np
from PIL import Image

FRAME = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_036.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide036"
im = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 110) & (g < 110) & (b < 110)

# diagram panel red border: horizontal lines
for y in (346, 347, 348, 349, 510, 511, 512):
    cols = np.where(red[y])[0]
    if len(cols):
        print(f"red row {y}: x {cols.min()}..{cols.max()} n={len(cols)}")
for x in (64, 65, 66, 67, 890, 891, 892, 893):
    rows = np.where(red[340:515, x])[0] + 340
    if len(rows):
        print(f"red col {x}: y {rows.min()}..{rows.max()} n={len(rows)}")

# where are pale-yellow and pink pixels?
py = (r > 235) & (g > 235) & (b > 110) & (b < 200)
ys, xs = np.where(py)
print("pale-yellow bbox: x", xs.min(), "..", xs.max(), " y", ys.min(), "..", ys.max(), "n=", len(ys))
# histogram by row band
import collections
cnt = collections.Counter((ys // 20) * 20)
print("  pale-yellow row bands:", sorted(cnt.items()))
pk = (r > 220) & (g < 210) & (b < 215) & (r - g > 40) & (r - b > 25)
ys, xs = np.where(pk)
print("pinkish bbox: x", xs.min(), "..", xs.max(), " y", ys.min(), "..", ys.max(), "n=", len(ys))
cnt = collections.Counter((ys // 20) * 20)
print("  pinkish row bands:", sorted(cnt.items()))

# box anatomy: 2D map of box 3 (x 321..359) rows 340..400 — print colored-class grid
def cls(px):
    rr, gg, bb = px
    if rr > 240 and gg > 240 and bb > 240: return "."
    if rr > 225 and gg > 235 and bb < 235 and bb > 195: return "g"  # pale green
    if rr > 235 and gg > 235 and 110 < bb < 210: return "y"        # pale yellow
    if rr > 200 and gg < 215 and bb < 215 and rr-gg > 30: return "p"  # pink
    if rr > 110 and gg < 110 and bb < 110: return "R"              # red
    if bb > 100 and rr < 110 and gg < 110: return "B"              # blue
    return "?"
print("\nbox3 Y col grid (x 318..362, y 340..400):")
for y in range(340, 400):
    print(f"{y:3d} " + "".join(cls(im[y, x]) for x in range(318, 363, 1)))
print("\nbox3 X col grid (x 318..362, y 455..490):")
for y in range(455, 490):
    print(f"{y:3d} " + "".join(cls(im[y, x]) for x in range(318, 363, 1)))

# arrow 2 anatomy: x 268..290, y 443..465
print("\narrow grid (x 268..292, y 442..466):")
for y in range(442, 466):
    print(f"{y:3d} " + "".join(cls(im[y, x]) for x in range(268, 293, 1)))

# color cores: banner fill (large patch), panel border, panel fill, green dot, blue dot, arrow outline
print("\ncores:")
print("banner fill:", np.median(im[398:412, 300:500].reshape(-1,3), axis=0))
print("panel border row 110:", np.median(im[109:112, 300:600].reshape(-1,3), axis=0))
print("panel fill:", np.median(im[170:190, 400:600].reshape(-1,3), axis=0))
print("Y box green cell:", np.median(im[363:373, 330:352].reshape(-1,3), axis=0))
print("X box green cell:", np.median(im[466:476, 330:352].reshape(-1,3), axis=0))
print("blue dot:", np.median(im[366:370, 627:631].reshape(-1,3), axis=0))
print("green dot:", np.median(im[469:472, 627:631].reshape(-1,3), axis=0))

# ---- crops for vision zoom ----
def crop(x0, y0, x1, y1, scale, name):
    c = Image.open(FRAME).convert("RGB").crop((x0, y0, x1, y1))
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    c.save(f"{OUT}/{name}.png")
    print("saved", name, c.size)

crop(168, 336, 222, 400, 6, "crop_ybox1")          # Y box 1 anatomy + label
crop(168, 455, 222, 488, 6, "crop_xbox1")          # X box 1 anatomy + label
crop(530, 336, 850, 400, 3, "crop_ytail")          # Y boxes 6..8 + dots + labels
crop(530, 455, 850, 490, 3, "crop_xtail")          # X tail
crop(93, 106, 867, 338, 2, "crop_panel")           # info panel full text
crop(58, 340, 178, 400, 5, "crop_gut_up")          # upper gutter label
crop(58, 435, 178, 505, 5, "crop_gut_dn")          # lower gutter label
crop(280, 482, 585, 508, 4, "crop_caption")        # caption
crop(160, 388, 890, 450, 2, "crop_banner")         # banner text
crop(262, 440, 300, 468, 8, "crop_arrow")          # arrow 2 shape
crop(296, 70, 722, 106, 3, "crop_title")           # title
