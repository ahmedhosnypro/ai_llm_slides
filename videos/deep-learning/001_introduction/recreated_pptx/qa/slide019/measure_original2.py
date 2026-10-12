#!/usr/bin/env python3
"""PIL measurement pass 2 for slide_019.jpg: exact node bboxes/borders/fills (modal),
title ink, ellipse border, dashed container, vertical box, annotation box, curves."""
from PIL import Image
import numpy as np
from collections import Counter

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_019.jpg").convert("RGB")
a = np.asarray(IM).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def modal(im_pixels, label):
    cnt = Counter(map(tuple, im_pixels.reshape(-1, 3)))
    print(f"  {label} modal:", cnt.most_common(4))

def box_info(name, x0, x1, y0, y1):
    """exact bbox of a node: fill-region inside [x0..x1]x[y0..y1] via non-white/non-gray ink"""
    sub = a[y0:y1, x0:x1]
    # ink = not chrome-gray and not white
    rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    white = (rr > 235) & (gg > 235) & (bb > 235)
    ys, xs = np.where(~white)
    if not len(ys):
        print(name, "EMPTY"); return
    bx0, bx1, by0, by1 = xs.min()+x0, xs.max()+x0, ys.min()+y0, ys.max()+y0
    print(f"{name}: x{bx0}..{bx1} y{by0}..{by1} (w{bx1-bx0+1} h{by1-by0+1})")
    # border stroke = 2px ring: sample modal of outermost ring
    ring = np.ones(sub.shape[:2], bool)
    ring[2:-2, 2:-2] = False
    ringpix = sub[ring & ~white]
    modal(ringpix, f"{name} ring")
    # fill core = central 40% box
    cy0, cy1 = int((by1-by0)*0.3), int((by1-by0)*0.7)
    cx0, cx1 = int((bx1-bx0)*0.3), int((bx1-bx0)*0.7)
    core = sub[cy0:cy1, cx0:cx1]
    # exclude near-black text and near-white
    nottext = ~((core[:, :, 0] < 100) & (core[:, :, 1] < 100) & (core[:, :, 2] < 100))
    modal(core[nottext], f"{name} fill-core")

# nodes (search windows from pass-1 samples)
box_info("input_samples", 70, 165, 200, 275)
box_info("pre_processing", 195, 290, 195, 275)
box_info("feature_extraction", 315, 410, 195, 275)
box_info("feature_selection", 430, 525, 195, 275)
box_info("classification", 540, 640, 195, 275)
box_info("predicted_labels", 655, 735, 200, 275)
box_info("samples_labels", 815, 905, 200, 275)

# vertical prediction error box
box_info("prediction_error_vert", 735, 800, 170, 310)

# ---- title ink rows 60..95 only ----
tred = (r > 140) & (g < 80) & (b < 80)
tm = np.zeros_like(tred); tm[58:96, 60:900] = tred[58:96, 60:900]
ys, xs = np.where(tm)
print(f"title ink: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} (w{xs.max()-xs.min()+1} h{ys.max()-ys.min()+1}) center=({(xs.min()+xs.max())/2:.1f})")
modal(a[tm], "title color")

# ---- training ellipse: border ring color + exact bbox ----
sub = a[100:170, 350:500]
rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
notwhite = ~((rr > 235) & (gg > 235) & (bb > 235))
ys, xs = np.where(notwhite)
print(f"ellipse ink: x{xs.min()+350}..{xs.max()+350} y{ys.min()+100}..{ys.max()+100}")
# ring = topmost rows of ink
top_rows = sub[ys.min():ys.min()+3, :]
modal(top_rows[notwhite[ys.min():ys.min()+3]], "ellipse top-ring")
# fill core
cy, cx = (ys.min()+ys.max())//2, (xs.min()+xs.max())//2
modal(a[cy-5:cy+5, cx-25:cx+25].reshape(-1,3), "ellipse fill-core")

# ---- bottom bands: row profiles at several columns ----
for x in (60, 200, 400, 600, 800, 900):
    col = a[460:540, x]
    kinds = []
    for y in range(460, 540):
        px = a[y, x]
        kinds.append(f"{y}:{tuple(px)}")
    # print compact: transitions only
    prev = None; trans = []
    for y in range(460, 540):
        px = tuple(a[y, x])
        lab = "black" if sum(px) < 180 else ("white" if min(px) > 235 else ("gray233" if abs(px[0]-233)<12 and abs(px[1]-233)<12 else ("gray204" if abs(px[0]-204)<15 and abs(px[1]-204)<15 else "other")))
        if lab != prev:
            trans.append(f"{y}:{lab}{px if lab=='other' else ''}")
            prev = lab
    print(f"col x{x}: " + " | ".join(trans))

# ---- dashed red container around nodes 2-5 ----
red = (r > 130) & (g < 90) & (b < 90)
rm = np.zeros_like(red); rm[180:290, 190:660] = red[180:290, 190:660]
ys, xs = np.where(rm)
print(f"red container ink: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
# dash pattern along top edge: find the top border row
toprow = Counter(ys).most_common(3)
print("container: most common rows:", toprow)

# ---- blue curves ----
blue = (b > 110) & (b - r > 50) & (b - g > 40)
bm = np.zeros_like(blue); bm[95:220, 60:920] = blue[95:220, 60:920]
ys, xs = np.where(bm)
print(f"blue ink: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
# split left/right of ellipse (x<372 vs x>466)
lm = bm.copy(); lm[:, 350:] = False
ys, xs = np.where(lm)
print(f"blue LEFT (solid): x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(ys)}")
rm2 = bm.copy(); rm2[:, :500] = False
ys, xs = np.where(rm2)
print(f"blue RIGHT (dashed): x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(ys)}")
modal(a[bm], "blue color")

# ---- green dashed feedback arrows (below pipeline, above annotation) ----
green = (g > 90) & (g - r > 40) & (g - b > 30)
gm = np.zeros_like(green); gm[265:340, 200:790] = green[265:340, 200:790]
ys, xs = np.where(gm)
print(f"green arrows ink: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(ys)}")
modal(a[gm], "green color")

# ---- annotation box exact + border + text color ----
sub = a[330:410, 180:820]
rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
palegreen = (gg > rr) & (gg > bb) & (gg > 200) & (rr > 190) & (bb > 190)
ys, xs = np.where(palegreen)
print(f"annotation fill: x{xs.min()+180}..{xs.max()+180} y{ys.min()+330}..{ys.max()+330}")
modal(sub[palegreen], "annotation fill-core")
# border ring
ring = np.ones(sub.shape, bool); ring[2:-2, 2:-2] = False
ringpix = sub[ring & (gg > rr-30) & (gg > bb-30)]
modal(ringpix, "annotation ring")
# text ink (dark green)
dk = (rr < 120) & (gg < 160) & (bb < 120)
ys, xs = np.where(dk)
print(f"annotation text ink: x{xs.min()+180}..{xs.max()+180} y{ys.min()+330}..{ys.max()+330}")
modal(sub[dk], "annotation text color")

# ---- pencil icon in pre_processing top-right ----
sub = a[195:235, 240:300]
rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
dk = (rr < 120) & (gg < 120) & (bb < 120)
ys, xs = np.where(dk)
if len(ys):
    print(f"pencil ink: x{xs.min()+240}..{xs.max()+240} y{ys.min()+195}..{ys.max()+195} n={len(ys)}")
