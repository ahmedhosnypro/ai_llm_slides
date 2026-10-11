#!/usr/bin/env python3
"""Measure slide_014.jpg (960x540, 1px = 1pt): panels, captions, arc, title, figure placement."""
import json
import numpy as np
from PIL import Image

FRAME = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_014.jpg"
im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
out = {}

def bbox(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(mask.sum())]

R, G, B = a[..., 0], a[..., 1], a[..., 2]

# --- red-ish ink (title, captions, arc, badge numeral?) ---
red = (R > 120) & (R - G > 60) & (R - B > 60)
out["red_all"] = bbox(red)

# --- blue-ish ink (takeaway) ---
blue = (B > 120) & (B - R > 60) & (B - G > 60)
out["blue_all"] = bbox(blue)

# --- white-ish pixels (panels) ---
white = (R > 235) & (G > 235) & (B > 235)
# label connected components of white via simple flood (scipy may not exist; use numpy labeling)
try:
    from scipy import ndimage
    lab, n = ndimage.label(white)
    sizes = ndimage.sum(white, lab, range(1, n + 1))
    order = np.argsort(sizes)[::-1][:6]
    comps = []
    for i in order:
        m = lab == (i + 1)
        comps.append({"bbox": bbox(m), "px": int(sizes[i])})
    out["white_components_top6"] = comps
except ImportError:
    out["white_components"] = "no scipy; coarse rows"

# --- gray panel (E9E9E7) extent ---
gray = (np.abs(R - 0xE9) < 10) & (np.abs(G - 0xE9) < 10) & (np.abs(B - 0xE7) < 10)
out["gray_panel"] = bbox(gray)

# --- red arc: red pixels in gutter x 400..510, y 240..370 ---
gut = np.zeros_like(red)
gut[230:380, 395:520] = True
arc = red & gut
out["arc_bbox"] = bbox(arc)
ys, xs = np.where(arc)
if len(xs) > 30:
    cx, cy = xs.mean(), ys.mean()
    ang = np.degrees(np.arctan2(-(ys - cy), xs - cx))  # 0=east, CCW positive, y up
    hist, edges = np.histogram(ang, bins=36, range=(-180, 180))
    out["arc_centroid"] = [float(cx), float(cy)]
    out["arc_angular_hist_10deg"] = [int(v) for v in hist]
    out["arc_extent"] = [float(xs.min()), float(xs.max()), float(ys.min()), float(ys.max())]
    # thickness profile per angle bin (radial spread)
    rr = np.hypot(xs - cx, ys - cy)
    out["arc_radius_mean_std"] = [float(rr.mean()), float(rr.std())]

# --- red caption region (right header) x 440..760, y 100..150 ---
hdr = np.zeros_like(red)
hdr[95:155, 430:780] = True
out["red_caption_bbox"] = bbox(red & hdr)

# --- blue takeaway x 430..900, y 460..540 ---
tk = np.zeros_like(blue)
tk[455:540, 420:920] = True
out["blue_takeaway_bbox"] = bbox(blue & tk)

# --- title: red pixels x 150..820, y 45..100 ---
tit = np.zeros_like(red)
tit[45:100, 150:830] = True
out["title_bbox"] = bbox(red & tit)

# --- badge numeral region (dark pixels in badge circle x 875..911, y 53..89) ---
dark = (R < 100) & (G < 100) & (B < 100)
bd = np.zeros_like(dark)
bd[53:90, 874:912] = True
out["badge_numeral_bbox"] = bbox(dark & bd)

# --- pastel fills present? sample color modes in left panel area ---
def color_modes(mask, k=14):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return []
    cols = a[ys, xs]
    # quantize to /16 buckets
    q = (cols // 16)
    keys, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
    order = np.argsort(counts)[::-1][:k]
    res = []
    for i in order:
        c = keys[i] * 16 + 8
        res.append(["#%02X%02X%02X" % tuple(c), int(counts[i])])
    return res

lp = np.zeros_like(white, dtype=bool)
lp[100:540, 60:440] = True
out["left_region_modes"] = color_modes(lp & white | (lp & ~white & ~gray & ~red & ~blue), k=10)

print(json.dumps(out, indent=1))
