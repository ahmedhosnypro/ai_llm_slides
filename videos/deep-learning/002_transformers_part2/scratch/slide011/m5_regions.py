#!/usr/bin/env python3
"""m5: targeted geometry scans on frame11 (slide coords) for divergent regions."""
from PIL import Image
import json
from collections import Counter

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
im = Image.open(f"{SCR}/frame11_slide.png").convert("RGB")
px = im.load()
W, H = im.size
out = {}

def near(p, t, tol):
    return all(abs(p[i] - t[i]) <= tol for i in range(3))

# ---- A) far-left column x40..95: what ink lives there?
pts = [(x, y) for y in range(46, 515) for x in range(44, 92)
       if sum(px[x, y]) < 690 and not near(px[x, y], (233, 233, 231), 14)]
out["A_left_col"] = {"n": len(pts)}
if pts:
    ys = [p[1] for p in pts]; xs = [p[0] for p in pts]
    out["A_left_col"]["bbox"] = (min(xs), min(ys), max(xs), max(ys))
    rowc = Counter(ys)
    bands = []
    ys_s = sorted(set(ys)); s = e = ys_s[0]
    for y in ys_s[1:]:
        if y - e <= 4: e = y
        else: bands.append((s, e)); s = e = y
    bands.append((s, e))
    out["A_left_col"]["row_bands"] = bands
    colc = Counter(xs)
    out["A_left_col"]["col_hist_top"] = colc.most_common(8)

# ---- B) title ink: y465..515, dark/red pixels
tpts = [(x, y) for y in range(465, 516) for x in range(200, 800)
        if (sum(px[x, y]) < 400) or (px[x, y][0] > 140 and px[x, y][0] - px[x, y][1] > 70 and px[x, y][0] - px[x, y][2] > 70)]
if tpts:
    xs = [p[0] for p in tpts]; ys = [p[1] for p in tpts]
    out["B_title_ink"] = {"bbox": (min(xs), min(ys), max(xs), max(ys))}
    red = [(x, y) for (x, y) in tpts if px[x, y][0] > 140 and px[x, y][0] - px[x, y][1] > 70]
    if red:
        rxs = [p[0] for p in red]
        out["B_title_ink"]["red_x_range"] = (min(rxs), max(rxs))
        # red bands (contiguous runs)
        rxs_s = sorted(set(rxs)); runs = []; s = e = rxs_s[0]
        for x in rxs_s[1:]:
            if x - e <= 12: e = x
            else: runs.append((s, e)); s = e = x
        runs.append((s, e))
        out["B_title_ink"]["red_runs"] = runs

# ---- C) top region: green dashed Y boxes + pale-yellow boxes + beam
# green text Y1..Y4 (22AA44)
gpts = [(x, y) for y in range(40, 235) for x in range(360, 760)
        if near(px[x, y], (34, 170, 68), 50) and px[x, y][1] - px[x, y][0] > 50]
if gpts:
    xs = [p[0] for p in gpts]; ys = [p[1] for p in gpts]
    out["C_green_top"] = {"n": len(gpts), "bbox": (min(xs), min(ys), max(xs), max(ys))}
    colc = Counter(xs); rowc = Counter(ys)
    out["C_green_top"]["dense_cols>15"] = sorted(c for c, n in colc.items() if n > 15)[:20]
    out["C_green_top"]["dense_rows>10"] = sorted(r for r, n in rowc.items() if n > 10)[:20]
# pale yellow F0E060 boxes
ypts = [(x, y) for y in range(40, 235) for x in range(360, 760)
        if near(px[x, y], (240, 224, 96), 42)]
if ypts:
    xs = [p[0] for p in ypts]; ys = [p[1] for p in ypts]
    out["C_paleyellow"] = {"n": len(ypts), "bbox": (min(xs), min(ys), max(xs), max(ys))}
    rowc = Counter(ys)
    bands = []
    ys_s = sorted(set(ys)); s = e = ys_s[0]
    for y in ys_s[1:]:
        if y - e <= 3: e = y
        else: bands.append((s, e)); s = e = y
    bands.append((s, e))
    out["C_paleyellow"]["row_bands"] = bands[:12]
# beam: yellow-green translucent EFF7A0 / D8E830 family
bpts = [(x, y) for y in range(40, 240) for x in range(360, 760)
        if near(px[x, y], (239, 247, 160), 26) or near(px[x, y], (216, 232, 48), 40)]
if bpts:
    xs = [p[0] for p in bpts]; ys = [p[1] for p in bpts]
    out["C_beam"] = {"n": len(bpts), "bbox": (min(xs), min(ys), max(xs), max(ys))}
    # beam edge profile: for each y, min/max x
    byr = {}
    for x, y in bpts:
        if y not in byr: byr[y] = [x, x]
        else:
            byr[y][0] = min(byr[y][0], x); byr[y][1] = max(byr[y][1], x)
    sample = {y: byr[y] for y in sorted(byr) if y % 12 == 0}
    out["C_beam"]["edge_profile"] = sample

# ---- D) right arc: red pixels x660..920 y190..470 (thick C00000-ish, excluding chips)
apts = [(x, y) for y in range(190, 470) for x in range(655, 920)
        if px[x, y][0] > 150 and px[x, y][0] - px[x, y][1] > 90 and px[x, y][0] - px[x, y][2] > 90]
if apts:
    xs = [p[0] for p in apts]; ys = [p[1] for p in apts]
    out["D_arc_red"] = {"n": len(apts), "bbox": (min(xs), min(ys), max(xs), max(ys))}
    ayr = {}
    for x, y in apts:
        if y not in ayr: ayr[y] = [x, x]
        else:
            ayr[y][0] = min(ayr[y][0], x); ayr[y][1] = max(ayr[y][1], x)
    sample = {y: ayr[y] for y in sorted(ayr) if y % 10 == 0}
    out["D_arc_red"]["xspan_by_y"] = sample

# ---- E) q zone x160..430 y390..470: boxes/text
qpts = [(x, y) for y in range(390, 470) for x in range(160, 430) if sum(px[x, y]) < 660]
qdark = [(x, y) for (x, y) in qpts if sum(px[x, y]) < 420]
out["E_qzone"] = {"n_dark": len(qdark)}
if qdark:
    xs = [p[0] for p in qdark]; ys = [p[1] for p in qdark]
    out["E_qzone"]["dark_bbox"] = (min(xs), min(ys), max(xs), max(ys))
    colc = Counter(xs)
    out["E_qzone"]["dark_cols_top"] = colc.most_common(10)

print(json.dumps(out, indent=1, default=str))
