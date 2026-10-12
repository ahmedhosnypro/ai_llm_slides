from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
dark = (R < 110) & (G < 110) & (B < 110)

# 1) L-bracket per-row x extent (x 628..648, y 393..500)
print("L-bracket per-row x extent (sampled rows):")
for y in range(394, 499, 6):
    m = dark[y, 628:649]
    rr = np.where(m)[0]
    if len(rr): print(f"  y={y}: x {628+rr[0]}..{628+rr[-1]}")
    else: print(f"  y={y}: -")
print("R-bracket per-row x extent (x 820..840):")
for y in range(394, 499, 6):
    m = dark[y, 820:841]
    rr = np.where(m)[0]
    if len(rr): print(f"  y={y}: x {820+rr[0]}..{820+rr[-1]}")
    else: print(f"  y={y}: -")

# bracket color sample
band = a[440:455, 633:640].reshape(-1, 3)
lum = band.sum(axis=1); i = lum.argmin()
print("L-bracket darkest px:", tuple(band[i]))
band = a[397:404, 633:645].reshape(-1, 3)
lum = band.sum(axis=1); i = lum.argmin()
print("L-bracket top-tick darkest px:", tuple(band[i]))

# 2) theta vs subscript extents per column (theta x-range vs sub x-range from col runs)
# col clusters: c1 647..676, c2 718..747, c3 789..819; rows: 401..423, 434..456, 467..489
for ci, (cx0, cx1) in enumerate([(647, 677), (718, 748), (789, 820)]):
    for ri, (ry0, ry1) in enumerate([(398, 426), (431, 459), (464, 492)]):
        sub = dark[ry0:ry1, cx0:cx1]
        rows = np.where(sub.any(axis=1))[0]; cols = np.where(sub.any(axis=0))[0]
        if not len(rows): print(f"  c{ci+1}r{ri+1}: EMPTY"); continue
        # theta-only: x 647..662 style split — find gap
        colc = sub.sum(axis=0)
        onc = colc > 0
        runs = []; s = None
        for x, v in enumerate(onc):
            if v and s is None: s = x
            if not v and s is not None: runs.append((cx0 + s, cx0 + x - 1)); s = None
        if s is not None: runs.append((cx0 + s, cx0 + len(onc) - 1))
        # vertical extent of theta part vs sub part
        if len(runs) >= 2:
            thx = runs[0]; sx = runs[-1]
            throws = np.where(sub[:, thx[0]-cx0:thx[1]-cx0+1].any(axis=1))[0]
            srows = np.where(sub[:, sx[0]-cx0:sx[1]-cx0+1].any(axis=1))[0]
            print(f"  c{ci+1}r{ri+1}: theta x{thx} y {ry0+throws[0]}..{ry0+throws[-1]} | sub x{sx} y {ry0+srows[0]}..{ry0+srows[-1]} | runs {runs}")
        else:
            print(f"  c{ci+1}r{ri+1}: single run {runs} y {ry0+rows[0]}..{ry0+rows[-1]}")
