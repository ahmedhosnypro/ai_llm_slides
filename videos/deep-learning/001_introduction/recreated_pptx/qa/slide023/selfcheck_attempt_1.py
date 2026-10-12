#!/usr/bin/env python3
"""Closed-loop pre-judge self-check for slide 023, attempt 1.
Renders are 150dpi (2000x1125 for 13.333x7.5in); original frame is 960x540 (1px=1pt).
Render px = frame px * 2000/960 = *2.08333. Equation-law tolerance ~4 render px.
"""
from PIL import Image
import numpy as np
import sys

ren = Image.open("videos/deep-learning/001_introduction/recreated_pptx/qa/slide023/render_1.png").convert("RGB")
a = np.asarray(ren).astype(int)
H, W, _ = a.shape
print(f"render size: {W}x{H}")
S = 2000 / 960.0

def ink(region, thr=140):
    y0, y1, x0, x1 = region
    sub = a[y0:y1, x0:x1]
    return (sub.mean(axis=2) < thr)

def band(mask, label, expect, tol, axis=0):
    """expect=(lo,hi) in render px along axis; tol in render px"""
    ys = np.where(mask.any(axis=1 if axis == 0 else 0))[0]
    if len(ys) == 0:
        print(f"FAIL {label}: NO INK"); return False
    lo, hi = ys.min(), ys.max()
    ok = abs(lo - expect[0]) <= tol and abs(hi - expect[1]) <= tol
    print(f"{'PASS' if ok else 'FAIL'} {label}: ink {lo}..{hi} expect {expect[0]}..{expect[1]} (tol {tol})")
    return ok

fails = 0
def check(name, ok):
    global fails
    if not ok: fails += 1

