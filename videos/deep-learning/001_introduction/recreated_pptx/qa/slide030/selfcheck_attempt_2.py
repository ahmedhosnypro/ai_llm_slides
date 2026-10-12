#!/usr/bin/env python3
"""Closed-loop self-check v2 for slide 030 (fixes v1's mask bugs: chrome-border and
red-dominant contamination, mis-zeroed caption band). Banks out_selfcheck_K.txt."""
import sys
import numpy as np
from PIL import Image

K = sys.argv[1] if len(sys.argv) > 1 else "2"
QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide030"
a = np.asarray(Image.open(f"{QA}/render_{K}.png").convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[..., 0], a[..., 1], a[..., 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B
red = (R > 130) & (G < 90) & (B < 90)
reddom = (R > 100) & (R > G + 40)
dark = (lum < 100) & ~reddom
S = 150 / 72.0
f2r = lambda v: int(round(v * S))

log = []
def logp(s):
    print(s); log.append(s)

def bbox(mask, name, conv=True):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        logp(f"{name}: NO PIXELS"); return None
    r = (xs.min(), ys.min(), xs.max(), ys.max())
    if conv:
        logp(f"{name}: frame x[{r[0]/S:.1f}..{r[2]/S:.1f}] y[{r[1]/S:.1f}..{r[3]/S:.1f}] px={len(xs)}")
    else:
        logp(f"{name}: render x[{r[0]}..{r[2]}] y[{r[1]}..{r[3]}] px={len(xs)}")
    return r

logp(f"render {W}x{H}")

# 1. TITLE (red, clean window: inside chrome borders)
t = red.copy()
t[:f2r(60), :] = False; t[f2r(130):, :] = False
t[:, :f2r(55)] = False; t[:, f2r(905):] = False
tr = bbox(t, "1. TITLE ink")
if tr is not None:
    adv = (tr[2] - tr[0] + 1) / S
    logp(f"   advance {adv:.1f} (target 753) | center {(tr[0]+tr[2])/2/S:.1f} (target 493) | "
         f"cap-top {tr[1]/S:.1f} (84) | bottom {tr[3]/S:.1f} (116)")

# 2. CAPTION (dark non-red; exclude border rows f2r(233.5)..f2r(237))
c = dark.copy()
c[:f2r(215), :] = False; c[f2r(283):, :] = False
c[:, :f2r(95)] = False; c[:, f2r(475):] = False
c[f2r(233.5):f2r(237.5), :] = False
cr = bbox(c, "2. CAPTION ink (border rows excluded)")
if cr is not None:
    adv = (cr[2] - cr[0] + 1) / S
    logp(f"   advance {adv:.1f} (target 333) | left {cr[0]/S:.1f} (116) | "
         f"cap-top {cr[1]/S:.1f} (246) | desc-bottom {cr[3]/S:.1f} (276)")
    cols = c.sum(axis=0)
    nzc = np.where(cols > 0)[0]
    words = []
    for x in nzc:
        if words and x - words[-1][1] <= int(9 * S):
            words[-1][1] = x
        else:
            words.append([x, x])
    logp("   words (frame): " + str([[round(w[0]/S,1), round(w[1]/S,1)] for w in words]) +
         "  (orig: e.g. 116-170, Sobel 185-277, 2-D 290-351, filter 363-449)")

# 3. MATRIX ink exists in photo (red in matrix region) — equation-region ink check
m = red.copy()
m[:f2r(300), :] = False; m[f2r(460):, :] = False
m[:, :f2r(120)] = False; m[:, f2r(460):] = False
mr = bbox(m, "3. MATRIX+brackets ink")
if mr is not None:
    logp(f"   target frame x139..399 y314..431 (crop shifted +91 on bottom '1')")
    logp(f"   EQUATION-REGION INK: {'OK' if mr[3]-mr[1] > int(100*S) else 'FAIL — near-empty'}")

# 4. ARROW (red in gap, excluding panel border col)
ar = red.copy()
ar[:, :f2r(480)] = False; ar[:, f2r(533):] = False
ar[:f2r(330)] = False; ar[f2r(420):] = False
arr = bbox(ar, "4. ARROW ink")
if arr is not None:
    logp(f"   target frame x484..534 y347..363")

# 5. RIGHT PANEL: dark image (non-red) + red border rows/cols
d = ((lum < 120) & ~reddom).copy()
d[:, :f2r(500)] = False; d[:f2r(250)] = False; d[f2r(470):] = False
dr = bbox(d, "5. RIGHT dark image")
if dr is not None:
    logp(f"   target frame x534..884 y270..444")
rp = red.copy()
rp[:f2r(255)] = False; rp[f2r(470):] = False; rp[:, :f2r(500)] = False
rr = bbox(rp, "   right red border")
if rr is not None:
    logp(f"   border target x534..884 y270..444")

# 6. BLACK BAR rows (dark non-red, full-width rows)
bb = dark.copy()
bb[:, :f2r(30)] = False; bb[:, f2r(935):] = False
rowsum = bb.sum(axis=1)
bar_rows = np.where(rowsum > int(700 * S))[0]
if len(bar_rows):
    logp(f"6. BAR rows frame {bar_rows.min()/S:.1f}..{bar_rows.max()/S:.1f} (target 518..539, drawn 518..537.5)")
    seg = bb[bar_rows.min():bar_rows.max() + 1]
    xs = np.where(seg.any(axis=0))[0]
    logp(f"   bar x extent frame {xs.min()/S:.1f}..{xs.max()/S:.1f} (target 38..921)")

# 7. LEFT PANEL border (red cols/rows in left half, tall structures)
lp = red.copy(); lp[:f2r(220)] = False; lp[f2r(490):] = False; lp[:, f2r(485):] = False
lcol = lp.sum(axis=0); lrow = lp.sum(axis=1)
logp(f"7. LEFT PANEL border cols>150fp: {[round(x/S,1) for x in np.where(lcol > 150*S)[0]]} (targets 85,478)")
logp(f"   border rows>300fp: {[round(y/S,1) for y in np.where(lrow > 300*S)[0]]} (targets 235,476)")

# 8. PHOTO placement: top/bottom/left/right edges via non-white non-red content
pnw = ((lum < 235) & ~reddom & ~red).copy()
pnw[:f2r(250)] = False; pnw[f2r(470):] = False; pnw[:, :f2r(90)] = False; pnw[:, f2r(480):] = False
pr = bbox(pnw, "8. PHOTO content bbox")
if pr is not None:
    logp(f"   target frame x105..442 y284..454")

# 9. Containment: content ink inside house chrome (panel x42..918, y45..bottom)
content = (red | dark | (lum < 220)).copy()
ys, xs = np.where(content)
viol_x = int(((xs < f2r(42)) | (xs > f2r(918))).sum())
viol_y = int((ys < f2r(45)).sum())
logp(f"9. Containment: {viol_x} px outside panel x-range, {viol_y} px above panel top (bar by design)")

with open(f"{QA}/out_selfcheck_{K}.txt", "w") as f:
    f.write("\n".join(log) + "\n")
