#!/usr/bin/env python3
"""Slide 055: zoomed crops for the batched vision structural read + remaining PIL scans."""
from PIL import Image
import json, os

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide055/crops"
os.makedirs(OUT, exist_ok=True)
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {}

CROPS = {
    "c1_title":      (150, 45, 850, 100),
    "c2_leftgroup":  (55, 140, 290, 400),
    "c3_dotprod":    (270, 150, 470, 400),
    "c4_scaling_softmax": (400, 150, 560, 400),
    "c5_sigma_O":    (520, 100, 720, 230),
    "c6_rightgroup": (620, 140, 918, 400),
    "c7_query_zrow": (180, 380, 560, 525),
    "c8_caption_legend": (500, 420, 918, 515),
}
for name, (x0, y0, x1, y1) in CROPS.items():
    c = img.crop((x0, y0, x1, y1))
    z = 3
    c = c.resize((c.width * z, c.height * z), Image.LANCZOS)
    p = f"{OUT}/{name}.png"
    c.save(p)
    out[name] = {"crop_box": [x0, y0, x1, y1], "file": p}

# ---- remaining targeted PIL scans ----
def near(p, c, tol):
    return all(abs(p[i] - c[i]) <= tol for i in range(3))
def is_red(p):
    r, g, b = p
    return r > 150 and g < 110 and b < 110 and (r - g) > 60

# 1. K.q label rescan x 355..420, y 180..212
kq = [(x, y) for y in range(180, 212) for x in range(355, 420) if is_red(px[x, y])]
if kq:
    xs = [p[0] for p in kq]; ys = [p[1] for p in kq]
    out["Kq_label_bbox2"] = [min(xs), min(ys), max(xs), max(ys), len(kq)]

# 2. fraction region precise: x 408..465, y 180..240, EXCLUDING column text (y<218)
fr = [(x, y) for y in range(180, 218) for x in range(405, 470) if is_red(px[x, y])]
if fr:
    xs = [p[0] for p in fr]; ys = [p[1] for p in fr]
    out["fraction_bbox2"] = [min(xs), min(ys), max(xs), max(ys), len(fr)]

# 3. tan box right edge at text-free row y=372..384
def is_tan(p):
    return near(p, (219, 203, 187), 14)
tan_cols_372 = [x for x in range(280, 430) if sum(1 for y in range(366, 384) if is_tan(px[x, y])) > 8]
out["tan_cols_y366_384"] = [min(tan_cols_372), max(tan_cols_372)] if tan_cols_372 else None
tan_rows_x320 = [y for y in range(170, 410) if is_tan(px[320, y])]
out["tan_rows_at_x320"] = [min(tan_rows_x320), max(tan_rows_x320)] if tan_rows_x320 else None

# 4. K->dot corridor shafts: red ink x 268..306 at dot rows
for name, (y0, y1) in {"corr_dot1": (232, 243), "corr_dot2": (271, 282), "corr_dot3": (310, 321), "corr_dot4": (353, 365)}.items():
    xs = [x for x in range(266, 310) for y in range(y0, y1) if is_red(px[x, y])]
    out[name] = [min(xs), max(xs), len(xs)] if xs else None

# 5. V labels x-extents at their rows
vgs = [(224, 232), (264, 272), (303, 311), (346, 354)]
vout = []
for (a, b) in vgs:
    xs = [x for x in range(600, 730) for y in range(a, b) if is_red(px[x, y])]
    vout.append([min(xs), max(xs), len(xs)] if xs else None)
out["V_label_xext"] = vout

# 6. V connector lines from W_v boxes to nodes: red/dark ink x 700..760 at node rows
def is_dark(p):
    return sum(p) < 300
vlines = []
for yy in [237, 277, 316, 359]:
    seg = [(x, "%s" % ("R" if is_red(px[x, yy]) else ("D" if is_dark(px[x, yy]) else "."))) for x in range(660, 770)]
    reds = [x for x, t in seg if t == "R"]
    darks = [x for x, t in seg if t == "D"]
    vlines.append({"y": yy, "red_x": [min(reds), max(reds)] if reds else None, "dark_x": [min(darks), max(darks)] if darks else None})
out["V_line_scan"] = vlines

# 7. similarity pill: sample colors around expected area
out["pill_samples"] = {}
for nm, (xx, yy) in {"sim_1": (320, 165), "sim_2": (340, 168), "prob_1": (480, 165), "prob_2": (500, 168),
                     "wsum_1": (650, 165), "wsum_2": (670, 168), "above_sim": (320, 150), "below_sim": (320, 180)}.items():
    out["pill_samples"][nm] = "%02X%02X%02X" % px[xx, yy]
# find pill fills: pale yellow columns in y 150..180 that are NOT peach (b>210)
def is_paleY(p):
    r, g, b = p
    return r > 235 and g > 230 and b > 200 and b < 245
pycols = [x for x in range(260, 760) if sum(1 for y in range(152, 180) if is_paleY(px[x, y])) > 10]
def group(xs, gap=4):
    gs, cur = [], []
    for v in xs:
        if cur and v - cur[-1] > gap:
            gs.append((cur[0], cur[-1]))
            cur = []
        cur.append(v)
    if cur:
        gs.append((cur[0], cur[-1]))
    return gs
