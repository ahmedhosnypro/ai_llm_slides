#!/usr/bin/env python3
"""slide033 debug3: precise probes on render_1 (all in slide pt)."""
import numpy as np
from PIL import Image

ra = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide033/render_3.png").convert("RGB")).astype(int)
RPT = 72 / 150.0
X = lambda pt: int(pt / RPT)
Y = lambda pt: int(pt / RPT)

def xext_red(ypt0, ypt1, x0, x1, label):
    sub = ra[Y(ypt0):Y(ypt1), X(x0):X(x1)]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    m = (r > 130) & (g < 100) & (b < 100)
    ys, xs = np.where(m)
    if len(xs) == 0:
        print(f"  {label}: NO RED")
        return
    print(f"  {label}: x {xs.min()*RPT+x0:.1f}..{xs.max()*RPT+x0:.1f} (n={len(xs)})")

def xext_col(ypt0, ypt1, x0, x1, label, mask_fn):
    sub = ra[Y(ypt0):Y(ypt1), X(x0):X(x1)]
    m = mask_fn(sub[..., 0], sub[..., 1], sub[..., 2])
    ys, xs = np.where(m)
    if len(xs) == 0:
        print(f"  {label}: NO INK")
        return None
    print(f"  {label}: x {xs.min()*RPT+x0:.1f}..{xs.max()*RPT+x0:.1f} y {ys.min()*RPT+ypt0:.1f}..{ys.max()*RPT+ypt0:.1f} (n={len(xs)})")
    return (xs.min() * RPT + x0, xs.max() * RPT + x0, ys.min() * RPT + ypt0, ys.max() * RPT + ypt0)

navy = lambda r, g, b: (b > 100) & (r < 100) & (b - r > 40)
red = lambda r, g, b: (r > 130) & (g < 100) & (b < 100)
dark = lambda r, g, b: (r < 120) & (g < 120) & (b < 120)
green_t = lambda r, g, b: (r < 150) & (g > 120) & (g < 200) & (g - r > 40) & (g - b > 40)

print("== TITLE (red, y48..70, x60..900) ==")
xext_col(48, 70, 60, 900, "title ink", red)
print("   orig: x326.0..611.1 y50.2..64.9")
print("== SUBTITLE (navy, y70..100) ==")
xext_col(70, 100, 60, 900, "subtitle ink", navy)
print("   orig: x129.4..812.9 y74.3..94.2")
print("== INDEX VALUES (red in strip x258..300) ==")
for v, b in [("i",143.4),("0",183.1),("1",213.5),("2",252.2),("3",284.6),("4",321.3),
             ("5",357.0),("2k",384.1),("2k+1",419.6),("d-1-1",484.5),("d-1",520.1)]:
    xext_red(b - 16, b + 3, 255, 302, f"idx {v}")
print("== VEC VALUES (dark) ==")
for v, b, cx in [("0",167.4,227.4),("1",236.5,227.4),("2",307.7,227.4),("K",406.0,227.4),("[d/2]-1",511.7,231.4)]:
    xext_col(b - 16, b + 3, cx - 22, cx + 22, f"vec {v}", dark)
print("== PAIR TEXTS (colored) ==")
rows = [("b1L1",141,158,"green_t"),("b1L2",172,196,"green_t"),("b2L1",203,228,"red"),
        ("b2L2",238,265,"red"),("b3L1",272,298,"green_t"),("b3L2",308,334,"green_t"),
        ("b4L1",372,398,"red"),("b4L2",406,433,"red"),("b5L1",471,498,"green_t"),("b5L2",508,535,"green_t")]
for lab, y0, y1, mk in rows:
    xext_col(y0, y1, 320, 400, lab, red if mk == "red" else green_t)
print("== EQ internals ==")
xext_col(370, 395, 720, 760, "omega(red)", red)
xext_col(388, 400, 745, 765, "Ksub(navy)", navy)
xext_col(380, 392, 760, 782, "eqbars(navy)", navy)
xext_col(382, 390, 780, 870, "fracbar(navy)", navy)
xext_col(360, 382, 810, 830, "one(dark)", dark)
xext_col(392, 414, 780, 845, "10000(dark)", dark)
xext_col(388, 404, 836, 870, "2k/d(red)", red)
print("== dx1 bracket + label ==")
xext_col(130, 530, 404, 420, "dx1 stem(red)", red)
xext_col(515, 540, 405, 460, "dx1 label(red)", red)
print("== navy mystery y225..245 ==")
xext_col(225, 245, 40, 900, "navy y225-245", navy)
xext_col(225, 245, 40, 210, "navy y225-245 x<210", navy)
xext_col(225, 245, 210, 320, "navy y225-245 x210-320", navy)
xext_col(225, 245, 320, 700, "navy y225-245 x320-700", navy)
print("== info box lines (dark, x48..202) ==")
xext_col(240, 335, 50, 200, "info dark ink", dark)
print("== omega box line bands (navy, x470..900) ==")
import scipy.ndimage as ndi
sub = ra[Y(312):Y(536), X(478):X(895)]
m = navy(sub[..., 0], sub[..., 1], sub[..., 2])
rows = m.sum(axis=1)
y = 0
bands = []
while y < len(rows):
    if rows[y] > 4:
        y2 = y
        while y2 < len(rows) - 1 and rows[y2 + 1] > 4:
            y2 += 1
        xs = np.where(m[y:y2 + 1].any(axis=0))[0]
        bands.append((312 + y * RPT, 312 + y2 * RPT, 478 + xs.min() * RPT, 478 + xs.max() * RPT))
        y = y2 + 1
    else:
        y += 1
for bd in bands:
    print(f"  navy band y {bd[0]:.1f}..{bd[1]:.1f} x {bd[2]:.1f}..{bd[3]:.1f}")
print("   orig: A1 320.2..329.6 x482.1..762.9 | A2 339.1..348.5 x482.1..747.3 | B1 424.9..437.4 x488.3..863.9")
print("         B2 443.7..456.3 x488.3..853.5 | Note 475.1..484.5 x487.3..519.5 | C2 494.0..506.5 x497.7..872.2")
print("         C3 512.8..525.3 x497.7..835.8")
