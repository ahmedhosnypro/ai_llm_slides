#!/usr/bin/env python3
"""Closed-loop self-check for slide 052 render_2.png (attempt 2 — after the
crop-check fixes: stacked-lid cascade, white top strips, bottom-aligned masked
text, 5 thin curved multi-color arrows per bundle, upper text 8.5pt/11.6).
Targets = the original frame's pixel-map measurements (box_ascii.txt).
Tolerance ~4 render px (~1.9 slide pt)."""
from PIL import Image
import numpy as np
import sys

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide052/render_2.png"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = im.shape[:2]
SX = 2001 / 960.0; SY = 1125 / 540.0
def RX(fx): return (fx - 18.63) / 0.96123 * SX
def RY(fy): return fy / 0.95556 * SY
r, g, b = im[..., 0], im[..., 1], im[..., 2]
fails = []
def near(hexc, tol):
    hr, hg, hb = int(hexc[1:3], 16), int(hexc[3:5], 16), int(hexc[5:7], 16)
    return (abs(r - hr) < tol) & (abs(g - hg) < tol) & (abs(b - hb) < tol)
def bbox_in(mask, x0, y0, x1, y1):
    ys, xs = np.where(mask[y0:y1, x0:x1])
    if not len(ys): return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())
def check(name, hexc, tol, fx0, fy0, fx1, fy1, pad=6, maxd=4.0):
    ex = (RX(fx0), RY(fy0), RX(fx1), RY(fy1))
    bb = bbox_in(near(hexc, tol), max(0, int(ex[0]) - pad), max(0, int(ex[1]) - pad),
                 min(W, int(ex[2]) + pad), min(H, int(ex[3]) + pad))
    if bb is None:
        fails.append(f"{name}: NO INK"); print(f"FAIL {name}"); return
    d = [bb[i] - ex[i] for i in range(4)]
    worst = max(abs(v) for v in d)
    tag = "OK " if worst <= maxd else "FAIL"
    print(f"{tag} {name}: {bb} vs {tuple(round(v,1) for v in ex)} d=({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f})")
    if tag == "FAIL": fails.append(f"{name} d={d}")

print("== boxes attempt 2 ==")
for i, (x0, x1) in enumerate([[334, 415], [437, 519], [545, 626], [660, 742], [763, 844]]):
    check(f"upper box{i+1} face", "#0010B4", 30, x0, 178, x1, 243)
for i, (x0, x1) in enumerate([[329, 410], [437, 518], [545, 626], [660, 742], [763, 844]]):
    check(f"masked box{i+1} face", "#0010B4", 30, x0, 344, x1, 384)
check("encoder face", "#0010B4", 30, 77, 305, 287, 425)
print("== static elements regression ==")
check("upper container", "#D6C6B4", 12, 318, 72, 870, 267)
check("lower container", "#F2DDF6", 12, 313, 294, 868, 516)
check("bar1", "#990000", 30, 338, 84, 834, 107)
check("purple bar", "#7A0080", 30, 344, 454, 832, 475)
check("K circle", "#C05055", 35, 309, 180, 324, 196)
check("V circle", "#3E8A3C", 35, 310, 231, 325, 247)
print("== white top strips ==")
strip = near("#EAF0F6", 22)
for i, (x0, x1) in enumerate([[334, 415], [763, 844]]):
    cnt = int(strip[int(RY(174)):int(RY(179)), int(RX(x0)):int(RX(x1))].sum())
    print(f"{'OK ' if cnt > 60 else 'FAIL'} upper box{i+1 if i==0 else 5} white strip px: {cnt}")
    if cnt <= 60: fails.append(f"upper strip {i}")
for i, (x0, x1) in enumerate([[329, 410], [763, 844]]):
    cnt = int(strip[int(RY(338)):int(RY(343)), int(RX(x0)):int(RX(x1))].sum())
    print(f"{'OK ' if cnt > 60 else 'FAIL'} masked box{i+1 if i==0 else 5} white strip px: {cnt}")
    if cnt <= 60: fails.append(f"masked strip {i}")
