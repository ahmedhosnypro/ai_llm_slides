#!/usr/bin/env python3
"""selfcheck_attempt_K.py — closed-loop verify: render (downsampled to 960x540) vs
remapped 002:8 frame targets. Identical masks/thresholds on both sides.
Usage: selfcheck_attempt_K.py <render_150dpi.png>
Gates (render px = slide px * 2.0844): delta elements <=5, imported blocks <=7
(documented 002-template systematic +2..3 slide-px).
"""
import sys
from PIL import Image
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
ren_path = sys.argv[1] if len(sys.argv) > 1 else f"{BASE}/recreated_pptx/qa/slide008/render_1.png"

im = Image.open(ren_path).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
S = W / 960.0
# downsample render to the frame's 960x540 space
im8 = im.resize((960, 540), Image.LANCZOS)
ren = np.asarray(im8).astype(int)
r, g, b = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
print(f"render {W}x{H} (scale {S:.4f}) -> downsampled 960x540; all coords slide px")

results = []
def check(tag, got, want, gate):
    d = max(abs(a1 - b1) for a1, b1 in zip(got, want)) * S
    ok = d <= gate
    results.append((tag, d, gate, ok))
    fs = f"  [{'OK ' if ok else 'FAIL'}] {tag:36s} delta {d:5.1f} rpx (gate {gate})  got {got} want {want}"
    print(fs)

def ink_rows(y0, y1, x0=150, x1=830, thr=120, minpx=8):
    reg = ren[y0:y1, x0:x1]
    dark = (reg.max(axis=2) < thr)
    rows = dark.sum(axis=1)
    on = [y0 + i for i, v in enumerate(rows) if v > minpx]
    return (on[0], on[-1]) if on else (None, None)

# 1. title
check("title L1 ink rows", ink_rows(50, 80), (61, 74), 5)
check("title L2 ink rows", ink_rows(78, 108), (83, 97), 5)

# 2. W_k box1 (fill extent via pale-green fill; borders flaky at hairline width)
dkg = (g - r > 25) & (abs(r - 120) < 50) & (abs(g - 178) < 50) & (abs(b - 120) < 50)
fillg = (g - r > 8) & (g > 210) & (b > 190) & (b < 250)
rows = [y for y in range(228, 271) if fillg[y, 163:193].sum() > 20]
check("W_k box1 fill rows", (rows[0], rows[-1]) if rows else (0, 0), (237, 260), 5)
cols = [x for x in range(150, 210) if dkg[240:258, x].sum() > 6]
check("W_k box1 border cols", (cols[0], cols[-1]) if cols else (0, 0), (161, 195), 5)

# 3. W_v box1 cols (non-peach extent)
peach = (abs(r - 247) < 14) & (abs(g - 226) < 14) & (abs(b - 205) < 14)
npf = ~peach
colson = [x for x in range(700, 748) if npf[240:256, x].sum() > 12]
check("W_v box1 cols", (colson[0], colson[-1]) if colson else (0, 0), (707, 741), 5)

# 4. DP box fill rows (band x336..344 stays right of the blue circle at bottom rows)
dpf = (abs(r - 220) < 16) & (abs(g - 202) < 18) & (abs(b - 187) < 18)
on = [y for y in range(160, 430) if dpf[y, 336:344].sum() > 4]
check("DP fill rows", (on[0], on[-1]), (196, 400), 6)
# (DP bottom border sub-pixel after downsample; fill extent + box h208 bound it)

