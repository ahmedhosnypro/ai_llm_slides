#!/usr/bin/env python3
"""Master geometry extraction for slide_026 -> JSON. All coords in FRAME px (960x540).
Mapping to slide pts: sx=(fx-18.628)/0.96123, sy=fy/0.95556."""
from PIL import Image
import numpy as np
from scipy import ndimage
import json

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg"
img = Image.open(F).convert("RGB")
a = np.asarray(img).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
out = {}

def near(c, tol):
    return (abs(r - c[0]) < tol) & (abs(g - c[1]) < tol) & (abs(b - c[2]) < tol)

def bbox_of(mask, label, minpx=50):
    ys, xs = np.nonzero(mask)
    if len(xs) < minpx:
        out[label] = None
        return None
    bb = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    out[label] = {"bbox": bb, "n": int(len(xs))}
    return bb

# ---- 1. white diagram panel: white rows/cols in known empty zones
white = (r > 240) & (g > 240) & (b > 240)
# panel top edge: scan column x=430 (inside panel, above container) for white start
col = white[:, 430]
ys = np.nonzero(col[120:500])[0] + 120
out["panel_col430_y"] = [int(ys.min()), int(ys.max())]
col = white[:, 700]
ys = np.nonzero(col[120:500])[0] + 120
out["panel_col700_y"] = [int(ys.min()), int(ys.max())]
row = white[165, :]
xs = np.nonzero(row[100:900])[0] + 100
out["panel_row165_x"] = [int(xs.min()), int(xs.max())]
row = white[466, :]
xs = np.nonzero(row[100:900])[0] + 100
out["panel_row466_x"] = [int(xs.min()), int(xs.max())]
# panel left/right edge scan at y=210 (gutter between blue box and container is white)
row = white[210, :]
xs = np.nonzero(row[150:900])[0] + 150
out["panel_row210_x"] = [int(xs.min()), int(xs.max())]

# ---- 2. blue box + white sub-blocks inside
blue = near((18, 189, 232), 60)
bb = bbox_of(blue, "blue_box")
# sub-blocks: white-ish pixels within blue bbox
sub = np.zeros_like(blue)
x0, y0, x1, y1 = bb
sub[y0:y1 + 1, x0:x1 + 1] = white[y0:y1 + 1, x0:x1 + 1]
lab, n = ndimage.label(sub)
sizes = ndimage.sum(sub, lab, range(1, n + 1))
subs = []
for i, s in enumerate(sizes, 1):
    if s > 200:
        sl = ndimage.find_objects(lab == i)[0] if False else None
for i in range(1, n + 1):
    if sizes[i - 1] > 200:
        m = lab == i
        ys2, xs2 = np.nonzero(m)
        subs.append([int(xs2.min()), int(ys2.min()), int(xs2.max()), int(ys2.max()), int(sizes[i - 1])])
subs.sort(key=lambda t: t[1])
out["blue_subblocks"] = subs

# ---- 3. gray bars (dark gray ~ (144..150)) + light gray 24V
dgray = near((146, 147, 143), 22)
lab, n = ndimage.label(dgray)
bars = []
for i in range(1, n + 1):
    m = lab == i
    npx = m.sum()
    if npx > 150:
        ys2, xs2 = np.nonzero(m)
        h = ys2.max() - ys2.min()
        w = xs2.max() - xs2.min()
        if w < 40 and h > 60:  # vertical bars
            bars.append([int(xs2.min()), int(ys2.min()), int(xs2.max()), int(ys2.max()), int(npx)])
bars.sort()
out["darkgray_vbars"] = bars
lgray = near((191, 191, 191), 22)
lab, n = ndimage.label(lgray)
sm = []
for i in range(1, n + 1):
    m = lab == i
    npx = int(m.sum())
    if npx > 100:
        ys2, xs2 = np.nonzero(m)
        sm.append([int(xs2.min()), int(ys2.min()), int(xs2.max()), int(ys2.max()), npx])
sm.sort(key=lambda t: -t[4])
out["lgray_comps_top"] = sm[:8]

