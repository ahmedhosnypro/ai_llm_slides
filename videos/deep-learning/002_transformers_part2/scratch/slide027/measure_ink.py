#!/usr/bin/env python3
"""Full ink measurement of slide_027.jpg -> TRUE slide coords.

Mapping (fitted from chrome landmarks, identical to slide_002's):
  frame_x = 18.63 + 0.96123*slide_x ; frame_y = 0.95556*slide_y
  -> slide_x = (frame_x-18.63)/0.96123 ; slide_y = frame_y/0.95556
Content: title lines, equation box, circle, word chips (pos+rotation),
arcs, +w labels, cursor, letterbox.
"""
import numpy as np
from PIL import Image
import json

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = im.shape
r, g, b = im[..., 0], im[..., 1], im[..., 2]

A, B, C = 18.63, 0.96123, 0.95556
def sx(fx): return (fx - A) / B
def sy(fy): return fy / C

out = {}

# ---- badge (yellow, top-right, y<110)
yel = (r > 225) & (g > 225) & (b > 120) & (b < 210)
ys, xs = np.where(yel)
m = (xs > 700) & (ys < 110)
bx, by = xs[m], ys[m]
out["badge_frame"] = [int(bx.min()), int(by.min()), int(bx.max()), int(by.max())]
out["badge_slide_center"] = [round(sx((bx.min()+bx.max())/2), 1), round(sy((by.min()+by.max())/2), 1)]

# ---- title: red text in top-left (x<320, y<160), excluding border cols
red = (r > 140) & (g < 90) & (b < 90)
tmask = np.zeros_like(red); tmask[50:170, 65:330] = True
tred = red & tmask
ys, xs = np.where(tred)
rows = np.unique(ys)
# split into lines by row gaps
lines, cur = [], [rows[0]]
for y in rows[1:]:
    if y - cur[-1] <= 2: cur.append(y)
    else: lines.append(cur); cur = [y]
lines.append(cur)
out["title_lines"] = []
for ln in lines:
    lm = np.isin(ys, ln)
    lx = xs[lm]
    out["title_lines"].append({
        "frame_y": [int(ln[0]), int(ln[-1])],
        "frame_x": [int(lx.min()), int(lx.max())],
        "slide": [round(sx(lx.min()),1), round(sy(ln[0]),1), round(sx(lx.max()),1), round(sy(ln[-1]),1)],
        "h_frame": int(ln[-1]-ln[0]+1),
    })

# ---- equation box: pale-yellow rect left side (x<250, y 150..300)
paleY = (r > 240) & (g > 240) & (b > 170) & (b < 235)
emask = np.zeros_like(paleY); emask[140:320, 60:280] = True
eb = paleY & emask
ys, xs = np.where(eb)
out["eqbox_frame"] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
out["eqbox_slide"] = [round(sx(xs.min()),1), round(sy(ys.min()),1), round(sx(xs.max()),1), round(sy(ys.max()),1)]

# equation box text ink: blue + red + green inside box
ink = np.zeros_like(red)
blue = (b > 120) & (r < 110) & (g < 110)
green = (g > 110) & (r < 110) & (b < 110)
ink[eb] = True
box = np.zeros_like(red); box[ys.min()+2:ys.max()-1, xs.min()+2:xs.max()-1] = True
tink = (red | blue | green) & box
ys2, xs2 = np.where(tink)
rows = np.unique(ys2)
lines, cur = [], [rows[0]]
for y in rows[1:]:
    if y - cur[-1] <= 2: cur.append(y)
    else: lines.append(cur); cur = [y]
lines.append(cur)
out["eqbox_lines"] = []
for ln in lines:
    lm = np.isin(ys2, ln); lx = xs2[lm]
    # color of the line
    colmask = {"red": int(red[ln[0]:ln[-1]+1, lx.min():lx.max()+1].sum()),
               "blue": int(blue[ln[0]:ln[-1]+1, lx.min():lx.max()+1].sum()),
               "green": int(green[ln[0]:ln[-1]+1, lx.min():lx.max()+1].sum())}
    out["eqbox_lines"].append({
        "frame_y": [int(ln[0]), int(ln[-1])], "frame_x": [int(lx.min()), int(lx.max())],
        "slide": [round(sx(lx.min()),1), round(sy(ln[0]),1), round(sx(lx.max()),1), round(sy(ln[-1]),1)],
        "h_frame": int(ln[-1]-ln[0]+1), "colors": colmask})

