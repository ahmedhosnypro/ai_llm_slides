#!/usr/bin/env python3
# probe44_resume5.py — LEFT face edges + RT/IN front seam check + remaining details.
import numpy as np
from PIL import Image

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_044.jpg").convert("RGB")
a = np.asarray(F).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
def near(c, tol): return (abs(R-c[0])<tol) & (abs(G-c[1])<tol) & (abs(B-c[2])<tol)
SALMON = (216,78,52); MAG = (157,0,166); MAG_D = (78,0,78)
m_sal = near(SALMON, 38); m_mag = near(MAG, 45); m_magd = near(MAG_D, 30)

print("== LEFT face: row scans (salmon runs x55..215) ==")
for yy in list(range(246, 262)) + list(range(405, 431, 2)):
    row = np.where(m_sal[yy, 55:215])[0] + 55
    if len(row):
        runs, s = [], row[0]
        for i in range(1, len(row)):
            if row[i] != row[i-1]+1: runs.append((s, row[i-1])); s = row[i]
        runs.append((s, row[-1]))
        print(f"  y{yy}: {runs} n={len(row)}")
    else: print(f"  y{yy}: none")
print("== LEFT face: col scans x66..70, x198..204 (top/bottom) ==")
for xx in (67, 69, 130, 199, 201):
    col = np.where(m_sal[180:460, xx])[0] + 180
    if len(col):
        runs, s = [], col[0]
        for i in range(1, len(col)):
            if col[i] != col[i-1]+1: runs.append((s, col[i-1])); s = col[i]
        runs.append((s, col[-1]))
        print(f"  x{xx}: {runs}")
print("== RT front: row-seam check (magenta-dark rows inside x692..816) ==")
for yy in range(170, 332):
    n = int(m_magd[yy, 692:816].sum())
    if n > 40: print(f"  RT magD row y{yy}: {n}")
print("== RT front: col-seam check ==")
for xx in range(689, 820):
    n = int(m_magd[180:330, xx].sum())
    if n > 40: print(f"  RT magD col x{xx}: {n}")
print("== IN front magD rows (x460..545) ==")
for yy in range(195, 356):
    n = int(m_magd[yy, 460:545].sum())
    if n > 30: print(f"  IN magD row y{yy}: {n}")
print("== GN front magD rows (x280..334) ==")
for yy in range(175, 336):
    n = int(m_magd[yy, 280:334].sum())
    if n > 30: print(f"  GN magD row y{yy}: {n}")
print("== GN/IN/RT front bottom + top edges (magenta col scans) ==")
for xx, y0, y1, nm in ((310, 160, 345, "GN mag col"), (500, 185, 365, "IN mag col"), (720, 160, 345, "RT mag col"), (800, 160, 345, "RT mag col2")):
    col = np.where((m_mag | m_magd)[y0:y1, xx])[0] + y0
    if len(col):
        runs, s = [], col[0]
        for i in range(1, len(col)):
            if col[i] != col[i-1]+1: runs.append((s, col[i-1])); s = col[i]
        runs.append((s, col[-1]))
        print(f"  {nm} x{xx}: {runs}")
print("== GN salmon part edges (col scans) ==")
for xx in (345, 380, 408):
    col = np.where(m_sal[150:345, xx])[0] + 150
    if len(col):
        runs, s = [], col[0]
        for i in range(1, len(col)):
            if col[i] != col[i-1]+1: runs.append((s, col[i-1])); s = col[i]
        runs.append((s, col[-1]))
        print(f"  GN sal col x{xx}: {runs}")
print("== IN salmon col + right face edges ==")
for xx in (551, 565, 576, 583, 587):
    col = np.where(m_sal[150:365, xx])[0] + 150
    if len(col):
        runs, s = [], col[0]
        for i in range(1, len(col)):
            if col[i] != col[i-1]+1: runs.append((s, col[i-1])); s = col[i]
        runs.append((s, col[-1]))
        print(f"  IN sal col x{xx}: {runs}")
print("== bright vertical seams left of fronts (very bright pink r>230,g>150,b>210) ==")
bp = (R>225) & (G>140) & (B>205)
for x0, x1, y0, y1, nm in ((262, 280, 175, 335, "GN-left"), (442, 458, 195, 355, "IN-left"), (672, 692, 165, 333, "RT-left"), (196, 212, 240, 430, "L-left")):
    for xx in range(x0, x1):
        n = int(bp[y0:y1, xx].sum())
        if n > 40: print(f"  {nm} x{xx}: {n}")
print("== samples arrow + left channels arrow (loose red) ==")
lr = (R>135) & ((R-G)>45) & ((R-B)>35)
ysA, xsA = np.where(lr[150:240, 40:200])
print("  Samples region red bbox: x", xsA.min()+40, xsA.max()+40, " y", ysA.min()+150, ysA.max()+150, " n", len(xsA))
for yy in range(425, 480):
    row = np.where(lr[yy, 40:260])[0] + 40
    if len(row) > 3: print(f"  left-chan y{yy}: x {row.min()}..{row.max()} n={len(row)}")
