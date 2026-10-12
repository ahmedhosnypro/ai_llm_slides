#!/usr/bin/env python3
"""slide_028 measurement pass 3 — corrected: true circle center (closed fill bbox),
closing-merged blobs, red/orange separation, fragment-merged labels, 12-ray spoke scan,
title/eqbox/badge verification. Compares against slide_027 certified values and the
component's polar rules for the delta blocks.
"""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import json

A = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
H, W = A.shape[:2]
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
out = {}

def sx(fx): return (fx - 18.63) / 0.96123
def sy(fy): return fy / 0.95556

# ---------- 1. true circle center: fill mask + closing ----------
cf = (r > 235) & (g > 235) & (b > 170) & (b < 230)
cf[:, :350] = False
st25 = np.ones((25, 25), bool)
cfc = ndi.binary_closing(cf, structure=st25)
lab, n = ndi.label(cfc)
sizes = ndi.sum(cfc, lab, range(1, n + 1))
big = int(np.argmax(sizes)) + 1
ys, xs = np.where(lab == big)
CXf, CYf = (xs.min() + xs.max()) / 2.0, (ys.min() + ys.max()) / 2.0
radf = ((xs.max() - xs.min()) + (ys.max() - ys.min())) / 4.0
print(f"circle: frame center ({CXf:.1f},{CYf:.1f}) r {radf:.1f}  -> slide ({sx(CXf):.1f},{sy(CYf):.1f}) r {radf:.1f}")
out["circle"] = {"frame_c": [round(CXf, 1), round(CYf, 1)], "frame_r": round(float(radf), 1),
                 "slide_c": [round(sx(CXf), 1), round(sy(CYf), 1)]}

CXs, CYs = 581.0, 297.2  # 027 certified (slide pt)
def polar_s(deg, rad):
    return (CXs + rad * np.cos(np.radians(deg)), CYs - rad * np.sin(np.radians(deg)))

REF_CHIPS = [[762.6, 297.2], [738.4, 204.6], [672.3, 138.6], [581.1, 113.3], [490.4, 139.9]]
REF_HEADS = [[776.4, 188.4], [692.6, 100.5], [585.6, 71.2], [473.3, 101.5]]
REF_LABELS = [[840.2, 236.5], [788.8, 104.1], [642.8, 75.4], [520.6, 75.4]]

def show(name, items):
    print(f"\n== {name} ==")
    for it in items:
        k = it["k"]
        line = f" k={k} ang {it['ang']:6.1f} R_slide {it['Rslide']:6.1f} slide ({it['slide'][0]:6.1f},{it['slide'][1]:6.1f}) wh {it['wh']}"
        if it.get("ref"):
            line += f"  d_cert=({it['slide'][0]-it['ref'][0]:+.1f},{it['slide'][1]-it['ref'][1]:+.1f})"
        if it.get("pred") is not None:
            line += f"  d_polar=({it['slide'][0]-it['pred'][0]:+.1f},{it['slide'][1]-it['pred'][1]:+.1f})"
        print(line)
    out[name] = items

# ---------- 2. chips ----------
ch = ((g - r) > 25) & ((g - b) > 25)
chc = ndi.binary_closing(ch, structure=np.ones((9, 9), bool))
lab, n = ndi.label(chc)
chips = []
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    area = len(ys)
    if area < 500: continue
    h = ys.max() - ys.min(); w = xs.max() - xs.min()
    if w > 120 or h > 120 or (w < 30 and h < 30): continue
    cx, cy = (xs.min() + xs.max()) / 2.0, (ys.min() + ys.max()) / 2.0
    ang = float(np.degrees(np.arctan2(-(cy - CYf), cx - CXf)) % 360)
    k = int(round(ang / 30)) % 12
    if k > 8: continue
    chips.append({"k": k, "ang": round(ang, 1),
                  "Rslide": round(float(np.hypot(sx(cx) - CXs, sy(cy) - CYs)), 1),
                  "slide": [round(sx(cx), 1), round(sy(cy), 1)], "wh": [int(w), int(h)],
                  "area": int(area), "ref": REF_CHIPS[k] if k < 5 else None,
                  "pred": list(polar_s(k * 30, 182.5))})
