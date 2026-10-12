#!/usr/bin/env python3
"""Pre-judge self-check battery for slide 020 attempt 1 (17 §2, adapted to the
playlist chrome law: the inner frame is the gray panel x 42..918, y 45..538
frame-px — ml-intro 0.15in values superseded).
Render: 2001x1125 @150dpi; frame-px -> render-px factor R = 2001/960 = 2.0844."""
from PIL import Image
import numpy as np, sys

RENDER = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide020/render_1.png'
R = 2001/960.0   # frame px -> render px
SC = 960/2001.0  # render px -> frame px (reporting)
PANEL = dict(x0=42, x1=918, y0=45, y1=538)  # frame-px; bottom stroke rows 538-539
fails = []

im = np.asarray(Image.open(RENDER).convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[...,0], im[...,1], im[...,2]
red = (r > 120) & (r - g > 60) & (r - b > 60)
white = (r > 225) & (g > 225) & (b > 225)

# render-px zones (frame-px * R)
ZX0, ZX1 = int(42*R), int(918*R)        # panel 87..1913
ZY0 = int(45*R)                          # 93
BADGE = np.s_[int(50*R):int(95*R), int(868*R):int(918*R)]  # y 104..198, x 1809..1913
# title-ink mask: red minus chrome strokes/badge/bottom-rule zones (render-px)
inner_red = red.copy()
inner_red[:105, :] = False; inner_red[1105:, :] = False
inner_red[:, :100] = False; inner_red[:, 1900:] = False
inner_red[BADGE] = False
ys, xs = np.nonzero(inner_red)
tx0, tx1, ty0, ty1 = xs.min()*SC, xs.max()*SC, ys.min()*SC, ys.max()*SC

# ---- CHECK A: frame containment (white outer margin must carry NO content ink)
margin = np.ones((H, W), bool)
margin[ZY0-6:int(538*R)+8, ZX0-6:ZX1+8] = False   # panel + border zone is not margin
ink_any = ~white
n_margin = int((ink_any & margin).sum())
if n_margin > 50:
    ys_m, xs_m = np.nonzero(ink_any & margin)
    fails.append(f"A: {n_margin} ink px on the white outer margin (bbox x {xs_m.min()}-{xs_m.max()} y {ys_m.min()}-{ys_m.max()})")
else:
    print(f"A1 PASS: outer white margin carries {n_margin} stray px (<=50 tol)")

if not (PANEL['x0'] + 2 < tx0 and tx1 < PANEL['x1'] - 2 and PANEL['y0'] + 2 < ty0 and ty1 < PANEL['y1'] - 2):
    fails.append(f"A: title ink x {tx0:.1f}-{tx1:.1f} y {ty0:.1f}-{ty1:.1f} not inside panel {PANEL}")
else:
    print(f"A2 PASS: title ink x {tx0:.1f}-{tx1:.1f} y {ty0:.1f}-{ty1:.1f} inside panel with clearance")

# ---- CHECK B: title geometry vs original (closed-loop re-assert)
ORIG = dict(x=(184, 774), y=(261, 297))
dx0, dx1 = tx0 - ORIG['x'][0], tx1 - ORIG['x'][1]
dy0, dy1 = ty0 - ORIG['y'][0], ty1 - ORIG['y'][1]
dw = (tx1 - tx0) - (ORIG['x'][1] - ORIG['x'][0])
if max(abs(dw), abs(dx0), abs(dx1), abs(dy0), abs(dy1)) > 4:
    fails.append(f"B: title geometry off (dL {dx0:.1f} dR {dx1:.1f} dT {dy0:.1f} dB {dy1:.1f} dW {dw:.1f} frame-px, tol 4)")
else:
    print(f"B PASS: title edges vs orig within 4 frame-px (dL {dx0:.1f} dR {dx1:.1f} dT {dy0:.1f} dB {dy1:.1f} dW {dw:.1f})")

# ---- CHECK C: badge center + numeral ink present
yel = (r > 200) & (g > 200) & (b < 190)
pys, pxs = np.nonzero(yel)
bcx = (pxs.min() + pxs.max())/2 * SC; bcy = (pys.min() + pys.max())/2 * SC
if abs(bcx - 893) > 4 or abs(bcy - 71) > 4:
    fails.append(f"C: badge center ({bcx:.1f},{bcy:.1f}) vs (893,71)")
else:
    print(f"C1 PASS: badge center ({bcx:.1f},{bcy:.1f}) vs (893,71)")
dark = (r[BADGE] < 120) & (g[BADGE] < 120) & (b[BADGE] < 120)
if dark.sum() < 30:
    fails.append(f"C: badge numeral ink missing ({int(dark.sum())} dark px)")
else:
    print(f"C2 PASS: badge numeral '20' ink present ({int(dark.sum())} dark px)")

# ---- CHECK D: bottom rule present (chrome panel bottom stroke) across the slide
bot = red[int(533*R):, :]
bc = np.where(bot.sum(axis=0) > 1)[0]
if not len(bc) or bc.min() > 60*R or bc.max() < 900*R:
    fails.append("D: bottom red rule missing/not across")
else:
    print(f"D PASS: bottom red rule across (x {bc.min()}-{bc.max()} render-px)")

# ---- CHECK E: no red ink outside the title band inside the panel (wrap check)
band_lo, band_hi = int(250*R), int(310*R)   # 521..646
stray = inner_red.copy()
stray[band_lo:band_hi, :] = False
n_stray = int(stray.sum())
if n_stray > 30:
    ys2, xs2 = np.nonzero(stray)
    fails.append(f"E: {n_stray} red px outside title band inside panel (y {ys2.min()}-{ys2.max()})")
else:
    print(f"E PASS: no red ink outside title band inside panel ({n_stray} stray px)")

# ---- CHECK F: equations / delimiters / tables — N/A (course-authored divider; none
# in spec; original-frame artifact scan found only title/badge/border/rule/cursor)
print("F N/A: no equations, delimiters, or tables on this slide (spec + frame scan)")

# ---- CHECK G: single-line title (explicit line-spacing law N/A for a 1-line box;
# assert no wrap via band height)
band_h = ty1 - ty0
if band_h > 45:
    fails.append(f"G: title band {band_h:.1f} frame-px — unexpected wrap")
else:
    print(f"G PASS: single line confirmed (band {band_h:.1f} frame-px)")

print()
if fails:
    print("SELFCHECK: FAIL"); [print("  -", f) for f in fails]; sys.exit(1)
print("SELFCHECK: ALL PASS")