# ---- 4. TIDA container: fill C4DCA0 union bbox + dashed border extent
lg = near((196, 219, 161), 24)
lg[:, :390] = False  # only container area
bb = bbox_of(lg, "container_fill")
# container full extent incl border: scan for the dashed border color (green ~ (110,170,90)?) and fill
cont = lg.copy()
# dashed border: darker green; find greenish pixels in 395..675 x 180..480
gb = (g > r + 15) & (g > b + 25) & (g > 120) & (g < 235) & (r > 60)
region = np.zeros_like(gb)
region[180:485, 390:680] = True
gb = gb & region
bb2 = bbox_of(gb, "container_greenish")
# white tag TIDA-00176 top-right inside container
tag = white & region
lab, n = ndimage.label(tag)
tg = []
for i in range(1, n + 1):
    m = lab == i
    npx = int(m.sum())
    if npx > 150:
        ys2, xs2 = np.nonzero(m)
        tg.append([int(xs2.min()), int(ys2.min()), int(xs2.max()), int(ys2.max()), npx])
tg.sort(key=lambda t: -t[4])
out["container_white_tags"] = tg[:8]

# ---- 5. orange + peach blocks
orange = near((247, 150, 70), 50)
lab, n = ndimage.label(orange)
oc = []
for i in range(1, n + 1):
    m = lab == i
    npx = int(m.sum())
    if npx > 200:
        ys2, xs2 = np.nonzero(m)
        oc.append([int(xs2.min()), int(ys2.min()), int(xs2.max()), int(ys2.max()), npx])
oc.sort(key=lambda t: -t[4])
out["orange_comps"] = oc
peach = near((250, 219, 185), 20)
lab, n = ndimage.label(peach)
pc = []
for i in range(1, n + 1):
    m = lab == i
    npx = int(m.sum())
    if npx > 250:
        ys2, xs2 = np.nonzero(m)
        pc.append([int(xs2.min()), int(ys2.min()), int(xs2.max()), int(ys2.max()), npx])
pc.sort(key=lambda t: -t[4])
out["peach_comps"] = pc

# ---- 6. green triangles (amp) + comparators
grn = near((96, 190, 135), 55)
lab, n = ndimage.label(grn)
gc = []
for i in range(1, n + 1):
    m = lab == i
    npx = int(m.sum())
    if npx > 120:
        ys2, xs2 = np.nonzero(m)
        gc.append([int(xs2.min()), int(ys2.min()), int(xs2.max()), int(ys2.max()), npx])
gc.sort(key=lambda t: -t[4])
out["green_tri"] = gc

# ---- 7. red arrow + red texts
red = (r - np.maximum(g, b) > 55) & (r > 130)
left = red.copy(); left[:, 225:] = False
bbox_of(left, "red_arrow_left")
title = red.copy(); title[:55] = False; title[85:] = False; title[:, :300] = False; title[:, 650:] = False
bbox_of(title, "title_red")
cap = red.copy(); cap[:470] = False
bbox_of(cap, "caption_red_all")
lab, n = ndimage.label(cap)
cl = []
for i in range(1, n + 1):
    m = lab == i
    npx = int(m.sum())
    if npx > 30:
        ys2, xs2 = np.nonzero(m)
        cl.append([int(xs2.min()), int(ys2.min()), int(xs2.max()), int(ys2.max()), npx])
cl.sort(key=lambda t: t[1])
out["caption_lines"] = cl
pos = red.copy(); pos[:280] = False; pos[340:] = False; pos[:, 235:] = False
bbox_of(pos, "position_label")

# ---- 8. subtitle blue text
bluet = (b - r > 60) & (b > 130) & (r < 160)
bluet[100:] = False; bluet[:78] = False
bbox_of(bluet, "subtitle_blue")

# ---- 9. right rounded rect: green border ring pixels x>670
gb2 = (g > r + 25) & (g > b + 30) & (g > 100) & (r < 160)
rr = np.zeros_like(gb2)
rr[150:500, 670:900] = True
gb2 = gb2 & rr
ys, xs = np.nonzero(gb2)
out["right_rect_border"] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(len(xs))]

# ---- 10. AC motor: dark-gray blob inside right rect (~753..787, 358..398)
mot = (abs(r - g) < 12) & (abs(g - b) < 12) & (r > 90) & (r < 200)
mm = np.zeros_like(mot)
mm[350:410, 740:850] = True
mot = mot & mm
bbox_of(mot, "ac_motor_gray")

print(json.dumps(out, indent=1))
