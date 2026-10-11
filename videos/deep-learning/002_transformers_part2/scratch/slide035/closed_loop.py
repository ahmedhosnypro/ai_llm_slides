#!/usr/bin/env python3
"""Closed-loop verification: PIL-measure ink bands in the 150dpi render (attempt K)
and compare to the mapped targets from the original frame (slide pts, 1pt = 150/72 px).
Tolerance ~4px @150dpi. Usage: closed_loop.py <render.png>"""
import sys
from PIL import Image
import numpy as np

REN = sys.argv[1]
K = REN  # for label
im = Image.open(REN).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
PT = 150 / 72.0

print(f"render: {W}x{H}  ({REN})")

# --- targets from the original frame measurement (slide pts)
targets = {
    "title":  dict(L=159.5, R=793.1, capTop=163.78, base=199.12),
    "adding": dict(L=105.4, base=332.27, ascTop=306.11),
    "l1":     dict(L=202.21, capTop=356.35, base=382.51),
    "l2":     dict(L=202.21, capTop=397.06, base=422.28),
    "l3":     dict(L=202.21, capTop=436.87, base=461.98),
}

# --- title red band (exclude chrome border: keep x 120..1880 render px, y 290..470)
red = (R > 120) & (R - G > 60) & (R - B > 60)
red[:290, :] = False; red[470:, :] = False
red[:, :120] = False; red[:, 1880:] = False
ys, xs = np.where(red)
if len(xs) == 0:
    print("TITLE: NO INK — BLOCKER"); sys.exit(1)
tL, tR, tT, tB = xs.min(), xs.max(), ys.min(), ys.max()
exp = targets["title"]
print(f"TITLE: x {tL}..{tR} (target {exp['L']*PT:.0f}..{exp['R']*PT:.0f}, dL {tL-exp['L']*PT:+.1f} dR {tR-exp['R']*PT:+.1f})  "
      f"y {tT}..{tB} (capTop {exp['capTop']*PT:.0f}, d {tT-exp['capTop']*PT:+.1f})")
# baseline: last row with count > 30% of max row count in the band
rows = red.sum(axis=1); band = rows[tT:tB+1]
mx = band.max()
title_base_row = max(y for y in range(tT, tB+1) if rows[y] > 0.35*mx)
print(f"       baseline (35% cut) row {title_base_row} vs target {exp['base']*PT:.0f} (d {title_base_row-exp['base']*PT:+.1f})")
ink_w = tR - tL + 1
print(f"       ink width {ink_w} (mapped target ink w {(exp['R']-exp['L'])*PT:.0f})")

# --- blue bands
blue = (B - R > 60) & (B - G > 60)
blue[:560, :] = False  # below title only
ys, xs = np.where(blue)
rows_sorted = sorted(set(ys))
bands = []
start = prev = rows_sorted[0]
for y in rows_sorted[1:]:
    if y - prev > 6:
        bands.append((start, prev)); start = y
    prev = y
bands.append((start, prev))
names = ["adding", "l1", "l2", "l3"]
ok = True
for name, (y0, y1) in zip(names, [b for b in bands if b[1]-b[0] > 15]):
    m = (ys >= y0) & (ys <= y1)
    lx, ly = xs[m], ys[m]
    e = targets[name]
    # baseline via 35% cut
    rh = blue.sum(axis=1)
    mx = rh[y0:y1+1].max()
    base_row = max(y for y in range(y0, y1+1) if rh[y] > 0.35*mx)
    top_t = e.get('capTop', e.get('ascTop'))
    print(f"{name.upper()}: x {lx.min()}..{lx.max()} (target L {e['L']*PT:.0f}, dL {lx.min()-e['L']*PT:+.1f})  "
          f"y {y0}..{y1}  top d {y0-top_t*PT:+.1f}  baseline d {base_row-e['base']*PT:+.1f}")
    if abs(lx.min()-e['L']*PT) > 6 or abs(base_row-e['base']*PT) > 6:
        ok = False
d_ok = abs(tL-exp['L']*PT) <= 6 and abs(tR-exp['R']*PT) <= 6 and abs(title_base_row-exp['base']*PT) <= 6
print("CLOSED LOOP:", "PASS" if (ok and d_ok) else "NEEDS CORRECTION")
