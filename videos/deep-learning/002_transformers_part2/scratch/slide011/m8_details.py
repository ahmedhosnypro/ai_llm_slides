#!/usr/bin/env python3
"""m8: blue frame right edge; top-zone structures; right W_v fill; query strips;
Dot Product box + label color; left-zone group outline + W boxes; K boxes."""
from PIL import Image
import json
from collections import Counter

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
im = Image.open(f"{SCR}/frame11_slide.png").convert("RGB")
px = im.load()
out = {}

def near(p, t, tol):
    return all(abs(p[i] - t[i]) <= tol for i in range(3))

# 1) blue right edge: cols 860..915, any blue-ish pixel
bl = {}
for x in range(855, 920):
    n = sum(1 for y in range(60, 515) if px[x, y][2] - px[x, y][0] > 35 and px[x, y][2] > 120 and px[x, y][1] < px[x, y][2])
    if n > 30: bl[x] = n
out["blue_right_cols"] = bl
# blue top edge rows 55..75
bt = {}
for y in range(52, 80):
    n = sum(1 for x in range(60, 880) if px[x, y][2] - px[x, y][0] > 35 and px[x, y][2] > 120 and px[x, y][1] < px[x, y][2])
    if n > 100: bt[y] = n
out["blue_top_rows"] = bt
# blue bottom rows 500..518
bb = {}
for y in range(498, 519):
    n = sum(1 for x in range(60, 880) if px[x, y][2] - px[x, y][0] > 35 and px[x, y][2] > 120 and px[x, y][1] < px[x, y][2])
    if n > 100: bb[y] = n
out["blue_bottom_rows"] = bb

