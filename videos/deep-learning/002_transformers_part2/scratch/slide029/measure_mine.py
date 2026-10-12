#!/usr/bin/env python3
"""slide029 delta measurement campaign (mine) — PIL on unique_slides/slide_029.jpg.

Frame->slide mapping (certified, build/slide_002.js + components/slide_027.js):
  fx = 18.63 + 0.96123*slide_x ; fy = 0.95556*slide_y
  => slide_x = (fx - 18.63)/0.96123 ; slide_y = fy/0.95556
Outputs measure_mine.json + crops for the vision gate.
"""
import json
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
A = np.asarray(Image.open(f"{BASE}/unique_slides/slide_029.jpg").convert("RGB")).astype(int)
H, W = A.shape[:2]
SLIDE_LAST_ROW = 516  # rows 517..539 are off-slide letterbox/bar

def to_slide(fx, fy):
    return ((fx - 18.63) / 0.96123, fy / 0.95556)

out = {}

R, G, B = A[:, :, 0], A[:, :, 1], A[:, :, 2]

# ---------- 1. NOTE BOX (bottom-left white rect + red border + text bands) ----------
# search window: frame x 0..430, y 360..516
win = np.zeros((H, W), bool); win[360:517, 0:430] = True
white = win & (R > 235) & (G > 235) & (B > 235)
ys, xs = np.where(white)
nb = {"white_bbox_frame": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
      "white_npx": int(white.sum())}
# red border: strong red in the window, excluding text rows (text is inside white)
red = win & (R > 140) & (R - G > 70) & (R - B > 70)
ys2, xs2 = np.where(red)
nb["red_bbox_frame"] = [int(xs2.min()), int(ys2.min()), int(xs2.max()), int(ys2.max())]
# border column/row profiles (which cols/rows are red)
nb["red_cols"] = sorted(set(int(x) for x in xs2))
nb["red_rows"] = sorted(set(int(y) for y in ys2))
# text bands inside the white box
inner = np.zeros((H, W), bool)
x0, y0, x1, y1 = nb["white_bbox_frame"]
inner[y0 + 2:y1 - 1, x0 + 2:x1 - 1] = True
blue = inner & (B > 130) & (B - R > 60) & (B - G > 60)
yellow = inner & (R > 200) & (G > 180) & (B < 120) & (R - B > 120)
redtxt = inner & (R > 140) & (R - G > 70) & (R - B > 70)
def bands(mask, axis):
    prof = mask.sum(axis=axis)
    idx = np.where(prof > 0)[0]
    if len(idx) == 0: return []
    bands, s = [], idx[0]
    for i in range(1, len(idx)):
        if idx[i] != idx[i - 1] + 1:
            bands.append([int(s), int(idx[i - 1])]); s = idx[i]
    bands.append([int(s), int(idx[-1])])
    return bands
def bbox(mask):
    ys, xs = np.where(mask)
    if len(ys) == 0: return None
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())], int(mask.sum())
for name, m in [("blue", blue), ("yellow", yellow), ("red", redtxt)]:
    bb = bbox(m)
    nb[name] = {"rows": bands(m, 1), "cols": bands(m, 0), "bbox": bb[0], "npx": bb[1]} if bb else None
out["notebox"] = nb

# ---------- 2. TITLE line 1 ink ----------
twin = np.zeros((H, W), bool); twin[52:105, 40:340] = True
tred = twin & (R > 140) & (R - G > 70) & (R - B > 70)
out["title_rows_bands"] = bands(tred, 1)
out["title_all_bbox"] = bbox(tred)
# line 1 only (first row band)
tr = bands(tred, 1)
if tr:
    l1 = np.zeros((H, W), bool); l1[tr[0][0]:tr[0][1] + 1, :] = tred[tr[0][0]:tr[0][1] + 1, :]
    out["title_line1_bbox"] = bbox(l1)

