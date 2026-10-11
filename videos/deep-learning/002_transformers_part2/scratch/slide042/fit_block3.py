#!/usr/bin/env python3
"""Right-block fit v3: FIXED evaluation window (x628..881, y222..483 frame px),
render block into the window, class-map disagreement vs original; red (arrows,
labels) and unclassifiable pixels ignored. Grid + coordinate refine."""
from PIL import Image, ImageDraw
import numpy as np
import json, itertools

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
SS = 4
RW, FH_R, P_R, BH_R, BW_R, Sh_R = 31, 27, 31.25, 15, 26, 14
WX0, WY0, WW, WH = 628, 222, 254, 262
SLABS = [  # front -> back; codes: 1 magenta 2 green-b 3 green-d 4 orange 5 yellow 6 blue 7 dark
    dict(front=(158, 0, 164), band=(79, 0, 82), gap=(196, 0, 205), cf=1, cb=7, cg=1),
    dict(front=(133, 255, 13), band=(87, 100, 18), gap=(160, 255, 60), cf=2, cb=3, cg=2),
    dict(front=(236, 122, 7), band=(112, 58, 10), gap=(248, 150, 40), cf=4, cb=7, cg=4),
    dict(front=(250, 255, 13), band=(191, 200, 11), gap=(255, 255, 90), cf=5, cb=5, cg=5),
    dict(front=(94, 125, 157), band=(41, 55, 64), gap=(130, 165, 195), cf=6, cb=7, cg=6),
]

def render_block(ox, oy, x0, Y0, want_image=False):
    img = Image.new("RGB", (WW * SS, WH * SS), (255, 255, 255))
    cls = np.zeros((WH, WW), dtype=np.uint8)
    d = ImageDraw.Draw(img)
    def P(pts, color, code):
        d.polygon([((x - WX0) * SS, (y - WY0) * SS) for x, y in pts], fill=color)
        mask = Image.new("L", (WW * SS, WH * SS), 0)
        md = ImageDraw.Draw(mask)
        md.polygon([((x - WX0) * SS, (y - WY0) * SS) for x, y in pts], fill=255)
        m = np.asarray(mask.resize((WW, WH), Image.NEAREST)) > 0
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
        return img, cls
    return cls

orig = Image.open(FR).convert("RGB")
A = np.asarray(orig).astype(int)
REG = A[WY0:WY0 + WH, WX0:WX0 + WW]

def classify_orig(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    out = np.full(a.shape[:2], 8, dtype=np.uint8)  # 8 = other/ignore
    m = (r > 235) & (g > 235) & (b > 230); out[m] = 0
    m = (r > 95) & (b > 95) & (g < 115) & (r - g > 40); out[m] = 1
    m = (g > 140) & (g - r > 30) & (g - b > 60); out[m] = 2
    m = (g > 55) & (g - r > 8) & (g - b > 15); out[m] = 3
    m = (r > 135) & (g > 45) & (g < 195) & (b < 95) & (r - g > 30); out[m] = 4
    m = (r > 165) & (g > 165) & (b < 145); out[m] = 5
    m = (b > 75) & (b - r > 8); out[m] = 6
    m = (r < 115) & (g < 115) & (b < 115); out[m] = 7
    m = (r > 110) & (r - g > 45) & (r - b > 45) & (g < 130); out[m] = 9  # red arrows/labels -> ignore
    return out

CO = classify_orig(REG)
IGNORE = (CO == 8) | (CO == 9)
VALID = ~IGNORE
print(f"window {WW}x{WH}; ignored {(IGNORE).sum()}, valid {VALID.sum()}")

def loss(params):
    ox, oy, x0, Y0 = params
    if not (-30 <= oy <= -4) or not (10 <= ox <= 30): return 10**9
    cls = render_block(ox, oy, x0, Y0)
    return int(((CO != cls) & VALID).sum())

best = None
for ox in range(12, 29, 1):
    for oy in range(-22, -5, 1):
        for x0 in (648, 650, 652, 654, 656, 658):
            for Y0 in (312, 314, 316, 318, 320, 322):
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
dis = ((CO != render_block(ox, oy, x0, Y0)) & VALID)
print(f"FINAL disagreement {dis.sum()} / {VALID.sum()} ({100.0*dis.sum()/VALID.sum():.2f}%)")
img, _ = render_block(ox, oy, x0, Y0, want_image=True)
img.resize((WW * 600 // 72, WH * 600 // 72), Image.LANCZOS).save(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/s042_right_block.png")
meta = dict(ox=ox, oy=oy, x0=x0, Y0=Y0, window=[WX0, WY0, WW, WH],
            slide_rect=[(WX0 - 18.66) / 0.96055, WY0 / 0.95556, WW / 0.96055, WH / 0.95556])
print(json.dumps(meta, indent=1))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/s042_right_block_meta.json", "w") as f:
    json.dump(meta, f, indent=1)

CH = ".MGgOYBDKR"
cls = render_block(ox, oy, x0, Y0)
print("ORIG (window, 2px):")
print("     " + "".join(str((WX0 + i * 2) % 10) for i in range(0, WW, 2)))
for yy in range(0, WH, 2):
    print(f"{WY0+yy:4d} " + "".join(CH[CO[yy, xx]] for xx in range(0, WW, 2)))
print("RENDER:")
for yy in range(0, WH, 2):
    print(f"{WY0+yy:4d} " + "".join(CH[cls[yy, xx]] for xx in range(0, WW, 2)))
