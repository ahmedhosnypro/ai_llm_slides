#!/usr/bin/env python3
"""TWIN VERIFICATION v2 — MATCHED-MASK closed loop (methodologically correct):
measure the ORIGINAL frame and the RENDER with the SAME ink predicates, map the
original's ink through THIS worker's independent mapping, compare. Tolerance 4px
@150dpi (= ~1.92 frame px... render px vs frame px scale 2.0844 -> 4 render px =
1.92 frame px)."""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_006.jpg"
RN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide006/render_2.png"

fr = np.asarray(Image.open(FR).convert("RGB")).astype(int)
rn = np.asarray(Image.open(RN).convert("RGB")).astype(int)

# --- THIS worker's independent mapping (fit from border stroke centers 57.7/900.7/42.9/516.5)
OX, SX = 17.33, 0.96123
OY, SY = -0.15, 0.95677
SC = rn.shape[1] / fr.shape[1]  # render px per frame px

def ink_bands(a, mask, x_lo, x_hi, y_lo, y_hi, min_mass, gap):
    x_lo, x_hi, y_lo, y_hi = int(x_lo), int(x_hi), int(y_lo), int(y_hi)
    sub = mask[y_lo:y_hi, x_lo:x_hi]
    prof = sub.sum(axis=1)
    rows = np.where(prof >= min_mass)[0]
    out = []
    if len(rows):
        s = p = rows[0]
        for y in rows[1:]:
            if y <= p + gap: p = y
            else: out.append((s, p)); s = p = y
        out.append((s, p))
    res = []
    for (y0, y1) in out:
        band = sub[y0:y1 + 1, :]
        ys, xs = np.where(band)
        res.append((y0 + y_lo, y1 + y_lo, xs.min() + x_lo, xs.max() + x_lo))
    return res

# SAME predicate families for both images (blue: blue-dominant, mid-dark)
def blue_mask(a):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (B > 110) & (B - R > 40) & (B - G > 40) & (R < 140)
def red_mask(a):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (R > 120) & (R - G > 50) & (R - B > 40)

fr_b = ink_bands(fr, blue_mask(fr), 90, 800, 130, 420, 2, 2)
rn_b = ink_bands(rn, blue_mask(rn), 90 * SC, 800 * SC, 130 * SC, 420 * SC, 3, 4)
fr_t = ink_bands(fr, red_mask(fr), 100, 820, 55, 120, 2, 2)
rn_t = ink_bands(rn, red_mask(rn), 100 * SC, 820 * SC, 55 * SC, 120 * SC, 3, 4)

print(f"frame bands: {len(fr_t)} title + {len(fr_b)} agenda | render bands: {len(rn_t)} + {len(rn_b)}")

def report(name, fband, rband):
    (fy0, fy1, fx0, fx1) = fband
    (ry0, ry1, rx0, rx1) = rband
    # map frame ink (frame px) -> slide pt -> render px (via SC)
    t = {"x0": (fx0 - OX) / SX * SC, "x1": (fx1 - OX) / SX * SC,
         "y0": (fy0 - OY) / SY * SC, "y1": (fy1 - OY) / SY * SC}
    m = {"x0": rx0, "x1": rx1, "y0": ry0, "y1": ry1}
    d = {k: m[k] - t[k] for k in t}
    worst = max(abs(v) for v in d.values())
    print(f"{name}: target_px {({k: round(v,1) for k,v in t.items()})} meas_px {({k: round(v,1) for k,v in m.items()})}")
    print(f"    delta_px {({k: round(v,1) for k,v in d.items()})} worst {worst:.1f} {'PASS' if worst <= 4 else 'FAIL'}")
    return worst <= 4

ok = True
names = ["L1", "L2", "L3", "L4", "L5", "L6"]
if len(fr_b) == len(rn_b) == 6:
    for nm, f, r in zip(names, fr_b, rn_b):
        ok &= report(nm, f, r)
else:
    print("BAND COUNT MISMATCH"); ok = False
if len(fr_t) == len(rn_t) == 1:
    ok &= report("TITLE", fr_t[0], rn_t[0])
else:
    print("TITLE BAND MISMATCH", len(fr_t), len(rn_t)); ok = False

print("TWIN MATCHED-MASK CLOSED-LOOP:", "PASS" if ok else "FAIL")
