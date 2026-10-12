#!/usr/bin/env python3
"""slide029 measurement round 2: chrome landmarks, title per-line, note box detail,
arc corridors 8-11 vs frame 28, k=8 label hunt, chip debug, color samples."""
import json
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
A29 = np.asarray(Image.open(f"{BASE}/unique_slides/slide_029.jpg").convert("RGB")).astype(int)
A28 = np.asarray(Image.open(f"{BASE}/unique_slides/slide_028.jpg").convert("RGB")).astype(int)
H, W = A29.shape[:2]
out = {}

def to_slide(fx, fy):
    return ((fx - 18.63) / 0.96123, fy / 0.95556)
def to_slide_x(fx):
    return (fx - 18.63) / 0.96123
def to_slide_y(fy):
    return fy / 0.95556

def bands(mask, axis, min_gap=1):
    prof = mask.sum(axis=axis)
    idx = np.where(prof > 0)[0]
    if len(idx) == 0: return []
    res, s = [], idx[0]
    for i in range(1, len(idx)):
        if idx[i] > idx[i - 1] + min_gap:
            res.append([int(s), int(idx[i - 1])]); s = idx[i]
    res.append([int(s), int(idx[-1])])
    return res

# ---------- a. chrome landmarks on frame 29 ----------
R, G, B = A29[:, :, 0], A29[:, :, 1], A29[:, :, 2]
redm = (R > 140) & (R - G > 70) & (R - B > 70)
# panel left border: strong-red cols in rows 100..300 (clear zone)
colprof = redm[100:300, :].sum(axis=0)
out["chrome_left_cols"] = [int(c) for c in np.where(colprof > 50)[0]]
# panel top border: rows with red across cols 200..800
rowprof = redm[:, 200:800].sum(axis=1)
out["chrome_top_rows"] = [int(r) for r in np.where(rowprof > 300)[0]]
# badge: yellow FDFD96 ring purple 6A5ACD — find purple ring px
purple = (np.abs(R - 106) < 45) & (np.abs(G - 90) < 45) & (np.abs(B - 205) < 45) & (B - G > 60)
ys, xs = np.where(purple[30:110, 840:930])
if len(xs):
    out["badge_ring_center_frame"] = [round(float(xs.mean()) + 840, 1), round(float(ys.mean()) + 30, 1)]
    out["badge_ring_center_slide"] = [round(to_slide_x(xs.mean() + 840), 1), round(to_slide_y(ys.mean() + 30), 1)]

# ---------- b. title per-line ink, frames 29 AND 28, same method ----------
def title_lines(A):
    Rr, Gg, Bb = A[:, :, 0], A[:, :, 1], A[:, :, 2]
    t = (Rr > 140) & (Rr - Gg > 70) & (Rr - Bb > 70)
    twin = np.zeros(A.shape[:2], bool); twin[52:135, 40:340] = True
    t = t & twin
    rows = bands(t, 1, min_gap=2)
    res = []
    for r0, r1 in rows[:4]:
        sub = t[r0:r1 + 1, :]
        cols = bands(sub, 0, min_gap=8)  # merge word gaps up to 8px
        x0, x1 = cols[0][0], cols[-1][1]
        res.append({"rows": [int(r0), int(r1)],
                    "cols": [int(x0), int(x1)],
                    "slide_x": [round(to_slide_x(x0), 2), round(to_slide_x(x1), 2)],
                    "slide_y": [round(to_slide_y(r0), 2), round(to_slide_y(r1), 2)],
                    "center_slide_x": round((to_slide_x(x0) + to_slide_x(x1)) / 2, 2),
                    "npx": int(sub.sum())})
    return res
out["title29"] = title_lines(A29)
out["title28"] = title_lines(A28)

# ---------- c. note box detail ----------
nb = {}
win = np.zeros((H, W), bool); win[380:515, 46:430] = True
Rr, Gg, Bb = A29[:, :, 0], A29[:, :, 1], A29[:, :, 2]
white = win & (Rr > 243) & (Gg > 243) & (Bb > 243)
ys, xs = np.where(white)
nb["white_bbox_frame"] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
nb["white_npx"] = int(white.sum())
redw = win & (Rr > 140) & (Rr - Gg > 70) & (Rr - Bb > 70)
colcnt = redw.sum(axis=0); rowcnt = redw.sum(axis=1)
nb["border_cols_gt40"] = [int(c) + 46 for c in np.where(colcnt > 40)[0]]
nb["border_rows_gt40"] = [int(r) + 380 for r in np.where(rowcnt > 40)[0]]
nb["border_cols_gt150"] = [int(c) + 46 for c in np.where(colcnt > 150)[0]]
nb["border_rows_gt100"] = [int(r) + 380 for r in np.where(rowcnt > 100)[0]]
# per-line text extents
blue = win & (Bb > 130) & (Bb - Rr > 60) & (Bb - Gg > 60)
yel = win & (Rr > 200) & (Gg > 180) & (Bb < 130) & (Rr - Bb > 110)
redt = win & (Rr > 140) & (Rr - Gg > 70) & (Rr - Bb > 70)
blue_rows = bands(blue, 1, 2)
nb["blue_rows"] = blue_rows
for i, (r0, r1) in enumerate(blue_rows):
    sub = blue[r0:r1 + 1, :]
    cb = bands(sub, 0, 12)
    nb[f"blue_L{i+1}_cols"] = [int(cb[0][0]) + 46, int(cb[-1][1]) + 46]
