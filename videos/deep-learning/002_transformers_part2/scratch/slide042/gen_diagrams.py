#!/usr/bin/env python3
"""Generate the three cube-diagram PNGs for slide 042 (600-dpi-equivalent, 4x SSAA).

Cube-wall model (measured from slide_042.jpg, see scratch measurements):
  - front faces: flat rects, bright color
  - dark top band per column: parallelogram (BW wide, sheared up-right by Sh over BH)
  - bright gap wedge between consecutive bands (to the column's right edge)
  - painter: rows bottom-up; within a row: bands+gaps strip, then fronts
Right block: 5 such walls staircase-offset (ox, oy) per slab, painter back-to-front.

All coordinates below are FRAME px (960x540, 1px = 1pt frame space). The pptx places
each PNG at slide coords via the fitted mapping (x/0.96055, y/0.95556).
"""
from PIL import Image, ImageDraw
import numpy as np
import json, sys

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets"
SS = 4  # supersample relative to frame px

def poly(d, pts, color):
    d.polygon([(x * SS, y * SS) for x, y in pts], fill=color)

def render_wall(cols, rows, x0, Y0, W, FH, P, BH, BW, Sh, front, band, gap, canvas_w, canvas_h, ox0=0.0, oy0=0.0):
    """Wall whose column c left edge = x0 + c*W (frame px). Rows' front-top Y = Y0 + r*P.
    Draws into a fresh canvas of (canvas_w, canvas_h) frame px with origin offset."""
    img = Image.new("RGB", (int(canvas_w * SS), int(canvas_h * SS)), (255, 255, 255))
    d = ImageDraw.Draw(img)
    for r in range(rows - 1, -1, -1):  # bottom-up
        Y = Y0 + r * P
        # bands + gaps strip
        for c in range(cols):
            xc = x0 + c * W
            # dark band parallelogram
            poly(d, [(xc, Y), (xc + BW, Y), (xc + BW + Sh, Y - BH), (xc + Sh, Y - BH)], band)
            # bright gap wedge from band right edge to column right edge, sheared
            if W - BW > 0.5:
                poly(d, [(xc + BW, Y), (xc + W, Y), (xc + W + Sh, Y - BH), (xc + BW + Sh, Y - BH)], gap)
        # fronts
        for c in range(cols):
            xc = x0 + c * W
            d.rectangle([xc * SS, Y * SS, (xc + W) * SS, (Y + FH) * SS], fill=front)
    return img

# ---------------- LEFT STACK: 1 col x 5 rows, big cubes ----------------
# measured: x0=168, front-top Y0=278, W=42, FH=26, P=30.5, BH=15, BW=26, Sh=14
# NOTE: left stack ink ends at x~210 (nothing beyond 213) -> canvas clipped there
L = dict(x0=168, Y0=278, W=42, FH=26, P=30.5, BH=15, BW=26, Sh=14,
         front=(90, 192, 5), band=(44, 95, 3), gap=(120, 235, 15))
lw = 210 - 168 + 1   # canvas width clipped at the column's right edge
lh = int(262, ) if False else None
l_top = 262; l_bot = 429
img_l = Image.new("RGB", (lw * SS, (l_bot - l_top) * SS), (255, 255, 255))
d = ImageDraw.Draw(img_l)
def lpol(pts, color): d.polygon([((x - 168) * SS, (y - l_top) * SS) for x, y in pts], fill=color)
for r in range(4, -1, -1):
    Y = L["Y0"] + r * L["P"]
    lpol([(168, Y), (194, Y), (208, Y - 15), (182, Y - 15)], L["band"])
    lpol([(194, Y), (210, Y), (210, Y - 15), (208, Y - 15)], L["gap"])
    d.rectangle([0, (Y - l_top) * SS, lw * SS, (Y + 26 - l_top) * SS], fill=L["front"])
