#!/usr/bin/env python3
"""Definitive component measurement of slide_027.jpg (frame 960x540, 1px=1pt frame-space).

Mapping (chrome-fit, same as slide_002): slide_x=(fx-18.63)/0.96123, slide_y=fy/0.95556
"""
import numpy as np
from PIL import Image
from scipy import ndimage
import json

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = im.shape
r, g, b = im[..., 0], im[..., 1], im[..., 2]

A, B, C = 18.63, 0.96123, 0.95556
def S(p):  # frame (x,y) -> slide pt
    return (round((p[0]-A)/B, 1), round(p[1]/C, 1))

out = {}

# ---------- circle: largest pale-yellow connected component right of x=300
paleY = (r > 238) & (g > 238) & (b > 168) & (b < 240)
paleY[:, :300] = False
lab, n = ndimage.label(paleY)
sizes = ndimage.sum(paleY, lab, range(1, n+1))
big = int(np.argmax(sizes)) + 1
m = lab == big
ys, xs = np.where(m)
cx, cy = xs.mean(), ys.mean()
# radius via extreme extents along center row/col
cyi, cxi = int(round(cy)), int(round(cx))
rowxs = np.where(m[cyi])[0]; colys = np.where(m[:, cxi])[0]
out["circle"] = {
    "frame_center": (round(float(cx),1), round(float(cy),1)),
    "slide_center": S((float(cx), float(cy))),
    "row_extent": [int(rowxs.min()), int(rowxs.max())],
    "col_extent": [int(colys.min()), int(colys.max())],
    "rx_px": int((rowxs.max()-rowxs.min())/2), "ry_px": int((colys.max()-colys.min())/2),
    "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
    "px": int(m.sum()),
}
# circle outline color: sample just outside fill on row cyi
for dx in (-2, 2):
    pass
ox = int(rowxs.max())
out["circle_edge_samples"] = [tuple(im[cyi, ox+k]) for k in range(0, 6)]

# ---------- word chips: mint fill components
chip = (g > 220) & (g - r > 10) & (g - b > 10) & (r > 165) & (r < 235)
chip[:, :300] = False
lab2, n2 = ndimage.label(chip)
out["chips"] = []
for i in range(1, n2+1):
    m = lab2 == i
    cnt = int(m.sum())
    if cnt < 120: continue
    ys, xs = np.where(m)
    x0, y0 = xs.mean(), ys.mean()
    xc, yc = (xs - x0).astype(float), (ys - y0).astype(float)
    cov = np.cov(np.vstack([xc, yc]))
    evals, evecs = np.linalg.eigh(cov)
    v = evecs[:, np.argmax(evals)]
    ang = float(np.degrees(np.arctan2(-v[1], v[0])))  # ccw from +x, screen y down corrected
    if ang <= -90: ang += 180
    if ang > 90: ang -= 180
    out["chips"].append({
        "px": cnt, "frame_center": (round(float(x0),1), round(float(y0),1)),
        "slide_center": S((x0, y0)),
        "angle_ccw": round(ang, 1),
        "axes_px": [round(float(np.sqrt(evals[1]))*4, 1), round(float(np.sqrt(evals[0]))*4, 1)],
        "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
    })
out["chips"].sort(key=lambda c: -c["px"])

