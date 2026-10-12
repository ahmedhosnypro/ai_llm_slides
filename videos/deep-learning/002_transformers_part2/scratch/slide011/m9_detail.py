#!/usr/bin/env python3
"""m9: left-zone row detail (transition maps at 4 row centers), outContainer
x755..810 detail, h-ovals, arc endpoints, W chip columns detail."""
from PIL import Image
import json
from collections import Counter

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
im = Image.open(f"{SCR}/frame11_slide.png").convert("RGB")
px = im.load()
out = {}

def scan_h(y, x0, x1, step=1):
    prev = None; ch = []
    for x in range(x0, x1, step):
        p = px[x, y]
        key = (p[0] // 18, p[1] // 18, p[2] // 18)
        if key != prev: ch.append((x, p)); prev = key
    return ch

# left zone rows: find row centers first — dashed group outline rows
# scan vertical at x94 (strip left edge in 015) and x105
out["scanv_x96"] = [(y, px[96, y]) for y in range(215, 370, 1)][:80]

# rows likely at same y as 015 (248/277/305/334) — scan each
for y in (248, 277, 305, 334):
    out[f"row_y{y}"] = scan_h(y, 88, 232)

# outContainer right: scanv/scanh around x755..812 y168..242
out["oc_scanv_x770"] = [(y, px[770, y]) for y in range(165, 245, 2)]
out["oc_scanh_y190"] = scan_h(190, 745, 830)
out["oc_scanh_y220"] = scan_h(220, 745, 830)

# h ovals: black pixels bbox per band y105..210 x590..815
hb = [(x, y) for y in range(100, 215) for x in range(588, 820) if sum(px[x, y]) < 210]
if hb:
    rowc = Counter(p[1] for p in hb)
    bands = []
    ys_s = sorted(set(p[1] for p in hb)); s = e = ys_s[0]
    for y in ys_s[1:]:
        if y - e <= 6: e = y
        else: bands.append((s, e)); s = e = y
    bands.append((s, e))
    per = {}
    for y0, y1 in bands:
        xs = [x for x, y in hb if y0 <= y <= y1]
        per[f"{y0}-{y1}"] = (min(xs), max(xs), len(xs))
    out["htags_bands"] = per

# W chip columns: find colored-border boxes x600..815 y290..430; per column band
# red borders (CC2222): vertical runs
for cname, t, tol in (("red", (204, 34, 34), 50), ("green", (46, 139, 87), 45), ("blue", (47, 85, 200), 50)):
    pts = [(x, y) for y in range(285, 435) for x in range(598, 820)
           if all(abs(px[x, y][i] - t[i]) <= tol for i in range(3))]
    if pts:
        colc = Counter(p[0] for p in pts)
        cols = sorted(c for c, n in colc.items() if n > 6)
        runs = []
        if cols:
            s = e = cols[0]
            for c in cols[1:]:
                if c - e <= 6: e = c
                else: runs.append((s, e)); s = e = c
            runs.append((s, e))
        out[f"chips_{cname}_col_runs"] = runs
        rowc = Counter(p[1] for p in pts)
        rows = sorted(r for r, n in rowc.items() if n > 6)
        rb = []
        if rows:
            s = e = rows[0]
            for r in rows[1:]:
                if r - e <= 4: e = r
                else: rb.append((s, e)); s = e = r
            rb.append((s, e))
        out[f"chips_{cname}_row_bands"] = rb

# arc: endpoint detail — top end and bottom end
out["arc_top_scanh"] = scan_h(248, 790, 835)
out["arc_bot_scanv_x668"] = [(y, px[668, y]) for y in range(330, 372, 2)]
out["arc_bot_scanv_x676"] = [(y, px[676, y]) for y in range(330, 372, 2)]

# V strips x508..532 + V labels: colored cells census
cen = Counter()
for y in range(235, 345):
    for x in range(506, 532):
        r, g, b = px[x, y]
        cen[(r // 16 * 16, g // 16 * 16, b // 16 * 16)] += 1
out["vstrip_census_top6"] = [(f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}", n) for c, n in cen.most_common(6)]

print(json.dumps(out, indent=1, default=str))
