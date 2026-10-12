#!/usr/bin/env python3
"""TWIN VERIFICATION of qa/slide006/render_2.png against THIS worker's independent
measurements (scratch/slide006): title + six agenda line ink bboxes.
My mapping: frame_x = 17.33 + 0.96123*slide_x ; frame_y = -0.15 + 0.95677*slide_y
Targets (slide pts) from my measure_original.py + font_fit.txt:
  Title ink x 226.4..630.0, y 72.3..99.4, cx 428.2
  L1 x0 114.1 y0 153.8 y1 167.4   L2 x0 115.2 y0 195.8 y1 209.3
  L3 x0 113.2 y0 240.7 y1 254.3   L4 x0 116.2 y0 282.5 y1 295.0
  L5 x0 117.2 y0 323.3 y1 336.9   L6 x0 115.2 y0 370.4 y1 382.9
(1pt = 2.0833 render px @150dpi; tolerance 4px = 1.92pt)"""
from PIL import Image
import numpy as np, json, sys

RENDER = sys.argv[1] if len(sys.argv) > 1 else "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide006/render_2.png"
a = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W = a.shape[:2]
PXPT = 150 / 72.0
print(f"render {W}x{H}")

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R > 120) & (G < 100) & (B < 100)
blue = (B > 110) & (R < 110) & (G < 110)

def bands(mask, x_lo, x_hi, y_lo, y_hi, min_mass=3, gap=3):
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
        res.append({"y0": y0 + y_lo, "y1": y1 + y_lo,
                    "x0": xs.min() + x_lo, "x1": xs.max() + x_lo})
    return res

def cmp2(name, meas, tgt):
    d = {k: round((meas[k] / PXPT) - tgt[k], 2) for k in tgt}
    worst_px = max(abs(v) for v in d.values()) * PXPT
    ok = worst_px <= 4.0
    print(f"{name}: meas_pt x {meas['x0']/PXPT:.1f}..{meas['x1']/PXPT:.1f} y {meas['y0']/PXPT:.1f}..{meas['y1']/PXPT:.1f}"
          f" | delta_pt {d} | worst {worst_px:.1f}px {'PASS' if ok else 'FAIL'}")
    return ok

ok_all = True

# title: red ink between panel top (~95px) and y 250, x 300..1600
tb = bands(red, 300, 1600, 100, 260, min_mass=3, gap=4)
if not tb:
    print("TITLE: NO RED INK FOUND — FAIL"); ok_all = False
else:
    t = tb[0]
    m = {"x0": t["x0"], "x1": t["x1"], "y0": t["y0"], "y1": t["y1"]}
    cx_m = (m["x0"] + m["x1"]) / 2 / PXPT
    ok_all &= cmp2("TITLE", m, {"x0": 226.4, "x1": 630.0, "y0": 72.3, "y1": 99.4})
    print(f"  title cx {cx_m:.1f} vs target 428.2 (delta {cx_m-428.2:+.1f}pt = {(cx_m-428.2)*PXPT:.1f}px)")

# agenda: blue bands below y 280, x 150..1200
ab = bands(blue, 150, 1200, 280, 900, min_mass=3, gap=4)
targets = [
    ("L1", {"x0": 114.1, "y0": 153.8, "y1": 167.4}),
    ("L2", {"x0": 115.2, "y0": 195.8, "y1": 209.3}),
    ("L3", {"x0": 113.2, "y0": 240.7, "y1": 254.3}),
    ("L4", {"x0": 116.2, "y0": 282.5, "y1": 295.0}),
    ("L5", {"x0": 117.2, "y0": 323.3, "y1": 336.9}),
    ("L6", {"x0": 115.2, "y0": 370.4, "y1": 382.9}),
]
print(f"agenda bands found: {len(ab)} (expect 6)")
if len(ab) != 6:
    ok_all = False
for (nm, tgt), bnd in zip(targets, ab):
    m = {"x0": bnd["x0"], "x1": bnd["x1"], "y0": bnd["y0"], "y1": bnd["y1"]}
    # x1 target: from my measured frame widths (w/S fit per line at build em) — compare width instead
    ok_all &= cmp2(nm + " x0/y", m, tgt)

# widths: rendered vs my measured frame widths mapped
w_tgts = [356.8, 203.9, 255.6, 195.4, 341.0, 134.0]
for (nm, _), bnd, wt in zip(targets, ab, w_tgts):
    wr = (bnd["x1"] - bnd["x0"] + 1) / PXPT
    d = wr - wt
    print(f"{nm} width {wr:.1f} vs target {wt:.1f} (delta {d:+.1f}pt = {d*PXPT:+.1f}px) {'PASS' if abs(d*PXPT) <= 4 else 'FAIL'}")
    if abs(d * PXPT) > 4: ok_all = False

print("TWIN CLOSED-LOOP:", "PASS (all within 4px)" if ok_all else "FAIL")