print("== slate cascade peek (right of masked box1) ==")
slate = near("#3E58A8", 30)
cnt = int(slate[int(RY(342)):int(RY(384)), int(RX(408)):int(RX(420))].sum())
print(f"{'OK ' if cnt > 60 else 'FAIL'} slate peek px right of masked box1: {cnt}")
if cnt <= 60: fails.append("slate peek")
print("== arrows: 5 traces under masked box1 and box5 ==")
colored = ((np.abs(r - g) > 40) | (np.abs(g - b) > 40) | (np.abs(r - b) > 40))
for i, (x0, x1, nm) in enumerate([[335, 404, "box1"], [769, 838, "box5"]]):
    band = colored[int(RY(388)):int(RY(446)), int(RX(x0)):int(RX(x1))]
    cols = np.where(band.sum(axis=0) > 3)[0]
    runs = 0; prev = None
    for c in cols:
        if prev is None or c > prev + 2: runs += 1
        prev = c
    print(f"{'OK ' if runs == 5 else 'FAIL'} traces under masked {nm}: {runs} (expect 5)")
    if runs != 5: fails.append(f"arrows {nm} = {runs}")
print("== text blocks ==")
wht = (r > 190) & (g > 190) & (b > 170)
yel = (r > 200) & (g > 200) & (b < 150)
def bands(m, x0f, y0f, x1f, y1f, minrow=2):
    sub = m[int(RY(y0f)):int(RY(y1f)), int(RX(x0f)):int(RX(x1f))]
    rows = np.where(sub.sum(axis=1) > minrow)[0]
    bl = []; s = p = None
    for v in rows:
        if s is None: s = p = v
        elif v == p + 1: p = v
        else: bl.append((s, p)); s = p = v
    if s is not None: bl.append((s, p))
    return bl
ub = bands(wht, 340, 180, 410, 243)
ok = len(ub) == 3
print(f"{'OK ' if ok else 'FAIL'} upper box1 label bands: {len(ub)} {ub}")
if not ok: fails.append("upper bands")
mb = bands(wht, 335, 346, 405, 384)
myb = bands(yel, 335, 346, 405, 384)
ok = len(mb) == 2 and len(myb) >= 1
print(f"{'OK ' if ok else 'FAIL'} masked box1: yellow 'Masked' bands {myb}, white bands {mb}")
if not ok: fails.append("masked bands")
# masked text block must sit LOW in the face (bottom-aligned): last white band bottom >= 80% of face
if mb:
    face_top, face_bot = RY(344.5), RY(384)
    last_bot = int(RY(346)) + mb[-1][1]
    frac = (last_bot - face_top) / (face_bot - face_top)
    ok = frac >= 0.80
    print(f"{'OK ' if ok else 'FAIL'} masked text bottom-aligned: last band bottom at {frac:.0%} of face")
    if not ok: fails.append("masked text not bottom-aligned")
ub2 = bands(wht, 340, 180, 410, 243)
if len(ub2) >= 2:
    pitch = (ub2[-1][0] - ub2[0][0]) / (len(ub2) - 1) * (960 / 2001) * (0.96123) if False else None
print("== containment ==")
px0, px1 = int(RX(42)), int(RX(918))
outmask = (np.abs(r - 233) > 26) | (np.abs(g - 233) > 26) | (np.abs(b - 231) > 26)
L, Rr = int(outmask[:, :px0 - 6].sum()), int(outmask[:, px1 + 6:].sum())
print(f"{'OK ' if L < 400 and Rr < 400 else 'FAIL'} ink outside panel L={L} R={Rr}")
if L >= 400 or Rr >= 400: fails.append("containment")
print()
print(f"SELF-CHECK ATTEMPT 2: {len(fails)} FAIL")
for f_ in fails: print("  -", f_)
sys.exit(1 if fails else 0)