chips.sort(key=lambda c: c["k"])
show("chips", chips)

# ---------- 3. heads ----------
ah = (r > 160) & ((r - g) > 80) & ((g - b) > 40)
ahc = ndi.binary_closing(ah, structure=np.ones((3, 3), bool))
lab, n = ndi.label(ahc)
heads = []
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    area = len(ys)
    if area < 25 or area > 600: continue
    h = ys.max() - ys.min(); w = xs.max() - xs.min()
    if w > 30 or h > 30: continue
    cx, cy = (xs.min() + xs.max()) / 2.0, (ys.min() + ys.max()) / 2.0
    ang = float(np.degrees(np.arctan2(-(cy - CYf), cx - CXf)) % 360)
    k = (int(round(ang / 30)) % 12) - 1
    if k < 0 or k > 7: continue
    heads.append({"k": k, "ang": round(ang, 1),
                  "Rslide": round(float(np.hypot(sx(cx) - CXs, sy(cy) - CYs)), 1),
                  "slide": [round(sx(cx), 1), round(sy(cy), 1)], "wh": [int(w), int(h)],
                  "area": int(area), "ref": REF_HEADS[k] if k < 4 else None,
                  "pred": list(polar_s((k + 1) * 30, 224.5))})
heads.sort(key=lambda c: c["k"])
show("heads", heads)

# ---------- 4. labels: red (b close to g), fragment-merged by dilation ----------
rl = (r > 150) & ((r - g) > 55) & (g < 185) & (b - g > -15)
Yg, Xg = np.mgrid[0:H, 0:W]
rr = np.hypot(Xg - CXf, Yg - CYf)
ann = rl & (rr > 185) & (rr < 340)
lab_d = ndi.binary_dilation(ann, structure=np.ones((13, 13), bool))
lab, n = ndi.label(lab_d)
labels = []
for i in range(1, n + 1):
    m = (lab == i) & ann
    ys, xs = np.where(m)
    if len(ys) < 14: continue
    cx, cy = xs.mean(), ys.mean()
    ang = float(np.degrees(np.arctan2(-(cy - CYf), cx - CXf)) % 360)
    k = (int(round(ang / 30)) % 12) - 1
    if k < 0 or k > 7: continue
    labels.append({"k": k, "ang": round(ang, 1),
                   "Rslide": round(float(np.hypot(sx(cx) - CXs, sy(cy) - CYs)), 1),
                   "slide": [round(sx(cx), 1), round(sy(cy), 1)],
                   "wh": [int(xs.max() - xs.min()), int(ys.max() - ys.min())],
                   "area": int(len(ys)), "ref": REF_LABELS[k] if k < 4 else None,
                   "pred": list(polar_s((2 * k + 1) * 15, 255))})
# merge duplicates (same k, close positions)
merged = {}
for lb in labels:
    if lb["k"] in merged:
        m0 = merged[lb["k"]]
        tot = m0["area"] + lb["area"]
        m0["slide"] = [round((m0["slide"][0] * m0["area"] + lb["slide"][0] * lb["area"]) / tot, 1),
                       round((m0["slide"][1] * m0["area"] + lb["slide"][1] * lb["area"]) / tot, 1)]
        m0["area"] = tot
    else:
        merged[lb["k"]] = dict(lb)
labels = [merged[k] for k in sorted(merged)]
show("labels", labels)

# ---------- 5. spokes: faint-ink ray scan at all 12 angles ----------
print("\n== faint-ink ray scan (r 135..245 frame from true center) ==")
sp = {}
for deg in range(0, 360, 30):
    hits = 0; tot = 0
    for rr_ in np.arange(135, 246, 1.0):
        x = CXf + rr_ * np.cos(np.radians(deg)); y = CYf - rr_ * np.sin(np.radians(deg))
        xi, yi = int(round(x)), int(round(y))
        if not (0 <= xi < W and 0 <= yi < H): continue
        c = A[yi, xi]
        d = (233 - c[0]) + (233 - c[1]) + (231 - c[2])
        tot += 1
        if d > 45: hits += 1
    sp[deg] = [hits, tot]
    print(f" {deg:3d}deg: faint hits {hits}/{tot}")
