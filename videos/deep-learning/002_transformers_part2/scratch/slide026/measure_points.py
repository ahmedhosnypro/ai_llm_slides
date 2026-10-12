#!/usr/bin/env python3
"""Sample exact pixels + tight-tolerance components for slide_026 frame."""
from PIL import Image
from collections import deque

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg').convert('RGB')
W, H = im.size
px = im.load()

def near(c, t, tol):
    return all(abs(c[i] - t[i]) <= tol for i in range(3))

# ---- point samples: background, panel, edges ----
print("--- point samples ---")
pts = {
    'corner 5,5': (5, 5), 'top-mid 480,20': (480, 20), 'left edge 30,270': (30, 270),
    'panel 480,100 (below title)': (480, 100), 'panel 200,300': (200, 300),
    'badge 877,68': (877, 68), 'badge 875,71': (875, 71), 'badge 880,71': (880, 71),
    'frame border col? 60,300': (60, 300), '58,300': (58, 300), '59,300': (59, 300),
    '902,300': (902, 300), '901,300': (901, 300), '900,300': (900, 300),
    'row43 x480': (480, 43), 'row44 x480': (480, 44), 'row45 x480': (480, 45),
    'row516 x480': (480, 516), 'row517 x480': (480, 517), 'row518 x480': (480, 518),
    'row519 x480': (480, 519), 'row520 x480': (480, 520),
    'bottom strip 480,530': (480, 530), '480,535': (480, 535), '480,539': (480, 539),
    'blue box 300,300': (300, 300), 'gray box 500,200': (500, 200),
    'green container 700,300': (700, 300), 'orange 490,260': (490, 260),
}
for k, (x, y) in pts.items():
    print(f"{k}: {px[x, y]}")

# ---- border scan: exact rows/cols where color deviates from local bg ----
print("\n--- col scan x=57..64 at y=300 ---")
for x in range(55, 66):
    print(x, px[x, 300])
print("--- col scan x=897..905 at y=300 ---")
for x in range(896, 906):
    print(x, px[x, 300])
print("--- row scan y=40..48 at x=480 ---")
for y in range(40, 49):
    print(y, px[480, y])
print("--- row scan y=512..522 at x=480 ---")
for y in range(512, 523):
    print(y, px[480, y])
print("--- row scan y=525..540 at x=480 (bottom strip?) ---")
for y in range(525, 540):
    print(y, px[480, y])
print("--- row scan y=525..540 at x=100 ---")
for y in range(525, 540):
    print(y, px[100, y])

# ---- badge: scan around (860..900, 50..95) for yellowish ----
print("\n--- badge region yellowish bbox ---")
YEL = (250, 250, 140)
minx, miny, maxx, maxy, n = 9999, 9999, -1, -1, 0
for y in range(45, 100):
    for x in range(840, 920):
        c = px[x, y]
        if c[0] > 200 and c[1] > 200 and 80 < c[2] < 200:
            n += 1
            minx = min(minx, x); maxx = max(maxx, x)
            miny = min(miny, y); maxy = max(maxy, y)
print("yellowish bbox", (minx, miny, maxx, maxy), "count", n)

# ---- tight components for key fills ----
def components(target, tol, min_size=120, step=1):
    pts_set = set()
    for y in range(H):
        for x in range(W):
            if near(px[x, y], target, tol):
                pts_set.add((x, y))
    seen = set()
    comps = []
    for p0 in list(pts_set):
        if p0 in seen:
            continue
        q = deque([p0]); seen.add(p0)
        minx = maxx = p0[0]; miny = maxy = p0[1]; n = 0
        while q:
            x, y = q.popleft(); n += 1
            minx = min(minx, x); maxx = max(maxx, x)
            miny = min(miny, y); maxy = max(maxy, y)
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                p = (x+dx, y+dy)
                if p in pts_set and p not in seen:
                    seen.add(p); q.append(p)
        if n >= min_size:
            comps.append((n, minx, miny, maxx, maxy, round(n / max(1, (maxx-minx+1)*(maxy-miny+1)), 2)))
    comps.sort(reverse=True)
    return comps

print("\n--- blue 00A9E0 tol15 ---")
for c in components((0, 169, 224), 15)[:6]:
    print(c)
print("\n--- gray BFBFBF tol12 ---")
for c in components((191, 191, 191), 12)[:14]:
    print(c)
print("\n--- lgreen DFEECD tol8 ---")
for c in components((223, 238, 205), 8)[:10]:
    print(c)
print("\n--- orange F79646 tol25 ---")
for c in components((247, 150, 70), 25)[:10]:
    print(c)
print("\n--- green 92D050 tol30 ---")
for c in components((146, 208, 80), 30)[:10]:
    print(c)
print("\n--- dark red C00000 tol35 ---")
for c in components((192, 0, 0), 35, 60)[:14]:
    print(c)
print("\n--- maroon 800000 tol25 ---")
for c in components((128, 0, 0), 25, 40)[:10]:
    print(c)
print("\n--- green border 00B050 tol35 ---")
for c in components((0, 176, 80), 35, 40)[:10]:
    print(c)