# 2) right W_v boxes fill x528..570: color census
cen = Counter()
for y in range(230, 345):
    for x in range(530, 568):
        r, g, b = px[x, y]
        cen[(r // 16 * 16, g // 16 * 16, b // 16 * 16)] += 1
out["wvzone_census_top8"] = [(f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}", n) for c, n in cen.most_common(8)]

# 3) top zone: Y dashed-green boxes. Widen green mask, y40..240 x360..780, g-r>40
gy = [(x, y) for y in range(40, 245) for x in range(360, 785)
      if px[x, y][1] - px[x, y][0] > 40 and px[x, y][1] > 110 and px[x, y][0] < 160 and px[x, y][2] < px[x, y][1]]
out["yzone_green_n"] = len(gy)
if gy:
    colc = Counter(p[0] for p in gy)
    cols = sorted(c for c, n in colc.items() if n > 8)
    runs = []
    if cols:
        s = e = cols[0]
        for c in cols[1:]:
            if c - e <= 5: e = c
            else: runs.append((s, e)); s = e = c
        runs.append((s, e))
    out["yzone_green_col_runs"] = runs
    rowc = Counter(p[1] for p in gy)
    rows = sorted(r for r, n in rowc.items() if n > 6)
    rb = []
    if rows:
        s = e = rows[0]
        for r in rows[1:]:
            if r - e <= 3: e = r
            else: rb.append((s, e)); s = e = r
        rb.append((s, e))
    out["yzone_green_row_bands"] = rb

# 4) pale-yellow boxes row: strict F0E060, get per-row-band col runs
py = [(x, y) for y in range(40, 245) for x in range(360, 785)
      if all(abs(px[x, y][i] - t) <= 22 for i, t in enumerate((240, 224, 96)))]
if py:
    rowc = Counter(p[1] for p in py)
    rows = sorted(r for r, n in rowc.items() if n > 10)
    rb = []
    if rows:
        s = e = rows[0]
        for r in rows[1:]:
            if r - e <= 4: e = r
            else: rb.append((s, e)); s = e = r
        rb.append((s, e))
    out["paleyellow_row_bands"] = rb
    # per band, col extents
    pr = {}
    for y0, y1 in rb:
        xs = [x for x, y in py if y0 <= y <= y1]
        if xs:
            colc = Counter(xs)
            cols = sorted(c for c, n in colc.items() if n > 3)
            runs = []
            if cols:
                s = e = cols[0]
                for c in cols[1:]:
                    if c - e <= 6: e = c
                    else: runs.append((s, e)); s = e = c
                runs.append((s, e))
            pr[f"{y0}-{y1}"] = runs
    out["paleyellow_band_cols"] = pr

# 5) Dot Product box: strict edges via tan runs on scanlines
def hruns(y, x0, x1, t, tol):
    xs = [x for x in range(x0, x1) if near(px[x, y], t, tol)]
    runs = []
    if xs:
        s = e = xs[0]
        for x in xs[1:]:
            if x - e <= 2: e = x
            else: runs.append((s, e)); s = e = x
        runs.append((s, e))
    return runs
out["tan_y300_runs"] = hruns(300, 190, 330, (216, 192, 180), 20)
out["tan_y200_runs"] = hruns(200, 190, 330, (216, 192, 180), 20)
def vruns(x, y0, y1, t, tol):
    ys = [y for y in range(y0, y1) if near(px[x, y], t, tol)]
    runs = []
    if ys:
        s = e = ys[0]
        for y in ys[1:]:
            if y - e <= 2: e = y
            else: runs.append((s, e)); s = e = y
        runs.append((s, e))
    return runs
out["tan_x250_runs"] = vruns(250, 180, 395, (216, 192, 180), 20)
# label color inside box top: pixels y215..232 x229..288
lab = [(x, y, px[x, y]) for y in range(213, 233) for x in range(230, 288) if sum(px[x, y]) < 500]
out["dotprod_label_n"] = len(lab)
if lab:
    rs = sum(1 for _, _, p in lab if p[0] - p[1] > 40)
    out["dotprod_label_redish"] = rs

# 6) K boxes between W boxes and Dot Product (spec: tiny boxes K1..K4): census x185..230 y230..345
cen2 = Counter()
for y in range(230, 345):
    for x in range(186, 230):
        r, g, b = px[x, y]
        cen2[(r // 16 * 16, g // 16 * 16, b // 16 * 16)] += 1
out["kzone_census_top8"] = [(f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}", n) for c, n in cen2.most_common(8)]

# 7) left W boxes green fill: x140..185 y230..345 census
cen3 = Counter()
for y in range(230, 345):
    for x in range(140, 186):
        r, g, b = px[x, y]
        cen3[(r // 16 * 16, g // 16 * 16, b // 16 * 16)] += 1
out["lwzone_census_top8"] = [(f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}", n) for c, n in cen3.most_common(8)]
# green fill bbox (W boxes green ~ 4C8C4C? measure)
gr = [(x, y) for y in range(230, 345) for x in range(140, 190)
      if px[x, y][1] > 90 and px[x, y][1] - px[x, y][0] > 25 and px[x, y][1] - px[x, y][2] > 15 and sum(px[x, y]) < 420]
out["lw_green_n"] = len(gr)
if gr:
    out["lw_green_bbox"] = (min(p[0] for p in gr), min(p[1] for p in gr), max(p[0] for p in gr), max(p[1] for p in gr))
    rowc = Counter(p[1] for p in gr)
    rows = sorted(r for r, n in rowc.items() if n > 6)
    rb = []
    if rows:
        s = e = rows[0]
        for r in rows[1:]:
            if r - e <= 4: e = r
            else: rb.append((s, e)); s = e = r
        rb.append((s, e))
    out["lw_green_row_bands"] = rb

# 8) dashed group outline in left zone: green dashed border x100..230 y225..365
gd = [(x, y) for y in range(220, 370) for x in range(98, 235)
      if px[x, y][1] - px[x, y][0] > 40 and px[x, y][1] > 100 and px[x, y][0] < 120 and px[x, y][2] < px[x, y][1] - 15]
out["group_green_n"] = len(gd)
if gd:
    colc = Counter(p[0] for p in gd)
    out["group_cols>25"] = sorted(c for c, n in colc.items() if n > 25)
    rowc = Counter(p[1] for p in gd)
    out["group_rows>40"] = sorted(r for r, n in rowc.items() if n > 40)

# 9) query row strips exact: scan y414 row for color transitions x170..400
def scan_h(y, x0, x1):
    prev = None; ch = []
    for x in range(x0, x1):
        p = px[x, y]
        key = (p[0] // 20, p[1] // 20, p[2] // 20)
        if key != prev: ch.append((x, p)); prev = key
    return ch
out["qrow_y415"] = scan_h(415, 170, 400)
out["qrow_y425"] = scan_h(425, 170, 400)

print(json.dumps(out, indent=1, default=str))
