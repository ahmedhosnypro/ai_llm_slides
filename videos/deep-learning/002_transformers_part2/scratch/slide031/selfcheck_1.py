#!/usr/bin/env python3
"""Self-check v2 for slide 031: adapted chrome check + content closed-loop.

Same-region ink-bbox comparison (NO region expansion — dense layout).
Render: 150dpi (1 frame px = 1 pt -> 2.0833 render px). Tol 4 render-px.
"""
import sys
import numpy as np
from PIL import Image

RENDER = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide031/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_031.jpg"
SC = 150.0 / 72.0

im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
H, W = im.shape[:2]
fails, notes = [], []

def cv(v): return v * SC

def band(img, y0, y1, x0, x1, thr=185):
    sub = img[int(y0):int(y1), int(x0):int(x1)]
    m = sub.min(axis=2) < thr
    ys, xs = np.where(m)
    if len(ys) == 0: return None
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())

def cmp_region(name, fy0, fy1, fx0, fx1, tol=4.0, tol_b=None):
    ob = band(orig, fy0, fy1, fx0, fx1)
    rb = band(im, fy0 * SC, min(H, fy1 * SC), fx0 * SC, min(W, fx1 * SC))
    if ob is None:
        fails.append(f"{name}: no ink in ORIGINAL region?!"); return
    if rb is None:
        fails.append(f"{name}: EMPTY region in render (BLOCKER)"); return
    exp = tuple(v * SC for v in ob)
    d = tuple(rb[i] - exp[i] for i in range(4))
    tols = (tol, tol, tol, tol_b if tol_b is not None else tol)
    bad = any(abs(v) > t for v, t in zip(d, tols))
    print(f"  {name:20s} d=({d[0]:+.0f},{d[1]:+.0f},{d[2]:+.0f},{d[3]:+.0f}) {'FAIL' if bad else 'ok'}"
          f"   render x{rb[0]:.0f}..{rb[1]:.0f} y{rb[2]:.0f}..{rb[3]:.0f}")
    if bad:
        fails.append(f"{name}: ink bbox off ({d[0]:+.0f},{d[1]:+.0f},{d[2]:+.0f},{d[3]:+.0f}) render-px")

# ---------------- adapted chrome check ----------------
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
gray = (np.abs(r - 233) < 16) & (np.abs(g - 233) < 16) & (np.abs(b - 231) < 18)
sl = gray[:, int(cv(44)):int(cv(64))]
rows_sl = np.where(sl.sum(axis=1) > 0.7 * sl.shape[1])[0]
if len(rows_sl) == 0:
    fails.append("chrome: no gray left sliver")
else:
    notes.append(f"gray left sliver rows {rows_sl.min()}..{rows_sl.max()} (expect {cv(45):.0f}..{cv(517):.0f})")
    if abs(rows_sl.min() - cv(45)) > 6:
        fails.append(f"chrome: panel top {rows_sl.min()} vs {cv(45):.0f}")
rr = gray[:, int(cv(872)):int(cv(914))]
if len(np.where(rr.sum(axis=1) > 0.7 * rr.shape[1])[0]) == 0:
    fails.append("chrome: no gray right region")
red = (r > 120) & (g < 110) & (b < 110)
if red[:int(cv(47)), int(cv(100)):int(cv(900))].sum() < 10:
    fails.append("chrome: top red stroke missing (y45)")
if red[int(cv(100)):int(cv(400)), :int(cv(50))].sum() < 10:
    fails.append("chrome: left red stroke missing")
if red[int(cv(100)):int(cv(400)), int(cv(910)):].sum() < 10:
    fails.append("chrome: right red stroke missing")
cx, cy, d = cv(893), cv(71), cv(36)
win = np.s_[int(cy - d):int(cy + d), int(cx - d):int(cx + d)]
wr, wg, wb = r[win], g[win], b[win]
yel = (wr > 200) & (wg > 200) & (wb < 190)
pys, pxs = np.where(yel)
if not len(pys):
    fails.append("chrome: badge yellow disc missing")
else:
    bcx = win[1].start + (pxs.min() + pxs.max()) / 2
    bcy = win[0].start + (pys.min() + pys.max()) / 2
    bw = pxs.max() - pxs.min() + 1
    notes.append(f"badge center ({bcx:.0f},{bcy:.0f}) d={bw} (expect ({cx:.0f},{cy:.0f}) d={d:.0f})")
    if abs(bcx - cx) > 8 or abs(bcy - cy) > 8: fails.append("chrome: badge center off")
    if abs(bw - d) > 12: fails.append("chrome: badge diameter off")
pur = (wb > 150) & (wr > 70) & (wr < 180) & (wg < 130)
if pur.sum() < 10: fails.append("chrome: purple ring missing")
# numeral 31 present in badge (dark px)
dark = (wr < 110) & (wg < 110) & (wb < 110)
if dark.sum() < 15: fails.append("chrome: badge numeral missing")