# ---- circle: pale-yellow blob right side (exclude eqbox region)
cmask = paleY.copy(); cmask[:, :300] = False
ys, xs = np.where(cmask)
cx, cy = xs.mean(), ys.mean()
# radius: use extents along axes through center
out["circle_frame_center"] = [round(float(cx),1), round(float(cy),1)]
out["circle_slide_center"] = [round(sx(float(cx)),1), round(sy(float(cy)),1)]
# horizontal extent at cy, vertical at cx
rowm = cmask[int(cy), :]
xs_row = np.where(rowm)[0]
colm = cmask[:, int(cx)]
ys_col = np.where(colm)[0]
out["circle_rx_frame"] = [int(xs_row.min()), int(xs_row.max()), int((xs_row.max()-xs_row.min())/2)]
out["circle_ry_frame"] = [int(ys_col.min()), int(ys_col.max()), int((ys_col.max()-ys_col.min())/2)]

# ---- word chips: mint green CCFFCC
chip = (g > 225) & (r > 175) & (r < 225) & (b > 175) & (b < 225) & (g - r > 15)
# restrict to circle vicinity (right 2/3)
chip[:, :320] = False
lab = np.zeros((H, W), dtype=int)
from scipy import ndimage
labm, n = ndimage.label(chip)
out["chips"] = []
for i in range(1, n+1):
    m = labm == i
    cnt = m.sum()
    if cnt < 60: continue
    ys, xs = np.where(m)
    # PCA for orientation
    x0, y0 = xs.mean(), ys.mean()
    xc, yc = xs - x0, ys - y0
    cov = np.cov(np.vstack([xc, yc]))
    evals, evecs = np.linalg.eigh(cov)
    # major axis = largest eigenvalue
    v = evecs[:, np.argmax(evals)]
    ang = np.degrees(np.arctan2(-v[1], v[0]))  # screen y down -> math angle ccw
    if ang < -90: ang += 180
    if ang > 90: ang -= 180
    ratio = np.sqrt(max(evals)/max(min(evals), 1e-9))
    scx, scy = sx(x0), sy(y0)
    out["chips"].append({"frame_center": [round(float(x0),1), round(float(y0),1)],
                         "slide_center": [round(float(scx),1), round(float(scy),1)],
                         "px": int(cnt), "angle_deg_ccw": round(float(ang),1),
                         "axis_ratio": round(float(ratio),2),
                         "frame_bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]})

# ---- arcs: orange E06010
arc = (r > 185) & (g > 60) & (g < 150) & (b < 70)
arc[:, :320] = False
labm, n = ndimage.label(arc)
out["arcs"] = []
for i in range(1, n+1):
    m = labm == i
    cnt = m.sum()
    if cnt < 40: continue
    ys, xs = np.where(m)
    out["arcs"].append({"px": int(cnt),
                        "frame_bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                        "slide_bbox": [round(sx(xs.min()),1), round(sy(ys.min()),1), round(sx(xs.max()),1), round(sy(ys.max()),1)]})

# ---- +w labels: red small text OUTSIDE circle top area
# red mask restricted outside circle, x 300..920, y<210
rr = np.hypot(xs*0, ys*0, )  # placeholder
out["plus_w"] = "see separate script"

# ---- mouse cursor: black pixels near circle center
blk = (r < 60) & (g < 60) & (b < 60)
blk[:, :320] = False; blk[480:, :] = False
labm, n = ndimage.label(blk)
cur = []
for i in range(1, n+1):
    m = labm == i
    if m.sum() < 15: continue
    ys, xs = np.where(m)
    cur.append({"px": int(m.sum()), "frame_bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]})
out["cursor_candidates"] = cur

print(json.dumps(out, indent=1))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide027/measure_ink.json", "w") as f:
    json.dump(out, f, indent=1)
