#!/usr/bin/env python3
"""Forensics 6: definitive measurements — true grid fills, outline colors, element bboxes."""
import numpy as np
from PIL import Image
from collections import Counter

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

TOP, PITCH, NCELL = 178.5, (462.5 - 178.5) / 18, 18
STACKS = [("Words Vectors", 163, 244), ("1st FM", 308, 390), ("2nd FM", 456, 537),
          ("3rd FM", 598, 679), ("4th FM", 737, 818)]

PAL = {
    "YELLOW_FFFFCC": (255, 255, 204), "PEACH_FFCC99": (255, 204, 153),
    "CYAN_99FFFF": (153, 255, 255), "PINK_FFCCFF": (255, 204, 255),
    "PGREEN_CCFFCC": (204, 255, 204), "WHITE": (255, 255, 255),
    "PANEL_E9E9E7": (233, 233, 231), "GRAY_BFBFBF": (191, 191, 191),
}

def classify_cell(nm, x0, x1, ci):
    y0 = int(TOP + PITCH * ci) + 3
    y1 = int(TOP + PITCH * (ci + 1)) - 3
    x0i, x1i = x0 + 4, x1 - 4
    patch = im[y0:y1, x0i:x1i].reshape(-1, 3)
    cnt = Counter()
    for px in patch:
        best, bd = None, 10**9
        for k, t in PAL.items():
            d = sum((int(px[i]) - t[i]) ** 2 for i in range(3))
            if d < bd:
                best, bd = k, d
        cnt[best] += 1
    tot = sum(cnt.values())
    top2 = cnt.most_common(2)
    return f"cell {ci+1:2d}: {top2[0][0].split('_')[0]} {100*top2[0][1]//tot}% " + (f"| {top2[1][0].split('_')[0]} {100*top2[1][1]//tot}%" if len(top2) > 1 else "")

print("=== per-cell fill (true grid) ===")
for nm, x0, x1 in STACKS:
    print(f"--- {nm} (x{x0}-{x1}) ---")
    out = []
    for ci in range(NCELL):
        out.append(classify_cell(nm, x0, x1, ci))
    print("   " + "\n   ".join(out))

print("\n=== outline colors ===")
# horizontal outline at y=241.5 (between cells 4 and 5) per stack
for nm, x0, x1 in STACKS:
    yl = 241
    seg = im[240:244, x0+10:x1-10].reshape(-1, 3)
    dark = [tuple(int(v) for v in p) for p in seg if p.mean() < 210]
    if dark:
        arr = np.array(dark)
        print(f"{nm} outline row y241: n={len(dark)} avg {tuple(round(v,1) for v in arr.mean(axis=0))}")
    else:
        print(f"{nm} outline row y241: no dark px")
# vertical edge columns: stack left/right at x0, x1
for nm, x0, x1 in STACKS:
    for lbl, xx in [("L", x0), ("R", x1)]:
        seg = im[200:440, xx-1:xx+2].reshape(-1, 3)
        dark = [tuple(int(v) for v in p) for p in seg if p.mean() < 210]
        if dark:
            arr = np.array(dark)
            print(f"{nm} edge {lbl} x{xx}: n={len(dark)} avg {tuple(round(v,1) for v in arr.mean(axis=0))}")
        else:
            print(f"{nm} edge {lbl} x{xx}: no dark px")

print("\n=== element bboxes ===")
def bbox(mask, label):
    ys, xs = np.where(mask)
    if not len(xs):
        print(f"{label}: EMPTY")
        return None
    print(f"{label}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  n={len(xs)}")
    return xs.min(), xs.max(), ys.min(), ys.max()

red = (r > 140) & (g < 110) & (b < 110)
blue = (b > 120) & (r < 110) & (g < 110)
green = (g > 110) & (r < 130) & (b < 130) & (g - r > 40) & (g - b > 40)
yellowish = (r > 230) & (g > 230) & (b < 190)
graybar = (abs(r - 191) < 22) & (abs(g - 191) < 22) & (abs(b - 191) < 22)
salmon = (r > 230) & (g > 120) & (g < 190) & (b > 120) & (b < 190)

bbox(red[:150, :], "title red (y<150)")
bbox(red[145:180, 140:260], "stack1 header red (y145-180,x140-260)")
bbox(red[145:180, 300:400], "stack2 header red")
bbox(red[145:180, 450:540], "stack3 header red")
bbox(red[145:180, 590:685], "stack4 header red")
bbox(red[145:180, 730:825], "stack5 header red")
bbox(red[100:200, 40:160], "kernel label red (y100-200,x40-160)")
bbox(salmon[80:160, 40:160], "kernel pictogram salmon")
bbox(green[100:200, 400:700], "green callout+leader (y100-200,x400-700)")
bbox(graybar[170:470, 400:440], "bar1 gray (x400-440)")
bbox(graybar[170:470, 550:590], "bar2 gray (x550-590)")
bbox(graybar[170:470, 690:730], "bar3 gray (x690-730)")
bbox(graybar[170:470, 820:860], "bar4 gray (x820-860)")
bbox(blue[170:470, 405:445], "bar1 blue text")
bbox(blue[170:470, 555:595], "bar2 blue text")
bbox(blue[170:470, 695:735], "bar3 blue text")
bbox(blue[170:470, 825:865], "bar4 blue text")
bbox(red[170:470, 120:170], "seq arrow red (x120-170)")
bbox(blue[170:470, 100:160], "seq label blue?? (x100-160)")
bbox(red[170:470, 100:160], "seq label red (x100-160)")
bbox(red[290:340, 245:310], "block arrow (x245-310,y290-340)")
bbox(red[170:300, 245:310], "triangle1 zone (y170-300)")
bbox(red[380:470, 245:310], "triangle2 zone (y380-470)")
bbox(red[300:380, 537:600], "triangle3 zone (y300-380)")
bbox(red[190:280, 679:740], "triangle4 zone (y190-280)")
bbox(red[465:505, 150:820], "hatch arrow red (y465-505)")
bbox(yellowish[330:500, 560:930], "banner yellow (y330-500)")
bbox(blue[330:500, 560:930], "banner blue text")
bbox(blue[495:530, 150:860], "caption blue (y495-530)")
bbox(red[:100, 850:960], "badge red? (top right)")
