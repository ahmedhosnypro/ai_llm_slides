#!/usr/bin/env python3
"""Phase 5: full content measurement for slide_020.jpg with the CLEAN chrome fit.

Mapping (refit here from clean stroke windows): slide = (frame - ax)/sx per axis.
Outputs slide-pt coordinates for: title, 4 row containers + their inner boxes,
ellipsis dots, bolts, +delta symbols, banner, arrows, brace, caption, inset, labels.
"""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_020.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {}


def near(p, c, tol):
    return all(abs(p[i] - c[i]) <= tol for i in range(3))


def is_red(p):
    r, g, b = p
    return r > 130 and (r - g) > 45 and (r - b) > 45


# ---------- 1. CLEAN chrome stroke centroids ----------
# left/right strokes in rows 440..500 (no content there except green inset/gray)
def stroke_center_x(x0, x1, y0, y1):
    cols = []
    for x in range(x0, x1):
        n = sum(1 for y in range(y0, y1) if is_red(px[x, y]))
        cols.append((x, n))
    tot = sum(n for _, n in cols)
    if tot < 10:
        return None
    return sum(x * n for x, n in cols) / tot


lc = stroke_center_x(40, 80, 440, 500)
rc = stroke_center_x(880, 925, 440, 500)
out["left_stroke"] = lc
out["right_stroke"] = rc

# top stroke rows 41..45 (loose detector, rows with n>200)
def is_redish(p):
    r, g, b = p
    return r > 130 and (r - g) > 35 and (r - b) > 35

trows = [(y, sum(1 for x in range(100, 860) if is_redish(px[x, y]))) for y in range(38, 48)]
trows = [(y, n) for y, n in trows if n > 200]
tc = sum(y * n for y, n in trows) / sum(n for _, n in trows)
brows = [(y, sum(1 for x in range(100, 860) if is_redish(px[x, y]))) for y in range(505, 526)]
brows = [(y, n) for y, n in brows if n > 200]
bc = sum(y * n for y, n in brows) / sum(n for _, n in brows)
out["top_stroke"] = tc
out["bottom_stroke"] = bc

# fit vs slide landmarks: left 42, right 919, top 45, bottom 540
sx = (rc - lc) / (919 - 42)
ax = lc - sx * 42
sy = (bc - tc) / (540 - 45)
ay = tc - sy * 45
out["fit"] = {"sx": round(sx, 6), "ax": round(ax, 3), "sy": round(sy, 6), "ay": round(ay, 3)}


def S(fx, fy):
    """frame -> slide pts"""
    return ((fx - ax) / sx, (fy - ay) / sy)


def Sbox(b):
    x0, y0 = S(b[0], b[1]); x1, y1 = S(b[2], b[3])
    return [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1),
            round(x1 - x0, 1), round(y1 - y0, 1)]


def bbox(pred, x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if pred(px[x, y])]
    if not pts:
        return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]


def col_clusters(pred, x0, x1, y0, y1, min_pts=2, gap=4):
    """cluster x columns containing pred pixels into [start,end] spans"""
    cols = []
    for x in range(x0, x1):
        n = sum(1 for y in range(y0, y1) if pred(px[x, y]))
        cols.append((x, n))
    spans = []
    cur = None
    for x, n in cols:
        if n >= min_pts:
            if cur and x <= cur[1] + gap:
                cur[1] = x
            else:
                if cur:
                    spans.append(cur)
                cur = [x, x]
    if cur:
        spans.append(cur)
    return spans


def row_clusters(pred, x0, x1, y0, y1, min_pts=2, gap=3):
    rows = []
    for y in range(y0, y1):
        n = sum(1 for x in range(x0, x1) if pred(px[x, y]))
        rows.append((y, n))
    spans = []
    cur = None
    for y, n in rows:
        if n >= min_pts:
            if cur and y <= cur[1] + gap:
                cur[1] = y
            else:
                if cur:
                    spans.append(cur)
                cur = [y, y]
    if cur:
        spans.append(cur)
    return spans