out["spokes"] = sp

# ---------- 6. title lines (x<360 to exclude label4) ----------
red = (r > 130) & (g < 100) & (b < 100)
tit = red.copy()
tit[:, 360:] = False; tit[:45] = False; tit[160:] = False
rows_ink = tit.sum(axis=1)
bands, inb = [], False
for y in range(45, 160):
    if rows_ink[y] > 0 and not inb: y0 = y; inb = True
    elif rows_ink[y] == 0 and inb: bands.append((y0, y - 1)); inb = False
if inb: bands.append((y0, 159))
print("\n== title lines (027 certified ink tops slide 61.7/89.0/117.2; L1 ink w 240.3, L2 242.4, L3 108.2) ==")
tt = []
for (y0, y1) in bands:
    band = tit[y0:y1 + 1]
    xs2 = np.where(band.sum(axis=0) > 0)[0]
    tt.append({"frame_y": [int(y0), int(y1)], "frame_x": [int(xs2.min()), int(xs2.max())],
               "slide_ytop": round(sy(y0), 1), "slide_x": [round(sx(xs2.min()), 1), round(sx(xs2.max()), 1)],
               "w_slide": round(sx(xs2.max()) - sx(xs2.min()), 1)})
    print(f" y {y0}..{y1} x {xs2.min()}..{xs2.max()}  slide ytop {sy(y0):.1f} x {sx(xs2.min()):.1f}..{sx(xs2.max()):.1f} w {sx(xs2.max())-sx(xs2.min()):.1f}")
out["title"] = tt

# ---------- 7. eq box ----------
eq = (r > 235) & (g > 235) & (b > 170) & (b < 230)
eq[:, 260:] = False; eq[:160] = False; eq[280:] = False
lab, n = ndi.label(eq)
if n:
    sizes = ndi.sum(eq, lab, range(1, n + 1))
    big = int(np.argmax(sizes)) + 1
    ys, xs = np.where(lab == big)
    print(f"\n== eq box: frame x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}  (027 certified frame [82,182,216,246]) ==")
    out["eqbox"] = {"frame": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]}
    sub = A[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    sr, sg, sb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    ink = ((sb > 120) & (sr < 130) & (sg < 130)) | ((sg > 110) & (sg - sr > 40) & (sg - sb > 40)) | ((sr > 140) & (sg < 100) & (sb < 100) & (sr - sg > 60))
    rws = ink.sum(axis=1)
    inb = False; lns = []
    for yy in range(ink.shape[0]):
        if rws[yy] > 0 and not inb: yy0 = yy; inb = True
        elif rws[yy] == 0 and inb: lns.append((yy0, yy - 1)); inb = False
    if inb: lns.append((yy0, ink.shape[0] - 1))
    for i, (yy0, yy1) in enumerate(lns):
        bnd = ink[yy0:yy1 + 1]
        xs4 = np.where(bnd.sum(axis=0) > 0)[0]
        print(f"  eq L{i+1}: frame y {ys.min()+yy0}..{ys.min()+yy1} x {xs.min()+xs4.min()}..{xs.min()+xs4.max()}")

# ---------- 8. badge numeral ----------
sub = A[52:92, 855:900]
dk = (sub[:, :, 0] < 150) & (sub[:, :, 1] < 150) & (sub[:, :, 2] < 150)
ysb, xsb = np.where(dk)
if len(ysb):
    print(f"\n== badge numeral ink: x {855+xsb.min()}..{855+xsb.max()} y {52+ysb.min()}..{52+ysb.max()} (h {ysb.max()-ysb.min()+1} w {xsb.max()-xsb.min()+1}) n={dk.sum()} ==")
    out["badge_numeral"] = {"frame_bbox": [int(855+xsb.min()), int(52+ysb.min()), int(855+xsb.max()), int(52+ysb.max())], "n": int(dk.sum())}

json.dump(out, open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide028/measure3.json", "w"), indent=1)
print("\nsaved measure3.json")
