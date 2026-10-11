#!/usr/bin/env python3
"""Measure slide_018.jpg (960x540 frame, video 002 zoomed-out capture).

Outputs all landmarks needed to build the recreation:
  - chrome border landmarks (red panel border strokes) -> frame->slide mapping
  - badge bbox (yellow) -> cross-check vs house position
  - letterbox rows (black strip, bottom) -> omitted from build
  - title ink bbox + core color
  - white box bbox + border color + shadow probe
  - content lines: per-line ink bands + per-color run spans + core colors
  - cursor artifact bbox (dark pixels below title) -> omitted
Run: python3 measure_original.py
"""
import json
import numpy as np
from PIL import Image

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_018.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def bbox(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]  # x0,y0,x1,y1 inclusive

def core_color(mask, region=None):
    m = mask if region is None else (mask & region)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    # median of the most saturated quartile (ink core, away from JPEG halo)
    px = im[ys, xs]
    sat = px.max(axis=1) - px.min(axis=1)
    idx = np.argsort(sat)[-max(1, len(sat) // 4):]
    med = np.median(px[idx], axis=0).astype(int)
    return "#%02X%02X%02X" % tuple(med)

# --- masks -------------------------------------------------------------------
# border stroke is sub-pixel + JPEG-haloed (core ~(110,45,55)); soft mask for
# chrome landmarks, strict mask for saturated text ink (title / "Encoding")
red_soft = ((R - G) > 35) & ((R - B) > 25) & (R > 60)
red = (R > 140) & (G < 90) & (B < 90) & ((R - G) > 80) & ((R - B) > 80)
blue = (B > 110) & (R < 110) & (G < 110) & ((B - R) > 60) & ((B - G) > 60)
mag = (R > 130) & (B > 130) & (G < 110) & ((R - G) > 60) & ((B - G) > 60)
yellow = (R > 225) & (G > 225) & (B > 90) & (B < 210)
black = (R < 60) & (G < 60) & (B < 60)
white = (R > 240) & (G > 240) & (B > 240)
dark = (R < 130) & (G < 130) & (B < 130)

out = {"frame_size": [W, H]}

# --- chrome border landmarks (red stroke centroids) ---------------------------
def stroke_centroid_col(x0, x1):
    prof = red_soft[:, x0:x1].sum(axis=0)
    peak = int(np.argmax(prof)) + x0
    lo, hi = max(x0, peak - 4), min(x1, peak + 5)
    w = red_soft[:, lo:hi].sum(axis=0).astype(float)
    return float((np.arange(lo, hi) * w).sum() / w.sum())

def stroke_centroid_row(y0, y1):
    prof = red_soft[y0:y1, :].sum(axis=1)
    peak = int(np.argmax(prof)) + y0
    lo, hi = max(y0, peak - 4), min(y1, peak + 5)
    w = red_soft[lo:hi, :].sum(axis=1).astype(float)
    return float((np.arange(lo, hi) * w).sum() / w.sum())

Lf = stroke_centroid_col(30, 100)
Rf = stroke_centroid_col(860, 940)
Tf = stroke_centroid_row(20, 80)
Bf = stroke_centroid_row(495, 530)
out["chrome_frame"] = {"left": Lf, "right": Rf, "top": Tf, "bottom": Bf}

# frame -> slide mapping (slide chrome anchors: 42, 919, 45, 540)
sx = (Rf - Lf) / (919 - 42)
sy = (Bf - Tf) / (540 - 45)
x0 = Lf - sx * 42
y0 = Tf - sy * 45
out["mapping"] = {"scale_x": sx, "scale_y": sy, "x0": x0, "y0": y0,
                  "slide_of": lambda fx, fy: ((fx - x0) / sx, (fy - y0) / sy)}

def to_slide(bbox4):
    x0f, y0f, x1f, y1f = bbox4
    a = (x0f - x0) / sx; b = (y0f - y0) / sy
    c = (x1f + 1 - x0) / sx; d = (y1f + 1 - y0) / sy  # +1: exclusive right/bottom
    return [round(a, 2), round(b, 2), round(c, 2), round(d, 2)]  # slide pts

# --- letterbox ----------------------------------------------------------------
row_mean = im.mean(axis=(1, 2))
lb = [int(i) for i in range(H) if row_mean[i] < 40]
out["letterbox_rows"] = [min(lb), max(lb)] if lb else None

# --- badge --------------------------------------------------------------------
ym = yellow.copy(); ym[:, :820] = False; ym[140:, :] = False
bb = bbox(ym)
out["badge_frame_bbox"] = bb
bcx, bcy = (bb[0] + bb[3] - 1) / 2, (bb[1] + bb[2] - 1) / 2
out["badge_frame_center"] = [bcx, bcy]
out["badge_slide_center"] = [round((bcx - x0) / sx, 2), round((bcy - y0) / sy, 2)]
out["badge_colors"] = {"fill": core_color(ym)}
ring = (R > 80) & (R < 150) & (G > 60) & (G < 130) & (B > 170) & (B < 235)
ring[:, :820] = False; ring[140:, :] = False
out["badge_ring_color"] = core_color(ring)

# --- title --------------------------------------------------------------------
tm = red.copy(); tm[:150, :] = False; tm[290:, :] = False; tm[:, :150] = False; tm[:, 820:] = False
tb = bbox(tm)
out["title_frame_bbox"] = tb
out["title_slide_bbox"] = to_slide(tb)
out["title_color"] = core_color(tm)

# cursor artifact: dark pixels below title band, above box, inside panel
cm = dark.copy(); cm[:tb[3] + 2, :] = False; cm[280:, :] = False
cm[:, :int(Lf) + 5] = False; cm[:, int(Rf) - 5:] = False
out["cursor_frame_bbox"] = bbox(cm)

# --- white box ----------------------------------------------------------------
# search white pixels strictly inside the panel interior
inpanel = np.zeros_like(white)
inpanel[int(Tf) + 6:int(Bf) - 6, int(Lf) + 6:int(Rf) - 6] = True
wm = white & inpanel
# largest dense rectangle: row profile then column profile of white counts
rows = wm.sum(axis=1)
box_rows = [i for i in range(H) if rows[i] > 200]
cols = wm[box_rows[0]:box_rows[-1] + 1, :].sum(axis=0)
box_cols = [j for j in range(W) if cols[j] > (box_rows[-1] - box_rows[0]) * 0.5]
wb = [min(box_cols), min(box_rows), max(box_cols), max(box_rows)]
out["whitebox_frame_bbox"] = wb
out["whitebox_slide_bbox"] = to_slide(wb)
# box border color: pixels just outside the white area along its top edge
by0, bx0, bx1 = wb[1], wb[0], wb[2]
band = im[by0 - 3:by0, bx0 + 20:bx1 - 20].reshape(-1, 3)
grayish = band[(band.max(axis=1) - band.min(axis=1) < 30) & (band.mean(axis=1) > 140) & (band.mean(axis=1) < 225)]
out["box_border_color"] = "#%02X%02X%02X" % tuple(np.median(grayish, axis=0).astype(int)) if len(grayish) else None
# shadow probe: mean luminance just below box bottom edge vs panel further below
sh1 = im[wb[3] + 2:wb[3] + 8, bx0 + 20:bx1 - 20].mean()
sh2 = im[wb[3] + 20:wb[3] + 30, bx0 + 20:bx1 - 20].mean()
out["shadow_probe"] = {"just_below": round(float(sh1), 1), "further_below": round(float(sh2), 1)}

# --- content lines ------------------------------------------------------------
# line bands: rows inside the box with any blue/red/mag ink
inbox = np.zeros_like(blue)
inbox[wb[1] + 2:wb[3] - 1, wb[0] + 2:wb[2] - 1] = True
ink = (blue | red | mag) & inbox
rprof = ink.sum(axis=1)
bands = []
in_b = False
for i in range(wb[1], wb[3] + 1):
    if rprof[i] > 2 and not in_b:
        b0 = i; in_b = True
    elif rprof[i] <= 2 and in_b:
        bands.append((b0, i - 1)); in_b = False
if in_b:
    bands.append((b0, wb[3]))
out["line_bands_frame"] = bands

lines = []
for (ya, yb) in bands:
    lmask = np.zeros_like(ink); lmask[ya:yb + 1, :] = True
    seg = {}
    for name, m in (("blue", blue), ("red", red), ("mag", mag)):
        s = m & lmask & inbox
        if s.sum() > 20:
            bb2 = bbox(s)
            seg[name] = {"frame_bbox": bb2, "color": core_color(s), "px": int(s.sum())}
    allink = (blue | red | mag) & lmask & inbox
    ab = bbox(allink)
    lines.append({
        "band_frame": [ya, yb],
        "ink_frame_bbox": ab,
        "ink_slide_bbox": to_slide(ab),
        "segments": seg,
    })
out["lines"] = lines
out["line1_slide"] = lines[0]["ink_slide_bbox"] if lines else None
out["line2_slide"] = lines[1]["ink_slide_bbox"] if len(lines) > 1 else None

# JSON-safe dump (mapping lambda dropped)
def dump(o):
    if isinstance(o, dict):
        return {k: dump(v) for k, v in o.items() if k != "slide_of"}
    return o
print(json.dumps(dump(out), indent=1))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide018/measure_original.json", "w") as f:
    json.dump(dump(out), f, indent=1)