RED = (192, 0, 0)
GREEN = (0, 165, 80)
BLUE = (51, 51, 204)
DRED = (153, 0, 0)
ORANGE = (255, 165, 0)
GRAY = (140, 140, 140)
YELLOW = (245, 230, 163)   # F5E6A3
PINKC = (242, 167, 195)    # F2A7C3

res = out.setdefault("elements", {})

# ---------- 2. title ----------
tb = bbox(is_red, 150, 840, 50, 95)
res["title_ink_frame"] = tb
res["title_ink_slide"] = Sbox(tb)
# title column profile -> word clusters (to see spacing/center)
res["title_word_cols"] = col_clusters(is_red, 150, 840, 55, 90, 1, 12)

# ---------- 3. row containers (dashed borders + fills) ----------
# fills are reliable; borders: find dashed edge rows via color counts in x 62..905
def edge_rows(color, tol, y0, y1, xa=62, xb=905, minn=40):
    spans = []
    for y in range(y0, y1):
        n = sum(1 for x in range(xa, xb) if near(px[x, y], color, tol))
        if n >= minn:
            spans.append((y, n))
    return spans


res["row1_red_edge_rows"] = edge_rows(RED, 55, 60, 150)
res["row2_green_edge_rows"] = edge_rows(GREEN, 55, 120, 210)
res["row3_blue_edge_rows"] = edge_rows(BLUE, 55, 200, 275)
res["row4_red_edge_rows"] = edge_rows(RED, 55, 330, 420)

def edge_cols(color, tol, x0, x1, ya, yb, minn=8):
    spans = []
    for x in range(x0, x1):
        n = sum(1 for y in range(ya, yb) if near(px[x, y], color, tol))
        if n >= minn:
            spans.append((x, n))
    return spans


res["row1_red_edge_cols"] = edge_cols(RED, 55, 50, 915, 75, 145)[:14] + ["..."] + edge_cols(RED, 55, 50, 915, 75, 145)[-6:]
res["row4_red_edge_cols"] = edge_cols(RED, 55, 50, 915, 335, 415)[:14] + ["..."] + edge_cols(RED, 55, 50, 915, 335, 415)[-6:]

# container fills (tight tol) for exact extents
FILLS = {
    "row1_fill": ((251, 234, 234), 60, 150),
    "row2_fill": ((232, 245, 233), 120, 210),
    "row3_fill": ((204, 204, 242), 200, 275),
    "row4_fill": ((251, 234, 234), 330, 420),
}
for name, (c, y0, y1) in FILLS.items():
    bb = bbox(lambda p, c=c: near(p, c, 10), 40, 920, y0, y1)
    res[name + "_frame"] = bb
    res[name + "_slide"] = Sbox(bb)

# ---------- 4. row1 word boxes (red-bordered, on pink fill) ----------
# red box borders within row1: column clusters over the row1 band
r1cols = col_clusters(lambda p: near(p, RED, 55), 60, 910, 84, 135, 3, 3)
res["row1_box_col_spans"] = r1cols
# word label ink (red text) inside row1
res["row1_label_rows"] = row_clusters(lambda p: near(p, RED, 60), 170, 880, 84, 135, 2, 3)
# gray ellipsis dots in the gap
res["row1_gap_dot_cols"] = col_clusters(lambda p: near(p, GRAY, 45), 480, 760, 100, 125, 1, 3)
res["row1_gap_dot_rows"] = row_clusters(lambda p: near(p, GRAY, 45), 480, 760, 100, 125, 1, 3)