# ---------- arcs: orange components
arc = (r > 180) & (g > 55) & (g < 160) & (b < 80)
arc[:, :300] = False
lab3, n3 = ndimage.label(arc)
out["arcs"] = []
for i in range(1, n3+1):
    m = lab3 == i
    cnt = int(m.sum())
    if cnt < 30: continue
    ys, xs = np.where(m)
    out["arcs"].append({"px": cnt, "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                        "center": (round(float(xs.mean()),1), round(float(ys.mean()),1))})
out["arcs"].sort(key=lambda a: -a["px"])

# ---------- red things right of x=300 (spokes, +w labels, arrowheads)
red = (r > 130) & (r - g > 55) & (r - b > 55)
red[:, :300] = False
lab4, n4 = ndimage.label(red)
out["red_components"] = []
for i in range(1, n4+1):
    m = lab4 == i
    cnt = int(m.sum())
    if cnt < 8: continue
    ys, xs = np.where(m)
    out["red_components"].append({"px": cnt, "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(xs.max())] if False else [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                                  "center": (round(float(xs.mean()),1), round(float(ys.mean()),1))})
# keep only reasonably large ones (labels/arrowheads); spokes are dotted -> many tiny comps
out["red_components"] = [c for c in out["red_components"] if c["px"] >= 15][:60]

# ---------- spokes: red-ish (lighter) dotted rays — looser threshold
red2 = (r > 150) & (r - g > 25) & (r - b > 25) & (g < 190)
red2[:, :300] = False
ys, xs = np.where(red2)
if len(xs):
    dx, dy = xs - out["circle"]["frame_center"][0], out["circle"]["frame_center"][1] - ys
    ang = np.degrees(np.arctan2(dy, dx))
    hist = {}
    for a in ang:
        k = int(round(((a + 360) % 360) / 30)) * 30 % 360
        hist[k] = hist.get(k, 0) + 1
    out["spoke_angle_hist"] = {str(k): v for k, v in sorted(hist.items())}
    # radial extent of spoke ink per angle bucket (min/max distance)
    ext = {}
    for a, d in zip(ang, np.hypot(dx, dy)):
        k = int(round(((a + 360) % 360) / 30)) * 30 % 360
        ext.setdefault(k, [1e9, 0])
        ext[k][0] = min(ext[k][0], d); ext[k][1] = max(ext[k][1], d)
    out["spoke_radial_extent"] = {str(k): [round(v[0]), round(v[1])] for k, v in sorted(ext.items())}

# ---------- horizontal gray line through center (transcript claim)
cyi = int(round(out["circle"]["frame_center"][1]))
cxi = int(round(out["circle"]["frame_center"][0]))
row = im[cyi, cxi-460:cxi+460]
grayline = (np.abs(row[:,0]-row[:,1]) < 25) & (np.abs(row[:,1]-row[:,2]) < 25) & (row[:,0] > 120) & (row[:,0] < 215)
idx = np.where(grayline)[0]
out["gray_hline_row_samples"] = {"row": cyi, "count": int(grayline.sum()),
                                 "runs": [int(i+cxi-460) for i in idx[:5]] + [int(i+cxi-460) for i in idx[-5:]] if len(idx) else []}

# ---------- inset box text colors: classify per line
# box measured separately: pale yellow comp in x 60..300, y 140..320
paleL = (r > 238) & (g > 238) & (b > 168) & (b < 240)
paleL[:, 300:] = False
lab5, n5 = ndimage.label(paleL)
sizes5 = ndimage.sum(paleL, lab5, range(1, n5+1))
big5 = int(np.argmax(sizes5)) + 1
m5 = lab5 == big5
ys5, xs5 = np.where(m5)
out["eqbox"] = {"bbox": [int(xs5.min()), int(ys5.min()), int(xs5.max()), int(ys5.max())],
                "slide_bbox": [S((xs5.min(), ys5.min())), S((xs5.max(), ys5.max()))]}
# text ink inside box (non-fill, non-border): dark-ish pixels
x0b, y0b, x1b, y1b = xs5.min(), ys5.min(), xs5.max(), ys5.max()
sub = im[y0b:y1b+1, x0b:x1b+1]
sr, sg, sb = sub[...,0], sub[...,1], sub[...,2]
inkm = ((sr < 200) | (sg < 200) | (sb < 200)) & ~((sr > 230) & (sg > 230))  # exclude pale fill+box border-ish
blue = (sb > 110) & (sr < 110) & (sg < 110)
redc = (sr > 130) & (sr - sg > 55) & (sr - sb > 55)
greenc = (sg > 100) & (sg - sr > 40) & (sg - sb > 40)
dark = (sr < 110) & (sg < 110) & (sb < 110)
rowsink = np.where(inkm.any(axis=1))[0]
segs = []
if len(rowsink):
    cur = [rowsink[0]]
    for y in rowsink[1:]:
        if y - cur[-1] <= 3: cur.append(y)
        else: segs.append((cur[0], cur[-1])); cur = [y]
    segs.append((cur[0], cur[-1]))
out["eqbox_lines"] = []
for (ya, yb) in segs:
    band = slice(ya, yb+1)
    def cnt(mm): return int(mm[band].sum())
    xs_ink = np.where(inkm[band].any(axis=0))[0]
    out["eqbox_lines"].append({
        "y_frame": [int(ya+y0b), int(yb+y0b)],
        "x_frame": [int(xs_ink.min()+x0b), int(xs_ink.max()+x0b)],
        "blue": cnt(blue), "red": cnt(redc), "green": cnt(greenc), "dark": cnt(dark),
    })

# ---------- badge precise (yellow comp near top-right)
yel = (r > 225) & (g > 225) & (b > 110) & (b < 215)
yel[:, :700] = False; yel[140:, :] = False
lab6, n6 = ndimage.label(yel)
if n6:
    sizes6 = ndimage.sum(yel, lab6, range(1, n6+1))
    big6 = int(np.argmax(sizes6)) + 1
    m6 = lab6 == big6
    ys6, xs6 = np.where(m6)
    out["badge"] = {"bbox": [int(xs6.min()), int(ys6.min()), int(xs6.max()), int(ys6.max())],
                    "center_frame": (round(float(xs6.mean()),1), round(float(ys6.mean()),1)),
                    "slide_center": S((float(xs6.mean()), float(ys6.mean()))),
                    "d_px": int(max(xs6.max()-xs6.min(), ys6.max()-ys6.min())+1)}

# ---------- cursor (black comp near center)
blk = (r < 80) & (g < 80) & (b < 80)
blk[:, :300] = False; blk[470:, :] = False; blk[:100, :] = False
lab7, n7 = ndimage.label(blk)
out["cursor"] = []
for i in range(1, n7+1):
    m = lab7 == i
    cnt = int(m.sum())
    if cnt < 12: continue
    ys7, xs7 = np.where(m)
    out["cursor"].append({"px": cnt, "bbox": [int(xs7.min()), int(ys7.min()), int(xs7.max()), int(ys7.max())]})

# ---------- title lines (left region)
tit = (r > 130) & (r - g > 55) & (r - b > 55)
tit[:, 340:] = False; tit[:50, :] = False; tit[170:, :] = False; tit[:, :62] = False
ys8, xs8 = np.where(tit)
rows8 = np.unique(ys8)
segs8, cur = [], [rows8[0]]
for y in rows8[1:]:
    if y - cur[-1] <= 3: cur.append(y)
    else: segs8.append((cur[0], cur[-1])); cur = [y]
segs8.append((cur[0], cur[-1]))
out["title_lines"] = []
for (ya, yb) in segs8:
    mm = (ys8 >= ya) & (ys8 <= yb)
    lx = xs8[mm]
    out["title_lines"].append({"y_frame": [int(ya), int(yb)], "x_frame": [int(lx.min()), int(lx.max())],
                               "h_px": int(yb-ya+1),
                               "slide": [S((lx.min(), ya)), S((lx.max(), yb))]})

print(json.dumps(out, indent=1, default=str))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide027/measure2.json", "w") as f:
    json.dump(out, f, indent=1, default=str)
