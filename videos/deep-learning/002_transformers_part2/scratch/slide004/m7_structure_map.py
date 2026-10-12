#!/usr/bin/env python3
# m7_structure_map.py — color-class ASCII maps: base render vs warped frame,
# right panel (and zone fill bboxes + full yellow/blue box census).
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
render = np.asarray(Image.open(f"{S}/base-1.png").convert("RGB"), dtype=np.float64)
warp = np.asarray(Image.open(f"{S}/frame_warped4.png").convert("RGB"), dtype=np.float64)

def classify(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    out = np.full(r.shape, '.', dtype='<U1')  # white/other
    out[(r > 235) & (g > 235) & (b > 235)] = '.'          # white
    out[(np.abs(r - 233) < 12) & (np.abs(g - 233) < 12) & (np.abs(b - 231) < 12)] = ','  # chrome gray
    out[(r > 245) & (g > 230) & (g < 245) & (b > 210) & (b < 230)] = 'p'  # peach FDEDDD
    out[(np.abs(r - 206) < 15) & (g > 245) & (np.abs(b - 225) < 15)] = 'm'  # mint CEFFE1
    out[(np.abs(r - 245) < 22) & (np.abs(g - 230) < 25) & (np.abs(b - 168) < 40) & (b < 205)] = 'y'  # attention yellow
    out[(np.abs(r - 157) < 30) & (np.abs(g - 195) < 30) & (b > 200)] = 'b'  # FF blue 9DC3E6
    out[(r > 230) & (np.abs(g - 193) < 35) & (np.abs(b - 206) < 35)] = 'k'  # pink F2C1CE
    out[(np.abs(r - 201) < 25) & (np.abs(g - 231) < 25) & (np.abs(b - 192) < 25)] = 's'  # softmax C9E7C0
    out[(np.abs(r - 197) < 25) & (np.abs(g - 192) < 25) & (np.abs(b - 232) < 25)] = 'l'  # linear C5C0E8
    out[(r > 150) & (g < 90) & (b < 90)] = 'R'            # red
    out[(g > 100) & (g - r > 40) & (g - b > 20)] = 'G'    # green
    out[(r > 200) & (b < 175) & (g > 130) & (g < 225) & ((r - b) > 60) & ((g - b) > 25)] = 'o'  # orange
    out[(r < 100) & (g < 100) & (b < 100)] = '#'          # dark ink
    return out

# right panel: render x 1190..1870, y 200..1060 -> 8px cells
def amap(a, x0, x1, y0, y1, step, tag):
    cls = classify(a)
    print(f"--- {tag} ---")
    hdr = "      " + "".join(str((x0 + i * step * (x1 - x0) // 1) // 100 % 10) for i in range(0, (x1 - x0) // step))
    print("      x(render px, left to right):")
    for cy in range(y0, y1, step * 2):
        row = []
        for cx in range(x0, x1, step):
            cell = cls[cy:cy + step * 2, cx:cx + step]
            chars, counts = np.unique(cell, return_counts=True)
            row.append(chars[np.argmax(counts)])
        print(f"  y{cy:4d} " + "".join(row))

amap(render, 1190, 1870, 200, 1064, 8, "BASE RENDER right panel (8x16px cells, R=red G=green y=yellow b=blue p=peach m=mint k=pink s=softmax l=linear o=orange #=ink .=white)")
amap(warp, 1190, 1870, 200, 1064, 8, "WARPED FRAME right panel")

# zone fill bboxes in render
r, g, b = render[..., 0], render[..., 1], render[..., 2]
peach = (r > 245) & (g > 230) & (g < 245) & (b > 210) & (b < 230)
mint = (np.abs(r - 206) < 15) & (g > 245) & (np.abs(b - 225) < 15)
for name, m in (("peach", peach), ("mint", mint)):
    m2 = m.copy(); m2[:, :1150] = False
    ys, xs = np.where(m2)
    if len(xs):
        print(f"{name}: render x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} -> slide x {xs.min()*72/150:.0f}..{xs.max()*72/150:.0f} y {ys.min()*72/150:.0f}..{ys.max()*72/150:.0f} n={len(xs)}")
