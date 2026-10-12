#!/usr/bin/env python3
"""Closed-loop self-check for slide 052 render_1.png (attempt 1).
Compares element ink bboxes in the 150dpi render (2001x1125) against the
ORIGINAL frame's measured positions (scratch/slide052 measurements), through
the verified deck transform:
  slide_x = (fx-18.63)/0.96123 ; slide_y = fy/0.95556
  render_x = slide_x * (2001/960) ; render_y = slide_y * (1125/540)
Tolerance ~4 render px (~1.9 slide pt). Prints per-element deltas.
"""
from PIL import Image
import numpy as np
from scipy import ndimage
import sys

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide052/render_1.png"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = im.shape[:2]
SX = 2001 / 960.0
SY = 1125 / 540.0
def RX(fx): return (fx - 18.63) / 0.96123 * SX
def RY(fy): return fy / 0.95556 * SY
r, g, b = im[..., 0], im[..., 1], im[..., 2]

fails, warns = [], []
def near(hexc, tol):
    hr, hg, hb = int(hexc[1:3], 16), int(hexc[3:5], 16), int(hexc[5:7], 16)
    return (abs(r - hr) < tol) & (abs(g - hg) < tol) & (abs(b - hb) < tol)

def bbox_of(mask, x0, y0, x1, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())

def check(name, hexc, tol, fx0, fy0, fx1, fy1, search_pad=40, maxd=4.0):
    ex = (RX(fx0), RY(fy0), RX(fx1), RY(fy1))
    x0 = max(0, int(ex[0]) - search_pad); y0 = max(0, int(ex[1]) - search_pad)
    x1 = min(W, int(ex[2]) + search_pad); y1 = min(H, int(ex[3]) + search_pad)
    bb = bbox_of(near(hexc, tol), x0, y0, x1, y1)
    if bb is None:
        fails.append(f"{name}: NO INK found near expected {tuple(int(v) for v in ex)}")
        return
    d = [bb[i] - ex[i] for i in range(4)]
    worst = max(abs(v) for v in d)
    tag = "OK " if worst <= maxd else ("WARN" if worst <= 7 else "FAIL")
    msg = (f"{tag} {name}: render {bb} vs expected {tuple(round(v,1) for v in ex)} "
           f"d=({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f})")
    print(msg)
    if tag == "FAIL": fails.append(msg)
    elif tag == "WARN": warns.append(msg)

print("== containers ==")
check("upper container", "#D6C6B4", 12, 318, 72, 870, 267)
check("lower container", "#F2DDF6", 12, 313, 294, 868, 516)
print("== bars ==")
check("bar1 residual", "#990000", 30, 338, 84, 834, 107)
check("bar FFN", "#0A9A08", 30, 338, 116, 834, 137)
check("bar2 residual", "#990000", 30, 338, 146, 834, 167)
check("bar lower residual", "#990000", 30, 338, 312, 834, 333)
check("bar purple", "#7A0080", 30, 344, 454, 832, 475)
print("== upper 3D boxes (fronts) ==")
for i, (x0, x1) in enumerate([[334, 415], [437, 519], [545, 626], [660, 742], [763, 844]]):
    check(f"upper box{i+1}", "#0010B4", 30, x0, 188, x1, 242)
print("== lower masked 3D boxes ==")
for i, (x0, x1) in enumerate([[329, 410], [437, 518], [545, 626], [660, 742], [763, 844]]):
    check(f"masked box{i+1}", "#0010B4", 30, x0, 347, x1, 383)
print("== encoder box ==")
check("encoder box", "#0010B4", 30, 77, 305, 287, 425)
print("== circles ==")
check("K circle", "#C05055", 35, 309, 180, 324, 196)
check("V circle", "#3E8A3C", 35, 310, 231, 325, 247)
check("Q circle 1", "#23209E", 35, 378, 247, 392, 261)
check("Q circle 5", "#23209E", 35, 806, 246, 820, 260)
print("== word boxes ==")
for i, (x0, x1) in enumerate([[329, 412], [436, 519], [545, 628], [658, 739], [767, 850]]):
    check(f"wordbox{i+1}", "#EAFBDC", 12, x0, 477, x1, 509)
