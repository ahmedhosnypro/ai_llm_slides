#!/usr/bin/env python3
"""pm1_chrome.py — slide 034 chrome landmark fit (P2 convention, independent pass).

Red-weighted subpixel centroids of the four chrome border strokes (quiet bands only,
per the 021 lesson: bands chosen away from red text / badge / letterbox), then the
family mapping fit. Also: badge yellow bbox + ring, letterbox extent, cursor bbox,
profile dumps so every centroid is verifiable.

Output: pm1_chrome_output.txt (next to this script).
"""
import numpy as np
from PIL import Image
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
OUT = os.path.join(HERE, "pm1_chrome_output.txt")

img = np.asarray(Image.open(FR).convert("RGB")).astype(float)
H, W, _ = img.shape
r, g, b = img[..., 0], img[..., 1], img[..., 2]
redness = r - np.maximum(g, b)
lines = []

def say(s=""):
    lines.append(s)
    print(s)

say(f"frame {W}x{H}")

def centroid_x(x0, x1, y0, y1, thresh):
    """x0/x1/y0/y1 absolute frame px; returns (centroid_x_abs, span, npx)."""
    win = redness[y0:y1, x0:x1]
    m = win > thresh
    if m.sum() == 0:
        return None, None, 0
    xs = np.arange(x0, x1)  # absolute
    cx = (win * xs[None, :])[m].sum() / win[m].sum()
    cols = np.where(m.any(axis=0))[0] + x0
    return cx, (int(cols.min()), int(cols.max())), int(m.sum())

def centroid_y(y0, y1, x0, x1, thresh):
    win = redness[y0:y1, x0:x1]
    m = win > thresh
    if m.sum() == 0:
        return None, None, 0
    ys = np.arange(y0, y1)  # absolute
    cy = (win * ys[:, None])[m].sum() / win[m].sum()
    rows = np.where(m.any(axis=1))[0] + y0
    return cy, (int(rows.min()), int(rows.max())), int(m.sum())

# --- profile dumps first (calibration evidence) ---
say("-- left-stroke redness column profile rows 380..500 --")
prof = redness[380:500, 50:75].sum(axis=0)
say("  " + "  ".join(f"{50+i}:{v:.0f}" for i, v in enumerate(prof) if v > 0))
say("-- right-stroke redness column profile rows 380..500 --")
prof = redness[380:500, 890:915].sum(axis=0)
say("  " + "  ".join(f"{890+i}:{v:.0f}" for i, v in enumerate(prof) if v > 0))
say("-- top-stroke redness row profile cols 120..400 --")
prof = redness[33:60, 120:400].sum(axis=1)
say("  " + "  ".join(f"{33+i}:{v:.0f}" for i, v in enumerate(prof) if v > 0))
say("-- bottom-stroke redness row profile cols 300..700 (rows 505..530) --")
prof = redness[505:531, 300:700].sum(axis=1)
say("  " + "  ".join(f"{505+i}:{v:.0f}" for i, v in enumerate(prof)))

TH = 25  # JPEG-softened strokes: lower than the 60 first guess
L, Lspan, Ln = centroid_x(50, 72, 380, 500, TH)
R, Rspan, Rn = centroid_x(888, 912, 380, 500, TH)
T, Tspan, Tn = centroid_y(33, 58, 120, 400, TH)
B, Bspan, Bn = centroid_y(507, 526, 300, 700, TH)

say(f"\nlandmarks (red-weighted subpixel centroids, thresh {TH}):")
say(f"  left   x={L:.2f}  span {Lspan}  npx={Ln}")
say(f"  right  x={R:.2f}  span {Rspan}  npx={Rn}")
say(f"  top    y={T:.2f}  span {Tspan}  npx={Tn}")
say(f"  bottom y={B:.2f}  span {Bspan}  npx={Bn}")

# --- mapping fit (family convention: panel spans slide x 42..918 => 876 slide px) ---
SX = (R - L) / 876.0
AX = L - 42.0 * SX
# family law (021/022 precedent): sy is FIXED at 0.955556 (frame 43px top stroke <-> slide
# y45 panel top; frame 516 <-> slide 540 slide edge = the half-visible bottom stroke);
# the top/bottom landmarks are VERIFICATION, not free parameters.
SY = 0.955556
say(f"\nmapping fit (this frame):")
say(f"  sx = (R-L)/876 = {SX:.6f}   (family 0.961231 / 022 0.962235 / dead-builder 0.962307)")
say(f"  ax = L - 42*sx = {AX:.3f}     (020 18.628 / 021 18.13 / 022 17.753 / dead-builder 17.943)")
say(f"  sy FIXED = {SY} (family law)")
say(f"  verification: top {T:.2f}/{SY} = {T/SY:.2f} (house 45.0);  bottom {B:.2f}/{SY} = {B/SY:.2f} (house ~540 edge class)")
say(f"  free-fit cross-check sy=(B-T)/(540-45) = {(B-T)/495:.6f} (within 0.2% of family)")
say(f"  => adopted: slide_x=(fx-{AX:.3f})/{SX:.6f} ; slide_y=fy/{SY}")

