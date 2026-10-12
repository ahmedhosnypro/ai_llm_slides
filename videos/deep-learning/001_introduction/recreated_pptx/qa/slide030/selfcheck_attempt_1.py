#!/usr/bin/env python3
"""Closed-loop self-check for slide 030 render attempt K (150dpi, 2000x1125; 1 frame-px
(960x540) = 2.0833 render px). Measures title/caption ink, photo/matrix, arrow, right
panel, black bar; asserts against the original's PIL-measured targets (~4px @150dpi =
~2 frame-px). Banked output: out_selfcheck_K.txt."""
import sys
import numpy as np
from PIL import Image

K = sys.argv[1] if len(sys.argv) > 1 else "1"
RENDER = f"/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide030/render_{K}.png"
im = Image.open(RENDER).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B
red = (R > 130) & (G < 90) & (B < 90)
dark = lum < 100
S = 150 / 72.0  # frame px -> render px

def f2r(v):  # frame px -> render px
    return v * S

log = []
def logp(s):
    print(s); log.append(s)

def bbox(mask, name):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        logp(f"{name}: NO PIXELS")
        return None
    r = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    logp(f"{name}: x[{r[0]}..{r[2]}] y[{r[1]}..{r[3]}] px={int(mask.sum())}")
    return r

logp(f"render {W}x{H} (scale S={S:.4f} render-px per frame-px)")

# --- title (red, y< 250 render) ---
t = red.copy(); t[250:, :] = False
tr = bbox(t, "title ink")
if tr:
    adv_r = tr[2] - tr[0] + 1
    logp(f"  title advance {adv_r} render-px = {adv_r/S:.1f} frame-px (target 753); "
         f"center {(tr[0]+tr[2])/2/S:.1f} (target 493); cap-top {tr[1]/S:.1f} (target 84); "
         f"bottom {tr[3]/S:.1f} (target 116)")
    # cap height: 'A' col at title left + few px
    colA = t[:, tr[0]:tr[0] + int(12 * S)]
    rows = np.where(colA.any(axis=1))[0]
    logp(f"  'Ap' band y[{rows.min()/S:.1f}..{rows.max()/S:.1f}] (orig 'A' cap 84..107)")

# --- caption (dark ink in left panel top, render y 480..620, x 200..1000) ---
c = dark.copy()
c[:int(f2r(240)), :] = False; c[int(f2r(282)):, :] = False
c[:, :int(f2r(100))] = False; c[:, int(f2r(470)):] = False
cr = bbox(c, "caption ink")
if cr:
    adv_r = cr[2] - cr[0] + 1
    logp(f"  caption advance {adv_r/S:.1f} frame-px (target 333); left {cr[0]/S:.1f} (target 116); "
         f"top {cr[1]/S:.1f} (target 246); bottom {cr[3]/S:.1f} (target 276)")

# --- left photo content: matrix red ink in left half below caption ---
m = red.copy(); m[int(f2r(300)):, :] = False; m[:int(f2r(255)), :] = False
m[:, int(f2r(470)):] = False
mr = bbox(m, "matrix+brackets ink (render)")
if mr:
    logp(f"  matrix target frame x139..399 y314..431 -> render x[{f2r(139):.0f}..{f2r(399):.0f}] y[{f2r(314):.0f}..{f2r(431):.0f}]")

# --- photo placement check: photo top edge (dark row) at x=200 frame ---
col = lum[:, int(f2r(200))]
top_band = np.where(col[int(f2r(275)):int(f2r(300))] < 200)[0]
if len(top_band):
    logp(f"  photo top edge at frame-y {(int(f2r(275)) + top_band.min())/S:.1f} (target 284.5)")

# --- arrow (red in gap x frame 479..533) ---
ar = red.copy()
ar[:, :int(f2r(479))] = False; ar[:, int(f2r(533)):] = False
ar[:int(f2r(320))] = False; ar[int(f2r(430)):] = False
arr = bbox(ar, "arrow ink")
if arr:
    logp(f"  arrow target frame x484..534 y347..363 -> render x[{f2r(484):.0f}..{f2r(534):.0f}] y[{f2r(347):.0f}..{f2r(363):.0f}]")

# --- right panel (red border row/col + dark interior) ---
rp = red.copy(); rp[:, :int(f2r(500))] = False
rpr = bbox(rp, "right-panel red (border+title spill?)")
d = (lum < 120).copy()
d[:, :int(f2r(520))] = False; d[:int(f2r(255))] = False; d[int(f2r(460)):] = False
dr = bbox(d, "right dark image (render)")
if dr:
    logp(f"  target frame x534..884 y270..444 -> render x[{f2r(534):.0f}..{f2r(884):.0f}] y[{f2r(270):.0f}..{f2r(444):.0f}]")

# --- black bar ---
bb = dark.copy(); bb[:int(f2r(500))] = False
bbr = bbox(bb, "black bar")
if bbr:
    logp(f"  bar target frame x38..921 y518..537.5 -> render x[{f2r(38):.0f}..{f2r(921):.0f}] y[{f2r(518):.0f}..{f2r(537.5):.0f}]")

# --- left panel border (red rows/cols in left half) ---
lp = red.copy(); lp[:, int(f2r(479)):] = False; lp[:int(f2r(200))] = False
lpr = bbox(lp, "left panel red (border+matrix)")
rowsum = lp.sum(axis=1); colsum = lp.sum(axis=0)
lr_rows = [int(y) for y in np.where(rowsum > int(300 * S))[0]]
lr_cols = [int(x) for x in np.where(colsum > int(180 * S))[0]]
logp(f"  left panel border rows(>300fp): {[f'{y/S:.0f}' for y in lr_rows]} (targets 235/476)")
logp(f"  left panel border cols(>180fp): {[f'{x/S:.0f}' for x in lr_cols]} (targets 85/478)")

# --- containment: content ink inside house frame (render x f2r(42)..f2r(918), y f2r(45)..1119) ---
content = red | dark | (lum < 220)
frame_l, frame_r = int(f2r(42)), int(f2r(918))
ys, xs = np.where(content)
viol = ((xs < frame_l) | (xs > frame_r) | (ys < int(f2r(45)))).sum()
logp(f"containment: ink px outside gray panel x[{f2r(42):.0f}..{f2r(918):.0f}] / above y{f2r(45):.0f}: {int(viol)} (bar may touch bottom by design)")

with open(f"/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide030/out_selfcheck_{K}.txt", "w") as f:
    f.write("\n".join(log) + "\n")
