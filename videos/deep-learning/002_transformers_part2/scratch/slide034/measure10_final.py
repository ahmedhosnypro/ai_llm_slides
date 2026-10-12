#!/usr/bin/env python3
"""measure10_final.py — vector box edges via pink fill; label extents; brace dark profile; slant."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = img[..., 0], img[..., 1], img[..., 2]
S = r + g + b

def runs(cols, gap=4):
    groups = []
    for c in cols:
        if groups and c - groups[-1][-1] <= gap: groups[-1].append(c)
        else: groups.append([c])
    return [(int(gp[0]), int(gp[-1])) for gp in groups]

# 1. vector box interiors via pink fill (r>238, g 195-228, b 205-240)
pinkf = (r > 238) & (g > 195) & (g < 228) & (b > 205) & (b < 240)
prof = pinkf[302:320, 160:900].sum(axis=0)
cols = np.where(prof >= 8)[0] + 160
print("VECTOR box pink-fill col runs:", runs(cols, gap=6))

# 2. token box interior fill? boxes share lane fill; instead use border cols (settled):
#    [180,239],[253,313],[327,386],[400,460],[474,533],[547,607],[735,799],[810,875]

# 3. left labels with wide window (x50..240)
navy = (b - r > 40) & (b - g > 30) & (S < 460)
redl = (r - g > 40) & (r - b > 40) & (S < 540)
for (nm, y0, y1, m) in [("lab1a", 138, 156, navy), ("lab1b", 156, 176, navy), ("lab1c", 180, 196, navy),
                        ("lab3a", 216, 234, redl), ("lab3b", 234, 254, redl), ("lab3c", 254, 272, navy)]:
    ys, xs = np.where(m[y0:y1, 50:240])
    if len(xs): print(f"{nm}: x {xs.min()+50}..{xs.max()+50} y {ys.min()+y0}..{ys.max()+y0} n={len(xs)}")

# check for lavender bg behind labels: sample y145 x100..165
print("y145 x100..165:", [f"{img[145, x, 0]},{img[145, x, 1]},{img[145, x, 2]}" for x in range(100, 166, 8)])
print("y260 x100..165:", [f"{img[260, x, 0]},{img[260, x, 1]},{img[260, x, 2]}" for x in range(100, 166, 8)])

# 4. brace with dark-red mask (r-g>30, S<520, r>90)
brm = (r - g > 30) & (S < 560) & (r > 90)
print("BRACE dark rows:")
for y in range(334, 352):
    xs = np.where(brm[y, 170:890])[0] + 170
    if len(xs) >= 2:
        print(f"  y{y}: n={len(xs)} x {xs.min()}..{xs.max()}", end=";")
print()
# spine solid extent at y343/344
for y in [342, 343, 344]:
    xs = np.where(brm[y, 170:890])[0] + 170
    if len(xs):
        # find runs
        print(f"  y{y} runs:", runs(xs, gap=3))

# 5. italic slant: digit '0' box1 (x195..230) top vs bottom x-centroid
dk = S < 500
ys, xs = np.where(dk[148:164, 192:235])
if len(xs):
    top = xs[ys < 4]; bot = xs[ys > 11]
    print(f"digit0 slant: top cx {top.mean()+192:.1f} (n={len(top)}) bottom cx {bot.mean()+192:.1f} (n={len(bot)})")
# vector label 'V' box1 slant: x192..210, y303..313
ys, xs = np.where(dk[303:320, 190:280])
if len(xs):
    top = xs[ys < 5]; bot = xs[ys > 8]
    if len(top) and len(bot):
        print(f"vector text slant: top cx {top.mean()+190:.1f} (n={len(top)}) bottom cx {bot.mean()+190:.1f} (n={len(bot)})")

# 6. L5 full extent (y477..495)
darkall = S < 330
ys, xs = np.where(darkall[475:497, 230:820])
print(f"L5 bbox: x {xs.min()+230}..{xs.max()+230} y {ys.min()+475}..{ys.max()+475}")

# 7. summary yellow highlight exact
yellowm = (r > 210) & (g > 200) & (b < 170) & (r - b > 60)
ys, xs = np.where(yellowm[405:440, 400:530])
print(f"N-1 highlight bbox: x {xs.min()+400}..{xs.max()+400} y {ys.min()+405}..{ys.max()+405} n={len(xs)}")

# 8. purple bar: yellow runs (word boundaries)
yel = (r > 210) & (g > 200) & (b < 160)
for y in [228, 234, 240]:
    xs = np.where(yel[y, 170:890])[0] + 170
    print(f"bar y{y} yellow runs:", runs(xs, gap=8))
wht = (r > 200) & (g > 200) & (b > 200)
for y in [234, 238]:
    xs = np.where(wht[y, 170:890])[0] + 170
    print(f"bar y{y} white runs:", runs(xs, gap=8))

# 9. token text bands per box (for em calibration): '0' in box1, 'N-2' box7
for nm, x0, x1 in [("t0", 195, 232), ("t5", 560, 600), ("tN2", 748, 790), ("tN1", 822, 866)]:
    ys, xs = np.where(dk[144:166, x0:x1])
    if len(xs): print(f"token {nm}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+144}..{ys.max()+144}")

# 10. vector text band per box
for nm, x0, x1 in [("v1", 182, 236), ("v6", 551, 612), ("v7", 737, 798), ("v8", 812, 874)]:
    ys, xs = np.where(dk[300:322, x0:x1])
    if len(xs): print(f"vector {nm}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+300}..{ys.max()+300}")

# 11. purple bar fill exact color + edges
purp = (r > 100) & (r < 190) & (g < 60) & (b > 100) & (b < 190)
ys, xs = np.where(purp[210:258, 160:900])
print(f"purple bar bbox: x {xs.min()+160}..{xs.max()+160} y {ys.min()+210}..{ys.max()+210}")
win = img[220:248, 200:300].reshape(-1, 3)
q, n = np.unique((win // 16) * 16, axis=0, return_counts=True)
print("bar fill core:", sorted(zip(q.tolist(), n.tolist()), key=lambda z: -z[1])[:3])