# ---------------- content closed-loop ----------------
print("== content closed-loop (tol 4 render-px) ==")
cmp_region("left panel", 44, 219, 58, 208)
cmp_region("mid panel", 44, 219, 206, 686)
cmp_region("lv1 row1", 74, 99, 95, 170, tol_b=9)  # bottom: DejaVu omega descender shallower than original metric (documented residual)
cmp_region("lv1 row2", 108, 130, 95, 170)
cmp_region("lv2 row1", 146, 172, 95, 168)
cmp_region("lv2 row2", 182, 206, 95, 168)
cmp_region("mva row1", 74, 100, 208, 330)
cmp_region("mva row2", 108, 135, 208, 330)
cmp_region("mvb row1", 76, 102, 366, 662)
cmp_region("mvb row2", 110, 136, 366, 662)
cmp_region("mvr row1", 152, 178, 388, 634)
cmp_region("mvr row2", 184, 210, 388, 634)
cmp_region("defbox1 band", 127, 155, 688, 867)
cmp_region("defbox2 band", 168, 204, 686, 864)
cmp_region("banner text", 227, 247, 67, 864)
cmp_region("deriv R1", 263, 291, 78, 760)
cmp_region("deriv R2", 296, 321, 78, 760)
cmp_region("deriv R3", 335, 359, 80, 700)
cmp_region("deriv R4", 359, 383, 80, 764)
cmp_region("deriv R5", 394, 420, 80, 764)
cmp_region("deriv R6", 429, 453, 78, 760)
cmp_region("deriv R7", 468, 500, 72, 545)
cmp_region("callout box", 467, 504, 572, 738)
cmp_region("footer bar", 516, 540, 30, 930)

# highlights: sample center px
for nm, (x, y) in {"hl R1-a": (347, 276), "hl R1-b": (716, 284),
                   "hl R7-a": (104, 483), "hl R7-b": (275, 483),
                   "hl LV2-a": (120, 155), "hl LV2-b": (120, 193)}.items():
    px = im[int(y * SC), int(x * SC)]
    oky = px[0] > 200 and px[1] > 180 and px[2] < 160
    okc = px[2] > 170 and px[1] > 150 and px[0] < 160
    print(f"  {nm:12s} center {tuple(px)} {'ok' if (oky or okc) else 'FAIL'}")
    if not (oky or okc):
        fails.append(f"{nm}: highlight not present at center ({tuple(px)})")

# ribbon (rotated): pale-yellow strip in bottom-right, compare bbox
reg = im[int(cv(396)):int(cv(516)), int(cv(739)):int(cv(864))]
py = (reg[:, :, 0] > 225) & (reg[:, :, 1] > 220) & (reg[:, :, 2] > 150) & (reg[:, :, 2] < 222) & \
     ((reg[:, :, 0] - reg[:, :, 2]) > 12)
ys, xs = np.where(py)
if len(ys) < 300:
    fails.append(f"ribbon: pale-yellow strip too small ({len(ys)} px)")
else:
    rx0, rx1 = cv(739) + xs.min(), cv(739) + xs.max()
    ry0, ry1 = cv(396) + ys.min(), cv(396) + ys.max()
    exp = (737 * SC, 851 * SC, 400 * SC, 511 * SC)
    dd = (rx0 - exp[0], rx1 - exp[1], ry0 - exp[2], ry1 - exp[3])
    print(f"  ribbon bbox render x{rx0:.0f}..{rx1:.0f} y{ry0:.0f}..{ry1:.0f} d=({dd[0]:+.0f},{dd[1]:+.0f},{dd[2]:+.0f},{dd[3]:+.0f})")
    if max(abs(v) for v in dd) > 14:
        fails.append(f"ribbon bbox off ({dd[0]:+.0f},{dd[1]:+.0f},{dd[2]:+.0f},{dd[3]:+.0f}) tol 14 (rotated)")

# containment
for nm, sl2 in {"left": np.s_[:, :int(cv(41))], "right": np.s_[:, int(cv(920)):],
                "top": np.s_[:int(cv(44)), :]}.items():
    arr = im[int(cv(46)):int(cv(516))] if nm != "top" else im[:int(cv(44))]
    if nm == "left": arr = arr[:, :int(cv(41))]
    elif nm == "right": arr = arr[:, int(cv(920)):]
    n = int((arr.min(axis=2) < 160).sum())
    print(f"  containment {nm:5s} ink n={n} {'ok' if n <= 40 else 'FAIL'}")
    if n > 40: fails.append(f"containment: {nm} ink n={n}")

print()
if fails:
    print(f"SELF-CHECK: {len(fails)} FAILURES")
    for f in fails: print("  -", f)
    sys.exit(1)
print("SELF-CHECK: ALL PASS")
for n in notes: print("  note:", n)