# 5. dots (navy centroids)
navy = (b - r > 60) & (b - g > 60) & (b > 100) & (b < 220)
nv = navy.copy(); nv[:200, :] = False; nv[420:, :] = False
nv[:, :250] = False; nv[:, 350:] = False
ys, xs = np.where(nv)
want = [(332, 249), (316, 290), (298, 331), (279, 375)]
if len(ys) > 40:
    order = np.argsort(ys); ys_s, xs_s = ys[order], xs[order]
    start = 0; dots = []
    for i in range(1, len(ys_s) + 1):
        if i == len(ys_s) or ys_s[i] - ys_s[i - 1] > 12:
            dots.append((float(xs_s[start:i].mean()), float(ys_s[start:i].mean())))
            start = i
    for i, gd in enumerate(dots[:4]):
        wd = want[i]
        d = max(abs(gd[0] - wd[0]), abs(gd[1] - wd[1])) * S
        ok = d <= 5
        results.append((f"dot{i+1}", d, 5, ok))
        print(f"  [{'OK ' if ok else 'FAIL'}] dot{i+1} (centroid)                   delta {d:5.1f} rpx (gate 5)  got ({gd[0]:.0f},{gd[1]:.0f}) want {wd}")

# 6. K.q ink bbox
kq = ((r - g > 40) & (r - b > 25) & (r > 110)).copy()
kq[:188, :] = False; kq[220:, :] = False; kq[:, :322] = False; kq[:, 375:] = False
ys, xs = np.where(kq)
if len(ys):
    check("K.q ink bbox", (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())), (347, 367, 200, 212), 6)
else:
    results.append(("K.q ink", 99, 6, False)); print("  [FAIL] K.q ink: none found")

# 7. blue circle tint rows (render has the true alpha circle over same backgrounds)
tint = ((b - r) > 12) & (b > 150) & (g < 245)
tc = tint.copy(); tc[:395, :] = False; tc[510:, :] = False
tc[:, :200] = False; tc[:, 420:] = False
for yy, wx in [(430, (244, 355)), (450, (243, 357))]:
    on = np.where(tc[yy - 2:yy + 3, 200:420].any(axis=0))[0]
    if len(on):
        check(f"circle tint row y{yy}", (int(on[0] + 200), int(on[-1] + 200)), wx, 8)

# 8. block arrow (isolated: below highlight bottom border, right of X1 label)
chunky = (r - g > 70) & (r - b > 70) & (r > 130)
ca = chunky.copy(); ca[:509, :] = False; ca[533:, :] = False
ca[:, :262] = False; ca[:, 298:] = False
ys, xs = np.where(ca)
if len(ys):
    check("block arrow bbox", (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())), (269, 289, 513, 529), 6)
else:
    results.append(("block arrow", 99, 6, False)); print("  [FAIL] block arrow: none found")

# 9. W_q box (blue-over-yellow — render tints too)
wq = ((g - b > 30) & (g - r > 8) & (g > 150)).copy()
wq[:425, :] = False; wq[485:, :] = False; wq[:, :260] = False; wq[:, 335:] = False
ys, xs = np.where(wq)
if len(ys):
    check("Wq box (blue-over-yellow)", (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())), (276, 321, 433, 479), 7)

# 10. multiply circles: per-ring band x-extent (stems merge y-clusters)
red = (r - g > 55) & (r - b > 40) & (r > 130)
want_c = [(532, 246), (563, 288), (592, 328), (622, 372)]
for i, (cx, cy) in enumerate(want_c):
    band = red[cy - 10:cy + 11, cx - 30:cx + 30]
    rowhits = band.any(axis=0)
    on = np.where(rowhits)[0]
    if len(on):
        # ring left edge = start of the first run of >=2 consecutive columns
        runs = []
        s0 = on[0]; pv = on[0]
        for v in on[1:]:
            if v - pv > 2:
                runs.append((s0, pv)); s0 = v
            pv = v
        runs.append((s0, pv))
        left = runs[0][0] + cx - 30
        gc = left + 9.5
        d = abs(gc - cx) * S
        ok = d <= 6
        results.append((f"circ{i+1} x", d, 6, ok))
        print(f"  [{'OK ' if ok else 'FAIL'}] circ{i+1} left-edge center             delta {d:5.1f} rpx (gate 6)  got {gc:.0f} want {cx} (left {left}, runs {runs[:3]})")
    else:
        results.append((f"circ{i+1} x", 99, 6, False))
        print(f"  [FAIL] circ{i+1} x: no ring ink in band")

