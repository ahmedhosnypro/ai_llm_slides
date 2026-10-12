#!/usr/bin/env python3
"""Slide 055: precise geometry — color samples at key points + row/col profiles per element."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {}

def hexs(p):
    return "%02X%02X%02X" % p

# ---- 1. point samples ----
samples = {
    "gray_panel(50,150)": (50, 150),
    "peach_panel_center(200,140)": (200, 140),
    "peach_panel_top_row(200,95)": (200, 95),
    "peach_panel(200,100)": (200, 100),
    "peach_panel(200,105)": (200, 105),
    "peach_panel(200,110)": (200, 110),
    "Wk_box_1(175,232)": (175, 232),
    "Wk_box_1(180,235)": (180, 235),
    "Kstrip_1(245,237)": (245, 237),
    "Kstrip_cell(250,237)": (250, 237),
    "dotprod_box(300,250)": (300, 250),
    "dotprod_box(300,300)": (300, 300),
    "scaling_col(400,280)": (400, 280),
    "scaling_col(398,300)": (398, 300),
    "softmax_col(500,280)": (500, 280),
    "softmax_col(505,300)": (505, 300),
    "softmax_col(515,300)": (515, 300),
    "sigma_box(560,200)": (560, 200),
    "sigma_box(600,200)": (600, 200),
    "sigma_box(640,205)": (640, 205),
    "O_box(600,130)": (600, 130),
    "O_box(610,140)": (610, 140),
    "Wv_box(735,240)": (735, 240),
    "Wv_box(740,245)": (740, 245),
    "Wq_box(330,430)": (330, 430),
    "Wq_box(335,435)": (335, 435),
    "zrow_cell(240,470)": (240, 470),
    "zrow_cell(310,470)": (310, 470),
    "zrow_Z2(320,470)": (320, 470),
    "legend_bg(760,440)": (760, 440),
    "legend_bg(800,450)": (800, 450),
    "hatch_left(120,180)": (120, 180),
    "hatch_left(150,185)": (150, 185),
    "yellow_container_L(140,240)": (140, 240),
    "node_zone(555,238)": (555, 238),
    "node_zone(558,275)": (558, 275),
    "arrow_red_left(75,180)": (75, 180),
}
out["samples"] = {k: hexs(px[x, y]) for k, (x, y) in samples.items()}

# ---- 2. peach panel edges: strict peach col/row profiles ----
def is_peach(p):
    r, g, b = p
    return r > 240 and 215 < g < 245 and 175 < b < 215
col_hits = [x for x in range(0, W) if sum(1 for y in range(120, 500) if is_peach(px[x, y])) > 100]
row_hits = [y for y in range(60, 540) if sum(1 for x in range(80, 880) if is_peach(px[x, y])) > 200]
out["peach_cols"] = [min(col_hits), max(col_hits)] if col_hits else None
out["peach_rows"] = [min(row_hits), max(row_hits)] if row_hits else None

# ---- 3. dot product box: tan profile ----
def is_tan(p):
    r, g, b = p
    return 160 < r < 200 and 150 < g < 185 and 130 < b < 165 and r >= g >= b
tcols = [x for x in range(260, 420) if sum(1 for y in range(210, 380) if is_tan(px[x, y])) > 60]
trows = [y for y in range(170, 420) if sum(1 for x in range(300, 360) if is_tan(px[x, y])) > 25]
out["dotprod_cols"] = [min(tcols), max(tcols)] if tcols else None
out["dotprod_rows"] = [min(trows), max(trows)] if trows else None

# ---- 4. scaling + softmax columns ----
def is_pinkc(p):
    r, g, b = p
    return r > 235 and 140 < g < 200 and 140 < b < 200
pcols = [x for x in range(360, 480) if sum(1 for y in range(240, 360) if is_pinkc(px[x, y])) > 60]
prows = [y for y in range(170, 420) if sum(1 for x in range(390, 430) if is_pinkc(px[x, y])) > 20]
out["scaling_cols"] = [min(pcols), max(pcols)] if pcols else None
out["scaling_rows"] = [min(prows), max(prows)] if prows else None

def is_violet(p):
    r, g, b = p
    return 185 < r < 235 and 135 < g < 185 and b > 225
vcols = [x for x in range(460, 560) if sum(1 for y in range(240, 360) if is_violet(px[x, y])) > 60]
vrows = [y for y in range(170, 420) if sum(1 for x in range(480, 530) if is_violet(px[x, y])) > 20]
out["softmax_cols"] = [min(vcols), max(vcols)] if vcols else None
out["softmax_rows"] = [min(vrows), max(vrows)] if vrows else None

# ---- 5. sigma box (light blue) ----
def is_sigblue(p):
    r, g, b = p
    return 175 < r < 215 and 210 < g < 240 and b > 235
scols = [x for x in range(480, 720) if sum(1 for y in range(195, 225) if is_sigblue(px[x, y])) > 15]
srows = [y for y in range(170, 250) if sum(1 for x in range(520, 700) if is_sigblue(px[x, y])) > 60]
out["sigma_cols"] = [min(scols), max(scols)] if scols else None
out["sigma_rows"] = [min(srows), max(srows)] if srows else None

# ---- 6. O output box (green fill + cells) ----
def is_ogreen(p):
    r, g, b = p
    return 120 < r < 190 and 170 < g < 215 and 120 < b < 175 and g > r and g > b
ocols = [x for x in range(520, 700) if sum(1 for y in range(115, 160) if is_ogreen(px[x, y])) > 8]
orows = [y for y in range(100, 180) if sum(1 for x in range(540, 680) if is_ogreen(px[x, y])) > 25]
out["O_cols"] = [min(ocols), max(ocols)] if ocols else None
out["O_rows"] = [min(orows), max(orows)] if orows else None

# ---- 7. dots (navy) full scan ----
def is_navy(p):
    r, g, b = p
    return b > 95 and r < 100 and g < 100 and (b - r) > 50
dots = []
y = 200
runs = []
for yy in range(200, 400):
    xs = [x for x in range(280, 420) if is_navy(px[x, yy])]
    if len(xs) >= 4:
        runs.append((yy, min(xs), max(xs), len(xs)))
# group consecutive rows into dots
groups = []
cur = []
for r in runs:
    if cur and r[0] - cur[-1][0] > 3:
        if len(cur) >= 3:
            groups.append(cur)
        cur = []
    cur.append(r)
if len(cur) >= 3:
    groups.append(cur)
out["dots"] = []
for g in groups:
    y0, y1 = g[0][0], g[-1][0]
    x0 = min(r[1] for r in g); x1 = max(r[2] for r in g)
    out["dots"].append([x0, y0, x1, y1, "c=(%.1f,%.1f)" % ((x0 + x1) / 2, (y0 + y1) / 2)])

# ---- 8. multiply nodes (red circle + x): scan for red ring clusters x 500..600 ----
def is_red(p):
    r, g, b = p
    return r > 150 and g < 90 and b < 90 and (r - g) > 70
node_rows = {}
for yy in range(200, 400):
    xs = [x for x in range(520, 610) if is_red(px[x, yy])]
    if len(xs) >= 3:
        node_rows[yy] = (min(xs), max(xs), len(xs))
out["node_rows_sample"] = {str(k): v for k, v in list(node_rows.items())[::2]}

# ---- 9. W_k / W_v / K rows: green + blue box y-tops ----
def is_wk_green(p):
    r, g, b = p
    return 170 < r < 225 and 215 < g < 245 and 170 < b < 215 and g > r and g > b
wkcols = [x for x in range(150, 260) if sum(1 for y in range(200, 400) if is_wk_green(px[x, y])) > 40]
out["wk_cols"] = [min(wkcols), max(wkcols)] if wkcols else None
wkrows = [y for y in range(200, 400) if sum(1 for x in range(160, 210) if is_wk_green(px[x, y])) > 20]
# group
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
out["wk_row_groups"] = group_ys(wkrows)

def is_wv_blue(p):
    r, g, b = p
    return 170 < r < 215 and 220 < g < 245 and b > 235
wvcols = [x for x in range(690, 790) if sum(1 for y in range(200, 400) if is_wv_blue(px[x, y])) > 40]
out["wv_cols"] = [min(wvcols), max(wvcols)] if wvcols else None
wvrows = [y for y in range(200, 400) if sum(1 for x in range(700, 760) if is_wv_blue(px[x, y])) > 20]
out["wv_row_groups"] = group_ys(wvrows)

# ---- 10. yellow containers exact + inner row strips ----
def is_yellow(p):
    r, g, b = p
    return r > 225 and g > 215 and b < 175
lycols = [x for x in range(60, 220) if sum(1 for y in range(210, 390) if is_yellow(px[x, y])) > 50]
lyrows = [y for y in range(200, 400) if sum(1 for x in range(95, 190) if is_yellow(px[x, y])) > 30]
out["Lcont_cols"] = [min(lycols), max(lycols)] if lycols else None
out["Lcont_row_groups"] = group_ys(lyrows)
rycols = [x for x in range(740, 900) if sum(1 for y in range(210, 390) if is_yellow(px[x, y])) > 50]
ryrows = [y for y in range(200, 400) if sum(1 for x in range(780, 870) if is_yellow(px[x, y])) > 30]
out["Rcont_cols"] = [min(rycols), max(rycols)] if rycols else None
out["Rcont_row_groups"] = group_ys(ryrows)

# ---- 11. Z row container (pink) ----
def is_zpink(p):
    r, g, b = p
    return r > 235 and 130 < g < 190 and 165 < b < 220
zpcols = [x for x in range(180, 560) if sum(1 for y in range(440, 510) if is_zpink(px[x, y])) > 20]
zprows = [y for y in range(420, 530) if sum(1 for x in range(200, 540) if is_zpink(px[x, y])) > 60]
out["zrow_cols"] = [min(zpcols), max(zpcols)] if zpcols else None
out["zrow_rows"] = [min(zprows), max(zprows)] if zprows else None

# ---- 12. legend pale green ----
def is_paleg(p):
    r, g, b = p
    return 185 < r < 235 and g > 225 and 185 < b < 235
lgcols = [x for x in range(700, 920) if sum(1 for y in range(410, 510) if is_paleg(px[x, y])) > 30]
lgrows = [y for y in range(400, 520) if sum(1 for x in range(730, 900) if is_paleg(px[x, y])) > 40]
out["legend_cols"] = [min(lgcols), max(lgcols)] if lgcols else None
out["legend_rows"] = [min(lgrows), max(lgrows)] if lgrows else None

# ---- 13. hatched From Encoder Output boxes: white center + red hatch ----
def is_white(p):
    return all(v > 235 for v in p)
hwcols = [x for x in range(60, 260) if sum(1 for y in range(160, 210) if is_white(px[x, y])) > 25]
hwrows = [y for y in range(150, 220) if sum(1 for x in range(80, 250) if is_white(px[x, y])) > 60]
out["Lhatch_cols"] = [min(hwcols), max(hwcols)] if hwcols else None
out["Lhatch_rows"] = [min(hwrows), max(hwrows)] if hwrows else None
hw2cols = [x for x in range(700, 920) if sum(1 for y in range(160, 210) if is_white(px[x, y])) > 25]
hw2rows = [y for y in range(150, 220) if sum(1 for x in range(720, 910) if is_white(px[x, y])) > 60]
out["Rhatch_cols"] = [min(hw2cols), max(hw2cols)] if hw2cols else None
out["Rhatch_rows"] = [min(hw2rows), max(hw2rows)] if hw2rows else None

print(json.dumps(out, indent=1))
