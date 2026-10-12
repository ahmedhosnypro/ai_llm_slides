#!/usr/bin/env python3
"""Closed-loop self-check attempt 1 for slide_027: compare the 150dpi render against
the PIL-measured ground-truth bands of the original frame (2001x1125 render; scale
S = 2001/960 render px per frame px; tolerance 4 frame px ~ 8.3 render px).
Checks: per-line ink band (rows/cols/center-x), effective ascent constant, core color,
panel containment, badge/chrome via separate house_chrome_check.py."""
import numpy as np
from PIL import Image

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide027/render_1.png"
im = np.asarray(Image.open(REN).convert("RGB")).astype(int)
H, W = im.shape[:2]
S = W / 960.0
print(f"render {W}x{H}, scale {S:.4f} render-px per frame-px; tol 4 frame px")
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 120) & (g < 110) & (b < 110)
fails = []

def band(y0, y1, x0, x1):
    m = red[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    if not len(ys):
        return None
    return (ys.min() + y0, ys.max() + y0, xs.min() + x0, xs.max() + x0, int(m.sum()))

# expected: name, rows(top,bottom), cols(left,right), measured from original frame
EXPECT = [
    ("L1 '[4] Introduction to'", 133, 179, 264, 682),
    ("L2 'Deep Learning'", 229, 295, 240, 719),
    ("L3 'and'", 312, 347, 439, 518),
    ("L4 'CNN'", 372, 423, 406, 551),
]
BASE_EXPECT = {0: 169.5, 1: 280.0, 2: 346.5, 3: 422.5}
for i, (name, e0, e1, e2, e3) in enumerate(EXPECT):
    wy0, wy1 = int((e0 - 15) * S), int((e1 + 15) * S)
    wx0, wx1 = int((e2 - 40) * S), int((e3 + 40) * S)
    res = band(wy0, wy1, wx0, wx1)
    if res is None:
        print(f"{name}: NO INK in window -> FAIL"); fails.append(name); continue
    ry0, ry1, rx0, rx1, n = res
    f0, f1, f2, f3 = ry0 / S, ry1 / S, rx0 / S, rx1 / S
    d = (abs(f0 - e0), abs(f1 - e1), abs(f2 - e2), abs(f3 - e3))
    cx = (f2 + f3) / 2; ecx = (e2 + e3) / 2
    ok = max(d) <= 4.0 and abs(cx - ecx) <= 4.0
    print(f"{name}: rows {f0:.1f}..{f1:.1f} (exp {e0}..{e1}, d {d[0]:.1f}/{d[1]:.1f}), "
          f"cols {f2:.1f}..{f3:.1f} (exp {e2}..{e3}, d {d[2]:.1f}/{d[3]:.1f}), "
          f"w {f3 - f2:.1f} (exp {e3 - e2}), cx {cx:.1f} (exp {ecx:.1f}, d {abs(cx - ecx):.1f}) "
          f"ink={n} -> {'OK' if ok else 'FAIL'}")
    if not ok:
        fails.append(name)

# baseline check: flat-glyph bottoms. 'I' of Introduction (L1), 'D' (L2), 'n' (L3), 'N' (L4).
# measure flat-glyph bottom in a narrow column window around the expected glyph.
def flat_bottom(y0, y1, x0, x1):
    res = band(y0, y1, x0, x1)
    return None if res is None else res[1] / S

flat = [
    ("L1 'I' bottom", int(120 * S), int(200 * S), int(339 * S), int(352 * S), 169.5),
    ("L2 'D' bottom", int(230 * S), int(300 * S), int(240 * S), int(292 * S), 280.0),
    ("L4 'N' bottom", int(365 * S), int(430 * S), int(460 * S), int(500 * S), 422.5),
]
for name, y0, y1, x0, x1, e in flat:
    fb = flat_bottom(y0, y1, x0, x1)
    if fb is None:
        print(f"{name}: NO INK -> FAIL"); fails.append(name); continue
    ok = abs(fb - e) <= 4.0
    print(f"{name}: {fb:.1f} (exp {e}, d {abs(fb - e):.1f}) -> {'OK' if ok else 'FAIL'}")
    if not ok:
        fails.append(name)

# text core color (5x5 all-red) in the L2 band region
core_red = red.copy()
core_red[:int(215 * S), :] = False; core_red[int(310 * S):, :] = False
core_red[:, :int(200 * S)] = False; core_red[:, int(760 * S):] = False
core = np.zeros_like(core_red)
rr, cc = np.where(core_red)
for y, x in zip(rr, cc):
    if core_red[y - 2:y + 3, x - 2:x + 3].all():
        core[y, x] = True
ys, xs = np.where(core)
if len(ys):
    ink = im[ys, xs]
    print(f"render text core mean: #{int(ink[:, 0].mean()):02X}{int(ink[:, 1].mean()):02X}{int(ink[:, 2].mean()):02X} n={len(ys)} (target B4000B)")
else:
    print("render text core: NO CORE PIXELS"); fails.append("core color")

# containment: TITLE ink only — scan the panel INTERIOR, excluding the chrome border
# strokes (render cols ~86..93 and ~1908..1915, top stroke rows ~94..101) and the
# badge area. Assert title ink sits inside frame cols 50..910 / rows 50..500 with
# clearance from every border stroke.
inner = red.copy()
inner[:, :100] = False; inner[:, 1900:] = False   # drop border stroke columns
inner[:105, :] = False; inner[int(500 * S):, :] = False   # frame rows 50..500 only
allx = np.where(inner.sum(axis=0) > 0)[0]
ally = np.where(inner.sum(axis=1) > 0)[0]
print(f"title ink cols {allx.min() / S:.1f}..{allx.max() / S:.1f} frame (panel interior 44.6..915.6, strokes excluded)")
print(f"title ink rows {ally.min() / S:.1f}..{ally.max() / S:.1f} frame (panel top stroke ~48.5)")
inside = (allx.min() / S > 50 and allx.max() / S < 910
          and ally.min() / S > 50 and ally.max() / S < 500)
print(f"containment (interior scan, tol: inside 50..910 x 50..500): {inside}")
if not inside:
    fails.append("containment")
# and: no red ink OUTSIDE the panel+border block at all (canvas must stay white;
# chrome strokes themselves live inside the block, verified by house_chrome_check.py).
# Panel border block, RENDER px: rows >= 90 (top stroke ~95..), cols 80..1920.
top_block = int(red[:90, :].sum())
left_block = int(red[:, :80].sum())
right_block = int(red[:, 1920:].sum())
n_out = top_block + left_block + right_block
print(f"red ink outside panel block (rows<90: {top_block}, cols<80: {left_block}, cols>1920: {right_block}, should be 0): {n_out}")
if n_out > 0:
    fails.append("ink-outside-panel")

print("RESULT:", "PASS" if not fails else f"FAIL {fails}")
