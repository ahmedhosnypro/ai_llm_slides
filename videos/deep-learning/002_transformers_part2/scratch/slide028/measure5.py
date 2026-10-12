#!/usr/bin/env python3
"""slide_028 measurement pass 5 — final: precise fit of the solid 300/330 lines,
wide-window re-measurement of labels 4..7 (full +omega blobs), and label 0..3
cross-check with the same wide-window method."""
import numpy as np
from PIL import Image
import json

A = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
H, W = A.shape[:2]
CXf, CYf = 578.0, 284.0
CXs, CYs = 581.0, 297.2
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
out = {}
def to_slide(fx, fy): return ((fx - 18.63) / 0.96123, fy / 0.95556)

# ---------- solid line fits (grayish ink, wedge, r>20, ring excluded r 118..134) ----------
d = (233 - r) + (233 - g) + (231 - b)
colored = (np.abs(r - g) > 45) | (np.abs(g - b) > 45) | (np.abs(r - b) > 45)
ink = (d > 60) & ~colored
Y, X = np.mgrid[0:H, 0:W]
dx = X - CXf; dy = Y - CYf
rr = np.hypot(dx, dy)
ang = (np.degrees(np.arctan2(-dy, dx))) % 360
for lo, hi, nm in ((288, 312, "line300"), (318, 344, "line330")):
    m = ink & (ang > lo) & (ang < hi) & (rr > 20) & (rr < 245) & ~((rr > 118) & (rr < 134))
    angf = np.where(m, ang, np.nan)
    med = float(np.nanmedian(angf))
    # radial extent along the median angle within +-3 deg
    m2 = m & (np.abs(((ang - med + 180) % 360) - 180) < 3)
    rads = rr[m2]
    print(f"{nm}: median angle {med:.2f} deg  n={m2.sum()}  r {rads.min():.0f}..{rads.max():.0f} (frame) "
          f"-> slide r {rads.min()/0.958:.0f}..{rads.max()/0.958:.0f}")
    out[nm] = {"angle": round(med, 2), "r_frame": [round(float(rads.min()), 0), round(float(rads.max()), 0)],
               "r_slide": [round(float(rads.min() / 0.958), 0), round(float(rads.max() / 0.958), 0)], "n": int(m2.sum())}

# ---------- labels: wide windows around measured rough positions ----------
rough = {0: (840.2, 236.5), 1: (788.8, 104.1), 2: (642.8, 75.4), 3: (520.6, 75.4),
         4: (407.6, 122.8), 5: (328.1, 230.0), 6: (329.1, 356.5), 7: (376.6, 489.9)}
REF = [[840.2, 236.5], [788.8, 104.1], [642.8, 75.4], [520.6, 75.4]]
rl = (r > 150) & ((r - g) > 55) & (g < 185) & ((b - g) > -15)
print("\n== labels (wide window +-42x+-26 frame px around rough positions) ==")
labels = []
for k in range(8):
    fx = 18.63 + 0.96123 * rough[k][0]; fy = 0.95556 * rough[k][1]
    x0, x1 = int(fx) - 42, int(fx) + 43
    y0, y1 = int(fy) - 26, int(fy) + 27
    sub = rl[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    n = len(ys)
    cx, cy = x0 + xs.mean(), y0 + ys.mean()
    sxx, syy = to_slide(cx, cy)
    ref = REF[k] if k < 4 else None
    line = f" label{k}: n={n} slide ({sxx:.1f},{syy:.1f}) wh [{xs.max()-xs.min()+1},{ys.max()-ys.min()+1}]"
    if ref: line += f"  d_cert=({sxx-ref[0]:+.1f},{syy-ref[1]:+.1f})"
    print(line)
    labels.append({"k": k, "n": n, "slide": [round(sxx, 1), round(syy, 1)],
                   "wh": [int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]})
out["labels"] = labels

json.dump(out, open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide028/measure5.json", "w"), indent=1)
print("\nsaved measure5.json")
