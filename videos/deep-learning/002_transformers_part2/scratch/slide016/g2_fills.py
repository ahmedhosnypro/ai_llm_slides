#!/usr/bin/env python3
# g2_fills.py — fills + panel geometry gaps left by m2/m3:
#   1. matrix container interior fills (Head1/2/3) — m3's fill samples used
#      slice-relative coords as absolute (coordinate bug) and m2's tint masks
#      missed Head1/Head3 -> re-measure at known-empty interior bands
#   2. m3 container fx-offset proof (comps printed in slice coords; abs = rel + (cx0-6))
#   3. 48 matrix-cell interior fills (border/text excluded via luminance percentile)
#   4. output-pill fills per group x row (sampled at left/right inner edge + top strip)
#   5. upper/lower panel edges (F2F1EF runs) + panel border color probes
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_016.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def med(x0, y0, x1, y1):
    p = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    m = np.median(p, axis=0).astype(int)
    return "#%02X%02X%02X" % (m[0], m[1], m[2])

def cellfill(x0, y0, x1, y1):
    p = a[y0 + 3:y1 - 2, x0 + 3:x1 - 2].reshape(-1, 3)
    if len(p) < 20:
        return "n/a(too small)"
    lum = p.mean(axis=1)
    keep = p[lum >= np.percentile(lum, 55)]
    m = np.median(keep, axis=0).astype(int)
    return "#%02X%02X%02X" % (m[0], m[1], m[2])

print("=== 1. CONTAINER INTERIOR FILLS (empty top/bottom bands inside each container) ===")
# abs container rects from m3 fill-comps after offset fix: Head1 fx 311..456,
# Head2 fx 478..623, Head3 fx 637..782; fy 132..308 (fy was absolute in m3)
for nm, (x0, x1) in [("Head1", (311, 456)), ("Head2", (478, 623)), ("Head3", (637, 782))]:
    top = med(x0 + 12, 135, x1 - 12, 146)
    bot = med(x0 + 12, 293, x1 - 12, 304)
    print(f"  {nm}: top-band {top}   bottom-band {bot}")

print("=== 2. m3 fx-OFFSET PROOF (row fy=140 crossing Head2 left edge) ===")
print("  fy140 fx 470..484: " + " ".join("%02X%02X%02X" % tuple(a[140, x]) for x in range(470, 485)))
print("  (478 = abs Head2 left edge if offset theory holds; 470..476 should be panel gray)")

print("=== 3. MATRIX CELL INTERIOR FILLS (48 cells, m3 bboxes, border/text excluded) ===")
H1 = [(317,152,342,169),(353,152,379,169),(390,152,416,169),(424,152,450,169),
      (317,189,342,206),(353,189,379,206),(391,189,416,206),(424,189,450,207),
      (386,220,416,248),(353,230,378,248),(424,231,449,248),(317,232,342,249),
      (317,269,342,287),(353,269,378,287),(390,269,416,287),(424,269,449,287)]
H2 = [(483,152,508,169),(519,152,544,169),(557,152,582,169),(590,152,615,169),
      (483,189,508,206),(519,189,544,206),(557,189,581,206),(590,189,615,206),
      (519,230,544,248),(483,231,508,249),(557,231,581,248),(590,231,615,248),
      (519,269,544,287),(483,270,508,287),(556,270,581,287),(590,270,615,287)]
H3 = [(679,151,704,170),(717,151,742,170),(643,152,668,170),(750,152,776,170),
      (643,189,668,207),(679,189,705,207),(717,189,742,207),(750,189,776,206),
      (679,230,704,248),(717,230,742,248),(750,230,776,248),(643,231,668,249),
      (643,269,668,287),(679,269,704,287),(717,269,742,287),(750,269,776,287)]
for nm, cells in (("Head1", H1), ("Head2", H2), ("Head3", H3)):
    rows = {}
    for c in cells:
        rk = 0 if c[1] < 175 else (1 if c[1] < 215 else (2 if c[1] < 258 else 3))
        rows.setdefault(rk, []).append(c)
    for rk in sorted(rows):
        fills = [f"({c[0]},{c[1]}){cellfill(*c)}" for c in sorted(rows[rk], key=lambda c: c[0])]
        art = "  <-- ARTIFACT ZONE (cursor box over Head1 row-3)" if nm == "Head1" and rk == 2 else ""
        print(f"  {nm} row{rk + 1}: " + "  ".join(fills) + art)

print("=== 4. OUTPUT-PILL FILLS (3 groups x 5 rows; left/right inner edge + top strip) ===")
GROUPS = [("g1", 298, 441), ("g2", 474, 661), ("g3", 643, 767)]
ROWCY = [348, 377, 406, 435, 464]
for nm, x0, x1 in GROUPS:
    for i, cy in enumerate(ROWCY):
        lft = med(x0 + 8, cy - 1, x0 + 18, cy + 1)
        rgt = med(x1 - 18, cy - 1, x1 - 8, cy + 1)
        top = med(x0 + 30, cy - 12, x1 - 30, cy - 10)
        print(f"  {nm} row{i + 1} (cy {cy}): L {lft}  R {rgt}  top-strip {top}")

print("=== 5. PANEL EDGES (F2F1EF fill runs) ===")
def runs_on_row(fy, x_from, x_to):
    m = (np.abs(R - 242) <= 6) & (np.abs(G - 241) <= 6) & (np.abs(B - 239) <= 7)
    xs = np.nonzero(m[fy, x_from:x_to + 1])[0]
    if len(xs) == 0:
        return f"fy {fy}: none"
    return f"fy {fy}: fill fx {int(xs.min()) + x_from}..{int(xs.max()) + x_from} (n={len(xs)})"

def runs_on_col(fx, y_from, y_to):
    m = (np.abs(R - 242) <= 6) & (np.abs(G - 241) <= 6) & (np.abs(B - 239) <= 7)
    ys = np.nonzero(m[y_from:y_to + 1, fx])[0]
    if len(ys) == 0:
        return f"fx {fx}: none"
    return f"fx {fx}: fill fy {int(ys.min()) + y_from}..{int(ys.max()) + y_from} (n={len(ys)})"

for fy in (150, 200, 300):
    print("  upper " + runs_on_row(fy, 40, 920))
for fy in (340, 400, 480):
    print("  lower " + runs_on_row(fy, 40, 920))
for fx in (100, 500, 880):
    print("  upper col " + runs_on_col(fx, 100, 320))
for fx in (500, 880):
    print("  lower col " + runs_on_col(fx, 320, 519))
print("=== 6. PANEL BORDER PROBES ===")
print("  upper-left edge fy200 fx 70..79: " + " ".join("%02X%02X%02X" % tuple(a[200, x]) for x in range(70, 80)))
print("  upper-top  edge fy 108..116 @fx500: " + " ".join("%02X%02X%02X" % tuple(a[y, 500]) for y in range(108, 117)))
print("  lower-left edge fy400 fx 258..270: " + " ".join("%02X%02X%02X" % tuple(a[400, x]) for x in range(258, 271)))
print("  lower-right edge fy400 fx 888..902: " + " ".join("%02X%02X%02X" % tuple(a[400, x]) for x in range(888, 903)))
