#!/usr/bin/env python3
"""Phase 4: precise chrome-landmark fit for slide_020.jpg (960x540).

Finds the four chrome border landmarks (panel left/right/top stroke centers +
bottom stroke) with subpixel centroids, the white->gray panel transition, the
badge, and the letterbox; then fits  frame = a + s * slide  per axis against
slide landmarks left 42 / right 919 / top 45 / bottom 540 (slide_003 certified
convention). Prints the fit + cross-checks. Part of the slide_020 build chain.
"""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_020.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {"size": [W, H]}


def is_red(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50


def is_redish(p):  # looser: catches JPEG-faded stroke px
    r, g, b = p
    return r > 130 and (r - g) > 35 and (r - b) > 35


# --- 1. full red row profile y 10..90 (x 100..860) with both detectors
prof_strict, prof_loose = [], []
for y in range(10, 90):
    ns = sum(1 for x in range(100, 860) if is_red(px[x, y]))
    nl = sum(1 for x in range(100, 860) if is_redish(px[x, y]))
    prof_strict.append((y, ns))
    prof_loose.append((y, nl))
out["row_profile_strict_top20"] = sorted(prof_strict, key=lambda t: -t[1])[:20]
out["row_profile_loose_top20"] = sorted(prof_loose, key=lambda t: -t[1])[:20]

# --- 2. white->gray transition per column sample (first y where panel gray E9E9E7)
def is_gray(p):
    r, g, b = p
    return abs(r - 233) <= 10 and abs(g - 233) <= 10 and abs(b - 231) <= 12

trans = {}
for x in (200, 480, 700, 830):
    for y in range(5, 120):
        if is_gray(px[x, y]) and is_gray(px[x, y + 1]) and is_gray(px[x, y + 2]):
            trans[x] = y
            break
out["gray_transition_cols"] = trans

# --- 3. left/right border stroke centers (weighted centroid of red columns)
def col_centroid(x0, x1, y0, y1, det):
    cols = []
    for x in range(x0, x1):
        n = sum(1 for y in range(y0, y1) if det(px[x, y]))
        cols.append((x, n))
    tot = sum(n for _, n in cols)
    if tot < 20:
        return None, cols
    cx = sum(x * n for x, n in cols) / tot
    return cx, cols

lc, lcols = col_centroid(40, 80, 150, 450, is_redish)
rc, rcols = col_centroid(880, 925, 150, 450, is_redish)
out["left_stroke_centroid"] = lc
out["right_stroke_centroid"] = rc

# --- 4. top stroke row centroid (rows 30..60 among rows with count>200, loose)
tc_rows = [(y, n) for y, n in prof_loose if 30 <= y <= 60 and n > 200]
if tc_rows:
    tot = sum(n for _, n in tc_rows)
    out["top_stroke_centroid"] = sum(y * n for y, n in tc_rows) / tot
else:
    out["top_stroke_centroid"] = None
out["top_rows_loose_30_60"] = [(y, n) for y, n in prof_loose if 30 <= y <= 62]

# --- 5. bottom red stroke rows (500..525)
bot = [(y, sum(1 for x in range(100, 860) if is_redish(px[x, y]))) for y in range(500, 526)]
out["bottom_profile"] = [(y, n) for y, n in bot if n > 50]
bt_rows = [(y, n) for y, n in bot if n > 200]
if bt_rows:
    tot = sum(n for _, n in bt_rows)
    out["bottom_stroke_centroid"] = sum(y * n for y, n in bt_rows) / tot

# --- 6. letterbox start
black_rows = [y for y in range(480, H) if sum(1 for x in range(200, 760) if sum(px[x, y]) < 120) > 500]
out["letterbox_rows"] = (min(black_rows), max(black_rows)) if black_rows else None

# --- 7. badge: yellow bbox + purple ring bbox
def is_yel(p):
    r, g, b = p
    return r > 225 and g > 225 and 120 < b < 215

ypts = [(x, y) for y in range(40, 110) for x in range(835, 915) if is_yel(px[x, y])]
if ypts:
    bx0, by0 = min(p[0] for p in ypts), min(p[1] for p in ypts)
    bx1, by1 = max(p[0] for p in ypts), max(p[1] for p in ypts)
    out["badge_yellow_bbox"] = [bx0, by0, bx1, by1]
    out["badge_center"] = [(bx0 + bx1) / 2, (by0 + by1) / 2]

def is_pur(p):
    r, g, b = p
    return b > 150 and 70 < r < 180 and g < 130

ppts = [(x, y) for y in range(35, 115) for x in range(830, 920) if is_pur(px[x, y])]
if ppts:
    out["badge_ring_bbox"] = [min(p[0] for p in ppts), min(p[1] for p in ppts),
                              max(p[0] for p in ppts), max(p[1] for p in ppts)]

# --- 8. title ink bbox (red text rows 45..95, x 150..800, EXCLUDING stroke rows)
tpts = [(x, y) for y in range(50, 95) for x in range(150, 800) if is_red(px[x, y])]
if tpts:
    out["title_ink_frame"] = [min(p[0] for p in tpts), min(p[1] for p in tpts),
                              max(p[0] for p in tpts), max(p[1] for p in tpts)]

# --- 9. fit the mapping (slide landmarks: left 42, right 919, top 45, bottom 540)
fit = {}
if lc is not None and rc is not None:
    sx = (rc - lc) / (919 - 42)
    ax = lc - sx * 42
    fit["sx"], fit["ax"] = sx, ax
if out.get("top_stroke_centroid") is not None and out.get("bottom_stroke_centroid") is not None:
    sy = (out["bottom_stroke_centroid"] - out["top_stroke_centroid"]) / (540 - 45)
    ay = out["top_stroke_centroid"] - sy * 45
    fit["sy"], fit["ay"] = sy, ay
out["fit"] = fit

def to_slide(fx, fy):
    return ((fx - fit["ax"]) / fit["sx"], (fy - fit["ay"]) / fit["sy"])

if "badge_center" in out and fit:
    sc = to_slide(*out["badge_center"])
    out["badge_center_slide"] = [round(sc[0], 1), round(sc[1], 1)]
    out["badge_delta_vs_house"] = [round(sc[0] - 893, 1), round(sc[1] - 71, 1)]
if "title_ink_frame" in out and fit:
    t = out["title_ink_frame"]
    s0 = to_slide(t[0], t[1]); s1 = to_slide(t[2], t[3])
    out["title_ink_slide"] = [round(s0[0], 1), round(s0[1], 1), round(s1[0], 1), round(s1[1], 1)]
    out["title_ink_slide_w"] = round(s1[0] - s0[0], 1)
    out["title_ink_slide_h"] = round(s1[1] - s0[1], 1)

print(json.dumps(out, indent=1))
