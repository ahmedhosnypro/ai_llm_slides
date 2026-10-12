#!/usr/bin/env python3
"""m20_final.py — last probes: dashed container edges/interior, block-arrow colors per zone,
purple short arrows, LN bar width, IO box borders, fan/RELU colors."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg"
A = np.asarray(Image.open(F).convert("RGB")).astype(int)
SX, OX, SY = 0.962329, 17.582, 0.955556
sx = lambda x: (x - OX) / SX
sy = lambda y: y / SY
hx = lambda c: "#%02X%02X%02X" % tuple(int(round(v)) for v in c)

print("== 1. DASHED CONTAINER edges (multi-column scans) ==")
for tag, y0, y1 in [("u1 top", 90, 102), ("u1 bottom", 164, 176), ("u2 top", 298, 312), ("u2 bottom", 372, 384)]:
    for xc in (250, 400, 520, 640, 700):
        col = A[y0:y1, xc]
        dark = [(y0 + i, hx(c)) for i, c in enumerate(col) if abs(c[0]-232)+abs(c[1]-178)+abs(c[2]-114) > 70]
        if dark: print(f" {tag} x={xc}: {dark[:6]}")

print("== 2. DASHED CONTAINER interior fill (clean spots) ==")
print(" u1 interior (slide 285, y~141):", hx(np.median(A[139:146, 287:297].reshape(-1,3),axis=0)))
print(" u1 interior (slide 720, y~141):", hx(np.median(A[139:146, 710:720].reshape(-1,3),axis=0)))
print(" u2 interior (slide 285, y~352):", hx(np.median(A[350:357, 287:297].reshape(-1,3),axis=0)))
print(" outside compare tan:", hx(np.median(A[139:146, 905:915].reshape(-1,3),axis=0)))

print("== 3. BLOCK ARROWS per zone at col1 (x 196..214) ==")
for tag, y0, y1 in [("X->MHA", 473, 492), ("C->MHA", 400, 414), ("B->FFN", 266, 280), ("FFN->A", 190, 204)]:
    reg = A[y0:y1, 196:215].reshape(-1, 3)
    light = reg[reg.sum(axis=1) > 600]
    mid = reg[(reg.sum(axis=1) > 350) & (reg.sum(axis=1) <= 600)]
    dark = reg[reg.sum(axis=1) <= 350]
    print(f" {tag}: light {hx(np.median(light,axis=0))} n={len(light)} | mid {hx(np.median(mid,axis=0))} n={len(mid)} | dark {hx(np.median(dark,axis=0))} n={len(dark)}")

print("== 4. PURPLE short arrows below discs (col1) ==")
for tag, y0, y1 in [("rowA->p1", 163, 172), ("rowC->p2", 375, 383)]:
    reg = A[y0:y1, 200:212].reshape(-1, 3)
    dk = reg[reg.sum(axis=1) < 480]
    print(f" {tag}: dark n={len(dk)} {hx(np.median(dk,axis=0)) if len(dk) else '-'}")

print("== 5. GREEN arrows LN2->rowB zone (frame 298..312) ==")
reg = A[298:312, 180:905]
m = (reg[:, :, 1] > reg[:, :, 0]) & (reg[:, :, 1] > reg[:, :, 2] + 10)
print(" n=", int(m.sum()), hx(np.median(reg[m],axis=0)) if m.sum() else "-")
cols = np.nonzero(m.any(axis=0))[0]
if len(cols):
    cl, cur = [], [cols[0]]
    for c in cols[1:]:
        if c - cur[-1] <= 4: cur.append(c)
        else: cl.append(cur); cur = [c]
    cl.append(cur)
    print(" clusters:", [(180+c[0], 180+c[-1]) for c in cl])

print("== 6. LN bar width (bottom border row y=129, color ~#C08B49) ==")
line = A[129]
m = [x for x in range(130, 910) if abs(line[x][0]-192)<40 and abs(line[x][1]-139)<45 and abs(line[x][2]-73)<50]
print(" border px x:", (m[0], m[-1]) if m else None, "-> slide", (sx(m[0]), sx(m[-1])) if m else None)

print("== 7. IO boxes: border rows/cols ==")
for tag, y0, y1 in [("Out", 42, 94), ("In", 462, 520)]:
    reg = A[y0:y1, 60:215]
    m = (reg[:, :, 0] > 130) & (reg[:, :, 1] < 90) & (reg[:, :, 2] < 90)
    rc = m.sum(axis=1)
    print(f" {tag} rows n>10:", [(y0+i, int(n)) for i, n in enumerate(rc) if n > 10])
    cc = m.sum(axis=0)
    print(f" {tag} cols n>6:", [(60+i, int(n)) for i, n in enumerate(cc) if n > 6])
    # text ink bbox inside borders
    if tag == "Out":
        tm = m[52:80]
        ys, xs = np.nonzero(tm)
        if len(ys): print(f"   Out text bbox: y {52+ys.min()}..{52+ys.max()} x {60+xs.min()}..{60+xs.max()} -> slide y {sy(52+ys.min()):.1f}..{sy(52+ys.max()):.1f} x {sx(60+xs.min()):.1f}..{sx(60+xs.max()):.1f}")
    else:
        tm = m[470:500]
        ys, xs = np.nonzero(tm)
        if len(ys): print(f"   In text bbox: y {470+ys.min()}..{470+ys.max()} x {60+xs.min()}..{60+xs.max()} -> slide y {sy(470+ys.min()):.1f}..{sy(470+ys.max()):.1f} x {sx(60+xs.min()):.1f}..{sx(60+xs.max()):.1f}")

print("== 8. tile1 fan lines + RELU ==")
reg = A[244:254, 196:216].reshape(-1, 3)
dk = reg[reg.sum(axis=1) < 430]
print(" fan px:", len(dk), hx(np.median(dk,axis=0)) if len(dk) else "-")
rel = A[226:240, 208:252]
rm = (rel[:, :, 0] > 150) & (rel[:, :, 1] < 135) & (rel[:, :, 2] < 100) & (rel[:,:,0]-rel[:,:,1] > 50)
print(" RELU-ish px:", int(rm.sum()), hx(np.median(rel[rm],axis=0)) if rm.sum() else "-",
      "bbox:", (np.nonzero(rm.any(axis=0))[0][[0,-1]]+208) if rm.sum() else "-", (np.nonzero(rm.any(axis=1))[0][[0,-1]]+226) if rm.sum() else "-")

print("== 9. FFN header text color (tight) ==")
reg = A[209:226, 290:770].reshape(-1, 3)
dk = reg[reg.sum(axis=1) < 360]
print(" header dark px:", len(dk), hx(np.median(dk,axis=0)) if len(dk) else "-")

print("== 10. container corner check: is it rounded? top-left corner (frame x 125..145, y 86..100) ==")
for y in range(86, 100, 2):
    row = A[y, 120:150]
    first_tan = next((120+i for i, c in enumerate(row) if abs(c[0]-232)+abs(c[1]-178)+abs(c[2]-114) < 60), None)
    print(f"  y={y}: first tan x={first_tan}")
