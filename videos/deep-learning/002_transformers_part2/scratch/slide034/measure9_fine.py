#!/usr/bin/env python3
"""measure9_fine.py — box edges via color masks, text line profiles, arrows, brace, dots."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = img[..., 0], img[..., 1], img[..., 2]
S = r + g + b

def cols_from_mask(mask, y0, y1, x0, x1, thr, name):
    prof = mask[y0:y1, x0:x1].sum(axis=0)
    cols = np.where(prof >= thr)[0] + x0
    groups = []
    for c in cols:
        if groups and c - groups[-1][-1] <= 2: groups[-1].append(c)
        else: groups.append([c])
    print(f"{name}: {[(int(gp[0]), int(gp[-1])) for gp in groups]}")

# 1. token box borders: blue-violet stroke (B-R>25, S<620)
tokb = (b - r > 25) & (S < 620)
cols_from_mask(tokb, 145, 164, 160, 900, 10, "TOKEN box borders (cols)")

# 2. vector box borders: rose stroke (R-G>25, R-B>15, S<620)
vecb = (r - g > 25) & (r - b > 15) & (S < 620)
cols_from_mask(vecb, 296, 325, 160, 900, 8, "VECTOR box borders (cols)")

# 3. token container fill extent per row
tokf = (r > 175) & (r < 220) & (g > 175) & (g < 220) & (b > 228)
for y in [140, 155, 170]:
    xs = np.where(tokf[y, 100:900])[0] + 100
    if len(xs): print(f"token fill y{y}: x {xs.min()}..{xs.max()} n={len(xs)}")
# vector fill
vecf = (r > 228) & (b > 228) & (g > 205) & (g < 242) & (r - g > 8)
for y in [294, 310, 324]:
    xs = np.where(vecf[y, 100:900])[0] + 100
    if len(xs): print(f"vector fill y{y}: x {xs.min()}..{xs.max()} n={len(xs)}")

# 4. arrows per-row shape
red2 = (r > 150) & (g < 90) & (b < 90)
print("\nARROW1 per-row x-extent:")
for y in range(176, 216, 2):
    xs = np.where(red2[y, 490:560])[0] + 490
    if len(xs): print(f"  y{y}: x {xs.min()}..{xs.max()} n={len(xs)}")
print("ARROW2 per-row x-extent:")
for y in range(252, 292, 2):
    xs = np.where(red2[y, 490:560])[0] + 490
    if len(xs): print(f"  y{y}: x {xs.min()}..{xs.max()} n={len(xs)}")
# arrow core color
win = img[180:212, 515:538].reshape(-1, 3)
m = win.sum(axis=1) < 420
print("arrow core:", [(tuple(q), int(n)) for q, n in zip(*np.unique((win[m] // 20) * 20, axis=0, return_counts=True))][:6] if m.sum() else "none")

# 5. title rows (red/blue) for cap/baseline
print("\nTITLE red rows x274..476:")
for y in range(58, 100):
    n = red2[y, 274:476].sum()
    if n > 3: print(f"  y{y}: {n}", end="")
print()
bluec = (b - r > 60) & (b - g > 40) & (r < 120)
print("TITLE blue rows x493..695:")
for y in range(58, 102):
    n = bluec[y, 493:695].sum()
    if n > 3: print(f"  y{y}: {n}", end="")
print()
print("SUBTITLE red rows x330..660:")
for y in range(98, 122):
    n = red2[y, 330:660].sum()
    if n > 2: print(f"  y{y}: {n}", end="")
print()
# subtitle x extent
ys, xs = np.where(red2[100:120, 300:700])
print(f"subtitle bbox: x {xs.min()+300}..{xs.max()+300} y {ys.min()+100}..{ys.max()+100}")
# title x extents
ys, xs = np.where(red2[58:98, 200:500])
print(f"title red bbox: x {xs.min()+200}..{xs.max()+200} y {ys.min()+58}..{ys.max()+58}")
ys, xs = np.where(bluec[58:98, 480:720])
print(f"title blue bbox: x {xs.min()+480}..{xs.max()+480} y {ys.min()+58}..{ys.max()+58}")

# 6. left label lines: profile x55..170, navy + red
navy = (b - r > 40) & (b - g > 30) & (S < 450)
redl = (r - g > 40) & (r - b > 40) & (S < 520)
print("\nLEFT labels navy rows x55..170:")
for y in range(135, 280):
    n = navy[y, 55:170].sum()
    if n > 3: print(f"  y{y}:{n}", end="")
print()
print("LEFT labels red rows x55..170:")
for y in range(210, 280):
    n = redl[y, 55:170].sum()
    if n > 3: print(f"  y{y}:{n}", end="")
print()
# x extents per line band
for (nm, y0, y1) in [("lab1a", 140, 158), ("lab1b", 158, 176), ("lab1c(paren)", 180, 196),
                     ("lab3a", 218, 236), ("lab3b", 236, 254), ("lab3c(paren)", 254, 272)]:
    ys, xs = np.where((navy[y0:y1, 50:180] | redl[y0:y1, 50:180]))
    if len(xs): print(f"{nm}: x {xs.min()+50}..{xs.max()+50} y {ys.min()+y0}..{ys.max()+y0}")

# 7. purple bar text profile
print("\nPURPLE bar yellow/white rows:")
yel = (r > 210) & (g > 200) & (b < 160)
for y in range(222, 250):
    ny_, nw_ = yel[y, 175:885].sum(), ((r > 235) & (g > 235) & (b > 235))[y, 175:885].sum()
    if ny_ > 2 or nw_ > 2: print(f"  y{y}: yel={ny_} wht={nw_}", end="")
print()
ys, xs = np.where(yel[222:250, 175:885]); print(f"yellow bbox: x {xs.min()+175}..{xs.max()+175} y {ys.min()+222}..{ys.max()+222}")
wht = (r > 235) & (g > 235) & (b > 235)
ys, xs = np.where(wht[222:250, 175:885]); print(f"white bbox: x {xs.min()+175}..{xs.max()+175} y {ys.min()+222}..{ys.max()+222}")

# 8. summary lines: dark rows x230..820
darkall = S < 300
print("\nSUMMARY dark rows x230..820:")
for y in range(368, 505):
    n = darkall[y, 230:820].sum()
    if n > 10: print(f"  y{y}:{n}", end="")
print()
# red rows
print("SUMMARY red rows x230..820:")
for y in range(368, 505):
    n = red2[y, 230:820].sum()
    if n > 8: print(f"  y{y}:{n}", end="")
print()
# per-line x extents (dark or red or yellow)
yellowm = (r > 210) & (g > 200) & (b < 160)
for (nm, y0, y1) in [("L1", 380, 400), ("L2", 400, 415), ("L3", 415, 433), ("L4", 433, 455), ("L5", 455, 480)]:
    m = (darkall | red2 | yellowm)[y0:y1, 230:820]
    ys, xs = np.where(m)
    if len(xs): print(f"{nm}: x {xs.min()+230}..{xs.max()+230} y {ys.min()+y0}..{ys.max()+y0}")

# 9. underline check below L4 (y452..460, contiguous run)
for y in range(450, 462):
    xs = np.where(red2[y, 250:800])[0] + 250
    if len(xs) > 40: print(f"underline row y{y}: n={len(xs)} x {xs.min()}..{xs.max()}")

# 10. dots bbox
dotm = (S < 640) & (b - r > 15)
ys, xs = np.where(dotm[146:166, 625:720])
print(f"\nDOTS bbox: x {xs.min()+625}..{xs.max()+625} y {ys.min()+146}..{ys.max()+146}")

# 11. brace rows fine
print("BRACE rows:")
for y in range(334, 352):
    xs = np.where(red2[y, 170:890])[0] + 170
    if len(xs): print(f"  y{y}: n={len(xs)} x {xs.min()}..{xs.max()}", end="; ")
print()
# brace core color
win = img[336:350, 180:870].reshape(-1, 3)
m = win.sum(axis=1) < 300
if m.sum():
    q, n = np.unique((win[m] // 20) * 20, axis=0, return_counts=True)
    print("brace core:", [(tuple(t), int(c)) for t, c in sorted(zip(q.tolist(), n.tolist()), key=lambda z: -z[1])][:5])
