#!/usr/bin/env python3
"""Third measurement pass: spoke profiles, arc annulus trace, arrowhead ASCII,
center/cursor dump, equation-box per-line advances, badge numeral scale."""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
CX, CY = 578.5, 283.5
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]

print("== 0deg spoke: vertical profile x=800, y 268..300 ==")
for y in range(268, 301):
    print(f" y={y}:", tuple(A[y, 800]), "| x=850:", tuple(A[y, 850]))

print("\n== 0deg spoke horizontal extent: y=284 darkness d=(233-r)+(233-g)+(231-b) ==")
for x in range(700, 906, 5):
    c = A[284, x]
    d = (233 - c[0]) + (233 - c[1]) + (231 - c[2])
    print(f" x={x} d={d}", tuple(c), end="  ")
    if (x - 695) % 20 == 0:
        print()

print("\n\n== 90deg spoke: horizontal profile y=150, x 568..592 ==")
for x in range(568, 593):
    print(f" x={x}:", tuple(A[150, x]))

print("\n== 90deg spoke vertical extent x=579 darkness y 48..160 ==")
for y in range(48, 161, 4):
    c = A[y, 579]
    print(f" y={y}", tuple(c), end="  ")
    if (y - 44) % 16 == 0:
        print()

print("\n\n== 180deg spoke: vertical profile x=350, y 274..294 ==")
for y in range(274, 295):
    print(f" y={y}:", tuple(A[y, 350]))

print("\n== 180deg spoke extent y=284 x 240..460 (d) ==")
row = []
for x in range(240, 461, 10):
    c = A[284, x]
    row.append(f"x{x}:d{(233-c[0])+(233-c[1])+(231-c[2])}")
print("  ".join(row))

print("\n== 270deg spoke: horizontal profile x=579? no: y=470, x 568..592 ==")
for x in range(568, 593):
    print(f" x={x}:", tuple(A[470, x]))

print("\n== 30deg diagonal: perpendicular darkness along ray ==")
a = np.radians(30)
for rad in range(130, 340, 6):
    vals = []
    for off in (-2, -1, 0, 1, 2):
        x = int(round(CX + rad * np.cos(a) - off * np.sin(a)))
        y = int(round(CY - rad * np.sin(a) - off * np.cos(a)))
        c = A[y, x]
        vals.append((233 - c[0]) + (233 - c[1]) + (231 - c[2]))
    print(f" rad {rad}: max dark {max(vals):3d} {vals}")

print("\n== 60deg diagonal ==")
a = np.radians(60)
for rad in range(130, 340, 6):
    vals = []
    for off in (-2, -1, 0, 1, 2):
        x = int(round(CX + rad * np.cos(a) - off * np.sin(a)))
        y = int(round(CY - rad * np.sin(a) - off * np.cos(a)))
        c = A[y, x]
        vals.append((233 - c[0]) + (233 - c[1]) + (231 - c[2]))
    print(f" rad {rad}: max dark {max(vals):3d} {vals}")

print("\n== 120deg diagonal ==")
a = np.radians(120)
for rad in range(130, 340, 6):
    vals = []
    for off in (-2, -1, 0, 1, 2):
        x = int(round(CX + rad * np.cos(a) - off * np.sin(a)))
        y = int(round(CY - rad * np.sin(a) - off * np.cos(a)))
        c = A[y, x]
        vals.append((233 - c[0]) + (233 - c[1]) + (231 - c[2]))
    print(f" rad {rad}: max dark {max(vals):3d} {vals}")

print("\n== arc annulus trace: orange-ish (r-(g+b)/2 > 25) rad 185..285, phi 0..130 ==")
hits = {}
for phi10 in range(0, 1301, 5):
    phi = phi10 / 10.0
    aa = np.radians(phi)
    best = None
    for rad in np.arange(185, 285, 1.0):
        x = int(round(CX + rad * np.cos(aa)))
        y = int(round(CY - rad * np.sin(aa)))
        if not (0 <= x < W and 0 <= y < H):
            continue
        c = A[y, x]
        om = c[0] - (c[1] + c[2]) / 2.0
        if om > 25 and c[0] > 150:
            if best is None or om > best[1]:
                best = (rad, om, tuple(c))
    if best:
        hits.setdefault(round(best[0] / 10) * 10, []).append((phi, best))
for k in sorted(hits):
    lst = hits[k]
    phis = [f"{p:.0f}" for p, _ in lst]
    print(f"rad~{k}: phis {','.join(phis)}  sample {lst[len(lst)//2][1]}")

print("\n== arrowhead ASCII (orangeness map) AH at ~(766,179) region x754..780 y168..190 ==")
for y in range(168, 191):
    line = ""
    for x in range(754, 781):
        c = A[y, x]
        om = c[0] - (c[1] + c[2]) / 2.0
        dk = (233 - c[0]) + (233 - c[1]) + (231 - c[2])
        line += "#" if om > 60 else ("+" if om > 30 else ("." if dk > 30 else " "))
    print(f"{y:3d} {line}")

print("\n== arrowhead ASCII AH at ~(581,67) region x570..594 y56..80 ==")
for y in range(56, 81):
    line = ""
    for x in range(570, 595):
        c = A[y, x]
        om = c[0] - (c[1] + c[2]) / 2.0
        dk = (233 - c[0]) + (233 - c[1]) + (231 - c[2])
        line += "#" if om > 60 else ("+" if om > 30 else ("." if dk > 30 else " "))
    print(f"{y:3d} {line}")

print("\n== center region darkness map x556..604 y252..318 ('#'=dark,'o'=warm,' '=fill) ==")
for y in range(252, 319, 2):
    line = ""
    for x in range(556, 605, 1):
        c = A[y, x]
        dk = (233 - c[0]) + (233 - c[1]) + (231 - c[2])
        warm = (c[0] - c[2]) > 40 and c[0] > 180
        dark = c[0] < 140 and c[1] < 140
        line += "@" if dark else ("o" if warm else ("." if dk > 25 else " "))
    print(f"{y:3d} {line}")

print("\n== equation box per-line ink (strict) ==")
for (y0, y1), nm in (((186, 206), "L1"), ((207, 226), "L2"), ((227, 244), "L3")):
    sub = A[y0:y1 + 1, 83:217]
    sr, sg, sb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    blue = (sb > 130) & (sr < 120) & (sg < 120)
    redt = (sr > 140) & (sg < 100) & (sb < 100) & (sr - sg > 60)
    grnt = (sg > 110) & (sg - sr > 40) & (sg - sb > 40)
    for m, cn in ((blue, "blue"), (redt, "red"), (grnt, "green")):
        ys, xs = np.where(m)
        if len(xs):
            print(f" {nm} {cn}: x {83+xs.min()}..{83+xs.max()} (w {xs.max()-xs.min()+1}) y {y0+ys.min()}..{y0+ys.max()} n={m.sum()}")

print("\n== badge numeral: dark px in badge bbox x859..892 y57..85 ==")
sub = A[57:86, 859:893]
dk = (sub[:, :, 0] < 150) & (sub[:, :, 1] < 150) & (sub[:, :, 2] < 150)
ys, xs = np.where(dk)
if len(ys):
    print(f"numeral ink: x {859+xs.min()}..{859+xs.max()} y {57+ys.min()}..{57+ys.max()} (h {ys.max()-ys.min()+1} w {xs.max()-xs.min()+1}) n={dk.sum()}")
