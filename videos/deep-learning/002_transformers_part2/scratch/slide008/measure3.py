#!/usr/bin/env python3
"""measure3: fine structure of remapped 002:8 delta regions."""
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
f8 = np.asarray(Image.open(f"{ROOT}/002_transformers_part2/scratch/slide008/frame8_remapped_960x540.png").convert("RGB")).astype(int)
f33 = np.asarray(Image.open(f"{ROOT}/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
r, g, b = f8[:, :, 0], f8[:, :, 1], f8[:, :, 2]

def census(img, x0, y0, x1, y1, tag, n=5):
    reg = img[y0:y1, x0:x1].reshape(-1, 3)
    q = (reg // 20) * 20
    vals, counts = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-counts)[:n]
    print(f"{tag} [{x0},{y0}..{x1},{y1}]: " + ", ".join(f"{tuple(int(v) for v in vals[i])}:{int(counts[i])}" for i in order))

def col_profile(mask, x0, x1, tag, thresh=3):
    cols = mask[:, x0:x1].sum(axis=0)
    on = [x0 + i for i, v in enumerate(cols) if v > thresh]
    print(f"{tag}: cols {on[0]}..{on[-1]}" if on else f"{tag}: none")

def row_profile(mask, y0, y1, tag, thresh=3):
    rows = mask[y0:y1, :].sum(axis=1)
    on = [y0 + i for i, v in enumerate(rows) if v > thresh]
    print(f"{tag}: rows {on[0]}..{on[-1]}" if on else f"{tag}: none")

print("=== W_k row-1 box (parent x150..200 y234..258) ===")
census(f8, 148, 236, 202, 256, "8 wk row1")
census(f33, 148, 236, 202, 256, "33 wk row1")
census(f8, 148, 276, 202, 298, "8 wk row2")
print("--- W_v row-1 box (parent x698..748 y234..258) ---")
census(f8, 696, 236, 750, 256, "8 wv row1")
census(f33, 696, 236, 750, 256, "33 wv row1")
census(f8, 696, 276, 750, 298, "8 wv row2")

print("\n=== greenish mask (box fills) left/right col profiles ===")
greenish = (g - r > 12) & (g - b > -12) & (g > 180)
col_profile(greenish, 130, 230, "8 greenish left x130..230", 10)
col_profile(greenish, 660, 780, "8 greenish right x660..780", 10)
row_profile(greenish[:, 130:230], 200, 420, "8 greenish left rows", 10)
row_profile(greenish[:, 660:780], 200, 420, "8 greenish right rows", 10)

print("\n=== red rings / multiply circles: red px clusters x495..665 y215..395 ===")
red = (r - g > 55) & (r - b > 40) & (r > 130)
rc = red.copy(); rc[:215, :] = False; rc[395:, :] = False; rc[:, :495] = False; rc[:, 665:] = False
ys, xs = np.where(rc)
print("red px:", len(ys))
if len(ys):
    # cluster by y with gap>8
    order = np.argsort(ys)
    ys_s = ys[order]; xs_s = xs[order]
    clusters = []
    start = 0
    for i in range(1, len(ys_s) + 1):
        if i == len(ys_s) or ys_s[i] - ys_s[i - 1] > 8:
            seg_y = ys_s[start:i]; seg_x = xs_s[start:i]
            clusters.append((int(seg_y.min()), int(seg_y.max()), int(seg_x.min()), int(seg_x.max()), i - start))
            start = i
    for c in clusters:
        print(f"  cluster y {c[0]}..{c[1]} x {c[2]}..{c[3]} n={c[4]} center ({(c[2]+c[3])//2},{(c[0]+c[1])//2})")

print("\n=== blue circle: constrained row/col profile (x230..480 y320..525) ===")
blue = (b - r > 25) & (b - g > 10) & (b > 130) & (r > 70) & (r < 220)
bc = blue.copy(); bc[:320, :] = False; bc[525:, :] = False; bc[:, :230] = False; bc[:, 480:] = False
ys, xs = np.where(bc)
print("blue px:", len(ys))
if len(ys):
    print("bbox x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
    # per-row extents
    for yy in range(ys.min(), ys.max() + 1, 12):
        m = ys == yy
        if m.sum():
            print(f"  row {yy}: x {xs[m].min()}..{xs[m].max()}")
    # alpha over peach (right side of circle over panel bg) and over DP fill (left-top)
    for px_, py_ in [(420, 400), (430, 440), (250, 380), (300, 350)]:
        obs = f8[py_, px_]
        bg = f33[py_, px_]
        den = bg[0] - 65
        a = (bg[0] - obs[0]) / den if abs(den) > 40 else float('nan')
        print(f"  alpha @({px_},{py_}): obs={tuple(int(v) for v in obs)} bg={tuple(int(v) for v in bg)} a={a:.2f}")

print("\n=== chunky arrow rows (x250..400 y480..535) ===")
chunky = (r - g > 70) & (r - b > 70) & (r > 130)
ca = chunky.copy(); ca[:480, :] = False; ca[536:, :] = False; ca[:, :250] = False; ca[:, 400:] = False
for yy in range(480, 536, 4):
    m = ca[yy]
    on = np.where(m)[0]
    if len(on) > 2:
        print(f"  row {yy}: x {on.min()}..{on.max()} n={len(on)}")

print("\n=== left input container (border 4E7D52 dashed) ===")
cont = (abs(r - 78) < 30) & (abs(g - 125) < 30) & (abs(b - 82) < 30)
cl = cont.copy(); cl[:, :40] = False; cl[:, 160:] = False; cl[:200, :] = False
row_profile(cl, 200, 430, "8 left cont rows")
col_profile(cl, 40, 170, "8 left cont cols", 4)
cr = cont.copy(); cr[:, :730] = False; cr[:, 860:] = False; cr[:200, :] = False
row_profile(cr, 200, 430, "8 right cont rows")
col_profile(cr, 720, 870, "8 right cont cols", 4)

print("\n=== sentence container rows ===")
sc = cont.copy(); sc[:440, :] = False
row_profile(sc, 440, 535, "8 sentence cont rows", 6)
col_profile(sc, 150, 520, "8 sentence cont cols", 4)

print("\n=== legend container (x700..920 y440..535) ===")
lg = cont.copy(); lg[:430, :] = False; lg[:, :690] = False
col_profile(lg, 690, 930, "8 legend cols", 4)
row_profile(lg[:, 690:930], 430, 540, "8 legend rows", 4)

print("\n=== DP box border (A69B90) bbox ===")
bord = (abs(r - 166) < 20) & (abs(g - 155) < 20) & (abs(b - 144) < 20)
db = bord.copy(); db[:, :240] = False; db[:, 360:] = False; db[:170, :] = False; db[420:, :] = False
row_profile(db, 170, 420, "8 DP border rows", 6)
col_profile(db, 240, 360, "8 DP border cols", 6)

print("\n=== softmax column (F8DDFC) bbox ===")
soft = (abs(r - 248) < 10) & (abs(g - 222) < 14) & (abs(b - 251) < 10)
sm = soft.copy(); sm[:, :440] = False; sm[:, 510:] = False; sm[:180, :] = False; sm[420:, :] = False
row_profile(sm, 180, 420, "8 softmax rows", 6)
col_profile(sm, 440, 510, "8 softmax cols", 6)

print("\n=== pills (FFFFE3) ===")
pill = (r > 245) & (g > 245) & (b > 205) & (b < 240)
p1 = pill.copy(); p1[:150, :] = False; p1[195:, :] = False; p1[:, :250] = False; p1[:, 360:] = False
ys, xs = np.where(p1)
if len(ys): print(f"Similarity pill: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
p2 = pill.copy(); p2[:145, :] = False; p2[195:, :] = False; p2[:, 410:] = False; p2[:, 530:] = False
ys, xs = np.where(p2)
if len(ys): print(f"Probabilities pill: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
p3 = pill.copy(); p3[:145, :] = False; p3[195:, :] = False; p3[:, 570:] = False; p3[:, 710:] = False
ys, xs = np.where(p3)
if len(ys): print(f"WeightedSUM pill: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")

print("\n=== q2 label + W_q region under blue (scan y390..475 x250..360) ===")
census(f8, 255, 405, 345, 470, "8 Wq region", 7)
census(f33, 255, 405, 345, 470, "33 Wq region", 7)

print("\n=== magenta X2 highlight ===")
mag = (r - g > 60) & (b - g > 30) & (r > 120)
mg = mag.copy(); mg[:440, :] = False; mg[520:, :] = False; mg[:, :240] = False; mg[:, 360:] = False
ys, xs = np.where(mg)
if len(ys): print(f"8 X2 magenta: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n=== K labels (red ink x230..270 y225..390) cluster ===")
redk = (r - g > 55) & (r - b > 30) & (r > 130)
rk = redk.copy(); rk[:, :225] = False; rk[:, 270:] = False; rk[:220, :] = False; rk[400:, :] = False
ys, xs = np.where(rk)
if len(ys):
    order = np.argsort(ys); ys_s = ys[order]; xs_s = xs[order]
    start = 0; clus = []
    for i in range(1, len(ys_s) + 1):
        if i == len(ys_s) or ys_s[i] - ys_s[i - 1] > 8:
            clus.append((int(ys_s[start:i].min()), int(ys_s[start:i].max()), int(xs_s[start:i].min()), int(xs_s[start:i].max())))
            start = i
    for c in clus: print(f"  K lbl y {c[0]}..{c[1]} x {c[2]}..{c[3]}")

print("\n=== V labels (red ink x620..670 y215..395) ===")
vk = redk.copy(); vk[:, :615] = False; vk[:, 670:] = False; vk[:210, :] = False; vk[400:, :] = False
ys, xs = np.where(vk)
if len(ys):
    order = np.argsort(ys); ys_s = ys[order]; xs_s = xs[order]
    start = 0; clus = []
    for i in range(1, len(ys_s) + 1):
        if i == len(ys_s) or ys_s[i] - ys_s[i - 1] > 8:
            clus.append((int(ys_s[start:i].min()), int(ys_s[start:i].max()), int(xs_s[start:i].min()), int(xs_s[start:i].max())))
            start = i
    for c in clus: print(f"  V lbl y {c[0]}..{c[1]} x {c[2]}..{c[3]}")