# 11. imported-block sanity (gate 7)
soft = (abs(r - 248) < 10) & (abs(g - 222) < 14) & (abs(b - 251) < 10)
on2 = [y for y in range(180, 420) if soft[y, 462:488].sum() > 12]
check("softmax fill rows (import)", (on2[0], on2[-1]), (196, 401), 7)
# full-resolution border checks (dashed strokes are sub-pixel after downsample)
ar = a  # 2001x1125
contF = (abs(ar[:, :, 0] - 78) < 40) & (abs(ar[:, :, 1] - 125) < 40) & (abs(ar[:, :, 2] - 82) < 40)
srowsF = [y for y in range(int(465 * S), int(525 * S)) if contF[y, int(170 * S):int(500 * S)].sum() > 40]
check("sentence cont border rows", (srowsF[0] / S, srowsF[-1] / S) if srowsF else (0, 0), (477, 518), 7)
lcolsF = [x for x in range(int(40 * S), int(170 * S)) if contF[int(230 * S):int(395 * S), x].sum() > 60]
check("left container cols (import)", (lcolsF[0] / S, lcolsF[-1] / S) if lcolsF else (0, 0), (58, 141), 7)
rcolsF = [x for x in range(int(720 * S), int(880 * S)) if contF[int(230 * S):int(395 * S), x].sum() > 60]
check("right container cols (import)", (rcolsF[0] / S, rcolsF[-1] / S) if rcolsF else (0, 0), (763, 843), 7)
# sigma fill (import)
sig = (abs(r - 234) < 12) & (abs(g - 254) < 8) & (abs(b - 252) < 10)
on3 = [y for y in range(180, 240) if sig[y, 520:648].sum() > 30]
check("sigma fill rows (import)", (on3[0], on3[-1]), (196, 217), 7)
# Y2 box (dashed green border ink)
grn = (g - r > 30) & (g - b > 20) & (g > 110)
gy = grn.copy(); gy[:110, :] = False; gy[150:, :] = False; gy[:, :535] = False; gy[:, 635:] = False
ys, xs = np.where(gy)
if len(ys):
    check("Y2 green ink bbox (import)", (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())), (549, 619, 121, 146), 8)
# legend W box (olive border) — full res, border-column peaks
wbF = ((ar[:, :, 0] > 150) & (ar[:, :, 0] < 225) & (ar[:, :, 1] > 135) & (ar[:, :, 1] < 210) & (ar[:, :, 2] > 85) & (ar[:, :, 2] < 150))
wbF[:int(460 * S), :] = False; wbF[int(512 * S):, :] = False
wbF[:, :int(780 * S)] = False; wbF[:, int(845 * S):] = False
ys, xs = np.where(wbF)
if len(ys):
    import collections
    cc = collections.Counter((xs // 2 * 2).tolist())
    peaks = sorted([x for x, c in cc.items() if c > 20])
    check("legend W box border cols", (peaks[0] / S, peaks[-1] / S) if peaks else (0, 0), (797, 826), 6)
    # side-border y extent only (the d*d caption AA below the box pollutes the full mask)
    colmask = wbF[:, peaks[0]:peaks[0] + 4].any(axis=1) | wbF[:, peaks[-1] - 3:peaks[-1] + 1].any(axis=1)
    rows_on = np.where(colmask)[0]
    check("legend W box y extent", (rows_on.min() / S, rows_on.max() / S), (471, 502), 7)
# pills
pill = (r > 245) & (g > 245) & (b > 205) & (b < 240)
p1 = pill.copy(); p1[:150, :] = False; p1[195:, :] = False; p1[:, :250] = False; p1[:, 360:] = False
ys, xs = np.where(p1)
if len(ys):
    check("Similarity pill (import)", (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())), (271, 338, 163, 185), 7)

n_fail = sum(1 for _, _, _, ok in results if not ok)
print(f"\nSELFCHECK RESULT: {len(results) - n_fail}/{len(results)} OK, {n_fail} FAIL")
for tag, d, gate, ok in results:
    if not ok:
        print(f"  FAILED: {tag} delta {d:.1f} rpx (gate {gate})")
