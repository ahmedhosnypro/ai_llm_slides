#!/usr/bin/env python3
"""Slide 055 geometry pass 3: nodes 3-4, pills, Z-row, hatch boxes, arrows, q2/Wq, V labels."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {}

def group(ys, gap=3):
    gs, cur = [], []
    for v in ys:
        if cur and v - cur[-1] > gap:
            gs.append((cur[0], cur[-1]))
            cur = []
        cur.append(v)
    if cur:
        gs.append((cur[0], cur[-1]))
    return gs

def near(p, c, tol):
    return all(abs(p[i] - c[i]) <= tol for i in range(3))

def is_red(p):
    r, g, b = p
    return r > 150 and g < 110 and b < 110 and (r - g) > 60

# ---- 1. all multiply nodes: red clusters x 520..690, y 210..390 ----
runs = []
for yy in range(210, 390):
    xs = [x for x in range(525, 690) if is_red(px[x, yy])]
    if len(xs) >= 3:
        runs.append((yy, min(xs), max(xs), len(xs)))
groups, cur = [], []
for r in runs:
    if cur and r[0] - cur[-1][0] > 5:
        if len(cur) >= 4:
            groups.append(cur)
        cur = []
    cur.append(r)
if len(cur) >= 4:
    groups.append(cur)
out["nodes3"] = []
for g in groups:
    y0, y1 = g[0][0], g[-1][0]
    x0 = min(r[1] for r in g); x1 = max(r[2] for r in g)
    out["nodes3"].append([x0, y0, x1, y1, "c=(%.1f,%.1f)" % ((x0 + x1) / 2, (y0 + y1) / 2)])

# ---- 2. pills: pale-yellow rounded rects in y 140..200 — find per-pill columns ----
def is_pill(p):
    r, g, b = p
    return r > 228 and g > 218 and 165 < b < 225
pill_cols = [x for x in range(250, 760) if sum(1 for y in range(148, 182) if is_pill(px[x, y])) > 8]
out["pill_col_groups"] = group(pill_cols, gap=4)
for a, b in group(pill_cols, gap=4):
    rows = [y for y in range(140, 200) if sum(1 for x in range(a, b + 1) if is_pill(px[x, y])) > (b - a) * 0.4]
    out.setdefault("pill_rows_per", []).append([a, b, (min(rows), max(rows)) if rows else None])
out["pill_fill_sample"] = ["%02X%02X%02X" % px[(a + b) // 2, 165] for a, b in group(pill_cols, gap=4)]

# ---- 3. Z-row container: pink fill F1ABCF with tol, count>8 per row ----
zp_rows = [y for y in range(430, 520) if sum(1 for x in range(200, 545) if near(px[x, y], (241, 171, 207), 30)) > 8]
out["zrow_rows3"] = group(zp_rows)
zp_cols = [x for x in range(180, 560) if sum(1 for y in range(450, 500) if near(px[x, y], (241, 171, 207), 30)) > 3]
out["zrow_cols3"] = [min(zp_cols), max(zp_cols)] if zp_cols else None
# cells inside: pale FFF3D0 columns
cell_cols = [x for x in range(200, 545) if sum(1 for y in range(455, 495) if near(px[x, y], (255, 243, 208), 22)) > 6]
out["zrow_cell_col_groups"] = group(cell_cols, gap=5)

# ---- 4. hatched boxes: white + red text "From Encoder Output" ----
def is_white(p):
    return all(v > 230 for v in p)
# left: scan y 150..215, x 60..260 for white center columns
lw = [(x, y) for y in range(150, 215) for x in range(60, 260) if is_white(px[x, y])]
if lw:
    xs = [p[0] for p in lw]; ys = [p[1] for p in lw]
    out["Lhatch_white_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(lw)]
rw = [(x, y) for y in range(150, 215) for x in range(700, 915) if is_white(px[x, y])]
if rw:
    xs = [p[0] for p in rw]; ys = [p[1] for p in rw]
    out["Rhatch_white_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(rw)]
# hatch border red rows: strong red in x 95..250, y 150..215
lh = [(x, y) for y in range(150, 215) for x in range(95, 255) if is_red(px[x, y])]
if lh:
    xs = [p[0] for p in lh]; ys = [p[1] for p in lh]
    out["Lhatch_red_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(lh)]
rh = [(x, y) for y in range(150, 215) for x in range(745, 900) if is_red(px[x, y])]
if rh:
    xs = [p[0] for p in rh]; ys = [p[1] for p in rh]
    out["Rhatch_red_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(rh)]

# ---- 5. red 3D block arrows at edges (wider red incl. darker) ----
def is_redw(p):
    r, g, b = p
    return r > 140 and g < 120 and b < 120 and (r - g) > 50
la = [(x, y) for y in range(160, 220) for x in range(58, 100) if is_redw(px[x, y])]
xs = [p[0] for p in la]; ys = [p[1] for p in la]
out["L3d_arrow"] = [min(xs), min(ys), max(xs), max(ys), len(la)] if la else None
ra = [(x, y) for y in range(160, 220) for x in range(872, 918) if is_redw(px[x, y])]
xs = [p[0] for p in ra]; ys = [p[1] for p in ra]
out["R3d_arrow"] = [min(xs), min(ys), max(xs), max(ys), len(ra)] if ra else None

# ---- 6. black thin arrows Y->Wk (x 182..196) and Wk->K (x 233..240) row centers ----
def is_dark(p):
    return sum(p) < 260
for name, (x0, x1) in {"arr_Y_Wk": (181, 197), "arr_Wk_K": (233, 245)}.items():
    rows = [y for y in range(210, 390) if sum(1 for x in range(x0, x1) if is_dark(px[x, y])) >= 2]
    out[name] = group(rows, gap=4)
for name, (x0, x1) in {"arr_Y_Wv": (762, 776), "arr_Wv_V": (757, 762)}.items():
    rows = [y for y in range(210, 390) if sum(1 for x in range(x0, x1) if is_dark(px[x, y])) >= 2]
    out[name] = group(rows, gap=4)

# ---- 7. q2 label + Wq box + query line ----
# red q2 text near x 300..330, y 390..415
q2 = [(x, y) for y in range(385, 420) for x in range(290, 345) if is_red(px[x, y])]
if q2:
    xs = [p[0] for p in q2]; ys = [p[1] for p in q2]
    out["q2_red_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(q2)]
# Wq white box: white-ish rect near x 310..350, y 415..450
def is_whitish(p):
    return all(v > 215 for v in p)
wq = [(x, y) for y in range(410, 460) for x in range(295, 370) if is_whitish(px[x, y])]
if wq:
    xs = [p[0] for p in wq]; ys = [p[1] for p in wq]
    out["Wq_white_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(wq)]
# query line: red vertical x 300..320, y 370..395
ql = [(x, y) for y in range(365, 400) for x in range(295, 325) if is_red(px[x, y])]
if ql:
    xs = [p[0] for p in ql]; ys = [p[1] for p in ql]
    out["query_line_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(ql)]

# ---- 8. V labels (red) right side x 640..700 ----
vrows = []
for yy in range(210, 390):
    xs = [x for x in range(635, 710) if is_red(px[x, yy])]
    if len(xs) >= 2:
        vrows.append(yy)
out["V_label_rows"] = group(vrows, gap=6)

# ---- 9. green block arrow (00B050) between Sigma and O ----
def is_garr(p):
    r, g, b = p
    return g > 120 and r < 100 and b < 130 and (g - r) > 40
ga = [(x, y) for y in range(140, 195) for x in range(560, 650) if is_garr(px[x, y])]
if ga:
    xs = [p[0] for p in ga]; ys = [p[1] for p in ga]
    out["green_arrow_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(ga)]

# ---- 10. thick red up-arrow below Z row (x 280..330, y 495..520) ----
ta = [(x, y) for y in range(490, 522) for x in range(270, 340) if is_redw(px[x, y])]
if ta:
    xs = [p[0] for p in ta]; ys = [p[1] for p in ta]
    out["Z_up_arrow_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(ta)]

# ---- 11. decoder caption magenta + white arrow ----
def is_mag(p):
    r, g, b = p
    return r > 150 and b > 150 and g < 120
mc = [(x, y) for y in range(440, 510) for x in range(500, 720) if is_mag(px[x, y])]
if mc:
    xs = [p[0] for p in mc]; ys = [p[1] for p in mc]
    out["caption_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(mc)]
# white arrow right of caption
wa = [(x, y) for y in range(455, 500) for x in range(655, 730) if is_white(px[x, y])]
if wa:
    xs = [p[0] for p in wa]; ys = [p[1] for p in wa]
    out["white_arrow_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(wa)]

# ---- 12. red mesh lines inside dot product box (thin red diagonals) ----
mesh = [(x, y) for y in range(220, 380) for x in range(295, 400) if is_red(px[x, y])]
if mesh:
    xs = [p[0] for p in mesh]; ys = [p[1] for p in mesh]
    out["mesh_red_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(mesh)]
    # columns histogram to find the K->dot corridor
    from collections import Counter
    ch = Counter(p[0] for p in mesh)
    out["mesh_col_hist_top"] = sorted(ch.items())[:12]

# ---- 13. K.q label top-right of dotprod box ----
kq = [(x, y) for y in range(180, 215) for x in range(400, 460) if is_red(px[x, y])]
if kq:
    xs = [p[0] for p in kq]; ys = [p[1] for p in kq]
    out["Kq_label_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(kq)]

# ---- 14. fraction K.q/sqrt(d) region: red ink above scaling col ----
fr = [(x, y) for y in range(180, 240) for x in range(408, 460) if is_red(px[x, y])]
if fr:
    xs = [p[0] for p in fr]; ys = [p[1] for p in fr]
    out["fraction_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(fr)]

# ---- 15. scaling col exact edges: pink F0BCB1..FFD4CA band ----
def is_pinkband(p):
    r, g, b = p
    return r > 235 and 165 < g < 225 and 160 < b < 220
sccols = [x for x in range(390, 470) if sum(1 for y in range(250, 350) if is_pinkband(px[x, y])) > 40]
scrows = [y for y in range(180, 400) if sum(1 for x in range(410, 445) if is_pinkband(px[x, y])) > 12]
out["scaling_cols2"] = [min(sccols), max(sccols)] if sccols else None
out["scaling_rows2"] = group(scrows, gap=6)

# ---- 16. softmax col exact edges ----
smcols = [x for x in range(470, 545) if sum(1 for y in range(230, 350) if near(px[x, y], (248, 222, 251), 14)) > 40]
smrows = [y for y in range(180, 400) if sum(1 for x in range(488, 514) if near(px[x, y], (248, 222, 251), 14)) > 12]
out["softmax_cols2"] = [min(smcols), max(smcols)] if smcols else None
out["softmax_rows2"] = group(smrows, gap=6)

# ---- 17. W_k boxes: bright green-yellow fill; scan x 190..245 ----
def is_wkg(p):
    r, g, b = p
    return g > 190 and b < 150 and (g - b) > 60 and r > 130
wk = [(x, y) for y in range(210, 390) for x in range(188, 245) if is_wkg(px[x, y])]
if wk:
    xs = [p[0] for p in wk]; ys = [p[1] for p in wk]
    out["Wk_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(wk)]
    wkr = sorted(set(ys))
    out["Wk_row_groups"] = group(wkr, gap=4)
    wkc = sorted(set(xs))
    out["Wk_col_groups"] = group(wkc, gap=4)

print(json.dumps(out, indent=1))
