#!/usr/bin/env python3
"""Slide 055 forensics 2: V corridor + softmax corridor with low threshold; K strips, W_k, Y rows, legend cells."""
from PIL import Image
import json
img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg").convert("RGB")
W, H = img.size
px = img.load()
out = {}
def redness(p):
    r, g, b = p
    return r - max(g, b)

# 1. V corridor: any ink (redness>18 or sum<420) x 570..730, y 215..375, excluding known boxes
hits = {}
for x in range(570, 732, 2):
    col = []
    for y in range(215, 376):
        p = px[x, y]
        r = redness(p); s = sum(p)
        if r > 18 or s < 420:
            col.append((y, "R" if r > 18 else "D", max(r, 300 - s // 3)))
    if col:
        hits[x] = col[:20]
# summarize: per column, y-ranges
summ = {}
for x, col in hits.items():
    ys = sorted(set(y for y, t, v in col))
    bands = []
    cur = [ys[0], ys[0]]
    for y in ys[1:]:
        if y - cur[1] <= 3:
            cur[1] = y
        else:
            bands.append(tuple(cur)); cur = [y, y]
    bands.append(tuple(cur))
    summ[x] = bands
out["Vcorr_cols"] = {str(k): v for k, v in list(summ.items())[::2]}

# 2. softmax->nodes corridor x 512..552, all y 210..375, low threshold
hits2 = {}
for x in range(512, 553, 2):
    col = []
    for y in range(210, 376):
        r = redness(px[x, y])
        if r > 18:
            col.append(y)
    if col:
        hits2[x] = col
out["SMcorr_cols"] = {str(k): v for k, v in hits2.items()}

# 3. K strip structure: x 230..275 at strip rows — column profile of non-peach
def near(p, c, tol):
    return all(abs(p[i] - c[i]) <= tol for i in range(3))
for nm, cy in {"K1": 230.5, "K2": 269.5, "K3": 309.5, "K4": 352}.items():
    row = []
    for x in range(230, 280):
        p = px[x, int(cy)]
        row.append((x, "%02X%02X%02X" % p))
    out[f"kstrip_{nm}_row"] = row

# 4. W_k boxes: bbox per box via green-yellow fill
def is_wkg(p):
    r, g, b = p
    return g > 190 and (g - b) > 55 and r > 120
wk = [(x, y) for y in range(210, 390) for x in range(185, 250) if is_wkg(px[x, y])]
rows = {}
for x, y in wk:
    rows.setdefault(y, []).append(x)
ygroups = []
ys = sorted(rows)
cur = [ys[0], ys[0]]
for y in ys[1:]:
    if y - cur[1] <= 3: cur[1] = y
    else: ygroups.append(tuple(cur)); cur = [y, y]
ygroups.append(tuple(cur))
out["wk_boxes_ygroups"] = ygroups
for a, b in ygroups:
    xs = [x for y in range(a, b + 1) for x in rows.get(y, [])]
    out.setdefault("wk_boxes", []).append([min(xs), a, max(xs), b])

# 5. Y container rows: strip structure at row centers x 100..185
for nm, cy in {"Y4": 232, "Y3": 271, "Y2": 311, "Y1": 353}.items():
    row = []
    for x in range(98, 190):
        p = px[x, cy]
        row.append((x, "%02X%02X%02X" % p))
    out[f"yrow_{nm}"] = row[::2]

# 6. right Y container rows
for nm, cy in {"Y4r": 232, "Y1r": 353}.items():
    row = []
    for x in range(775, 870):
        p = px[x, cy]
        row.append((x, "%02X%02X%02X" % p))
    out[f"yrow_{nm}"] = row[::2]

# 7. legend interior: cells (yellow FDFD96-ish) columns
def is_yellow(p):
    r, g, b = p
    return r > 225 and g > 215 and b < 180
ly = [(x, y) for y in range(415, 515) for x in range(725, 910) if is_yellow(px[x, y])]
cols = {}
for x, y in ly:
    cols.setdefault(x, []).append(y)
xs = sorted(cols)
groups, cur = [], []
for v in xs:
    if cur and v - cur[-1] > 3: groups.append((cur[0], cur[-1])); cur = []
    cur.append(v)
if cur: groups.append((cur[0], cur[-1]))
out["legend_yellow_cols"] = [(a, b, min(cols[a]), max(cols[a])) for a, b in groups]

# 8. legend white W box
def is_white(p):
    return all(v > 240 for v in p)
lw = [(x, y) for y in range(425, 505) for x in range(780, 880) if is_white(px[x, y])]
if lw:
    xs2 = [p[0] for p in lw]; ys2 = [p[1] for p in lw]
    out["legend_W_white"] = [min(xs2), min(ys2), max(xs2), max(ys2), len(lw)]

# 9. q2 glyph cells: pale/white right of q2 text (x 328..350, y 393..412)
qc = [(x, y) for y in range(390, 415) for x in range(325, 355) if is_white(px[x, y])]
if qc:
    xs3 = [p[0] for p in qc]; ys3 = [p[1] for p in qc]
    out["q2_glyph_white"] = [min(xs3), min(ys3), max(xs3), max(ys3), len(qc)]

# 10. Z-row: cell structure — full row sample at y=472 x 195..540
row = []
for x in range(195, 545, 1):
    p = px[x, 472]
    row.append((x, "%02X%02X%02X" % p))
out["zrow_y472"] = row[::3]

# 11. Z2 dashed border: redness rows x 255..370
zr = {}
for y in range(438, 502):
    xs4 = [x for x in range(250, 375) if redness(px[x, y]) > 50]
    if len(xs4) >= 2:
        zr[y] = (min(xs4), max(xs4), len(xs4))
out["z2_dash_rows"] = {str(k): v for k, v in zr.items()}

# 12. O box flanking cells: row sample at y=131, x 540..710
row = []
for x in range(540, 712):
    p = px[x, 131]
    row.append((x, "%02X%02X%02X" % p))
out["O_row131"] = row[::2]

print(json.dumps(out, indent=1))