img_l = img_l.resize((lw * 600 // 72, (l_bot - l_top) * 600 // 72), Image.LANCZOS)
img_l.save(f"{OUT}/s042_left_stack.png")

# ---------------- MIDDLE GRID: 4 cols x 5 rows ----------------
M = dict(x0=379, Y0=270, W=31, FH=24, P=31, BH=15, BW=26, Sh=14,
         front=(90, 192, 5), band=(43, 97, 2), gap=(140, 255, 20))
m_left = 379; m_right = 517; m_top = 254; m_bot = 419
img_m = render_wall(4, 5, M["x0"], M["Y0"], M["W"], M["FH"], M["P"], M["BH"], M["BW"], M["Sh"],
                    M["front"], M["band"], M["gap"], m_right - m_left, m_bot - m_top)
img_m = img_m.resize(((m_right - m_left) * 600 // 72, (m_bot - m_top) * 600 // 72), Image.LANCZOS)
img_m.save(f"{OUT}/s042_mid_grid.png")

# ---------------- RIGHT BLOCK: 5 slabs (walls), staircase ----------------
# magenta wall: x0=653, Y0=317, rows: front tops 317/348/380/411/442 (P=31.25), FH=27
# per-slab colors (front, band, gap) measured medians
SLABS = [  # front -> back
    dict(name="magenta", front=(158, 0, 164), band=(79, 0, 82), gap=(196, 0, 205)),
    dict(name="green",   front=(133, 255, 13), band=(87, 100, 18), gap=(160, 255, 60)),
    dict(name="orange",  front=(236, 122, 7), band=(112, 58, 10), gap=(248, 150, 40)),
    dict(name="yellow",  front=(250, 255, 13), band=(191, 200, 11), gap=(255, 255, 90)),
    dict(name="blue",    front=(94, 125, 157), band=(41, 55, 64), gap=(130, 165, 195)),
]
RW, FH_R, P_R, BH_R, BW_R, Sh_R = 31, 27, 31.25, 15, 26, 14

def render_block(ox, oy, x0, Y0):
    cw = int(4 * ox + 124 + Sh_R + 30); ch = int(4 * -oy + BH_R + 4 * P_R + FH_R + 10)
    img = Image.new("RGB", (cw * SS, ch * SS), (255, 255, 255))
    d = ImageDraw.Draw(img)
    # canvas origin in frame space:
    cx0 = x0 - 10; cy0 = Y0 + 4 * oy - BH_R - 6
    for k in range(4, -1, -1):  # back (blue) -> front (magenta)
        s = SLABS[k]
        wx = x0 + k * ox; wy = Y0 + k * oy
        for r in range(4, -1, -1):
            Y = wy + r * P_R
            for c in range(4):
                xc = wx + c * RW
                poly(d, [(xc - cx0, Y - cy0), (xc + BW_R - cx0, Y - cy0),
                         (xc + BW_R + Sh_R - cx0, Y - BH_R - cy0), (xc + Sh_R - cx0, Y - BH_R - cy0)], s["band"])
                poly(d, [(xc + BW_R - cx0, Y - cy0), (xc + RW - cx0, Y - cy0),
                         (xc + RW + Sh_R - cx0, Y - BH_R - cy0), (xc + BW_R + Sh_R - cx0, Y - BH_R - cy0)], s["gap"])
            for c in range(4):
                xc = wx + c * RW
                d.rectangle([(xc - cx0) * SS, (Y - cy0) * SS, (xc + RW - cx0) * SS, (Y + FH_R - cy0) * SS],
                            fill=s["front"])
    return img, cx0, cy0

# fit (ox, oy, x0, Y0) against the original crop
orig = Image.open(FR).convert("RGB")
A = np.asarray(orig).astype(int)

def classify(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    out = np.zeros(a.shape[:2], dtype=np.uint8)  # 0 white 1 M 2 G 3 O 4 Y 5 B/b 6 K 7 other
    out += 0
    m = (r > 235) & (g > 235) & (b > 230); out[m] = 0
    m = (r > 100) & (b > 100) & (g < 110); out[m] = 1
    m = (g > 140) & (g - r > 30) & (out == 0); out[m] = 2
    m = (g > 60) & (g - r > 10) & (g - b > 20) & (out == 0); out[m] = 2
    m = (r > 150) & (g > 60) & (g < 190) & (b < 100) & (out == 0); out[m] = 3
    m = (r > 170) & (g > 170) & (b < 140) & (out == 0); out[m] = 4
    m = (b > 80) & (b - r > 5) & (out == 0); out[m] = 5
    m = (r < 110) & (g < 110) & (b < 110) & (out == 0); out[m] = 6
    m = (out == 0); out[m] = 7
    return out

def loss(params):
    ox, oy, x0, Y0 = params
    img, cx0, cy0 = render_block(ox, oy, x0, Y0)
    B = np.asarray(img.resize((img.width // SS, img.height // SS), Image.LANCZOS)).astype(int)
    # map onto the frame region
    x0f, y0f = int(cx0), int(cy0)
    h, w = B.shape[:2]
    region = A[y0f:y0f + h, x0f:x0f + w]
    if region.shape[0] != h or region.shape[1] != w:
        return 1e9
    ca, cb = classify(region), classify(B)
    return float((ca != cb).sum())

best = None
for ox in range(14, 27, 2):
    for oy in range(-26, -9, 2):
        for x0 in (651, 653, 655):
            for Y0 in (315, 317, 319):
                l = loss((ox, oy, x0, Y0))
                if best is None or l < best[0]:
                    best = (l, ox, oy, x0, Y0)
print("coarse best:", best)
l0, ox, oy, x0, Y0 = best
for d_ox in (-1, 0, 1):
    for d_oy in (-1, 0, 1):
        for dx0 in (-1, 0, 1):
            for dY0 in (-1, 0, 1):
                l = loss((ox + d_ox, oy + d_oy, x0 + dx0, Y0 + dY0))
                if l < best[0]:
                    best = (l, ox + d_ox, oy + d_oy, x0 + dx0, Y0 + dY0)
print("fine best:", best)
_, ox, oy, x0, Y0 = best
img, cx0, cy0 = render_block(ox, oy, x0, Y0)
bw = img.width // SS; bh = img.height // SS
img = img.resize((bw * 600 // 72, bh * 600 // 72), Image.LANCZOS)
img.save(f"{OUT}/s042_right_block.png")
meta = dict(ox=ox, oy=oy, x0=x0, Y0=Y0, canvas_frame_origin=[cx0, cy0],
            canvas_frame_size=[bw, bh],
            slide_rect=[(cx0 - 18.66) / 0.96055, cy0 / 0.95556, bw / 0.96055, bh / 0.95556])
print(json.dumps(meta, indent=1))
with open(f"{OUT}/s042_right_block_meta.json", "w") as f:
    json.dump(meta, f, indent=1)
with open(f"{OUT}/s042_left_meta.json", "w") as f:
    json.dump(dict(canvas_frame_origin=[168, l_top], canvas_frame_size=[lw, l_bot - l_top],
                   slide_rect=[(168 - 18.66) / 0.96055, l_top / 0.95556, lw / 0.96055, (l_bot - l_top) / 0.95556]), f, indent=1)
with open(f"{OUT}/s042_mid_meta.json", "w") as f:
    json.dump(dict(canvas_frame_origin=[m_left, m_top], canvas_frame_size=[m_right - m_left, m_bot - m_top],
                   slide_rect=[(m_left - 18.66) / 0.96055, m_top / 0.95556, (m_right - m_left) / 0.96055, (m_bot - m_top) / 0.95556]), f, indent=1)
print("PNGs written")