# ---------- 3. CHIPS k=9,10,11 (green fill CCFFCC blobs) ----------
gwin = np.zeros((H, W), bool); gwin[300:517, 380:900] = True
gfill = gwin & (np.abs(R - 204) < 40) & (np.abs(G - 255) < 25) & (np.abs(B - 204) < 40) & (G - R > 25) & (G - B > 25)
# connected components via simple flood (scipy may not exist) — use label by rows
try:
    from scipy import ndimage
    lab, n = ndimage.label(gfill)
    chips = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 200: continue
        bb = bbox(m)
        cx, cy = (bb[0][0] + bb[0][2]) / 2, (bb[0][1] + bb[0][3]) / 2
        sx, sy = to_slide(cx, cy)
        chips.append({"bbox_frame": bb[0], "npx": bb[1], "center_frame": [cx, cy],
                      "center_slide": [round(sx, 2), round(sy, 2)]})
    out["chips_green"] = chips
except ImportError:
    out["chips_green"] = "no scipy — fallback below"

# ---------- 4. ARCS pale stroke presence per angle bin ----------
CX, CY = 581.0, 297.2
yy, xx = np.mgrid[0:H, 0:W]
sx_full = (xx - 18.63) / 0.96123
sy_full = yy / 0.95556
dx = sx_full - CX; dy = sy_full - CY
rr = np.sqrt(dx * dx + dy * dy)
ang = (np.degrees(np.arctan2(-dy, dx))) % 360
pale = (R > 225) & (np.abs(G - 201) < 20) & (B > 150) & (B < 195) & (R - B > 40) & (R - B < 85) & (rr > 205) & (rr < 250) & (yy < SLIDE_LAST_ROW)
bins = {}
for a in range(0, 360, 5):
    m = pale & (ang >= a) & (ang < a + 5)
    c = int(m.sum())
    if c > 0: bins[a] = c
out["pale_angle_bins"] = bins

# ---------- 5. HEADS orange E06010 ----------
ohw = np.zeros((H, W), bool); ohw[40:516, 300:900] = True
orange = ohw & (R > 180) & (G > 55) & (G < 150) & (B < 80) & (R - G > 80)
try:
    from scipy import ndimage
    lab, n = ndimage.label(orange)
    heads = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 12: continue
        bb = bbox(m)
        cx, cy = (bb[0][0] + bb[0][2]) / 2, (bb[0][1] + bb[0][3]) / 2
        sx, sy = to_slide(cx, cy)
        heads.append({"bbox_frame": bb[0], "npx": bb[1],
                      "center_slide": [round(sx, 2), round(sy, 2)],
                      "angle_deg": round(float(np.degrees(np.arctan2(-(sy - CY), sx - CX))) % 360, 1)})
    out["heads_orange"] = heads
except ImportError:
    out["heads_orange"] = "no scipy"

# ---------- 6. '+w' LABELS red CC0000 outside circle/boxes ----------
# red text px in the annulus zone r>235 (outside chips/head zone), excluding title/badge/notebox/eqbox
lzone = (rr > 233) & (rr < 300) & (yy > 100) & (yy < SLIDE_LAST_ROW) & (xx > 40) & (xx < 918)
lred = lzone & (R > 140) & (R - G > 70) & (R - B > 70)
# exclude the horizontal dashed axis band? axis is faded, not caught by this mask
try:
    from scipy import ndimage
    lab, n = ndimage.label(lred)
    labels = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 25: continue
        bb = bbox(m)
        cx, cy = (bb[0][0] + bb[0][2]) / 2, (bb[0][1] + bb[0][3]) / 2
        sx, sy = to_slide(cx, cy)
        labels.append({"bbox_frame": bb[0], "npx": bb[1],
                       "center_slide": [round(sx, 2), round(sy, 2)],
                       "angle_deg": round(float(np.degrees(np.arctan2(-(sy - CY), sx - CX))) % 360, 1),
                       "r_pt": round(float(np.hypot(sx - CX, sy - CY)), 1)})
    out["labels_red"] = labels
except ImportError:
    out["labels_red"] = "no scipy"

# ---------- 7. bottom-edge red band (rows 510..516) ----------
edge = np.zeros((H, W), bool); edge[505:517, 40:918] = True
ered = edge & (R > 140) & (R - G > 70) & (R - B > 70)
out["bottom_edge_red"] = {"bands_cols": bands(ered, 0), "bands_rows": bands(ered, 1), "npx": int(ered.sum())}

with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide029/measure_mine.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
