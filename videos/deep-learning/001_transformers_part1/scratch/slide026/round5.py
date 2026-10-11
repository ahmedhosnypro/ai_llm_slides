#!/usr/bin/env python3
import numpy as np
from PIL import Image
from scipy import ndimage

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
PEACH = np.array([247, 227, 206])

print("== 1. label zone fill stats ==")
for nm, (x0, x1) in {"Sim": (255, 355), "Prob": (415, 515), "WSum": (570, 700)}.items():
    sub = A[158:190, x0:x1].reshape(-1, 3)
    d_peach = (np.abs(sub - PEACH).sum(axis=1) <= 45).mean()
    pale_y = ((sub[:, 0] > 242) & (sub[:, 1] > 242) & (sub[:, 2] > 195) & (sub[:, 2] < 235)).mean()
    white = ((sub > 242).all(axis=1)).mean()
    mint = ((sub[:, 1] > 240) & (sub[:, 1] - sub[:, 0] > 8)).mean()
    blue = ((sub[:, 2] - sub[:, 0] > 30)).mean()
    print(f"  {nm}: peach={d_peach:.2f} paleYellow={pale_y:.2f} white={white:.2f} mint={mint:.2f} blueish={blue:.2f}")

print("== 2. green arrow extent: cols x550..576, y146..200 ==")
for x in range(550, 578, 2):
    col = A[146:200, x]
    g = [146 + i for i in range(len(col)) if col[i][1] - col[i][0] > 25 and col[i][1] > 120]
    r = [146 + i for i in range(len(col)) if col[i][0] - col[i][1] > 60 and col[i][0] > 120]
    print(f"  x={x}: green_ys={g[:6]}..{g[-3:] if g else ''} n={len(g)}  red_ys={r}")

print("== 3. red blob x575..590, y143..160 ==")
sub = A[143:160, 575:590]
m = (sub[:, :, 0] - sub[:, :, 1] > 40)
ys, xs = np.where(m)
if len(xs): print(f"  red bbox x{575+xs.min()}..{575+xs.max()} y{143+ys.min()}..{143+ys.max()} n={len(xs)} core_min={sub[m].sum(axis=1).min()}")

print("== 4. right dashed curve: x495..860, y396..480 greenish ==")
sub = A[396:480, 495:860]
m = (sub[:, :, 1] - sub[:, :, 0] > 12) & (sub[:, :, 1] - sub[:, :, 2] > 12) & (sub.sum(axis=2) < 700)
ys, xs = np.where(m)
print(f"  n={len(xs)}", end="")
if len(xs):
    print(f" x{495+xs.min()}..{495+xs.max()} y{396+ys.min()}..{396+ys.max()}")
    # path: for each x-bucket of 20, the mean y
    for bx in range(0, 360, 20):
        sel = (xs >= bx) & (xs < bx + 20)
        if sel.sum() >= 3:
            print(f"    x{495+bx}..{495+bx+19}: y~{396+int(ys[sel].mean())} n={int(sel.sum())}")
else:
    print()

print("== 5. left dashed curve path: x40..180, y388..480 ==")
sub = A[388:480, 40:180]
m = (sub[:, :, 1] - sub[:, :, 0] > 12) & (sub[:, :, 1] - sub[:, :, 2] > 12) & (sub.sum(axis=2) < 700)
ys, xs = np.where(m)
print(f"  n={len(xs)}", end="")
if len(xs):
    print(f" x{40+xs.min()}..{40+xs.max()} y{388+ys.min()}..{388+ys.max()}")
    for bx in range(0, 140, 14):
        sel = (xs >= bx) & (xs < bx + 14)
        if sel.sum() >= 2:
            print(f"    x{40+bx}..{40+bx+13}: y~{388+int(ys[sel].mean())} n={int(sel.sum())}")
else:
    print()

print("== 6. line4 continuation x645..765, y366..380 ==")
sub = A[366:380, 645:765]
m = (np.abs(sub - PEACH).sum(axis=2) > 60) & (np.abs(sub - np.array([233,233,231])).sum(axis=2) > 60)
print(f"  n={int(m.sum())} of {m.size}")
ys2, xs2 = np.where(m)
if len(xs2):
    import collections
    cc = collections.Counter((645 + x // 10 * 10) for x in xs2)
    print("  cols:", sorted(cc.items())[:20])

print("== 7. darkest inks ==")
def darkest(nm, x0, y0, x1, y1):
    sub = A[y0:y1, x0:x1].reshape(-1, 3)
    i = np.argmin(sub.sum(axis=1))
    c = sub[i]
    print(f"  {nm:24s} darkest #{c[0]:02X}{c[1]:02X}{c[2]:02X} {tuple(c)}")
darkest("softmax_label", 462, 260, 486, 340)
darkest("dotprod_label", 268, 198, 325, 228)
darkest("subtitle_X_tokens", 400, 80, 810, 100)
darkest("sim_label", 280, 166, 330, 182)
darkest("w_label1", 496, 226, 510, 238)
darkest("X1_on_glyph_L1", 88, 240, 110, 254)
darkest("query_arrow", 293, 405, 303, 475)
darkest("red_block_arrow", 264, 508, 290, 530)
darkest("x2_border", 260, 470, 338, 510)
darkest("stack_border", 55, 224, 142, 230)

print("== 8. X2 glyph stats ==")
sub = A[476:505, 266:332].reshape(-1, 3)
pinkish = ((sub[:, 0] > 200) & (sub[:, 1] > 120) & (sub[:, 1] < 210) & (sub[:, 2] > 170)).mean()
print(f"  pinkish frac={pinkish:.2f} med={np.median(sub, axis=0)}")

print("== 9. sigma fill median (excl glyph) ==")
sub = np.concatenate([A[200:214, 520:575].reshape(-1, 3), A[200:214, 592:645].reshape(-1, 3)])
print(f"  med={np.median(sub, axis=0)}")

print("== 10. container border green histogram ==")
zones = np.concatenate([A[226:230, 60:136].reshape(-1, 3), A[226:230, 766:840].reshape(-1, 3),
                        A[391:395, 60:136].reshape(-1, 3), A[473:477, 180:490].reshape(-1, 3)])
m = (zones[:, 1] - zones[:, 0] > 15) & (zones[:, 1] - zones[:, 2] > 15) & (zones.sum(axis=1) < 640)
sel = zones[m]
print(f"  n={len(sel)} med={np.median(sel, axis=0) if len(sel) else 'none'} dark_min={sel.sum(axis=1).min() if len(sel) else '-'}")

print("== 11. glyph top/bottom edge rows: left stack row2 (y280..295) ==")
for yy in (281, 283, 292, 294):
    row = A[yy, 60:140]
    print(f"  y{yy}: " + "".join(
        "Y" if (c[0]>240 and c[1]>240 and c[2]<225) else
        "P" if (c[0]>235 and 130<c[1]<215 and c[2]>190) else
        "L" if (c[0]>200 and c[1]>170 and c[2]>235) else
        "m" if (c[1]>c[0] and c[1]>c[2] and c[1]>230 and c[0]>200) else
        "w" if (c>235).all() else "." for c in row))

print("== 12. Y-box columns ==")
for x in (549, 552, 560, 572, 576, 584, 592, 600, 608, 613, 616):
    col = A[114:150, x]
    cls = "".join("G" if (c[1] - c[0] > 15 and c[1] - c[2] > 5) else ("K" if c.sum() < 400 else ("?" if abs(c[0]-247)+abs(c[1]-227)+abs(c[2]-206) > 60 else ".")) for c in col)
    print(f"  x={x}: {cls}   (y114+)")