print("== callouts (red borders) ==")
check("callout1 border", "#CC0000", 40, 64, 62, 296, 107)
check("callout2 border", "#CC0000", 40, 64, 127, 296, 178)
print("== legend ==")
check("legend box", "#EAFBDC", 12, 64, 485, 245, 511)

# --- text fit: white ink bands inside bars / boxes must not wrap ---
print("== text-fit checks ==")
def bands_in(hexc, tol, fx0, fy0, fx1, fy1, label, expect_bands, band_kind="light"):
    x0, y0 = int(RX(fx0)), int(RY(fy0)); x1, y1 = int(RX(fx1)), int(RY(fy1))
    if band_kind == "light":
        m = (r > 190) & (g > 190) & (b > 170)
    else:
        m = near(hexc, tol)
    sub = m[y0:y1, x0:x1]
    rows = np.where(sub.sum(axis=1) > 2)[0]
    if not len(rows):
        fails.append(f"{label}: no text ink")
        print(f"FAIL {label}: no text ink"); return
    bl = []
    s = p = rows[0]
    for v in rows[1:]:
        if v == p + 1: p = v
        else: bl.append((s, p)); s = p = v
    bl.append((s, p))
    print(f"{'OK ' if len(bl)==expect_bands else 'FAIL'} {label}: {len(bl)} ink bands (expect {expect_bands}) at rel rows {bl}")
    if len(bl) != expect_bands: fails.append(f"{label}: {len(bl)} bands vs {expect_bands}")

bands_in("#990000", 30, 350, 86, 830, 105, "bar1 caption single line", 1)
bands_in("#0A9A08", 30, 350, 118, 830, 135, "FFN caption single line", 1)
bands_in("#7A0080", 30, 350, 456, 830, 473, "purple caption single line", 1)
bands_in("#0010B4", 30, 340, 190, 410, 240, "upper box1 3-line label", 3)
bands_in("#0010B4", 30, 335, 349, 405, 381, "masked box1 3-line label", 3)
bands_in("#CC0000", 40, 70, 64, 290, 105, "callout1 2-line text", 2)
bands_in("#CC0000", 40, 70, 129, 290, 176, "callout2 2-line text", 2)

# --- line pitch of the 3-line labels (explicit lineSpacing check) ---
x0, x1 = int(RX(340)), int(RX(410))
m = (r > 190) & (g > 190) & (b > 170)
sub = m[int(RY(190)):int(RY(240)), x0:x1]
rows = np.where(sub.sum(axis=1) > 2)[0]
if len(rows):
    bl = []; s = p = rows[0]
    for v in rows[1:]:
        if v == p + 1: p = v
        else: bl.append((s + p) / 2); s = p = v
    bl.append((s + p) / 2)
    if len(bl) >= 2:
        pitch = (bl[-1] - bl[0]) / (len(bl) - 1)
        exp = 13 * 2.0833  # lineSpacing 13pt
        ok = abs(pitch - exp) <= 4
        print(f"{'OK ' if ok else 'FAIL'} upper box line pitch {pitch:.1f}px vs pinned {exp:.1f}px")
        if not ok: fails.append(f"line pitch {pitch:.1f} vs {exp:.1f}")

# --- frame containment: no content ink outside the gray panel (x 42..918pt, y 45..540) ---
px0, px1 = int(RX(42)), int(RX(918))
outmask = (np.abs(r - 233) > 26) | (np.abs(g - 233) > 26) | (np.abs(b - 231) > 26)
# exclude the chrome border band and badge area; look strictly outside panel columns
left_band = outmask[:, : px0 - 6]
right_band = outmask[:, px1 + 6:]
print(f"OK  containment scan: ink outside panel columns L={int(left_band.sum())} R={int(right_band.sum())} px (border AA allowed small)")
if left_band.sum() > 400 or right_band.sum() > 400:
    fails.append(f"content ink outside panel: L={int(left_band.sum())} R={int(right_band.sum())}")

print()
if fails:
    print(f"SELF-CHECK: {len(fails)} FAIL, {len(warns)} WARN")
    for f_ in fails: print("  -", f_)
    sys.exit(1)
print(f"SELF-CHECK: ALL PASS ({len(warns)} warns)")
