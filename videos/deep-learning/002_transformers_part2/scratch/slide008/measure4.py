#!/usr/bin/env python3
"""measure4: final precision measurements on remapped 002:8."""
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
f8 = np.asarray(Image.open(f"{ROOT}/002_transformers_part2/scratch/slide008/frame8_remapped_960x540.png").convert("RGB")).astype(int)
f33 = np.asarray(Image.open(f"{ROOT}/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
r, g, b = f8[:, :, 0], f8[:, :, 1], f8[:, :, 2]

def runs_in_row(mask_row, x0=0):
    on = np.where(mask_row)[0]
    if len(on) == 0: return []
    out = []; s = on[0]; p = on[0]
    for v in on[1:]:
        if v - p > 3:
            out.append((s + x0, p + x0)); s = v
        p = v
    out.append((s + x0, p + x0))
    return out

print("=== W_k boxes left: pale-green fill (g>r, g>b-8, g>215) per-row runs x130..235 ===")
wkfill = (g - r > 8) & (g > 210) & (b > 190) & (b < 250)
for yy in range(226, 400, 6):
    rr = runs_in_row(wkfill[yy, 130:235], 130)
    if rr: print(f"  y{yy}: {rr}")

print("\n=== W_k border dark-green (120,180,120)-ish bbox ===")
dkg = (abs(r - 120) < 45) & (abs(g - 175) < 45) & (abs(b - 120) < 45) & (g - r > 25)
dk = dkg.copy(); dk[:, :130] = False; dk[:, 240:] = False; dk[:215, :] = False; dk[405:, :] = False
ys, xs = np.where(dk)
if len(ys): print(f"left darkgreen: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n=== W_v boxes right: pale-cyan fill (b>r+8, g>215) per-row runs x660..790 ===")
wvfill = (b - r > 8) & (g > 210) & (b > 215) & (r < 245)
for yy in range(226, 400, 6):
    rr = runs_in_row(wvfill[yy, 660:790], 660)
    if rr: print(f"  y{yy}: {rr}")

print("\n=== W_v border olive-ish bbox (like A2AC3C) x660..790 ===")
olv = (abs(r - 162) < 40) & (abs(g - 172) < 40) & (abs(b - 60) < 50)
ov = olv.copy(); ov[:, :660] = False; ov[:, 790:] = False; ov[:215, :] = False; ov[405:, :] = False
ys, xs = np.where(ov)
if len(ys): print(f"Wv border: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")
else: print("none — check border color:")
c8 = f8[246, 700:755]
print("  row246 x700..755:", [f"{x}:{tuple(int(v) for v in c8[i])}" for i, x in enumerate(range(700, 755)) if i % 4 == 0])

print("\n=== DP box fill extent: DCCBBB rows in clean band x325..345 ===")
dpf = (abs(r - 220) < 16) & (abs(g - 202) < 18) & (abs(b - 187) < 18)
cnt = dpf[:, 325:346].sum(axis=1)
on = [y for y in range(160, 430) if cnt[y] > 8]
print("DP fill rows (x325..345):", on[0], "..", on[-1] if on else None)
cnt2 = dpf[240:310, :].sum(axis=0)
on2 = [x for x in range(230, 370) if cnt2[x] > 20]
print("DP fill cols (y240..310):", on2[0], "..", on2[-1] if on2 else None)

print("\n=== DP 'Dot Product' text ink (6E5133) bbox ===")
tink = (abs(r - 110) < 45) & (abs(g - 81) < 40) & (abs(b - 51) < 40) & (r - b > 30)
ti = tink.copy(); ti[:, :255] = False; ti[:, 345:] = False; ti[:185, :] = False; ti[240:, :] = False
ys, xs = np.where(ti)
if len(ys): print(f"DotProduct text: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n=== multiply rings: per-row red runs x495..665 (ring = two runs ~14-19 apart) ===")
red = (r - g > 55) & (r - b > 40) & (r > 130)
for yy in range(222, 390, 3):
    rr = runs_in_row(red[yy, 495:665], 495)
    rr = [x for x in rr if x[1] - x[0] < 12]
    if len(rr) >= 2:
        widths = [x[1] - x[0] for x in rr]
        print(f"  y{yy}: {rr}")

print("\n=== blue circle: tint map (b-r>12, b>150) x200..400 y300..525 ===")
tint = ((b - r) > 12) & (b > 150) & (g < 245)
tc = tint.copy(); tc[:300, :] = False; tc[525:, :] = False; tc[:, :200] = False; tc[:, 400:] = False
ys, xs = np.where(tc)
print("tint px:", len(ys))
if len(ys):
    for yy in range(ys.min(), ys.max() + 1, 10):
        m = ys == yy
        if m.sum() > 3:
            print(f"  row {yy}: x {xs[m].min()}..{xs[m].max()} n={int(m.sum())}")

print("\n=== W_q box: blue-tinted-yellow (g-b>15, g 140..230, r<235) x250..350 y395..480 ===")
wq = (g - b > 15) & (g > 140) & (g < 235) & (r < 240) & (r > 100)
wqc = wq.copy(); wqc[:395, :] = False; wqc[480:, :] = False; wqc[:, :250] = False; wqc[:, 350:] = False
ys, xs = np.where(wqc)
if len(ys): print(f"Wq yellow-under-blue: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n=== q2 red label x265..320 y385..425 ===")
q2 = ((r - g > 45) & (r > 110)).copy(); q2[:385, :] = False; q2[425:, :] = False; q2[:, :262] = False; q2[:, 320:] = False
ys, xs = np.where(q2)
if len(ys): print(f"q2 ink: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n=== K.q text x325..365 y190..218 ===")
kq = ((r - g > 40) & (r - b > 25) & (r > 110)).copy(); kq[:188, :] = False; kq[220:, :] = False; kq[:, :322] = False; kq[:, 368:] = False
ys, xs = np.where(kq)
if len(ys): print(f"K.q ink: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n=== right container border cols (4E7D52 dashed, thresh 2) x725..860 ===")
cont = (abs(r - 78) < 32) & (abs(g - 125) < 32) & (abs(b - 82) < 32)
cr = cont.copy(); cr[:210, :] = False; cr[410:, :] = False
cols = cr[:, 720:865].sum(axis=0)
print("  col counts>2:", {720 + i: int(v) for i, v in enumerate(cols) if v > 2})
print("  census x728..768 y300:", [tuple(int(v) for v in f8[300, x]) for x in range(728, 769, 8)])
print("  census x838..852 y300:", [tuple(int(v) for v in f8[300, x]) for x in range(838, 853, 4)])

print("\n=== sentence container rows in x150..520 (thresh 2) ===")
sc = cont.copy(); sc[:, :150] = False; sc[:, 520:] = False
rows = sc[440:540, 150:520].sum(axis=1)
print("  rows>2:", {440 + i: int(v) for i, v in enumerate(rows) if v > 2})

print("\n=== X2 highlight: dark magenta (r-g>50, b-g>20) x240..350 y470..515 ===")
mg = ((r - g > 50) & (b - g > 20) & (r > 110)).copy(); mg[:470, :] = False; mg[515:, :] = False; mg[:, :240] = False; mg[:, 350:] = False
ys, xs = np.where(mg)
if len(ys): print(f"X2 highlight: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n=== X2 pink cells bbox (r>230, g 150..215, b 180..235) x245..345 y470..515 ===")
pk = ((r > 225) & (g > 145) & (g < 220) & (b > 175) & (b < 240)).copy(); pk[:470, :] = False; pk[515:, :] = False; pk[:, :245] = False; pk[:, 345:] = False
ys, xs = np.where(pk)
if len(ys): print(f"X2 pink: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n=== Y2 box: dashed border ink (33A02C-ish) x535..630 y110..150 ===")
yb = ((g - r > 60) & (g - b > 40) & (g > 110) & (g < 200)).copy(); yb[:105, :] = False; yb[155:, :] = False; yb[:, :530] = False; yb[:, 635:] = False
ys, xs = np.where(yb)
if len(ys): print(f"Y2 border ink: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n=== blue circle alpha over yellow band (W_q box) — pick px inside box ===")
if len(ys):
    pass
for (px_, py_) in [(290, 430), (300, 450), (310, 440)]:
    obs = f8[py_, px_]
    # bg = yellow band F7F96B
    a_r = (247 - obs[0]) / (247 - 65)
    a_g = (249 - obs[1]) / (249 - 105)
    a_b = (225 - obs[2]) / (225 - 107)
    print(f"  ({px_},{py_}) obs={tuple(int(v) for v in obs)} alpha_est r/g/b: {a_r:.2f}/{a_g:.2f}/{a_b:.2f}")
