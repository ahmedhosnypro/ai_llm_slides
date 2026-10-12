#!/usr/bin/env python3
"""slide029 round 3: diff-based arc corridors, full +w label centroids, note box
border raw samples, glyph color samples, k=10 '+' check, k=11 absence check."""
import json
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
A29 = np.asarray(Image.open(f"{BASE}/unique_slides/slide_029.jpg").convert("RGB")).astype(int)
A28 = np.asarray(Image.open(f"{BASE}/unique_slides/slide_028.jpg").convert("RGB")).astype(int)
H, W = A29.shape[:2]
out = {}

def to_slide_x(fx): return (fx - 18.63) / 0.96123
def to_slide_y(fy): return fy / 0.95556

# ---------- 1. diff-based arc corridors (new ink on 29) ----------
diff = np.abs(A29 - A28).max(axis=2) > 45
yy, xx = np.mgrid[0:H, 0:W]
sx = (xx - 18.63) / 0.96123; sy = yy / 0.95556
dx = sx - 581.0; dy = sy - 297.2
rr = np.sqrt(dx * dx + dy * dy)
ang = (np.degrees(np.arctan2(-dy, dx))) % 360
corr = {}
for k in [0, 3, 6, 7, 8, 9, 10, 11]:
    a0, a1 = k * 30 + 13, (k + 1) * 30 - 2
    m = diff & (rr > 208) & (rr < 242) & (ang >= a0) & (ang < a1) & (yy < 514)
    corr[f"k{k}"] = int(m.sum())
out["diff_corridors"] = corr
# controls should be ~0 (identical ink on both frames); new arcs large.

# ---------- 2. full +w label centroids (include '+' glyph), windows ----------
def label_ink(x0, x1, y0, y1, min_npx=8):
    R, G, B = A29[:, :, 0], A29[:, :, 1], A29[:, :, 2]
    win = np.zeros((H, W), bool); win[y0:y1, x0:x1] = True
    red = win & (R > 140) & (R - G > 60) & (R - B > 60)
    ys, xs = np.where(red)
    if len(xs) < min_npx: return None
    bx = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    cx, cy = (bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2
    return {"bbox_frame": bx, "npx": int(len(xs)),
            "center_slide": [round(to_slide_x(cx), 2), round(to_slide_y(cy), 2)],
            "ink_center_slide_bbox": [round(to_slide_x(bx[0]), 2), round(to_slide_y(bx[1]), 2),
                                       round(to_slide_x(bx[2]), 2), round(to_slide_y(bx[3]), 2)]}
labs = {}
labs["k7"] = label_ink(395, 435, 445, 470)
labs["k8"] = label_ink(505, 548, 488, 512)
labs["k9"] = label_ink(615, 658, 494, 512)
labs["k10"] = label_ink(720, 762, 455, 480)
labs["k11_check"] = label_ink(785, 845, 385, 445)   # expect None (absent)
labs["k4_control"] = label_ink(395, 430, 108, 130)  # certified (407.6,122.8)
labs["k0_control"] = label_ink(815, 865, 220, 250)  # certified (840.2,236.5)
out["labels_full"] = labs

# ---------- 3. note box border raw samples ----------
def px(y, x): return A29[y, x].tolist()
out["border_samples"] = {
    "top_row_scan_col200": {str(r): px(r, 200) for r in range(386, 400)},
    "bottom_row_scan_col200": {str(r): px(r, 200) for r in range(504, 514)},
    "left_col_scan_row450": {str(c): px(450, c) for c in range(58, 72)},
    "right_col_scan_row450": {str(c): px(450, c) for c in range(360, 370)},
    "top_row_scan_col300": {str(r): px(r, 300) for r in range(386, 400)},
}
# darkest glyph colors
def darkest(y0, y1, x0, x1, chan):
    reg = A29[y0:y1, x0:x1].reshape(-1, 3)
    i = np.argmin(reg[:, chan])
    return reg[i].tolist()
out["glyph_colors"] = {
    "blue_L2_darkest_B": darkest(421, 429, 90, 340, 2),
    "red_L3_darkest_R": darkest(458, 466, 110, 320, 0),
    "yellow_hl_mean": A29[400:413, 160:205].reshape(-1, 3).mean(axis=0).round(0).tolist(),
    "title_darkest_R": darkest(62, 78, 80, 300, 0),
}

# ---------- 4. head k=8/9/10 fine bboxes via diff (orange on 29 only) ----------
R, G, B = A29[:, :, 0], A29[:, :, 1], A29[:, :, 2]
orange = (R > 180) & (G > 55) & (G < 150) & (B < 80) & (R - G > 80)
heads = {}
for name, (x0, x1, y0, y1) in {"k8": (560, 590, 488, 510), "k9": (672, 695, 462, 482),
                                "k10": (756, 780, 382, 400)}.items():
    win = np.zeros((H, W), bool); win[y0:y1, x0:x1] = True
    m = orange & win
    ys, xs = np.where(m)
    if len(xs):
        bx = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        heads[name] = {"bbox": bx, "npx": int(len(xs)),
                       "center_slide": [round(to_slide_x((bx[0] + bx[2]) / 2), 2),
                                         round(to_slide_y((bx[1] + bx[3]) / 2), 2)]}
out["heads_fine"] = heads

# ---------- 5. note box white inner bbox (clean window) ----------
win = np.zeros((H, W), bool); win[396:508, 68:360] = True
white = win & (R > 243) & (G > 243) & (B > 243)
ys, xs = np.where(white)
out["notebox_white_inner"] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]

# ---------- 6. title L1 ink for closed-loop later (already have) ----------

with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide029/measure_mine3.json", "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
