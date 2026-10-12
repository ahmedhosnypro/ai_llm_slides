#!/usr/bin/env python3
"""m15_census.py — final geometry+color census for slide 047 (frame law).
Mapping (m13c final fit = 045-certified): slide_x = (fx-17.582)/0.962329, slide_y = fy/0.955556.
Every measurement printed in slide pt (1px frame = ~1.04pt at this scale)."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg"
A = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = A.shape[:2]
SX, OX, SY = 0.962329, 17.582, 0.955556
fx = lambda sx: sx * SX + OX
fy = lambda sy: sy * SY
sx = lambda x: (x - OX) / SX
sy = lambda y: y / SY
hx = lambda c: "#%02X%02X%02X" % tuple(int(round(v)) for v in c)

def med(y0, y1, x0, x1):
    return np.median(A[y0:y1, x0:x1].reshape(-1, 3), axis=0)

print("== 1. TAN CONTAINER ==")
print(" fill (clean spots):", hx(med(300, 316, 868, 890)), hx(med(196, 203, 700, 760)), hx(med(296, 305, 690, 756)))
# border scans
row = A[250, 100:150]
print(" left border cols y=250:", [(100 + i, hx(c)) for i, c in enumerate(row) if c.sum() < 560][:8])
row = A[250, 885:915]
print(" right border cols y=250:", [(885 + i, hx(c)) for i, c in enumerate(row) if c.sum() < 560][:8])
col = A[78:100, 500]
print(" top border rows x=500:", [(78 + i, hx(c)) for i, c in enumerate(col) if c.sum() < 560][:8])
col = A[466:492, 300]
print(" bottom border rows x=300:", [(466 + i, hx(c)) for i, c in enumerate(col) if c.sum() < 560][:8])
print(" -> slide: left", round(sx(126), 1), "right", round(sx(898), 1), "top", round(sy(87.5), 1), "bottom", round(sy(478), 1))

print("== 2. STRIP ROWS: cell runs at row center ==")
ROWS = {"output": 67, "A": 181, "B": 289, "C": 391, "X": 501}
for name, yc in ROWS.items():
    line = A[yc, 180:905]
    runs = []
    prev = None
    start = 180
    for i, c in enumerate(line):
        q = tuple((c // 24) * 24)
        if prev is None:
            prev, start = q, 180 + i
        elif q != prev:
            if i + 180 - start >= 4:
                runs.append((start, 180 + i, hx(np.median(A[yc, start:180 + i], axis=0))))
            prev, start = q, 180 + i
    runs.append((start, 905, hx(np.median(A[yc, start:905], axis=0))))
    print(f" {name} y={yc} (slide cy {sy(yc):.1f}): runs>=4px:")
    for a, b, h in runs:
        print(f"    fx {a}..{b} (slide {sx(a):.1f}..{sx(b):.1f}) {h}")

print("== 3. ROW top/bottom edges (gray outline rows) at col1 x=205 ==")
for name, yc in ROWS.items():
    col = A[yc - 14:yc + 14, 205]
    dark = [yc - 14 + i for i, c in enumerate(col) if c.sum() < 480]
    print(f" {name}: dark rows {dark[:3]}..{dark[-3:] if dark else []} -> slide {sy(dark[0]):.1f}..{sy(dark[-1]):.1f}" if dark else f" {name}: none")

print("== 4. DASHED GROUP CONTAINERS (green-ish px) ==")
for y0, y1, tag in [(88, 185, "unit1"), (300, 400, "unit2")]:
    reg = A[y0:y1, 110:915]
    mask = (reg[:, :, 1] > reg[:, :, 0] + 15) & (reg[:, :, 1] > reg[:, :, 2] + 15)
    ys, xs = np.nonzero(mask)
    if len(ys):
        rows_with = np.unique(ys)
        # cluster rows
        cl, cur = [], [rows_with[0]]
        for r in rows_with[1:]:
            if r - cur[-1] <= 2: cur.append(r)
            else: cl.append(cur); cur = [r]
        cl.append(cur)
        print(f" {tag}: green row-clusters (frame y):", [(y0 + c[0], y0 + c[-1], int((ys >= c[0]) & (ys <= c[-1])).__class__ and len(xs[(ys >= c[0]) & (ys <= c[-1])])) for c in cl][:6])
        top = cl[0]; bot = cl[-1]
        tys = ys[(ys >= top[0]) & (ys <= top[-1])]
        print(f"   top edge frame y {y0+top[0]}..{y0+top[-1]} x {xs[(ys>=top[0])&(ys<=top[-1])].min()}..{xs[(ys>=top[0])&(ys<=top[-1])].max()} -> slide y {sy(y0+top[0]):.1f} x {sx(xs[(ys>=top[0])&(ys<=top[-1])].min()):.1f}..{sx(xs[(ys>=top[0])&(ys<=top[-1])].max()):.1f}")
        bys = ys[(ys >= bot[0]) & (ys <= bot[-1])]
        print(f"   bottom edge frame y {y0+bot[0]}..{y0+bot[-1]} -> slide y {sy(y0+bot[0]):.1f}")
        samp = reg[(ys[:200], xs[:200])]
        print("   dash color median:", hx(np.median(samp, axis=0)))
    else:
        print(f" {tag}: no green px")

print("== 5. LN BARS ==")
for tag, ytop, ybot in [("LN1", 101, 130), ("LN2", 312, 341)]:
    ymid = (ytop + ybot) // 2
    line = A[ymid, 150:895]
    # bar fill vs container fill: find where color ~ (235,176,118)
    isbar = [i for i, c in enumerate(line) if abs(c[0] - 235) < 14 and abs(c[1] - 176) < 14 and abs(c[2] - 118) < 16]
    print(f" {tag}: bar-fill x extent {150+isbar[0]}..{150+isbar[-1]} -> slide {sx(150+isbar[0]):.1f}..{sx(150+isbar[-1]):.1f}; fill {hx(med(ytop+6, ybot-6, 200, 300))}")
    print(f"   top {sy(ytop):.1f} bottom {sy(ybot):.1f} h {sy(ybot-ytop):.1f}")

print("== 6. MHA BAR ==")
line = A[445, 120:915]
isbar = [i for i, c in enumerate(line) if c[0] < 190 and c[2] > c[1] and c.sum() < 420]
print(f" bar x extent {120+isbar[0]}..{120+isbar[-1]} -> slide {sx(120+isbar[0]):.1f}..{sx(120+isbar[-1]):.1f}")
print(f" y 415..471 -> slide {sy(415):.1f}..{sy(471):.1f} h {sy(56):.1f}; fill {hx(med(455, 465, 300, 360))}")
reg = A[436:452, 380:666]
ink = reg.reshape(-1, 3)[(reg.reshape(-1, 3).sum(axis=1) > 560)]
print(" text px median:", hx(np.median(ink, axis=0)) if len(ink) else "none", "n=", len(ink))

print("== 7. FFN BOX ==")
print(" interior fill:", hx(med(230, 240, 620, 630)), hx(med(252, 258, 240, 250)))
line = A[235, 145:910]
# border = orange darker
print(" header ink: darkest in rows 211..224 x 282..770:", end=" ")
reg = A[211:225, 282:770].reshape(-1, 3)
dk = reg[reg.sum(axis=1) < 420]
print(hx(np.median(dk, axis=0)) if len(dk) else "none", "n=", len(dk))
# tiles: scan row through tile dot band y=247
line = A[247, 150:905]
runs = []
prev, start = None, 150
for i, c in enumerate(line):
    q = tuple((c // 28) * 28)
    if prev is None: prev, start = q, 150 + i
    elif q != prev:
        if 150 + i - start >= 5: runs.append((start, 150 + i, hx(np.median(A[247, start:150 + i], axis=0))))
        prev, start = q, 150 + i
print(" tile band y=247 runs>=5:", [(a, b, h) for a, b, h in runs][:24])
# tile edges at col1: vertical scan x=205
col = A[222:268, 205]
print(" col1 tile vertical x=205:", [(222 + i, hx(c)) for i, c in enumerate(col)][::4])

print("== 8. PLUS DISCS + ARROWS zones ==")
for tag, yc in [("u1", 151), ("u2", 363)]:
    line = A[yc, 180:905]
    isd = [i + 180 for i, c in enumerate(line) if c[0] > 150 and c[1] < 140 and c[2] < 110]
    # cluster
    cl, cur = [], None
    for x in isd:
        if cur and x - cur[-1] <= 3: cur.append(x)
        else:
            if cur: cl.append(cur)
            cur = [x]
    if cur: cl.append(cur)
    print(f" {tag} disc x-clusters:", [(c[0], c[-1], round(sx((c[0]+c[-1])/2), 1)) for c in cl])
# green arrows zones
for tag, y0, y1 in [("rowC->p2", 368, 380), ("p2->LN2", 344, 360), ("LN2->rowB", 312, 320),
                    ("rowA->p1", 163, 171), ("p1->LN1", 132, 148), ("red out", 76, 99)]:
    reg = A[y0:y1, 180:905]
    if tag == "red out":
        mask = (reg[:, :, 0] > 130) & (reg[:, :, 1] < 90) & (reg[:, :, 2] < 90)
    else:
        mask = (reg[:, :, 1] > reg[:, :, 0] + 25) & (reg[:, :, 1] > reg[:, :, 2] + 25)
    n = int(mask.sum())
    if n:
        xs = np.nonzero(mask.any(axis=0))[0] + 180
        samp = reg[mask]
        print(f" {tag}: n={n} x {xs.min()}..{xs.max()} color {hx(np.median(samp, axis=0))}")
    else:
        print(f" {tag}: none")

print("== 9. BLOCK ARROWS: zone X->MHA (frame y 474..492) col1 ==")
reg = A[473:493, 195:216]
print(" px sample:", [hx(c) for c in reg.reshape(-1, 3)[::40]][:10])
reg2 = A[401:414, 340:362]
dk2 = reg2.reshape(-1, 3); dk2 = dk2[dk2.sum(axis=1) < 400]
print(" zone1 arrow dark px median:", hx(np.median(dk2, axis=0)) if len(dk2) else "none", "n=", len(dk2))
lt2 = reg2.reshape(-1, 3); lt2 = lt2[lt2.sum(axis=1) > 640]
print(" zone1 arrow light px median:", hx(np.median(lt2, axis=0)) if len(lt2) else "none")
reg3 = A[267:279, 340:362]
dk3 = reg3.reshape(-1, 3); dk3 = dk3[dk3.sum(axis=1) < 400]
print(" FFN-gap-down dark px median:", hx(np.median(dk3, axis=0)) if len(dk3) else "none")

print("== 10. VERTICAL TITLE ==")
reg = A[118:424, 60:160]
mask = reg.sum(axis=2) < 480
ys = np.sort(np.nonzero(mask.any(axis=1))[0]) + 118
cl, cur = [], [ys[0]]
for y in ys[1:]:
    if y - cur[-1] <= 3: cur.append(y)
    else: cl.append(cur); cur = [y]
cl.append(cur)
print(" letter bands:", [(c[0], c[-1]) for c in cl])
for c in cl[:4]:
    sub = mask[(c[0] - 118):(c[-1] - 118 + 1)]
    xs = np.nonzero(sub.any(axis=0))[0]
    print(f"   band {c[0]}..{c[-1]}: x {60+xs.min()}..{60+xs.max()} (cap w {xs.max()-xs.min()+1}px={ (xs.max()-xs.min()+1)/SY:.1f}pt)")
ink = reg[mask]
print(" title ink median:", hx(np.median(ink, axis=0)), "n=", len(ink))

print("== 11. BLOCK OUTPUT / INPUT BOXES ==")
for tag, y0, y1 in [("Output", 36, 95), ("Input", 470, 522)]:
    reg = A[y0:y1, 40:210]
    mask = (reg[:, :, 0] > 120) & (reg[:, :, 1] < 80) & (reg[:, :, 2] < 80)
    ys2, xs2 = np.nonzero(mask)
    if len(ys2):
        print(f" {tag}: red px bbox frame x {40+xs2.min()}..{40+xs2.max()} y {y0+ys2.min()}..{y0+ys2.max()} -> slide x {sx(40+xs2.min()):.1f}..{sx(40+xs2.max()):.1f} y {sy(y0+ys2.min()):.1f}..{sy(y0+ys2.max()):.1f}")
        # border rows: rows where red count > 40
        rc = mask.sum(axis=1)
        brows = [(y0 + i, int(n)) for i, n in enumerate(rc) if n > 40]
        print("   red-heavy rows:", brows[:8])
        # fill: center of bbox away from text
        cx0, cx1 = 40 + xs2.min(), 40 + xs2.max()
        print("   fill near left edge:", hx(med(y0 + (ys2.min()) + 6, y0 + ys2.max() - 6, cx0 + 4, cx0 + 14)))
        # text ink
        tmask = mask.copy()
        ink = reg[tmask]
        print("   red ink median:", hx(np.median(ink, axis=0)))

print("== 12. misc fills ==")
print(" panel gray (right of container):", hx(med(300, 320, 905, 918)), " left of container:", hx(med(300, 320, 100, 118)))
print(" output row bg:", hx(med(45, 52, 300, 320)), " X row bg:", hx(med(512, 515, 300, 320)))
print(" black strip top:", [(y, hx(A[y, 480])) for y in (514, 516, 518, 520)])