# ---------- 5. row2 embedding boxes + cells ----------
r2cols = col_clusters(lambda p: near(p, GREEN, 55), 60, 910, 135, 200, 3, 3)
res["row2_box_col_spans"] = r2cols
res["row2_yellow_cells"] = col_clusters(lambda p: near(p, YELLOW, 30), 60, 910, 140, 195, 2, 2)
res["row2_pink_cells"] = col_clusters(lambda p: near(p, PINKC, 35), 60, 910, 140, 195, 2, 2)
res["row2_cell_rows_yellow"] = row_clusters(lambda p: near(p, YELLOW, 30), 70, 890, 135, 200, 2, 2)
# X_i red symbols in row2
res["row2_xsym_cols"] = col_clusters(lambda p: near(p, RED, 60), 60, 910, 140, 195, 1, 3)
res["row2_xsym_rows"] = row_clusters(lambda p: near(p, RED, 60), 70, 300, 135, 200, 1, 3)
res["row2_gap_dot_cols"] = col_clusters(lambda p: near(p, GREEN, 55), 480, 760, 150, 185, 1, 3)
res["row2_gap_dot_rows"] = row_clusters(lambda p: near(p, GREEN, 55), 480, 760, 150, 185, 1, 3)

# ---------- 6. row3 pos boxes + bolts + deltas ----------
r3cols = col_clusters(lambda p: near(p, BLUE, 55), 60, 910, 210, 265, 3, 3)
res["row3_box_col_spans"] = r3cols
res["row3_label_rows"] = row_clusters(lambda p: near(p, BLUE, 60), 170, 880, 210, 265, 2, 3)
res["row3_gap_dot_cols"] = col_clusters(lambda p: near(p, BLUE, 55), 480, 760, 225, 250, 1, 3)
res["row3_gap_dot_rows"] = row_clusters(lambda p: near(p, BLUE, 55), 480, 760, 225, 250, 1, 3)
res["bolt_cols"] = col_clusters(lambda p: near(p, ORANGE, 55), 60, 910, 240, 270, 1, 3)
res["bolt_rows"] = row_clusters(lambda p: near(p, ORANGE, 55), 60, 910, 240, 270, 1, 3)
# delta symbols: red glyphs in rows 246..266 EXCLUDING arrow x ranges (565..745)
def not_in_arrows(x):
    return not (560 <= x <= 750)

dpts = [(x, y) for y in range(244, 268) for x in range(90, 860)
        if near(px[x, y], RED, 60) and not_in_arrows(x)]
if dpts:
    db = [min(p[0] for p in dpts), min(p[1] for p in dpts), max(p[0] for p in dpts), max(p[1] for p in dpts)]
    res["delta_band_frame"] = db
    res["delta_band_slide"] = Sbox(db)
    # cluster into individual symbols
    xs = sorted(set(p[0] for p in dpts))
    spans = []
    cur = [xs[0], xs[0]]
    for x in xs[1:]:
        if x <= cur[1] + 6:
            cur[1] = x
        else:
            spans.append(cur); cur = [x, x]
    spans.append(cur)
    res["delta_symbol_spans_frame"] = spans
    res["delta_symbol_spans_slide"] = [[round((s[0] - ax) / sx, 1), round((s[1] - ax) / sx, 1)] for s in spans]
    res["delta_row_spans"] = row_clusters(lambda p: near(p, RED, 60) and True, 90, 560, 244, 268, 1, 3)

# ---------- 7. banner ----------
bb = bbox(lambda p: near(p, DRED, 30), 40, 920, 265, 355)
res["banner_frame"] = bb
res["banner_slide"] = Sbox(bb)
# banner text: yellow glyphs + white glyphs
res["banner_yellow_cols"] = col_clusters(lambda p: near(p, (255, 215, 0), 60), 70, 890, 285, 335, 1, 8)[:8]
yb = bbox(lambda p: near(p, (255, 215, 0), 60), 70, 890, 280, 340)
res["banner_yellow_ink_frame"] = yb
res["banner_yellow_ink_slide"] = Sbox(yb)
wb = bbox(lambda p: near(p, (255, 255, 255), 25), 70, 890, 280, 340)
res["banner_white_ink_frame"] = wb
res["banner_white_ink_slide"] = Sbox(wb)
res["banner_text_rows"] = row_clusters(lambda p: near(p, (255, 215, 0), 60) or near(p, (255, 255, 255), 25), 70, 890, 280, 340, 2, 3)

