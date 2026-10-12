#!/usr/bin/env python3
"""measure3 — slide_021.jpg: mode-based color censuses + structure refinements
+ visual crops (upscaled) for qualitative confirmation.
"""
from PIL import Image
import json
from collections import Counter

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_021.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {}


def mode_color(x0, x1, y0, y1, det=None, q=8):
    """mode of quantized colors (optionally filtered by det); returns hex + count"""
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = px[x, y]
            if det and not det(p):
                continue
            c[(p[0] // q * q, p[1] // q * q, p[2] // q * q)] += 1
    if not c:
        return None
    (r, g, b), n = c.most_common(1)[0]
    return {"hex": "%02X%02X%02X" % (r + q // 2, g + q // 2, b + q // 2), "n": n}


def is_red(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50


def is_blueish(p):
    r, g, b = p
    return b > 100 and (b - r) > 40 and (b - g) > 30


def is_darkred_loose(p):
    r, g, b = p
    return r > 100 and (r - g) > 30 and (r - b) > 30


# ---------- mode censuses ----------
out["m_title_red"] = mode_color(273, 478, 60, 96, is_red)
out["m_title_blue"] = mode_color(493, 663, 60, 96, is_blueish)
out["m_row1_dash"] = mode_color(175, 890, 131, 139, lambda p: sum(p) < 500 and p[2] > p[0])
out["m_row1_fill"] = mode_color(185, 230, 140, 172)
out["m_row1_digit_core"] = mode_color(195, 220, 142, 168, lambda p: sum(p) < 420)
out["m_navy"] = mode_color(180, 880, 218, 248)
out["m_navy_yel"] = mode_color(286, 374, 224, 243, lambda p: p[0] > 180 and p[1] > 180)
out["m_navy_white"] = mode_color(400, 860, 224, 243, lambda p: sum(p) > 600)
out["m_row3_fill"] = mode_color(185, 225, 295, 320)
out["m_row3_all_band"] = mode_color(180, 890, 280, 335)
out["m_brace_core"] = mode_color(200, 850, 336, 356, is_darkred_loose)
out["m_ybox_fill"] = mode_color(100, 250, 390, 490)
out["m_ybox_text"] = mode_color(84, 242, 395, 480, lambda p: sum(p) < 450)
out["m_gbox_border_core"] = mode_color(314, 316, 380, 480, lambda p: p[1] > p[0] and p[1] > p[2])
out["m_gbox_text"] = mode_color(340, 733, 378, 465, lambda p: sum(p) < 250)
out["m_dot_core"] = mode_color(632, 710, 148, 164, lambda p: abs(p[0] - p[1]) < 50 and p[2] > p[0] and sum(p) < 560)
out["m_tanline_core"] = mode_color(240, 465, 296, 348, lambda p: p[0] > 170 and (p[0] - p[2]) > 25 and p[1] > 140)

# red check loose inside yellow box
out["ybox_red_loose"] = [(x, y, px[x, y]) for y in range(390, 495) for x in range(80, 260)
                         if is_darkred_loose(px[x, y])][:20]

# ---------- navy bar cols ----------
def is_navy(p):
    r, g, b = p
    return b > 90 and b < 200 and r < 80 and g < 80
cols = [(x, sum(1 for y in range(220, 248) if is_navy(px[x, y]))) for x in range(100, 910)]
xs = [x for x, n in cols if n >= 20]
out["navy_bar_x"] = [min(xs), max(xs)] if xs else None
rows = [(y, sum(1 for x in range(180, 870) if is_navy(px[x, y]))) for y in range(200, 265)]
ys = [y for y, n in rows if n >= 500]
out["navy_bar_y"] = [min(ys), max(ys)] if ys else None

# ---------- row3: find the greens actually present ----------
band = Counter()
for y in range(280, 340):
    for x in range(170, 900):
        p = px[x, y]
        if p[1] > p[0] + 15 and p[1] > p[2] + 15:
            band[(p[0] // 16 * 16, p[1] // 16 * 16, p[2] // 16 * 16)] += 1
out["row3_greenish_modes"] = [[("%02X%02X%02X" % k), n] for k, n in band.most_common(8)]

# row3 box borders: green-ish stroke columns/rows
def is_gline(p):
    r, g, b = p
    return g > 110 and (g - r) > 30 and (g - b) > 30
r3rows = [(y, sum(1 for x in range(175, 895) if is_gline(px[x, y]))) for y in range(275, 345)]
out["row3_gline_rows"] = [(y, n) for y, n in r3rows if n > 40]
r3cols = [(x, sum(1 for y in range(282, 332) if is_gline(px[x, y]))) for x in range(160, 910)]
out["row3_gline_cols"] = [(x, n) for x, n in r3cols if n >= 10]

# row3 box fill extent per column (any non-white, non-border ink in box band)
def is_inkish(p):
    return sum(p) < 700
r3fill = [(x, sum(1 for y in range(290, 325) if is_inkish(px[x, y]))) for x in range(160, 910)]
runs = []
cur = None
for x, n in r3fill:
    if n >= 20:
        cur = [x, x] if cur is None else [cur[0], x]
    else:
        if cur:
            runs.append(tuple(cur))
            cur = None
if cur:
    runs.append(tuple(cur))
out["row3_box_cols_inkish"] = runs
r3fillrows = [(y, sum(1 for x in range(180, 260) if is_inkish(px[x, y]))) for y in range(275, 345)]
ys2 = [y for y, n in r3fillrows if n >= 50]
out["row3_box_rows_inkish_x180_260"] = [min(ys2), max(ys2)] if ys2 else None

# ---------- row1 lane extent ----------
def is_blue(p):
    r, g, b = p
    return b > 110 and (b - r) > 60 and (b - g) > 40
r1rows = [(y, sum(1 for x in range(172, 900) if is_blue(px[x, y]))) for y in range(125, 195)]
out["row1_blue_rows_x172_900"] = [(y, n) for y, n in r1rows if n > 50]
r1cols = [(x, sum(1 for y in range(133, 182) if is_blue(px[x, y]))) for x in range(160, 920)]
out["row1_blue_cols"] = [(x, n) for x, n in r1cols if n >= 10][:6] + [(x, n) for x, n in r1cols if n >= 10][-6:]

# ---------- dots detail ----------
def is_dot(p):
    r, g, b = p
    return 90 < r < 200 and 100 < g < 210 and 130 < b < 230 and abs(r - g) < 45 and (b - r) > 15
dcols = [(x, sum(1 for y in range(146, 166) if is_dot(px[x, y]))) for x in range(615, 745)]
runs = []
cur = None
for x, n in dcols:
    if n >= 4:
        cur = [x, x] if cur is None else [cur[0], x]
    else:
        if cur:
            runs.append(tuple(cur))
            cur = None
if cur:
    runs.append(tuple(cur))
out["dot_col_runs"] = runs
drows = [(y, sum(1 for x in range(630, 712) if is_dot(px[x, y]))) for y in range(140, 172)]
out["dot_row_prof"] = [(y, n) for y, n in drows if n > 2]

# ---------- brace profile ----------
def is_br(p):
    r, g, b = p
    return r > 140 and (r - g) > 45 and (r - b) > 45
prof = {}
for y in range(332, 358):
    xs = [x for x in range(160, 900) if is_br(px[x, y])]
    if xs:
        prof[y] = [min(xs), max(xs), len(xs)]
out["brace_profile"] = prof
# per-column presence at spine row and top row
top_cols = [x for x in range(160, 900) if is_br(px[x, 337])]
out["brace_top337_cols"] = [min(top_cols), max(top_cols), len(top_cols)] if top_cols else None
gap_zone = [x for x in range(480, 570) if not is_br(px[x, 343])]
out["brace_spine343_gap"] = [min(gap_zone), max(gap_zone)] if gap_zone else None

# ---------- title detail ----------
out["title_red_blue_boundary"] = {"red_x1": 477, "blue_x0": 493}
# red word rows (P of Position) tighter: x 318..477
def is_red2(p):
    r, g, b = p
    return r > 130 and (r - g) > 45 and (r - b) > 45
rr = [(y, sum(1 for x in range(318, 478) if is_red2(px[x, y]))) for y in range(52, 105)]
out["title_red_rows_word"] = [(y, n) for y, n in rr if n > 2]
bb = [(y, sum(1 for x in range(493, 663) if is_blue(px[x, y]))) for y in range(52, 105)]
out["title_blue_rows_word"] = [(y, n) for y, n in bb if n > 2]
# bracket [1] bbox
out["title_bracket"] = None
brk = [(x, y) for y in range(52, 105) for x in range(260, 320) if is_red2(px[x, y])]
if brk:
    out["title_bracket"] = [min(p[0] for p in brk), min(p[1] for p in brk), max(p[0] for p in brk), max(p[1] for p in brk)]

# ---------- yellow box border (all sides) ----------
def is_tb(p):
    r, g, b = p
    return 180 < r < 248 and 150 < g < 220 and 100 < b < 185 and (r - b) > 35
tb_rows = [(y, sum(1 for x in range(76, 268) if is_tb(px[x, y]))) for y in range(370, 505)]
out["ybox_tb_rows"] = [(y, n) for y, n in tb_rows if n > 60]
tb_cols = [(x, sum(1 for y in range(384, 494) if is_tb(px[x, y]))) for x in range(60, 290)]
out["ybox_tb_cols"] = [(x, n) for x, n in tb_cols if n > 40]

# yellow box text line x-extents per line band
def is_blue(p):
    r, g, b = p
    return b > 110 and (b - r) > 60 and (b - g) > 40
for name, (ya, yb) in {"L1": (396, 412), "L2": (413, 428), "L3": (447, 465), "L4": (466, 481)}.items():
    pts = [(x, y) for y in range(ya, yb) for x in range(78, 264) if is_blue(px[x, y])]
    out[f"ybox_{name}"] = [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)] if pts else None

# ---------- green box text lines x-extents ----------
def is_black(p):
    return sum(px[0, 0]) < 0  # placeholder
def is_blk(p):
    r, g, b = p
    return sum(p) < 260
for name, (ya, yb) in {"G1": (378, 399), "G2": (400, 420), "G3": (443, 464)}.items():
    pts = [(x, y) for y in range(ya, yb) for x in range(318, 756) if is_blk(px[x, y])]
    out[f"gbox_{name}"] = [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)] if pts else None

# ---------- left labels detail ----------
for name, (ya, yb), det in (("blue1", (138, 156), is_blue), ("blue2", (156, 172), is_blue),
                            ("red1", (215, 233), is_red), ("red2", (233, 250), is_red)):
    pts = [(x, y) for y in range(ya, yb) for x in range(62, 170) if det(px[x, y])]
    out[f"lab_{name}"] = [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)] if pts else None

# ---------- row1 box borders (blue line rows per box x-band) ----------
b0rows = [(y, sum(1 for x in range(182, 233) if is_blue(px[x, y]))) for y in range(128, 185)]
out["row1_box0_blue_rows"] = [(y, n) for y, n in b0rows if n > 20]

# ---------- SAVE CROPS ----------
crops = {
    "row1": (160, 120, 905, 195),
    "row3": (160, 275, 905, 340),
    "brace": (160, 325, 905, 362),
    "tanline": (230, 230, 480, 420),
    "ybox": (60, 370, 290, 505),
    "gbox": (300, 360, 780, 500),
    "labels": (55, 125, 175, 260),
    "title": (250, 45, 690, 105),
    "arrows": (490, 165, 560, 300),
    "navy": (150, 205, 900, 260),
}
for name, (x0, y0, x1, y1) in crops.items():
    c = img.crop((x0, y0, x1, y1))
    c = c.resize(((x1 - x0) * 2, (y1 - y0) * 2), Image.LANCZOS)
    c.save(f"/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide021/crop_{name}.png")

print(json.dumps(out, indent=1, default=str))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide021/measure3_output.txt", "w") as f:
    f.write(json.dumps(out, indent=1, default=str))
