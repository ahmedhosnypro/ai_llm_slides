#!/usr/bin/env python3
# selfcheck_worker2.py — INDEPENDENT verification of the certified deliverable
# (concurrent worker's attempt-1 build) against THIS worker's own frame measurements.
# Checks: (1) inheritance confinement — render vs certified base differs ONLY inside
# the two highlight zones + badge numeral; (2) blend accuracy over clean fields vs the
# frame's measured cores; (3) rendered rect edges vs this worker's blend-segment
# 50%-coverage crossings (tolerance ~4px @150dpi = 1.92pt).
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide004"
ren = np.asarray(Image.open(S + "/deliverable-1.png").convert("RGB"), dtype=np.float64)
base = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
frame = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB"), dtype=np.float64)
ax, sx, ay, sy = np.load(S + "/fit_content.npy")

# --- 1. inheritance confinement ---
d = np.abs(ren - base).sum(axis=2)
hot = d > 20
zones = np.zeros_like(hot)
zones[742:845, 1210:1536] = True   # H1 (their rect + 4px pad)
zones[571:680, 1533:1848] = True   # H2
zones[105:190, 1820:1900] = True   # badge numeral 4 vs 15
out = hot & ~zones
print(f"[1] inheritance: hot px {int(hot.sum())}, outside zones {int(out.sum())}")
ys, xs = np.where(out)
if len(xs):
    print("    outside-zone hot px bbox:", xs.min(), xs.max(), ys.min(), ys.max())

# --- 2. blend accuracy over clean fields (deliverable vs frame cores) ---
def mean_patch(a, x0, x1, y0, y1):
    return a[y0:y1, x0:x1].reshape(-1, 3).mean(axis=0)
ren_peach = mean_patch(ren, 1230, 1330, 755, 830)
ren_mint = mean_patch(ren, 1755, 1855, 595, 670)
# frame cores from this worker's m10b medians (clean flat-flat pairs)
fr_peach = np.array([246.0, 179.0, 111.0]); fr_mint = np.array([223.0, 189.0, 115.0])
print(f"[2] blend over peach: deliverable {ren_peach.round(1)} vs frame {fr_peach} -> err {np.abs(ren_peach - fr_peach).round(1)}")
print(f"    blend over mint : deliverable {ren_mint.round(1)} vs frame {fr_mint} -> err {np.abs(ren_mint - fr_mint).round(1)}")
# what F07A00@50 would give (this worker's clean-pair fit)
O2 = np.array([240.0, 122.0, 2.0])
print(f"    (F07A00@50 would predict peach {0.5*O2+0.5*np.array([253,237,221]).round(1)}, "
      f"mint {0.5*O2+0.5*np.array([206,255,225]).round(1)})")

# --- 3. rendered rect edges vs this worker's frame-derived targets ---
def edges(x0, x1, y0, y1):
    sub = (d[y0:y1, x0:x1] > 30).astype(float)
    sub = ndimage_median(sub)
    colcov = sub.mean(axis=0); rowcov = sub.mean(axis=1)
    def cross(prof, off):
        idx = np.where(prof > 0.5)[0]
        i0, i1 = idx[0], idx[-1]
        def interp(i, up):
            j = i - 1 if up else i + 1
            if j < 0 or j >= len(prof) or prof[i] == prof[j]: return off + i
            t = (0.5 - prof[j]) / (prof[i] - prof[j])
            return off + j + t
        return interp(i0, True), interp(i1, False)
    lx, rx_ = cross(colcov, x0); ty, by = cross(rowcov, y0)
    return lx, rx_, ty, by

def ndimage_median(a):
    from scipy import ndimage
    return ndimage.median_filter(a, 3)

e1 = edges(1200, 1545, 735, 850)
e2 = edges(1545, 1860, 565, 685)
tgt1 = (583.5 / 0.48, 735.8 / 0.48, 356.3 / 0.48, 401.7 / 0.48)
tgt2 = (736.8 / 0.48, 887.6 / 0.48, 275.5 / 0.48, 323.9 / 0.48)
print(f"[3] H1 rendered edges {tuple(round(v,1) for v in e1)} vs frame targets {tuple(round(v,1) for v in tgt1)}")
print(f"    d(px) = {tuple(round(a - b, 1) for a, b in zip(e1, tgt1))}  (tol ~4px)")
print(f"    H2 rendered edges {tuple(round(v,1) for v in e2)} vs frame targets {tuple(round(v,1) for v in tgt2)}")
print(f"    d(px) = {tuple(round(a - b, 1) for a, b in zip(e2, tgt2))}")
