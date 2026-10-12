#!/usr/bin/env python3
"""Slide 055 forensics 3: differential redness scans (baseline peach ~+21, ink >+35)."""
from PIL import Image
import json
img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg").convert("RGB")
px = img.load()
out = {}
def redness(p):
    r, g, b = p
    return r - max(g, b)

# 1. V corridor rows: max redness per x, node rows +/-3, x 566..730
for cy in [237, 277, 316, 359]:
    prof = []
    for x in range(566, 732):
        m = max(redness(px[x, y]) for y in range(cy - 3, cy + 4))
        if m > 35:
            prof.append((x, m))
    out[f"Vrow_{cy}"] = prof

# 2. SM corridor: max redness per x, x 514..546
for cy in [237, 277, 316, 359]:
    prof = []
    for x in range(512, 548):
        m = max(redness(px[x, y]) for y in range(cy - 3, cy + 4))
        if m > 35:
            prof.append((x, m))
    out[f"SMrow_{cy}"] = prof

# 3. node->sigma shafts: max redness per y at node x +/-2, y 210..238
for nx in [557, 587, 616, 645]:
    prof = []
    for y in range(209, 240):
        m = max(redness(px[x, y]) for x in range(nx - 2, nx + 3))
        if m > 35:
            prof.append((y, m))
    out[f"NS_x{nx}"] = prof

# 4. sigma box: verify fill + extent via light-blue; and O box flanking cells
def near(p, c, tol):
    return all(abs(p[i] - c[i]) <= tol for i in range(3))
sb = [(x, y) for y in range(180, 260) for x in range(500, 720) if near(px[x, y], (234, 254, 252), 14)]
if sb:
    xs = [p[0] for p in sb]; ys = [p[1] for p in sb]
    out["sigmabox_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(sb)]

# 5. O box row 131 detail: group colors (done before) — flank cells extent via non-peach at y 125..140
nz = []
for x in range(540, 715):
    cnt = sum(1 for y in range(122, 142) if not near(px[x, y], (247, 226, 205), 20))
    if cnt > 12:
        nz.append(x)
out["O_nonpeach_cols"] = [min(nz), max(nz)] if nz else None

# 6. hatch box borders: redness rows x 92..200 (left), y 170..220 — border = long horizontal run
for nm, (x0, x1) in {"Lhb": (94, 200), "Rhb": (752, 860)}.items():
    rows = {}
    for y in range(168, 222):
        cnt = sum(1 for x in range(x0, x1) if redness(px[x, y]) > 45)
        if cnt > (x1 - x0) * 0.5:
            rows[y] = cnt
    out[nm + "_border_rows"] = rows
    cols = {}
    for x in range(x0 - 6, x1 + 6):
        cnt = sum(1 for y in range(172, 218) if redness(px[x, y]) > 45)
        if cnt > 30:
            cols[x] = cnt
    out[nm + "_border_cols"] = cols

# 7. yellow container borders: green dashed border (92D050-ish) rows/cols
def is_dashgreen(p):
    r, g, b = p
    return 110 < r < 180 and g > 180 and b < 120 and (g - r) > 30
lb = [(x, y) for y in range(205, 395) for x in range(92, 195) if is_dashgreen(px[x, y])]
if lb:
    xs = [p[0] for p in lb]; ys = [p[1] for p in lb]
    out["Lcont_green_border"] = [min(xs), min(ys), max(xs), max(ys), len(lb)]
rb = [(x, y) for y in range(205, 395) for x in range(768, 872) if is_dashgreen(px[x, y])]
if rb:
    xs = [p[0] for p in rb]; ys = [p[1] for p in rb]
    out["Rcont_green_border"] = [min(xs), min(ys), max(xs), max(ys), len(rb)]

# 8. Z-row container: violet-pink fill F5C5FF extent + border
def is_zfill(p):
    r, g, b = p
    return r > 235 and 180 < g < 215 and b > 235
zf = [(x, y) for y in range(430, 510) for x in range(190, 560) if is_zfill(px[x, y])]
if zf:
    xs = [p[0] for p in zf]; ys = [p[1] for p in zf]
    out["Zrow_fill_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(zf)]

# 9. magenta Z2 cells extent
def is_mag2(p):
    r, g, b = p
    return r > 190 and b > 150 and g < 160 and (r - g) > 50
m2 = [(x, y) for y in range(445, 500) for x in range(260, 400) if is_mag2(px[x, y])]
if m2:
    xs = [p[0] for p in m2]; ys = [p[1] for p in m2]
    out["Z2_mag_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(m2)]

# 10. query line + q2 glyph: pale cells right of q2 text
row = []
for x in range(325, 360):
    p = px[x, 403]
    row.append((x, "%02X%02X%02X" % p))
out["q2_row403"] = row
# query vertical: redness per y at x 313..319
qv = []
for y in range(360, 400):
    m = max(redness(px[x, y]) for x in range(311, 322))
    if m > 35:
        qv.append((y, m))
out["query_vert"] = qv

# 11. W_k box fill + border color sample
out["wk_fill"] = "%02X%02X%02X" % px[210, 232]
out["wk_fill2"] = "%02X%02X%02X" % px[220, 242]
out["wk_border"] = "%02X%02X%02X" % px[199, 237]

# 12. W_v box borders: blue border color + box bboxes
def is_blueborder(p):
    r, g, b = p
    return b > 130 and (b - r) > 50 and g < 140
wb = [(x, y) for y in range(215, 385) for x in range(715, 775) if is_blueborder(px[x, y])]
rows = {}
for x, y in wb:
    rows.setdefault(y, []).append(x)
yg = []
ys = sorted(rows)
if ys:
    cur = [ys[0], ys[0]]
    for y in ys[1:]:
        if y - cur[1] <= 4: cur[1] = y
        else: yg.append(tuple(cur)); cur = [y, y]
    yg.append(tuple(cur))
out["wv_border_ygroups"] = yg
for a, b in yg:
    xs2 = [x for y in range(a, b + 1) for x in rows.get(y, [])]
    out.setdefault("wv_boxes", []).append([min(xs2), a, max(xs2), b])

# 13. black arrows: Y->Wk heads near x 181..199; Wk->K stubs x 229..238
def is_dark(p):
    return sum(p) < 330
for nm, (x0, x1) in {"arrL1": (180, 200), "arrL2": (228, 240), "arrR1": (758, 778), "arrR2": (752, 762)}.items():
    rr = {}
    for y in range(215, 380):
        cnt = sum(1 for x in range(x0, x1) if is_dark(px[x, y]))
        if cnt >= 2:
            rr[y] = cnt
    out[nm] = rr

print(json.dumps(out, indent=1))
