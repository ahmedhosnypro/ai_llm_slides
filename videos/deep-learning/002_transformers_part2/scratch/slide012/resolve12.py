#!/usr/bin/env python3
# resolve12.py — targeted frame scans to resolve banked-measurement conflicts:
# panel vertical extents, canvas bounds, pink box, strips (frame px, 960x540).
from PIL import Image
import numpy as np

ORG = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_012.jpg'
a = np.asarray(Image.open(ORG).convert('RGB')).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def classify(y, x):
    R, G, B = a[y, x]
    mx, mn = int(max(R, G, B)), int(min(R, G, B))
    if mx > 246 and mn > 246: return 'W'          # white
    if R > 200 and G > 240 and B > 210 and G >= R: return 'g'   # green pastel
    if R > 235 and G > 215 and B > 190 and R >= G >= B: return 'o'  # orange pastel
    if B > 235 and R > 195 and abs(int(R) - int(G)) < 12 and B - G > 15: return 'l'  # lavender
    if R > 245 and G > 215 and B > 235: return 'p'  # pink
    if mx - mn < 25 and mx > 225: return '.'       # gray/white-ish
    if mx - mn < 25: return 'k'                    # dark/neutral
    return '?'

print("=== 1. vertical class maps (single columns) ===")
for fx in (320, 380, 485, 540, 645, 700):
    runs = []
    prev = None
    for fy in range(150, 400):
        c = classify(fy, fx)
        if c != prev:
            runs.append([c, fy, fy])
            prev = c
        else:
            runs[-1][2] = fy
    s = " ".join(f"{c}{y0}-{y1}" for c, y0, y1 in runs if y1 - y0 >= 1 or c not in ".?")
    print(f"fx {fx}: {s}")

print("\n=== 2. panel horizontal extents (rows) ===")
for fy in (170, 250, 320, 335, 345, 352, 356):
    runs = []
    prev = None
    for fx in range(240, 740):
        c = classify(fy, fx)
        if c != prev:
            runs.append([c, fx, fx])
            prev = c
        else:
            runs[-1][2] = fx
    s = " ".join(f"{c}{x0}-{x1}" for c, x0, x1 in runs if (x1 - x0 >= 2 and c in 'golpW') or (x1 - x0 >= 4 and c in 'k.'))
    print(f"fy {fy}: {s}")

print("\n=== 3. pink box: strict pink bbox ===")
m = (r > 248) & (g > 215) & (g < 245) & (b > 235)
sub = m[140:260, 90:260]
ys, xs = np.where(sub)
if len(ys):
    print(f"pink bbox fx {xs.min()+90}..{xs.max()+90}  fy {ys.min()+140}..{ys.max()+140}  n={len(ys)}")
print("pink fill sample (no rim):", a[175, 108], a[182, 110], a[168, 240])

print("\n=== 4. canvas (white rect) bounds: white runs ===")
for fy in (125, 300, 460, 466, 469):
    row = a[fy, 80:790]
    w = (row.max(axis=1) > 246) & (row.min(axis=1) > 246)
    xs = np.where(w)[0]
    if len(xs):
        print(f"fy {fy}: white fx {xs.min()+80}..{xs.max()+80} n={len(xs)}")
for fx in (100, 760):
    col = a[110:500, fx]
    w = (col.max(axis=1) > 246) & (col.min(axis=1) > 246)
    ys = np.where(w)[0]
    if len(ys):
        print(f"fx {fx}: white fy {ys.min()+110}..{ys.max()+110} n={len(ys)}")

print("\n=== 5. strips: pastel bboxes (strict, per head color) ===")
for nm, mask in [
    ("s1-green", (g > 240) & (r > 195) & (r < 235) & (b > 210) & (b < 245) & (g - r > 15)),
    ("s2-orange", (r > 238) & (g > 218) & (g < 242) & (b > 190) & (b < 222) & (r - b > 25)),
    ("s3-lav", (b > 238) & (r > 198) & (r < 228) & (g > 198) & (g < 228) & (b - r > 15)),
]:
    sub = mask[350:395, 240:740]
    ys, xs = np.where(sub)
    if len(ys) > 20:
        print(f"{nm}: fx {xs.min()+240}..{xs.max()+240}  fy {ys.min()+350}..{ys.max()+350} n={len(ys)}")

print("\n=== 6. panels: strict pastel bboxes ===")
for nm, mask in [
    ("H1", (g > 240) & (r > 195) & (r < 235) & (b > 210) & (b < 245) & (g - r > 15)),
    ("H2", (r > 238) & (g > 218) & (g < 242) & (b > 190) & (b < 222) & (r - b > 25)),
    ("H3", (b > 238) & (r > 198) & (r < 228) & (g > 198) & (g < 228) & (b - r > 15)),
]:
    sub = mask[140:350, 240:740]
    ys, xs = np.where(sub)
    if len(ys) > 50:
        print(f"{nm}: fx {xs.min()+240}..{xs.max()+240}  fy {ys.min()+140}..{ys.max()+140} n={len(ys)}")

print("\n=== 7. gap between panel bottom and strip top (fy 330..360 @ fx 320) ===")
for fy in range(328, 362, 2):
    print(f"fy {fy}: {a[fy, 320]} {a[fy, 480]} {a[fy, 700]}")
