#!/usr/bin/env python3
"""m6: mystery left-line x56-58; title band; top structures with tight color
separation; q-zone structures."""
from PIL import Image
import json
from collections import Counter

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
im = Image.open(f"{SCR}/frame11_slide.png").convert("RGB")
px = im.load()
out = {}

# 1) colors along x55..60 at several y
for y in (100, 200, 300, 400, 470, 500):
    out[f"x50_62_y{y}"] = [(x, px[x, y]) for x in range(50, 63)]

# 2) title band: strong dark ink only (sum<330), y470..516
tp = [(x, y) for y in range(470, 516) for x in range(240, 780) if sum(px[x, y]) < 330]
xs = [p[0] for p in tp]; ys = [p[1] for p in tp]
out["title_dark_bbox"] = (min(xs), min(ys), max(xs), max(ys))
rowc = Counter(ys)
out["title_row_bands"] = sorted(r for r, n in rowc.items() if n > 3)
red = [(x, y) for (x, y) in tp if px[x, y][0] - px[x, y][1] > 60]
out["title_red_runs"] = None
if red:
    rxs = sorted(set(x for x, _ in red)); runs = []; s = e = rxs[0]
    for x in rxs[1:]:
        if x - e <= 10: e = x
        else: runs.append((s, e)); s = e = x
    runs.append((s, e))
    out["title_red_runs"] = runs

# 3) top structures, tight masks
# 3a) pale-yellow SOLID boxes (F0E060 core, tol 20)
py = [(x, y) for y in range(40, 235) for x in range(360, 760)
      if all(abs(px[x, y][i] - t) <= 20 for i, t in enumerate((240, 224, 96)))]
if py:
    xs = [p[0] for p in py]; ys = [p[1] for p in py]
    out["paleyellow_strict"] = {"n": len(py), "bbox": (min(xs), min(ys), max(xs), max(ys))}
    colc = Counter(xs)
    cols = sorted(c for c, n in colc.items() if n > 12)
    # compress col runs
    runs = []
    if cols:
        s = e = cols[0]
        for c in cols[1:]:
            if c - e <= 3: e = c
            else: runs.append((s, e)); s = e = c
        runs.append((s, e))
    out["paleyellow_strict"]["col_runs"] = runs
    rowc = Counter(ys)
    rows = sorted(r for r, n in rowc.items() if n > 12)
    out["paleyellow_strict"]["dense_rows"] = (rows[0], rows[-1]) if rows else None
# 3b) beam strict: yellow-green translucent (215..245, 235..255, 130..185)
bm = [(x, y) for y in range(40, 240) for x in range(360, 760)
      if 200 <= px[x, y][0] <= 246 and 232 <= px[x, y][1] <= 255 and 120 <= px[x, y][2] <= 190
      and px[x, y][1] - px[x, y][2] > 45 and px[x, y][1] - px[x, y][0] > 6]
if bm:
    xs = [p[0] for p in bm]; ys = [p[1] for p in bm]
    out["beam_strict"] = {"n": len(bm), "bbox": (min(xs), min(ys), max(xs), max(ys))}
    byr = {}
    for x, y in bm:
        if y not in byr: byr[y] = [x, x]
        else:
            byr[y][0] = min(byr[y][0], x); byr[y][1] = max(byr[y][1], x)
    out["beam_strict"]["edge_profile"] = {y: byr[y] for y in sorted(byr) if y % 10 == 0}
# 3c) green dashed Y boxes borders (green ~2E8B57/22AA44, tol 40, g-r>50)
gy = [(x, y) for y in range(40, 240) for x in range(360, 780)
      if px[x, y][1] - px[x, y][0] > 50 and px[x, y][1] > 120 and px[x, y][2] < px[x, y][1] - 20 and px[x, y][0] < 150]
if gy:
    xs = [p[0] for p in gy]; ys = [p[1] for p in gy]
    out["green_top_strict"] = {"n": len(gy), "bbox": (min(xs), min(ys), max(xs), max(ys))}
    colc = Counter(xs)
    cols = sorted(c for c, n in colc.items() if n > 10)
    out["green_top_strict"]["dense_cols"] = cols[:40]
    rowc = Counter(ys)
    rows = sorted(r for r, n in rowc.items() if n > 8)
    out["green_top_strict"]["dense_rows"] = rows[:30]

# 4) q zone: bright red box (CC0000) + white W box + beige strips
qr = [(x, y) for y in range(350, 470) for x in range(200, 340)
      if px[x, y][0] > 170 and px[x, y][0] - px[x, y][1] > 100 and px[x, y][0] - px[x, y][2] > 100]
if qr:
    xs = [p[0] for p in qr]; ys = [p[1] for p in qr]
    out["qzone_red"] = {"n": len(qr), "bbox": (min(xs), min(ys), max(xs), max(ys))}
    colc = Counter(xs)
    cols = sorted(c for c, n in colc.items() if n > 8)
    runs = []
    if cols:
        s = e = cols[0]
        for c in cols[1:]:
            if c - e <= 4: e = c
            else: runs.append((s, e)); s = e = c
        runs.append((s, e))
    out["qzone_red"]["col_runs"] = runs
# W box white w/ border at x244..265 y375..400 (015 hypothesis)
out["qzone_scanv_x254"] = [(y, px[254, y]) for y in range(350, 412, 2)]
# query row container + strips verification (015: rrect(173,401,219x32), GROUPS x180..383 y406..427)
gr = [(x, y) for y in range(395, 445) for x in range(170, 400)
      if all(abs(px[x, y][i] - t) <= 16 for i, t in enumerate((238, 253, 220)))]
out["queryrow_palegreen"] = {"n": len(gr)}
if gr:
    xs = [p[0] for p in gr]; ys = [p[1] for p in gr]
    out["queryrow_palegreen"]["bbox"] = (min(xs), min(ys), max(xs), max(ys))

print(json.dumps(out, indent=1, default=str))