pg = group(pycols)
out["paleY_col_groups"] = pg
rows_per = []
for a, b in pg:
    rr = [y for y in range(140, 195) if sum(1 for x in range(a, b + 1) if is_paleY(px[x, y])) > (b - a) * 0.5]
    rows_per.append([a, b, (min(rr), max(rr)) if rr else None, "%02X%02X%02X" % px[(a + b) // 2, 165]])
out["paleY_details"] = rows_per

# 8. Z-row container full extent + fill
zp_rows = [y for y in range(430, 522) if sum(1 for x in range(190, 700, 2) if near(px[x, y], (241, 171, 207), 32)) > 30]
out["zrow_rows4"] = [min(zp_rows), max(zp_rows)] if zp_rows else None
zp_cols = [x for x in range(180, 700) if sum(1 for y in range(445, 500) if near(px[x, y], (241, 171, 207), 32)) > 8]
out["zrow_cols4"] = [min(zp_cols), max(zp_cols)] if zp_cols else None
# Z2 highlight: deeper pink E6A9D5 columns
z2 = [x for x in range(190, 700) if sum(1 for y in range(450, 495) if near(px[x, y], (230, 169, 213), 22)) > 8]
out["z2_col_groups"] = group(z2, gap=5)
# dashed red border on Z2: red ink y 440..500 x 260..380
z2red = [(x, y) for y in range(438, 500) for x in range(255, 385) if is_red(px[x, y])]
if z2red:
    xs = [p[0] for p in z2red]; ys = [p[1] for p in z2red]
    out["z2_red_dash_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(z2red)]

# 9. Z up arrow precise: red x 285..330, y 495..520
ta = [(x, y) for y in range(494, 521) for x in range(280, 340) if is_red(px[x, y])]
if ta:
    xs = [p[0] for p in ta]; ys = [p[1] for p in ta]
    out["Z_arrow_precise"] = [min(xs), min(ys), max(xs), max(ys), len(ta)]

# 10. legend contents: ink columns inside legend box (736..899, 425..505)
lg_red = [(x, y) for y in range(420, 512) for x in range(730, 905) if is_red(px[x, y])]
if lg_red:
    xs = [p[0] for p in lg_red]; ys = [p[1] for p in lg_red]
    out["legend_red_ink"] = [min(xs), min(ys), max(xs), max(ys), len(lg_red)]
def is_navy(p):
    r, g, b = p
    return b > 110 and r < 110 and (b - r) > 40 and g < 110
lg_navy = [(x, y) for y in range(420, 512) for x in range(730, 905) if is_navy(px[x, y])]
if lg_navy:
    xs = [p[0] for p in lg_navy]; ys = [p[1] for p in lg_navy]
    out["legend_navy_ink"] = [min(xs), min(ys), max(xs), max(ys), len(lg_navy)]
lg_dark = [(x, y) for y in range(420, 512) for x in range(730, 905) if sum(px[x, y]) < 260]
if lg_dark:
    xs = [p[0] for p in lg_dark]; ys = [p[1] for p in lg_dark]
    out["legend_dark_ink"] = [min(xs), min(ys), max(xs), max(ys), len(lg_dark)]

# 11. O box + flanking cells: green fill A4C6A2-ish rows/cols
def is_og(p):
    r, g, b = p
    return 140 < r < 190 and 175 < g < 215 and 130 < b < 180 and g > r
og = [(x, y) for y in range(110, 165) for x in range(540, 700) if is_og(px[x, y])]
if og:
    xs = [p[0] for p in og]; ys = [p[1] for p in og]
    out["O_box_bbox"] = [min(xs), min(ys), max(xs), max(ys), len(og)]

# 12. hatched box borders (red rectangle outline + hatch) — red rows/cols in left hatch zone
lh_rows = {}
for yy in range(160, 215):
    xs = [x for x in range(60, 265) if is_red(px[x, yy])]
    if len(xs) >= 3:
        lh_rows[yy] = (min(xs), max(xs), len(xs))
out["Lhatch_red_rows"] = {str(k): v for k, v in lh_rows.items() if k % 2 == 0}

# 13. letterbox precise
out["letterbox_top"] = next((y for y in range(505, 540) if sum(1 for x in range(0, W, 4) if sum(px[x, y]) < 150) > 100), None)

# 14. softmax column top/bottom + scaling column: fills
out["scaling_fill_sample"] = "%02X%02X%02X" % px[425, 300]
out["scaling_fill_sample2"] = "%02X%02X%02X" % px[430, 250]
out["softmax_fill_sample"] = "%02X%02X%02X" % px[500, 350]
out["softmax_fill_sample2"] = "%02X%02X%02X" % px[495, 230]

# 15. title red spans: red ink in title rows
def is_redt(p):
    r, g, b = p
    return r > 150 and g < 100 and b < 100 and (r - g) > 60
t1r = [(x, y) for y in range(58, 72) for x in range(150, 850) if is_redt(px[x, y])]
if t1r:
    xs = sorted(p[0] for p in t1r)
    out["title1_red_x_groups"] = group(xs, gap=8)
t2r = [(x, y) for y in range(79, 95) for x in range(150, 850) if is_redt(px[x, y])]
if t2r:
    xs = sorted(p[0] for p in t2r)
    out["title2_red_x_groups"] = group(xs, gap=8)

print(json.dumps(out, indent=1))
