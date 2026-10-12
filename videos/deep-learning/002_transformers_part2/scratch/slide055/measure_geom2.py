#!/usr/bin/env python3
"""Slide 055 geometry pass 2: calibrated profiles per element + zoom crops."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {}

def group_ys(ys, gap=3):
    gs, cur = [], []
    for v in ys:
        if cur and v - cur[-1] > gap:
            gs.append((cur[0], cur[-1]))
            cur = []
        cur.append(v)
    if cur:
        gs.append((cur[0], cur[-1]))
    return gs

def group_xs(xs, gap=3):
    return group_ys(sorted(xs), gap)

def near(p, c, tol):
    return all(abs(p[i] - c[i]) <= tol for i in range(3))

# ---- 1. peach panel precise edges (fill F7E2CD core) ----
peach_rows = [y for y in range(60, 540) if sum(1 for x in range(90, 870, 2) if near(px[x, y], (247, 226, 205), 14)) > 300]
out["peach_rows_strict"] = [min(peach_rows), max(peach_rows)] if peach_rows else None
y_mid = 300
peach_cols = [x for x in range(40, 940) if near(px[x, y_mid], (247, 226, 205), 14)]
out["peach_cols_at_y300"] = [min(peach_cols), max(peach_cols)] if peach_cols else None
# top edge scan at x=200: first peach y
col200 = [y for y in range(80, 130) if near(px[200, y], (247, 226, 205), 18)]
out["peach_top_at_x200"] = col200[:6]
# bottom edge at x=200
col200b = [y for y in range(480, 520) if near(px[200, y], (247, 226, 205), 18)]
out["peach_bottom_at_x200"] = col200b[-6:] if col200b else None
# left edge at y=300
row300 = [x for x in range(50, 110) if near(px[x, 300], (247, 226, 205), 18)]
out["peach_left_at_y300"] = row300[:6]
row300r = [x for x in range(860, 920) if near(px[x, 300], (247, 226, 205), 18)]
out["peach_right_at_y300"] = row300r[-6:] if row300r else None

# ---- 2. scaling column: sample the actual fill left of text ----
for xx in range(378, 420, 2):
    out.setdefault("scaling_row280", []).append((xx, "%02X%02X%02X" % px[xx, 280]))
for xx in range(378, 420, 2):
    out.setdefault("scaling_row330", []).append((xx, "%02X%02X%02X" % px[xx, 330]))
# column vertical extent at x=395
out["scaling_colvert_x395"] = [y for y in range(180, 400) if near(px[395, y], (255, 194, 181), 30)][:4] + ["..."] + [y for y in range(180, 400) if near(px[395, y], (255, 194, 181), 30)][-4:]

# ---- 3. softmax column ----
for xx in range(480, 540, 2):
    out.setdefault("softmax_row340", []).append((xx, "%02X%02X%02X" % px[xx, 340]))
out["softmax_colvert_x520"] = [y for y in range(180, 400) if near(px[520, y], (254, 182, 255), 40)][:4] + ["..."] + [y for y in range(180, 400) if near(px[520, y], (254, 182, 255), 40)][-4:]

# ---- 4. dot product box: fill DBCBBB ----
dcols = [x for x in range(260, 420) if sum(1 for y in range(220, 370) if near(px[x, y], (219, 203, 187), 16)) > 60]
drows = [y for y in range(170, 420) if sum(1 for x in range(290, 360) if near(px[x, y], (219, 203, 187), 16)) > 25]
out["dotprod_cols"] = [min(dcols), max(dcols)] if dcols else None
out["dotprod_rows"] = group_ys(drows)

# ---- 5. sigma box: EAFEFC-ish ----
scols = [x for x in range(470, 720) if sum(1 for y in range(190, 220) if near(px[x, y], (234, 254, 252), 12)) > 12]
srows = [y for y in range(170, 260) if sum(1 for x in range(500, 700) if near(px[x, y], (234, 254, 252), 12)) > 60]
out["sigma_cols"] = [min(scols), max(scols)] if scols else None
out["sigma_rows"] = [min(srows), max(srows)] if srows else None

# ---- 6. O box greens ----
ogreen_rows = [y for y in range(100, 180) if sum(1 for x in range(540, 680) if near(px[x, y], (155, 195, 145), 45) and px[x, y][1] > px[x, y][0]) > 30]
out["O_rows2"] = group_ys(ogreen_rows)

# ---- 7. W_k boxes (yellow-green F5FF09 core / DCE2A4) ----
def is_wk(p):
    r, g, b = p
    return g > 200 and b < 120 and r > 140
wkcols = [x for x in range(150, 280) if sum(1 for y in range(210, 390) if is_wk(px[x, y])) > 30]
out["wk_cols2"] = [min(wkcols), max(wkcols)] if wkcols else None
wkrows = [y for y in range(200, 400) if sum(1 for x in range(195, 235) if is_wk(px[x, y])) > 15]
out["wk_row_groups2"] = group_ys(wkrows)

# ---- 8. W_v boxes (light blue C1F4ED w/ blue border) ----
def is_wv(p):
    r, g, b = p
    return b > 225 and g > 220 and r < 215
wvcols = [x for x in range(680, 800) if sum(1 for y in range(210, 390) if is_wv(px[x, y])) > 30]
out["wv_cols2"] = [min(wvcols), max(wvcols)] if wvcols else None
wvrows = [y for y in range(200, 400) if sum(1 for x in range(720, 770) if is_wv(px[x, y])) > 15]
out["wv_row_groups2"] = group_ys(wvrows)

# ---- 9. K strips: striped cells at x~240..270; profile rows by non-peach ink in x 238..268 ----
kstrip_rows = []
for y in range(210, 390):
    cnt = sum(1 for x in range(238, 270) if not near(px[x, y], (247, 226, 205), 20))
    if cnt > 12:
        kstrip_rows.append(y)
out["kstrip_row_groups"] = group_ys(kstrip_rows)

# ---- 10. Z row: pink container fill F1ABCF-ish + cells ----
zp_rows = [y for y in range(430, 520) if sum(1 for x in range(200, 540) if near(px[x, y], (241, 171, 207), 25)) > 60]
out["zrow_rows2"] = [min(zp_rows), max(zp_rows)] if zp_rows else None
zp_cols = [x for x in range(180, 560) if sum(1 for y in range(450, 495) if near(px[x, y], (241, 171, 207), 25)) > 10]
out["zrow_cols2"] = [min(zp_cols), max(zp_cols)] if zp_cols else None

# ---- 11. legend box: fill F8FEDA / EDF3CF ----
lg_rows = [y for y in range(400, 520) if sum(1 for x in range(730, 905) if near(px[x, y], (248, 254, 218), 16)) > 60]
out["legend_rows2"] = [min(lg_rows), max(lg_rows)] if lg_rows else None
lg_cols = [x for x in range(700, 920) if sum(1 for y in range(430, 500) if near(px[x, y], (248, 254, 218), 16)) > 20]
out["legend_cols2"] = [min(lg_cols), max(lg_cols)] if lg_cols else None

# ---- 12. hatched boxes: white centers ----
def is_white(p):
    return all(v > 232 for v in p)
lw_cols = [x for x in range(60, 260) if sum(1 for y in range(165, 205) if is_white(px[x, y])) > 20]
lw_rows = [y for y in range(150, 215) if sum(1 for x in range(85, 250) if is_white(px[x, y])) > 40]
out["Lhatch_cols2"] = [min(lw_cols), max(lw_cols)] if lw_cols else None
out["Lhatch_rows2"] = [min(lw_rows), max(lw_rows)] if lw_rows else None
rw_cols = [x for x in range(700, 920) if sum(1 for y in range(165, 205) if is_white(px[x, y])) > 20]
rw_rows = [y for y in range(150, 215) if sum(1 for x in range(740, 915) if is_white(px[x, y])) > 40]
out["Rhatch_cols2"] = [min(rw_cols), max(rw_cols)] if rw_cols else None
out["Rhatch_rows2"] = [min(rw_rows), max(rw_rows)] if rw_rows else None

# ---- 13. red 3D arrows at edges: strong red clusters near x 60..95 and 880..915, y 160..210 ----
def is_red(p):
    r, g, b = p
    return r > 160 and g < 100 and b < 100 and (r - g) > 80
la = [(x, y) for y in range(150, 220) for x in range(58, 100) if is_red(px[x, y])]
if la:
    xs = [p[0] for p in la]; ys = [p[1] for p in la]
    out["Lred_arrow_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(la)]
ra = [(x, y) for y in range(150, 220) for x in range(875, 918) if is_red(px[x, y])]
if ra:
    xs = [p[0] for p in ra]; ys = [p[1] for p in ra]
    out["Rred_arrow_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(ra)]

# ---- 14. all 4 multiply nodes: red ring clusters, x 520..620 ----
nodes = []
for yy in range(210, 390):
    xs = [x for x in range(525, 615) if is_red(px[x, yy])]
    if len(xs) >= 3:
        nodes.append((yy, min(xs), max(xs), len(xs)))
groups = []
cur = []
for r in nodes:
    if cur and r[0] - cur[-1][0] > 5:
        if len(cur) >= 4:
            groups.append(cur)
        cur = []
    cur.append(r)
if len(cur) >= 4:
    groups.append(cur)
out["nodes"] = []
for g in groups:
    y0, y1 = g[0][0], g[-1][0]
    x0 = min(r[1] for r in g); x1 = max(r[2] for r in g)
    out["nodes"].append([x0, y0, x1, y1, "c=(%.1f,%.1f)" % ((x0 + x1) / 2, (y0 + y1) / 2)])

# ---- 15. title lines: dark+red ink rows ----
def ink(p):
    return sum(p) < 300
t_rows = [y for y in range(40, 105) if sum(1 for x in range(150, 830) if ink(px[x, y])) > 8]
out["title_row_groups"] = group_ys(t_rows)
for i, (a, b) in enumerate(group_ys(t_rows)):
    xs = [x for x in range(150, 830) for yy in range(a, b + 1) if ink(px[x, yy])]
    out[f"title_L{i+1}_x"] = [min(xs), max(xs)]

# ---- 16. Similarity / Probabilities / Weighted SUM pills: pale yellow F0F0D8-ish? sample ----
for name, (xx, yy) in {"sim_pill": (300, 165), "prob_pill": (490, 165), "wsum_pill": (640, 165)}.items():
    out[f"{name}_sample"] = "%02X%02X%02X" % px[xx, yy]
# pill rows: pale-yellow in y 150..185
def is_pill(p):
    r, g, b = p
    return r > 225 and g > 220 and 175 < b < 230
pill_rows = [y for y in range(140, 200) if sum(1 for x in range(250, 720) if is_pill(px[x, y])) > 20]
out["pill_rows"] = group_ys(pill_rows)

print(json.dumps(out, indent=1))