# ---------- 1. frame containment: no content ink outside the house frame ----------
inner = a[:, :]
dark_all = inner.mean(axis=2) < 100
dark_all[1075:, :] = False          # black bar region
dark_all[:100, :] = False           # chrome top border zone
dark_all[:, :100] = False           # chrome left border zone
dark_all[:, 1945:] = False          # chrome right zone
ys, xs = np.where(dark_all)
# everything left is expected content; assert it sits inside the chrome border (x>=95, y>=90)
ok = xs.min() >= 95 and xs.max() <= 1944 and ys.min() >= 90
print(f"{'PASS' if ok else 'FAIL'} frame containment: content ink x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
check("containment", ok)

# ---------- 2. black bar ----------
bar_abs = a[1060:1125, 300:1700].mean(axis=2) < 60
rows_abs = np.where(bar_abs.any(axis=1))[0] + 1060
ok = abs(rows_abs.min() - 1081) <= 6 and abs(rows_abs.max() - 1119) <= 6
print(f"{'PASS' if ok else 'FAIL'} black bar rows: {rows_abs.min()}..{rows_abs.max()} expect 1081..1119 (tol 6)")
check("black bar", ok)

# ---------- 3. title ----------
tit_abs = ink((110, 200, 250, 1650), 120)
tys = np.where(tit_abs.any(axis=1))[0] + 110
ok = abs(tys.min() - 127.1) <= 7 and abs(tys.max() - 182.0) <= 7
print(f"{'PASS' if ok else 'FAIL'} title caps+desc band: {tys.min()}..{tys.max()} expect 127..182 (tol 7)")
cols = np.where(tit_abs.any(axis=0))[0] + 250
ok2 = abs(cols.min() - 316.7) <= 10 and abs(cols.max() - 1522.9) <= 12
print(f"{'PASS' if ok2 else 'FAIL'} title ink x: {cols.min()}..{cols.max()} expect ~317..1523")
check("title band", ok); check("title x", ok2)
# two colors present
sub = a[110:200, 250:1650]
rr = ((sub[:, :, 0] - sub[:, :, 1]) > 60).sum()
bb = ((sub[:, :, 2] - sub[:, :, 0]) > 60).sum()
ok = rr > 400 and bb > 200
print(f"{'PASS' if ok else 'FAIL'} title two-color: red px {rr}, blue px {bb}")
check("title colors", ok)

# ---------- 4. equation box + 3 line bands ----------
eqb = a[200:500, 100:1000]
cream = (eqb[:, :, 0] > 240) & (eqb[:, :, 1] > 235) & (eqb[:, :, 2] > 215) & (eqb[:, :, 2] < 248)
ys, xs = np.where(cream)
ys += 200; xs += 100
# keep only the contiguous cream region of the box: clip to the box neighborhood
sel = (xs < 1000) & (ys > 195) & (ys < 505)
xs, ys = xs[sel], ys[sel]
ok = abs(ys.min() - 206.2) <= 8 and abs(ys.max() - 495.8) <= 8 and abs(xs.min() - 108.3) <= 8 and abs(xs.max() - 985.4) <= 14
print(f"{'PASS' if ok else 'FAIL'} eq box fill: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} expect x 108..985 y 206..496")
check("eq box", ok)
# equation ink bands (inside box, excluding border): baselines 123.5/171.5/219.5 -> 257.3/357.3/457.3
eink = a[215:490, 162:872].mean(axis=2) < 150   # frame x 78..419: excludes panel border (x423)
for i, (blo, bhi) in enumerate([(225, 269), (325, 369), (423, 470)]):
    m = eink[blo - 215 - 10:bhi - 215 + 10, :]
    ok = m.sum() > 300
    ys2 = np.where(m.any(axis=1))[0] + (blo - 10)  # m window row 0 = absolute blo-10
    lo, hi = ys2.min(), ys2.max()
    ok2 = abs(lo - blo) <= 10 and abs(hi - bhi) <= 10
    print(f"{'PASS' if ok and ok2 else 'FAIL'} eq line {i+1}: ink y {lo}..{hi} n={int(m.sum())} expect {blo}..{bhi} (tol 10)")
    check(f"eq line {i+1}", ok and ok2)
# red tail present in each line (b_j*1) — line m's tail is wider, extend x window
for i, (rlo, rhi, rx0, rx1) in enumerate([(232, 260, 820, 940), (332, 360, 820, 940), (428, 470, 860, 965)]):
    sub = a[rlo:rhi, rx0:rx1]
    red = ((sub[:, :, 0] - sub[:, :, 1]) > 60).sum()
    ok = red > 60
    print(f"{'PASS' if ok else 'FAIL'} eq line {i+1} red tail: red px {red}")
    check(f"eq red tail {i+1}", ok)

# ---------- 5. tan box + text ----------
tsub = a[735:855, 270:695]
tan = (np.abs(tsub[:, :, 0] - 224) < 22) & (np.abs(tsub[:, :, 1] - 224) < 22) & (tsub[:, :, 2] > 175) & (tsub[:, :, 2] < 225)
ys, xs = np.where(tan)
ys += 735; xs += 270
ok = abs(xs.min() - 285.4) <= 8 and abs(xs.max() - 679.2) <= 8 and abs(ys.min() - 750) <= 8 and abs(ys.max() - 839.6) <= 8
print(f"{'PASS' if ok else 'FAIL'} tan box: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} expect x 285..679 y 750..840")
check("tan box", ok)
# text color 8B0000 (139,0,0): select it specifically (box border is C00000 192,0,0)
Rc, Gc, Bc = tsub[:, :, 0], tsub[:, :, 1], tsub[:, :, 2]
tink = (Rc > 100) & (Rc < 172) & (Gc < 40) & (Bc < 40)
trs = np.where(tink.any(axis=1))[0] + 735
ok = abs(trs.min() - 769) <= 10 and abs(trs.max() - 833) <= 10
print(f"{'PASS' if ok else 'FAIL'} tan text rows (8B0000 ink): {trs.min()}..{trs.max()} expect 769..833 (tol 10)")
check("tan text", ok)

# ---------- 6. network panel border ----------
psub = a[300:1060, 860:1890]
nb = (psub[:, :, 2] - psub[:, :, 0] > 25) & (psub.mean(axis=2) < 190)
ys, xs = np.where(nb)
ys += 300; xs += 860
ok = abs(xs.min() - 881.3) <= 8 and abs(xs.max() - 1868.8) <= 10 and abs(ys.min() - 316.7) <= 8 and abs(ys.max() - 1041.7) <= 10
print(f"{'PASS' if ok else 'FAIL'} panel border: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} expect x 881..1869 y 317..1042")
check("panel border", ok)

# ---------- 7. Sigma circles (cyan fill at 3 centers) ----------
for i, (cx, cy) in enumerate([(1418.7, 389.6), (1418.7, 666.7), (1418.7, 949.0)]):
    sub = a[int(cy) - 40:int(cy) + 40, int(cx) - 40:int(cx) + 40]
    cy2 = (sub[:, :, 1] - sub[:, :, 0] > 12) & (sub[:, :, 2] > 200) & (sub[:, :, 1] > 200)
    ok = cy2.sum() > 500
    ys2, xs2 = np.where(cy2)
    if ok:
        ok2 = abs(ys2.mean() + int(cy) - 40 - cy) <= 8 and abs(xs2.mean() + int(cx) - 40 - cx) <= 8
    else:
        ok2 = False
    print(f"{'PASS' if ok and ok2 else 'FAIL'} Sigma {i+1}: cyan px {int(cy2.sum())} center ({xs2.mean() + int(cx) - 40:.0f},{ys2.mean() + int(cy) - 40:.0f}) expect ({cx},{cy})")
    check(f"Sigma {i+1}", ok and ok2)

# ---------- 8. ellipsis circles ----------
for i, cy in enumerate([742.7, 800.0, 857.3]):
    sub = a[int(cy) - 18:int(cy) + 18, 1400:1440]
    m = sub.mean(axis=2) < 200
    ok = m.sum() > 25
    print(f"{'PASS' if ok else 'FAIL'} ellipsis circle {i+1}: ink px {int(m.sum())}")
    check(f"ellipsis {i+1}", ok)

# ---------- 9. input labels (7 ink bands at x~900-935) + red 1 ----------
isub = a[560:930, 895:945].mean(axis=2) < 130
rows = np.where(isub.any(axis=1))[0]
# expect 7 bands
bands = []
prev = -10
for r in rows:
    if r - prev > 4: bands.append([r, r])
    else: bands[-1][1] = r
    prev = r
ok = 7 <= len(bands) <= 8   # a fan line may cross the label column (present in the original too)
print(f"{'PASS' if ok else 'FAIL'} input labels: {len(bands)} bands (expect 7-8; fan line may cross) at {[(b[0]+560, b[1]+560) for b in bands]}")
check("input labels count", ok)
exp_bands = [(589.6, 602.1), (635, 648.8), (679.2, 695), (737.5, 745.8), (783.3, 791.7), (820.8, 841.7), (864.6, 885.4)]
bi = 0
for e in exp_bands:
    match = [b for b in bands if abs(b[0] + 560 - e[0]) <= 12 and abs(b[1] + 560 - e[1]) <= 12]
    ok = len(match) >= 1
    print(f"{'PASS' if ok else 'FAIL'} input band @y{e[0]}: {'found ' + str(match[0][0]+560) + '..' + str(match[0][1]+560) if match else 'MISSING'}")
    check(f"input band {e[0]}", ok)
sub = a[855:895, 895:945]
red1 = ((sub[:, :, 0] - sub[:, :, 1]) > 60).sum()
ok = red1 > 40
print(f"{'PASS' if ok else 'FAIL'} red bias '1': red px {red1}")
check("red 1", ok)

# ---------- 10. weight labels (15 colored clusters) ----------
wexp = [
    (483, 261.5, "red"), (481, 280.5, "red"), (482, 300.5, "red"), (483, 352.5, "red"), (482, 393.5, "red"),
    (570, 302.5, "blue"), (548, 313.5, "blue"), (555, 335.5, "blue"), (555, 354.5, "blue"), (579, 366.5, "blue"),
    (579, 389.5, "green"), (567, 404.5, "green"), (567, 419.5, "green"), (560, 434.5, "green"), (572, 451.5, "green"),
]
for i, (fx, fy, col) in enumerate(wexp):
    cx, cy = int(fx * S), int(fy * S)
    sub = a[cy - 14:cy + 12, cx - 6:cx + 58]
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    if col == "red": m = ((R - G) > 55) & (R > 120)
    elif col == "blue": m = ((B - R) > 45) & (B > 110)
    else: m = ((G - R) > 30) & ((G - B) > 30) & (G > 100)
    ok = m.sum() > 25
    print(f"{'PASS' if ok else 'FAIL'} weight {i+1} ({col}): px {int(m.sum())} @({fx},{fy})")
    check(f"weight {i+1}", ok)

# ---------- 11. activation boxes + glyphs + arrows ----------
for i, cy in enumerate([389.6, 666.7, 949.0]):
    sub = a[int(cy) - 45:int(cy) + 45, 1495:1605]
    pink = (sub[:, :, 0] > 235) & (sub[:, :, 1] > 195) & (sub[:, :, 1] < 245) & (sub[:, :, 2] > 225)
    ok = pink.sum() > 400
    blu = ((sub[:, :, 2] - sub[:, :, 1]) > 60).sum()
    ok2 = blu > 80
    ar = a[int(cy) - 12:int(cy) + 12, 1445:1505]
    reda = ((ar[:, :, 0] - ar[:, :, 1]) > 60).sum()
    ok3 = reda > 40
    print(f"{'PASS' if ok and ok2 and ok3 else 'FAIL'} row {i+1}: act pink {int(pink.sum())}, glyph blue {int(blu)}, arrow red {int(reda)}")
    check(f"act row {i+1}", ok and ok2 and ok3)

# ---------- 12. output texts (3 rows x 3 bands, left x~1675) ----------
for i, (b1, b3) in enumerate([(387.5, 445.8), (658.3, 716.7), (943.8, 1002.1)]):
    sub = a[int(b1) - 25:int(b3) + 22, 1660:1850]
    m = sub.mean(axis=2) < 110
    rows = np.where(m.any(axis=1))[0]
    bands2 = []
    prev = -10
    for r in rows:
        if r - prev > 5: bands2.append([r, r])
        else: bands2[-1][1] = r
        prev = r
    ok = len(bands2) == 3
    print(f"{'PASS' if ok else 'FAIL'} output {i+1}: {len(bands2)} text bands (expect 3) {[(b[0]+int(b1)-25, b[1]+int(b1)-25) for b in bands2]}")
    check(f"output {i+1}", ok)

# ---------- 13. explicit lineSpacing verify (output band pitch = 14pt = 29.17px) ----------
sub = a[360:460, 1660:1850]
m = sub.mean(axis=2) < 110
rows = np.where(m.any(axis=1))[0]
bands3 = []
prev = -10
for r in rows:
    if r - prev > 5: bands3.append([r, r])
    else: bands3[-1][1] = r
    prev = r
if len(bands3) >= 2:
    pitch = (bands3[1][0] - bands3[0][0])
    ok = abs(pitch - 29.17) <= 3
    print(f"{'PASS' if ok else 'FAIL'} lineSpacing pin: output band pitch {pitch} px (pinned 29.17 = 14pt)")
    check("lineSpacing", ok)

print(f"\nTOTAL FAILS: {fails}")
sys.exit(1 if fails else 0)
