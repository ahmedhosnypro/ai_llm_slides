#!/usr/bin/env python3
"""measure5: close the remaining unknowns on remapped 002:8."""
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
f8 = np.asarray(Image.open(f"{ROOT}/002_transformers_part2/scratch/slide008/frame8_remapped_960x540.png").convert("RGB")).astype(int)
f33 = np.asarray(Image.open(f"{ROOT}/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
r, g, b = f8[:, :, 0], f8[:, :, 1], f8[:, :, 2]

def ascii_map(img, x0, x1, y0, y1, test, step=2):
    print("    " + "".join(str((x // 10) % 10) for x in range(x0, x1, step)))
    for y in range(y0, y1, step):
        line = ""
        for x in range(x0, x1, step):
            line += "#" if test(img[y, x]) else "."
        print(f"{y:4d}" + line)

print("=== K.q region map (reddish: r-g>35 & r>110), 8 then 33 ===")
tst = lambda p: p[0] - p[1] > 35 and p[0] > 110
ascii_map(f8, 325, 378, 194, 218, tst)
print("--- 33 ---")
ascii_map(f33, 325, 378, 194, 218, tst)

print("\n=== W_q box: blue-over-yellow (g-b>30, g-r>8) x250..350 y390..485 ===")
wq = ((g - b > 30) & (g - r > 8) & (g > 150)).copy()
wqc = wq.copy(); wqc[:390, :] = False; wqc[485:, :] = False; wqc[:, :250] = False; wqc[:, 350:] = False
ys, xs = np.where(wqc)
if len(ys):
    print(f"bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")
    for yy in range(ys.min(), ys.max() + 1, 8):
        m = ys == yy
        if m.sum() > 3: print(f"  row {yy}: x {xs[m].min()}..{xs[m].max()} n={int(m.sum())}")

print("\n=== q2 label: red ink x262..296 y380..430 (left of arrow) ===")
q2 = ((r - g > 45) & (r > 110)).copy(); q2[:380, :] = False; q2[430:, :] = False; q2[:, :262] = False; q2[:, 296:] = False
ys, xs = np.where(q2)
if len(ys): print(f"q2 ink: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n=== vertical red line profile x294..306, y350..445 ===")
redl = ((r - g > 45) & (r > 110))
for yy in range(350, 446, 5):
    rr = np.where(redl[yy, 294:307])[0]
    if len(rr): print(f"  y{yy}: x {[294 + int(v) for v in rr]}")

print("\n=== X2->W_q arrow: red x302..318 y440..480 ===")
for yy in range(440, 481, 4):
    rr = np.where(redl[yy, 300:320])[0]
    if len(rr): print(f"  y{yy}: x {[300 + int(v) for v in rr]}")

print("\n=== X2 highlight magenta border profiles ===")
mag = ((r - g > 50) & (b - g > 20) & (r > 100)).copy()
mg = mag.copy(); mg[:465, :] = False; mg[520:, :] = False; mg[:, :245] = False; mg[:, 345:] = False
rows = mg.sum(axis=1); cols = mg[465:520, :].sum(axis=0)
print("  rows>6:", {y: int(rows[y]) for y in range(465, 520) if rows[y] > 6})
print("  cols>6:", {x: int(cols[x]) for x in range(245, 345) if cols[x] > 6})

print("\n=== sentence container fill (E7FFE9) rows x180..480 ===")
pg = ((abs(r - 231) < 14) & (g > 246) & (abs(b - 233) < 14)).copy()
pf = pg.copy(); pf[:, :180] = False; pf[:, 480:] = False
rows = pf[440:540, 180:480].sum(axis=1)
on = [440 + i for i, v in enumerate(rows) if v > 60]
print("  fill rows:", on[0], "..", on[-1] if on else None)
cols = pf[455:535, 150:520].sum(axis=0)
onc = [150 + i for i, v in enumerate(cols) if v > 20]
print("  fill cols:", onc[0], "..", onc[-1] if onc else None)

print("\n=== W_k box bands: dark-green border rows x158..198 ===")
dkg = ((g - r > 25) & (abs(r - 120) < 50) & (abs(g - 178) < 50) & (abs(b - 120) < 50)).copy()
dkb = dkg.copy(); dkb[:, :158] = False; dkb[:, 198:] = False
rows = dkb[215:405, 158:198].sum(axis=1)
print("  border rows>18:", {215 + i: int(v) for i, v in enumerate(rows) if v > 18})
print("  fill samples:", [tuple(int(v) for v in f8[y, 163]) for y in [244, 248, 288, 292, 330, 334, 378, 382]])
print("  fill samples right edge:", [tuple(int(v) for v in f8[y, 193]) for y in [244, 288, 330, 378]])

print("\n=== W_v box bands: border rows x706..742 ===")
rows = dkb[215:405, 706:742].sum(axis=1)
print("  darkgreen rows>12:", {215 + i: int(v) for i, v in enumerate(rows) if v > 12})
olv = ((r > 130) & (r < 200) & (g > 140) & (g < 210) & (b < 110)).copy()
ovb = olv.copy(); ovb[:, :706] = False; ovb[:, 742:] = False
rows = ovb[215:405, 706:742].sum(axis=1)
print("  olive rows>12:", {215 + i: int(v) for i, v in enumerate(rows) if v > 12})
print("  fill samples:", [tuple(int(v) for v in f8[y, 713]) for y in [244, 248, 288, 292, 330, 334, 378, 382]])
print("  fill samples right:", [tuple(int(v) for v in f8[y, 735]) for y in [244, 288, 330, 378]])

print("\n=== K vector (x204..238 y228..246) 8 vs 33 ===")
print("  8 :", [tuple(int(v) for v in f8[237, x]) for x in range(204, 239, 6)])
print("  33:", [tuple(int(v) for v in f33[237, x]) for x in range(204, 239, 6)])
print("=== V vector (x664..700 y228..246) ===")
print("  8 :", [tuple(int(v) for v in f8[237, x]) for x in range(664, 700, 6)])
print("  33:", [tuple(int(v) for v in f33[237, x]) for x in range(664, 700, 6)])

print("\n=== blue circle via 8-vs-33 tint diff ===")
tintdiff = (b - r) - (f33[:, :, 2] - f33[:, :, 0])
td = (tintdiff > 18).copy(); td[:300, :] = False; td[532:, :] = False; td[:, :200] = False; td[:, 420:] = False
ys, xs = np.where(td)
print("  diff-tint px:", len(ys))
if len(ys):
    for yy in range(ys.min(), ys.max() + 1, 10):
        m = ys == yy
        if m.sum() > 5: print(f"  row {yy}: x {xs[m].min()}..{xs[m].max()} n={int(m.sum())}")
    # alpha over peach: mean tintdiff in clean area
    sel = td & (np.arange(f8.shape[0])[:, None] >= 340) & (np.arange(f8.shape[0])[:, None] <= 380)
    vals = tintdiff[sel]
    print(f"  mean tintdiff y340..380: {vals.mean():.1f} -> alpha over peach = {vals.mean()/160:.2f}")

print("\n=== block arrow rows x250..330 y500..535 ===")
chunky = ((r - g > 70) & (r - b > 70) & (r > 130)).copy()
ca = chunky.copy(); ca[:500, :] = False; ca[536:, :] = False; ca[:, :250] = False; ca[:, 330:] = False
for yy in range(500, 536, 3):
    rr = np.where(ca[yy])[0]
    if len(rr) > 1: print(f"  y{yy}: x {rr.min() + 250}..{rr.max() + 250} n={len(rr)}")

print("\n=== Y2 region: green rows x535..635 y105..175 ===")
grn = ((g - r > 30) & (g - b > 20) & (g > 110)).copy()
gb = grn.copy(); gb[:, :535] = False; gb[:, 635:] = False; gb[:105, :] = False; gb[175:, :] = False
rows = gb.sum(axis=1)
print("  green rows>4:", {105 + i: int(v) for i, v in enumerate(rows) if v > 4})
for yy in [117, 121, 125, 133, 141, 146, 152, 158, 163]:
    rr = np.where(gb[yy])[0]
    if len(rr): print(f"  y{yy}: x {rr.min() + 535}..{rr.max() + 535}")

print("\n=== red triangle head near Y2 (x570..600 y138..165) ===")
tri = ((r - g > 70) & (r - b > 70) & (r > 110)).copy()
tb = tri.copy(); tb[:138, :] = False; tb[168:, :] = False; tb[:, :565] = False; tb[:, 605:] = False
ys, xs = np.where(tb)
if len(ys): print(f"  tri ink: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n=== legend W box (C87A2A border) x780..840 y460..510 ===")
wb = ((r > 170) & (r < 230) & (g > 90) & (g < 160) & (b < 90)).copy()
wbb = wb.copy(); wbb[:455, :] = False; wbb[:, 770:] = False; wbb[:, 850:] = False
ys, xs = np.where(wbb)
if len(ys): print(f"  legend orange ink: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n=== convergence lines present? red rows x275..340 y330..400 (thin) ===")
cv = redl.copy(); cv[:330, :] = False; cv[400:, :] = False; cv[:, :275] = False; cv[:, 340:] = False
print("  red px count:", int(cv.sum()))

print("\n=== dot centroid check (navy) x250..350 y200..420 ===")
navy = ((b - r > 60) & (b - g > 60) & (b > 100) & (b < 220)).copy()
nv = navy.copy(); nv[:200, :] = False; nv[:, :250] = False; nv[:, 350:] = False; nv[420:, :] = False
ys, xs = np.where(nv)
if len(ys):
    order = np.argsort(ys); ys_s = ys[order]; xs_s = xs[order]
    start = 0
    for i in range(1, len(ys_s) + 1):
        if i == len(ys_s) or ys_s[i] - ys_s[i - 1] > 12:
            cy = ys_s[start:i].mean(); cx = xs_s[start:i].mean()
            print(f"  dot: centroid ({cx:.1f},{cy:.1f}) n={i - start}")
            start = i
