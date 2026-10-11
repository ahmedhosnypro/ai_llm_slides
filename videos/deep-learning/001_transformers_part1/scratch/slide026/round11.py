#!/usr/bin/env python3
import numpy as np
from PIL import Image
IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
PEACH = np.array([247, 227, 206])

print("== SENSITIVE scan x346..446 at line rows (any pixel diff>25) ==")
for y0 in (244, 285, 326, 370):
    for y in range(y0, y0 + 6):
        seg = A[y, 346:446]
        d = np.abs(seg - PEACH).sum(axis=1)
        idx = np.where(d > 25)[0]
        if len(idx):
            print(f"  y{y}: n={len(idx)} x{346+idx.min()}..{346+idx.max()} med_diff={int(np.median(d[idx]))}")

print("\n== ellipse fills (medians, off-text) ==")
for nm, (x, y) in {"Sim_ell": (275, 168), "Sim_ell2": (330, 182), "Prob_ell": (437, 168),
                   "Prob_ell2": (505, 185), "WSum_ell": (580, 160), "WSum_ell2": (680, 180)}.items():
    reg = A[y-2:y+3, x-2:x+3].reshape(-1, 3)
    m = np.median(reg, axis=0).astype(int)
    print(f"  {nm:10s} ({x},{y}) #{m[0]:02X}{m[1]:02X}{m[2]:02X}")

print("\n== X2 border dots: most saturated ring pixels ==")
ring = np.concatenate([A[471:476, 258:340].reshape(-1,3), A[505:510, 258:340].reshape(-1,3),
                       A[476:505, 258:263].reshape(-1,3), A[476:505, 333:338].reshape(-1,3)])
sat = ring[(ring[:, 0].astype(int) + ring[:, 2] - 2*ring[:, 1]) > 120]
print(f"  n={len(sat)} med={np.median(sat, axis=0) if len(sat) else 'none'}")
sat2 = ring[(ring[:, 0] > 150) & (ring[:, 2] > 150) & (ring[:, 1] < 120)]
print(f"  magenta-ish n={len(sat2)} med={np.median(sat2, axis=0) if len(sat2) else 'none'}")

print("\n== feed curve pixel colors ==")
for (x, y) in [(795,425),(788,435),(779,444),(761,455),(745,464),(708,474),(653,484),(560,494),
               (103,430),(107,455),(110,465)]:
    c = A[y, x]
    print(f"  ({x},{y}) #{c[0]:02X}{c[1]:02X}{c[2]:02X} {tuple(c)}")

print("\n== strip X3 glyph cell structure: col medians y482..500, x336..410 ==")
prev = None
for x in range(336, 410):
    col = A[482:500, x]
    m = np.median(col, axis=0).astype(int)
    key = tuple((m // 24).tolist())
    if key != prev:
        print(f"  x{x}: #{m[0]:02X}{m[1]:02X}{m[2]:02X}")
        prev = key

print("\n== softmax label color: darkest in bar ==")
sub = A[262:338, 462:486].reshape(-1, 3)
i = np.argmin(sub.sum(axis=1))
print(f"  darkest #{sub[i][0]:02X}{sub[i][1]:02X}{sub[i][2]:02X} {tuple(sub[i])}")
# purple-ish selection
pu = sub[(sub[:, 0] > 60) & (sub[:, 2] > 100) & (sub[:, 1] < sub[:, 2] - 30)]
print(f"  purple-ish n={len(pu)} med={np.median(pu, axis=0) if len(pu) else 'none'}")

print("\n== softmax bar: does label reach both words? ink cols in bar x458..488 ==")
sub = A[240:360, 458:489]
m = (np.abs(sub - np.array([248, 222, 251])).sum(axis=2) > 60)
cols = np.where(m.sum(axis=0) > 2)[0]
print("  ink cols:", 458 + cols.min(), "..", 458 + cols.max())
rows = np.where(m.sum(axis=1) > 2)[0]
print("  ink rows:", 240 + rows.min(), "..", 240 + rows.max())

print("\n== Y label in Y-box: darkest ==")
sub = A[124:142, 574:596].reshape(-1, 3)
i = np.argmin(sub.sum(axis=1))
print(f"  darkest #{sub[i][0]:02X}{sub[i][1]:02X}{sub[i][2]:02X} {tuple(sub[i])}")

print("\n== green arrow full column x560 (y144..200) ==")
for y in range(144, 200, 2):
    c = A[y, 560]
    print(f"  y{y}: #{c[0]:02X}{c[1]:02X}{c[2]:02X}", end="")
print()
print("== red arrow column x583 (y140..200) ==")
for y in range(140, 200, 2):
    c = A[y, 583]
    print(f"  y{y}: #{c[0]:02X}{c[1]:02X}{c[2]:02X}", end="")
print()