yel_rows = bands(yel, 1, 2)
nb["yellow_rows"] = yel_rows
if yel_rows:
    sub = yel[yel_rows[0][0]:yel_rows[-1][1] + 1, :]
    cb = bands(sub, 0, 6)
    nb["yellow_cols"] = [int(cb[0][0]) + 46, int(cb[-1][1]) + 46]
# red text lines below blue (exclude border cols)
redtxt = redt.copy()
redtxt[:, :70] = False; redtxt[:, 360:] = False
red_rows = bands(redtxt, 1, 2)
nb["red_text_rows"] = red_rows
for i, (r0, r1) in enumerate(red_rows):
    sub = redtxt[r0:r1 + 1, :]
    cb = bands(sub, 0, 12)
    if cb:
        nb[f"red_L{i+1}_cols"] = [int(cb[0][0]) + 46, int(cb[-1][1]) + 46]
# color samples
def sample(y, x, r=2):
    reg = A29[y - r:y + r + 1, x - r:x + r + 1].reshape(-1, 3)
    return reg.mean(axis=0).round(0).tolist()
nb["sample_blue_text"] = sample(407, 100)
nb["sample_red_text_L3"] = sample(461, 120)
nb["sample_yellow_hl"] = sample(406, 180)
nb["sample_border_top"] = sample(394, 200)
nb["sample_white_fill"] = sample(440, 300)
out["notebox2"] = nb

# ---------- d. arc corridors 8..11: pale ink on 29 vs 28 ----------
def pale_count(A, a0, a1, r0=210, r1=240):
    Rr, Gg, Bb = A[:, :, 0], A[:, :, 1], A[:, :, 2]
    yy, xx = np.mgrid[0:A.shape[0], 0:A.shape[1]]
    sx = (xx - 18.63) / 0.96123; sy = yy / 0.95556
    dx = sx - 581.0; dy = sy - 297.2
    rr = np.sqrt(dx * dx + dy * dy)
    ang = (np.degrees(np.arctan2(-dy, dx))) % 360
    m = (rr > r0) & (rr < r1) & (ang >= a0) & (ang < a1) & (yy < 514)
    # pale salmon F0C9B0 on gray E9E9E7 or on circle fill: R high, R-B 30..90, G between
    p = m & (Rr > 215) & (Rr - Bb > 25) & (Rr - Bb < 95) & (Rr - Gg > 8) & (Rr - Gg < 60) & (Gg > Bb - 5)
    return int(p.sum())
out["arc_corr"] = {}
for k in [7, 8, 9, 10, 11]:
    a0, a1 = k * 30 + 13, (k + 1) * 30 - 2
    out["arc_corr"][f"k{k}"] = {"a": [a0, a1], "f29": pale_count(A29, a0, a1), "f28": pale_count(A28, a0, a1)}
# control: arc 3 (exists on both)
out["arc_corr"]["k3_ctrl"] = {"a": [43, 58], "f29": pale_count(A29, 43, 58), "f28": pale_count(A28, 43, 58)}

# ---------- e. k=8 label hunt: red ink below circle, cols 430..680, rows 470..516 ----------
Rr, Gg, Bb = A29[:, :, 0], A29[:, :, 1], A29[:, :, 2]
zone = np.zeros((H, W), bool); zone[470:515, 430:680] = True
zred = zone & (Rr > 140) & (Rr - Gg > 70) & (Rr - Bb > 70)
try:
    from scipy import ndimage
    lab, n = ndimage.label(zred)
    blobs = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 15: continue
        ys, xs = np.where(m)
        blobs.append({"bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                      "npx": int(m.sum()),
                      "center_slide": [round(to_slide_x((xs.min() + xs.max()) / 2), 2),
                                        round(to_slide_y((ys.min() + ys.max()) / 2), 2)]})
    out["k8_label_hunt"] = blobs
except ImportError:
    out["k8_label_hunt"] = "no scipy"
# also rows 503..516 anywhere cols 400..700 (label tops above bottom edge)
zone2 = np.zeros((H, W), bool); zone2[500:515, 400:700] = True
z2 = zone2 & (Rr > 140) & (Rr - Gg > 70) & (Rr - Bb > 70)
out["bottom_label_zone_rows"] = bands(z2, 1, 1)
cb = bands(z2, 0, 4)
out["bottom_label_zone_cols"] = [[int(c[0]) + 400, int(c[1]) + 400] for c in cb]

# ---------- f. chip green debug ----------
reg = A29[440:460, 560:600].reshape(-1, 3)
out["chip9_region_sample_mean"] = reg.mean(axis=0).round(0).tolist()
gfill = (np.abs(Rr - 204) < 45) & (Gg > 225) & (np.abs(Bb - 204) < 45) & (Gg - Rr > 20) & (Gg - Bb > 20)
zw = np.zeros((H, W), bool); zw[300:515, 380:900] = True
gfill = gfill & zw
try:
    from scipy import ndimage
    lab, n = ndimage.label(gfill)
    chips = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 150: continue
        ys, xs = np.where(m)
        cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
        chips.append({"bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                      "npx": int(m.sum()),
                      "center_slide": [round(to_slide_x(cx), 2), round(to_slide_y(cy), 2)],
                      "angle": round(float(np.degrees(np.arctan2(-(to_slide_y(cy) - 297.2), to_slide_x(cx) - 581))) % 360, 1)})
    out["chips_green2"] = sorted(chips, key=lambda c: c["angle"])
except ImportError:
    out["chips_green2"] = "no scipy"

with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide029/measure_mine2.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