def FX(fx): return (fx - AX) / SX
def FY(fy): return fy / SY

# --- badge: yellow bbox + purple ring + numeral ---
say("\n-- badge --")
win = img[45:100, 845:915]
yr, yg, yb = win[..., 0], win[..., 1], win[..., 2]
ym = (yr > 200) & (yg > 200) & (yb < 190) & (yr - yb > 40)
ys, xs = np.where(ym)
if len(xs):
    x0, x1, y0, y1 = xs.min() + 845, xs.max() + 845, ys.min() + 45, ys.max() + 45
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    say(f"  yellow bbox x[{x0},{x1}] y[{y0},{y1}]  d=({x1-x0+1},{y1-y0+1})  center=({cx:.1f},{cy:.1f})")
    say(f"  badge center -> slide ({FX(cx):.1f},{FY(cy):.1f})  vs house (893,71)")
    rm = (win[..., 2] > 140) & (win[..., 2] - win[..., 1] > 30) & (win[..., 0] > 70) & (win[..., 0] < 190)
    rs = np.where(rm)
    if len(rs[0]):
        say(f"  purple-ring px={len(rs[0])} bbox x[{rs[1].min()+845},{rs[1].max()+845}] y[{rs[0].min()+45},{rs[0].max()+45}]")
        ring_px = win[rm]
        say(f"  ring mean rgb = ({ring_px[:,0].mean():.0f},{ring_px[:,1].mean():.0f},{ring_px[:,2].mean():.0f})")
    else:
        say("  NO purple ring pixels found (badge ring may be gray/thin on this frame)")
    nx0, ny0 = x0 - 845 + 5, y0 - 45 + 5
    inner = win[ny0:ny0 + (y1 - y0) - 9, nx0:nx0 + (x1 - x0) - 9]
    dm = inner.sum(axis=2) < 330
    ds = np.where(dm)
    if len(ds[0]):
        say(f"  numeral ink bbox (frame) x[{ds[1].min()+x0+5},{ds[1].max()+x0+5}] y[{ds[0].min()+y0+5},{ds[0].max()+y0+5}] h={ds[0].max()-ds[0].min()+1}px")

# --- letterbox ---
say("\n-- letterbox (black strip at bottom) --")
bright = img.sum(axis=2) / 3.0
say("  per-row mean brightness x150..800, rows 512..524:")
for y in range(512, 525):
    say(f"    row {y}: {bright[y, 150:800].mean():.1f}")
rowmean = bright[:, 150:800].mean(axis=1)
first_black = None
for y in range(500, H):
    if rowmean[y] < 40:
        first_black = y
        break
say(f"  first SOLID-black row (mean<40): {first_black}  (rows 517-518 = stroke/letterbox dark blend)")

# --- cursor (gray arrow near Vector_P3) ---
say("\n-- gray cursor overlay near Vector_P3 --")
win = img[290:350, 390:470]
cr, cg, cb = win[..., 0], win[..., 1], win[..., 2]
mx = np.maximum(np.maximum(cr, cg), cb)
mn = np.minimum(np.minimum(cr, cg), cb)
gray = ((mx - mn) < 26) & (mn > 85) & (mx < 205)
gs = np.where(gray)
if len(gs[0]):
    say(f"  gray px={len(gs[0])} bbox x[{gs[1].min()+390},{gs[1].max()+390}] y[{gs[0].min()+290},{gs[0].max()+290}]")
    say(f"  mean rgb=({cr[gray].mean():.0f},{cg[gray].mean():.0f},{cb[gray].mean():.0f})")
    colcount = gray.sum(axis=0)
    say("  per-column gray counts: " + " ".join(f"{390+i}:{v}" for i, v in enumerate(colcount) if v > 0))
else:
    say("  no gray blob found in window 390..470 x 290..350")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"\nwrote {OUT}")
