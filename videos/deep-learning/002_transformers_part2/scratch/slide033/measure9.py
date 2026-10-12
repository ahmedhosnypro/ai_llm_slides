#!/usr/bin/env python3
"""slide033 measure-9: pair-box text bands, ellipsis dots, vector-col text, cuts crops."""
import numpy as np
from PIL import Image
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)
MAPX = lambda fx: (fx - 18.63) / 0.96123
MAPY = lambda fy: fy / 0.95556
S = lambda x0, x1, y0, y1: (f"f[{x0},{y0}..{x1},{y1}] slide[{MAPX(x0):.1f}..{MAPX(x1):.1f} x {MAPY(y0):.1f}..{MAPY(y1):.1f}] in[{MAPX(x0)/72:.3f}..{MAPX(x1)/72:.3f}, {MAPY(y0)/72:.3f}..{MAPY(y1)/72:.3f}]")

def bands(x0, x1, y0, y1, kind, gap=4, min_area=4, label=""):
    sub = a[y0:y1 + 1, x0:x1 + 1]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    if kind == "red": m = (r > 120) & (g < 95) & (b < 95)
    elif kind == "orange": m = (r > 170) & (g > 70) & (g < 175) & (b < 120) & (r - b > 70)
    elif kind == "greenD": m = (r < 150) & (g > 110) & (g < 200) & (b < 160) & (g - r > 25) & (g - b > 25)
    elif kind == "dark": m = (r < 130) & (g < 130) & (b < 130)
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    boxes = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_area: continue
        boxes.append([int(xs.min()) + x0, int(ys.min()) + y0, int(xs.max()) + x0, int(ys.max()) + y0])
    boxes.sort(key=lambda t: (t[1], t[0]))
    out, cur = [], None
    for t in boxes:
        if cur is None or t[1] - cur[3] > gap:
            if cur: out.append(cur)
            cur = [t[0], t[1], t[2], t[3]]
        else:
            cur[0] = min(cur[0], t[0]); cur[1] = min(cur[1], t[1])
            cur[2] = max(cur[2], t[2]); cur[3] = max(cur[3], t[3])
    if cur: out.append(cur)
    print(f"--- {kind} {label} ---")
    for bd in out:
        print(f"  {S(bd[0], bd[2], bd[1], bd[3])}")
    return out

# pair column boxes: y 125..184, 194..250, 258..318, 354..412, 450..510; x ~318..406
for i, (ya, yb) in enumerate([(125, 184), (194, 250), (258, 318), (354, 412), (450, 510)], 1):
    kind = "greenD" if i % 2 == 1 else "orange"
    bands(320, 404, ya, yb, kind, gap=3, label=f"pair box {i} text")
    bands(320, 404, ya, yb, "dark", gap=3, label=f"pair box {i} dark")

# vector pairs column text: boxes y 126..182, 194..251, 258..318, 354..414, 450..510; x 222..254
for i, (ya, yb, val) in enumerate([(126, 182, "0"), (194, 251, "1"), (258, 318, "2"),
                                    (354, 414, "K"), (450, 510, "[d/2]-1")], 1):
    bands(220, 258, ya, yb, "dark", gap=3, label=f"vector '{val}'")

# index column red text: strip x 267..309, y 125..512
bands(269, 308, 125, 512, "red", gap=6, label="index strip values")

# ellipsis dots between boxes: gaps y 318..355 and y 412..450, x 222..254 and x 318..406
print("=== ellipsis gap dot check ===")
for (x0, x1, y0, y1, lab) in [(222, 256, 319, 354, "vec gap 2->K"), (222, 256, 413, 449, "vec gap K->d/2-1"),
                               (318, 406, 319, 353, "pair gap 3->4"), (318, 406, 413, 449, "pair gap 4->5")]:
    sub = a[y0:y1 + 1, x0:x1 + 1]
    dark = (sub.mean(axis=2) < 200)
    ys, xs = np.where(dark)
    if len(ys):
        print(f"  {lab}: ink f[{xs.min()+x0},{ys.min()+y0}..{xs.max()+x0},{ys.max()+y0}] n={len(ys)}")
    else:
        print(f"  {lab}: EMPTY")

# green info box: exact border rect (green stroke ~00B050) + text bands
print("=== info box border ===")
gm = (np.abs(a[..., 1] - 176) < 60) & (a[..., 0] < 160) & (a[..., 2] < 170) & (a[..., 1] - a[..., 0] > 40) & (a[..., 1] - a[..., 2] > 20)
sub = gm[220:330, 60:220]
ys, xs = np.where(sub)
print(f"  green stroke bbox f[{xs.min()+60},{ys.min()+220}..{xs.max()+60},{ys.max()+220}]  {S(xs.min()+60, xs.max()+60, ys.min()+220, ys.max()+220)}")

# title/subtitle font width fitting prep
print("=== crop cut ===")
im = Image.open(FR)
SC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide033/"
crops = [
    ("crop_eq.png",      (698, 334, 876, 404), 3),
    ("crop_defs.png",    (425, 98, 766, 292), 2),
    ("crop_example.png", (771, 98, 893, 291), 2),
    ("crop_pairbox.png", (82, 106, 200, 224), 3),
    ("crop_omega.png",   (471, 295, 882, 514), 1),
    ("crop_title.png",   (320, 40, 810, 100), 2),
]
for name, box, scale in crops:
    c = im.crop(box)
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    c.save(SC + name)
    print(f"  saved {name} box={box} scale={scale} -> {c.size}")
