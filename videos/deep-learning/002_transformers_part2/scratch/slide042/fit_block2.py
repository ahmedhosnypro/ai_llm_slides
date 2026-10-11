#!/usr/bin/env python3
"""Right-block fit v2 with a CORRECT class-map loss.
Render class map is built directly from the drawn shapes (no color classification).
Original is classified with a fixed-precedence mask chain; '?' (arrows/text/jpeg mush)
is IGNORED in the loss. Grid search + coordinate refine over (ox, oy, x0, Y0).
"""
from PIL import Image, ImageDraw
import numpy as np
import json

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
SS = 4
RW, FH_R, P_R, BH_R, BW_R, Sh_R = 31, 27, 31.25, 15, 26, 14
# class codes: 0 white, 1 magenta, 2 green-bright, 3 green-dark, 4 orange, 5 yellow, 6 blue, 7 dark, 8 other
SLABS = [  # front -> back
    dict(front=(158, 0, 164), band=(79, 0, 82), gap=(196, 0, 205), cf=1, cb=7, cg=1),
    dict(front=(133, 255, 13), band=(87, 100, 18), gap=(160, 255, 60), cf=2, cb=3, cg=2),
    dict(front=(236, 122, 7), band=(112, 58, 10), gap=(248, 150, 40), cf=4, cb=7, cg=4),
    dict(front=(250, 255, 13), band=(191, 200, 11), gap=(255, 255, 90), cf=5, cb=5, cg=5),
    dict(front=(94, 125, 157), band=(41, 55, 64), gap=(130, 165, 195), cf=6, cb=7, cg=6),
]

def render_block(ox, oy, x0, Y0, want_image=False):
    cw = int(4 * ox + 124 + Sh_R + 40); ch = int(-4 * oy + BH_R + 4 * P_R + FH_R + 14)
    img = Image.new("RGB", (cw * SS, ch * SS), (255, 255, 255))
    cls = np.full((ch, cw), 0, dtype=np.uint8)
    d = ImageDraw.Draw(img)
    cx0 = x0 - 12; cy0 = Y0 + 4 * oy - BH_R - 8
    def P(pts, color, code):
        d.polygon([((x - cx0) * SS, (y - cy0) * SS) for x, y in pts], fill=color)
        import PIL.ImageDraw as ID
        mask = Image.new("L", (cw * SS, ch * SS), 0)
        md = ID.Draw(mask)
        md.polygon([((x - cx0) * SS, (y - cy0) * SS) for x, y in pts], fill=255)
        m = np.asarray(mask.resize((cw, ch), Image.NEAREST)) > 0
        cls[m] = code
    for k in range(4, -1, -1):
        s = SLABS[k]
        wx = x0 + k * ox; wy = Y0 + k * oy
        for r in range(4, -1, -1):
            Y = wy + r * P_R
            for c in range(4):
                xc = wx + c * RW
                P([(xc, Y), (xc + BW_R, Y), (xc + BW_R + Sh_R, Y - BH_R), (xc + Sh_R, Y - BH_R)], s["band"], s["cb"])
                P([(xc + BW_R, Y), (xc + RW, Y), (xc + RW + Sh_R, Y - BH_R), (xc + BW_R + Sh_R, Y - BH_R)], s["gap"], s["cg"])
            for c in range(4):
                xc = wx + c * RW
                P([(xc, Y), (xc + RW, Y), (xc + RW, Y + FH_R), (xc, Y + FH_R)], s["front"], s["cf"])
    if want_image:
        return img, cls, cx0, cy0
    return cls, cx0, cy0

orig = Image.open(FR).convert("RGB")
A = np.asarray(orig).astype(int)

def classify_orig(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    out = np.full(a.shape[:2], 8, dtype=np.uint8)
    m = (r > 235) & (g > 235) & (b > 230); out[m] = 0
    m = (r > 95) & (b > 95) & (g < 115) & (r - g > 40); out[m] = 1
    m = (g > 140) & (g - r > 30) & (g - b > 60); out[m] = 2
    m = (g > 55) & (g - r > 8) & (g - b > 15); out[m] = 3
    m = (r > 135) & (g > 45) & (g < 195) & (b < 95) & (r - g > 30); out[m] = 4
    m = (r > 165) & (g > 165) & (b < 145); out[m] = 5
    m = (b > 75) & (b - r > 8); out[m] = 6
    m = (r < 115) & (g < 115) & (b < 115); out[m] = 7
    return out

def loss(params, ret_maps=False):
    ox, oy, x0, Y0 = params
    try:
        cls, cx0, cy0 = render_block(ox, oy, x0, Y0)
    except Exception:
        return 1e9
    h, w = cls.shape
    x0f, y0f = int(round(cx0)), int(round(cy0))
    region = A[y0f:y0f + h, x0f:x0f + w]
    if region.shape[:2] != (h, w): return 1e9
    co = classify_orig(region)
    ignore = (co == 8)
    dis = (co != cls) & (~ignore)
    if ret_maps: return dis, co, cls, (x0f, y0f)
    return int(dis.sum())

best = None
import itertools
for ox in range(14, 27, 1):
    for oy in range(-22, -7, 1):
        for x0 in (650, 652, 654, 656, 658):
            for Y0 in (314, 316, 318, 320):
                l = loss((ox, oy, x0, Y0))
                if best is None or l < best[0]: best = (l, ox, oy, x0, Y0)
print("coarse best:", best)
improved = True
while improved:
    improved = False
    l0, ox, oy, x0, Y0 = best
    for d in itertools.product((-1, 0, 1), repeat=4):
        if d == (0, 0, 0, 0): continue
        l = loss((ox + d[0], oy + d[1], x0 + d[2], Y0 + d[3]))
        if l < best[0]:
            best = (l, ox + d[0], oy + d[1], x0 + d[2], Y0 + d[3]); improved = True
print("refined best:", best)

l, ox, oy, x0, Y0 = best
dis, co, cls, (x0f, y0f) = loss((ox, oy, x0, Y0), ret_maps=True)
tot = (~dis).sum() + dis.sum()
print(f"disagreement {dis.sum()} / {tot} ({100.0*dis.sum()/tot:.2f}%) of non-ignored pixels")
img, _, cx0, cy0 = render_block(ox, oy, x0, Y0, want_image=True)
bw = img.width // SS; bh = img.height // SS
img.resize((bw * 600 // 72, bh * 600 // 72), Image.LANCZOS).save(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/s042_right_block.png")
meta = dict(ox=ox, oy=oy, x0=x0, Y0=Y0, canvas_frame_origin=[cx0, cy0], canvas_frame_size=[bw, bh],
            slide_rect=[(cx0 - 18.66) / 0.96055, cy0 / 0.95556, bw / 0.96055, bh / 0.95556])
print(json.dumps(meta, indent=1))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/s042_right_block_meta.json", "w") as f:
    json.dump(meta, f, indent=1)

# diagnostic side-by-side (2px step)
CH = ".MGgoOYBDK?"
# co: 0 white 1 magenta 2 green-b 3 green-d 4 orange 5 yellow 6 blue 7 dark 8 other
CH = ".MGgOYBDK?"
h, w = co.shape
print("ORIG:")
print("     " + "".join(str((x0f + i * 2) % 10) for i in range(0, w, 2)))
for yy in range(0, h, 2):
    print(f"{y0f+yy:4d} " + "".join(CH[co[yy, xx]] for xx in range(0, w, 2)))
print("RENDER:")
for yy in range(0, h, 2):
    print(f"{y0f+yy:4d} " + "".join(CH[cls[yy, xx]] for xx in range(0, w, 2)))
