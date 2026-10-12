#!/usr/bin/env python3
"""forensics21: corrected scaling. Star/badge-window + arrow region, org vs render_5.
Render 2001x1125 (s=ren_H/540). Frame px for org; render/s for ren."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
org = np.asarray(Image.open(VID + "/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(VID + "/recreated_pptx/qa/slide045/render_5.png").convert("RGB")).astype(int)
s = ren.shape[0] / 540.0
print(f"org {org.shape[:2]}, ren {ren.shape[:2]}, s={s:.4f}")

def masks(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return {
        "yel": (r > 200) & (g > 200) & (b < 190),
        "yel2": (r > 200) & (g > 200) & (b < 220),
        "red": (r > 120) & (g < 110) & (b < 110),
        "dark": (r < 110) & (g < 110) & (b < 110),
    }
O, R = masks(org), masks(ren)

def rslice(m, x0, x1, y0, y1):  # frame-coords slice of the render
    return m[int(y0*s):int(y1*s), int(x0*s):int(x1*s)]

print("== A. checker-yellow in BADGE WINDOW x857..929 y35..107 (frame) ==")
for name, M, sl in (("org", O, lambda m: m[35:107, 857:929]), ("ren5", R, lambda m: rslice(m, 857, 929, 35, 107))):
    w = sl(M["yel"])
    n = int(w.sum())
    if n:
        ys, xs = np.where(w)
        print(f"  {name}: n={n} bbox x{857+xs.min()}..{857+xs.max()} y{35+ys.min()}..{35+ys.max()}")
    else:
        print(f"  {name}: n=0")
    # loose yellow too
    w2 = sl(M["yel2"]); n2 = int(w2.sum())
    if n2:
        ys, xs = np.where(w2)
        print(f"  {name} loose: n={n2} bbox x{857+xs.min()}..{857+xs.max()} y{35+ys.min()}..{35+ys.max()}")

print("== B. star ink bbox (loose-yellow|red) region x730..935 y25..175 (frame) ==")
for name, M, sl in (("org", O, lambda m: m[25:175, 730:935]), ("ren5", R, lambda m: rslice(m, 730, 935, 25, 175))):
    m = M["yel2"] | M["red"]
    w = sl(m)
    ys, xs = np.where(w)
    if len(ys):
        print(f"  {name}: star ink bbox x{730+xs.min()}..{730+xs.max()} y{25+ys.min()}..{25+ys.max()} n={len(ys)}")

print("== C. ren5 star bottom envelope (frame coords, x756..935 step 4) ==")
m = rslice(R["yel2"] | R["red"], 730, 935, 25, 175)
for x in range(0, 200, 6):
    col = np.where(m[:, x])[0]
    if len(col):
        print(f"  x{730+x}: y {25+col.min()}..{25+col.max()}", end="  |")
print()

print("== D. line-1 dark ink y117..150 x756..900 (frame) — is 'values),' visible? ==")
for name, M, sl in (("org", O, lambda m: m[117:150, 756:900]), ("ren5", R, lambda m: rslice(m, 756, 900, 117, 150))):
    w = sl(M["dark"])
    ys, xs = np.where(w)
    print(f"  {name}: n={len(ys)} bbox x{756+xs.min()}..{756+xs.max()} y{117+ys.min()}..{117+ys.max()}" if len(ys) else f"  {name}: none")

print("== E. ARROW region map org x596..636 y334..362 (w=sub_a zone) ==")
def amap(Mred, Mdark, sl_red, sl_dark, x0, x1, y0, y1, tag):
    print(f"  -- {tag} (left x{x0}) --")
    rr, dd = sl_red(Mred)[0:y1-y0, 0:x1-x0], sl_dark(Mdark)[0:y1-y0, 0:x1-x0]
    for i in range(y1-y0):
        row = ""
        for j in range(x1-x0):
            row += "r" if rr[i, j] else ("#" if dd[i, j] else ".")
        print(f"  y{y0+i:3d} {row}")
amap(O["red"], O["dark"], lambda m: m[334:362, 596:636], lambda m: m[334:362, 596:636], 596, 636, 334, 362, "ORG wedge/sub zone x596..636")
amap(R["red"], R["dark"], lambda m: rslice(m, 596, 636, 334, 362), lambda m: rslice(m, 596, 636, 334, 362), 596, 636, 334, 362, "REN5 wedge/sub zone x596..636")

print("== F. vertical red band org x688..712 y292..330 and y455..480 (top/bottom ends) ==")
amap(O["red"], O["dark"], lambda m: m[292:330, 688:712], lambda m: m[292:330, 688:712], 688, 712, 292, 330, "ORG vert band TOP x688..712")
amap(O["red"], O["dark"], lambda m: m[455:480, 688:712], lambda m: m[455:480, 688:712], 688, 712, 455, 480, "ORG vert band BOTTOM x688..712")

print("== G. shaft-band red cols y346..356 x624..700 (frame) ==")
for name, M, sl in (("org", O, lambda m: m[346:356, 624:700]), ("ren5", R, lambda m: rslice(m, 624, 700, 346, 356))):
    w = sl(M["red"])
    cols = np.where(w.any(axis=0))[0] + 624
    print(f"  {name}: red cols n={len(cols)}: {list(cols)}")

print("== H. ren5 vertical red band x688..712 (ren coords) sample rows ==")
rr = rslice(R["red"], 688, 712, 292, 480)
rowsum = rr.sum(axis=1)
nz = np.where(rowsum > 0)[0]
if len(nz):
    print(f"  ren5 vert red present rows y{292+nz.min()}..{292+nz.max()}, per-row max width {rowsum.max()}")