# ---------- 8. arrows (strict red, away from banner) ----------
for name, (x0, x1, y0, y1) in {
    "arrow1": (560, 700, 195, 272),
    "arrow2": (655, 760, 240, 272),
    "arrow3": (440, 570, 315, 372),
    "arrow4": (440, 570, 405, 455),
}.items():
    bb2 = bbox(lambda p: near(p, RED, 45), x0, x1, y0, y1)
    res[name + "_frame"] = bb2
    res[name + "_slide"] = Sbox(bb2) if bb2 else None

# ---------- 9. row4 boxes + brace + caption ----------
r4cols = col_clusters(lambda p: near(p, RED, 55), 60, 910, 335, 415, 3, 3)
res["row4_box_col_spans"] = r4cols
res["row4_label_rows"] = row_clusters(lambda p: near(p, RED, 60), 170, 880, 335, 415, 2, 3)
brb = bbox(lambda p: near(p, RED, 70), 60, 910, 436, 452)
res["brace_frame"] = brb
res["brace_slide"] = Sbox(brb) if brb else None
capb = bbox(lambda p: near(p, (34, 34, 204), 70), 300, 720, 450, 480)
res["caption_frame"] = capb
res["caption_slide"] = Sbox(capb) if capb else None

# ---------- 10. inset schematic ----------
res["inset_green_frame"] = bbox(lambda p: near(p, (0, 128, 0), 55), 30, 230, 400, 525)
res["inset_green_slide"] = Sbox(res["inset_green_frame"])
res["inset_pink_frame"] = bbox(lambda p: near(p, (244, 184, 208), 30), 40, 230, 405, 525)
res["inset_pink_slide"] = Sbox(res["inset_pink_frame"])
res["inset_black_rows"] = row_clusters(lambda p: sum(p) < 200, 45, 215, 405, 525, 1, 3)
res["inset_bolt_cols"] = col_clusters(lambda p: near(p, ORANGE, 60), 45, 215, 405, 525, 1, 3)
res["inset_bolt_rows"] = row_clusters(lambda p: near(p, ORANGE, 60), 45, 215, 405, 525, 1, 3)

# ---------- 11. left labels ----------
# gray italic label rows 80..145, x 40..160
res["lab1_rows"] = row_clusters(lambda p: near(p, GRAY, 50), 40, 165, 75, 150, 2, 4)
res["lab1_cols"] = col_clusters(lambda p: near(p, GRAY, 50), 40, 165, 75, 150, 1, 6)
res["lab2_rows"] = row_clusters(lambda p: near(p, GREEN, 60), 40, 165, 125, 205, 2, 4)
res["lab2_cols"] = col_clusters(lambda p: near(p, GREEN, 60), 40, 165, 125, 205, 1, 6)
res["lab3_rows"] = row_clusters(lambda p: near(p, BLUE, 60), 40, 165, 210, 270, 2, 4)
res["lab3_cols"] = col_clusters(lambda p: near(p, BLUE, 60), 40, 165, 210, 270, 1, 6)
res["lab4_rows"] = row_clusters(lambda p: near(p, RED, 60), 40, 165, 335, 415, 2, 4)
res["lab4_cols"] = col_clusters(lambda p: near(p, RED, 60), 40, 165, 335, 415, 1, 6)
# caption/inset-side green label
res["lab5_rows"] = row_clusters(lambda p: near(p, (0, 128, 0), 60), 195, 300, 440, 500, 2, 4)
res["lab5_cols"] = col_clusters(lambda p: near(p, (0, 128, 0), 60), 195, 300, 440, 500, 1, 6)

# ---------- convert all element frame boxes to slide ----------
def conv_key(k, v):
    if isinstance(v, list) and v and isinstance(v[0], (int, float)) and len(v) == 4:
        sk = k + "_slide"
        if sk not in res:
            res[sk] = Sbox(v)

for k in list(res.keys()):
    v = res[k]
    if isinstance(v, list) and v and isinstance(v[0], list):
        continue
    conv_key(k, v)

print(json.dumps(out, indent=1))
