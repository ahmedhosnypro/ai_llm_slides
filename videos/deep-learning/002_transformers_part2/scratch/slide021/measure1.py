#!/usr/bin/env python3
"""measure1 — slide_021.jpg (960x540): chrome-landmark fit + full content
inventory. Same methodology as the certified slide_020 chain (measure4).

Chrome fit: four border landmarks (panel left/right/top/bottom stroke centers,
subpixel red centroids) -> frame = a + s*slide against slide landmarks
left 42 / right 919 / top 45 / bottom 540 (slide_003 certified convention).

Content inventory (color-windowed ink bboxes + censuses):
  title (red + blue split), diagram blue box border, row1 lane+boxes+dots,
  left labels (blue/red), arrows (red), navy bar + text, row3 lane+boxes,
  brace, connector line, yellow note box + lines, green note box + lines.
"""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_021.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {"size": [W, H]}


def is_red(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50


def is_redish(p):
    r, g, b = p
    return r > 130 and (r - g) > 35 and (r - b) > 35


def is_gray(p):
    r, g, b = p
    return abs(r - 233) <= 10 and abs(g - 233) <= 10 and abs(b - 231) <= 12


# --- 1. chrome landmarks ---------------------------------------------------
def col_centroid(x0, x1, y0, y1, det):
    cols = []
    for x in range(x0, x1):
        n = sum(1 for y in range(y0, y1) if det(px[x, y]))
        cols.append((x, n))
    tot = sum(n for _, n in cols)
    if tot < 20:
        return None
    return sum(x * n for x, n in cols) / tot


lc = col_centroid(40, 80, 150, 450, is_redish)
rc = col_centroid(880, 925, 150, 450, is_redish)

prof = [(y, sum(1 for x in range(100, 860) if is_redish(px[x, y]))) for y in range(30, 62)]
tc_rows = [(y, n) for y, n in prof if n > 200]
top_c = sum(y * n for y, n in tc_rows) / sum(n for _, n in tc_rows) if tc_rows else None

bot = [(y, sum(1 for x in range(100, 860) if is_redish(px[x, y]))) for y in range(500, 526)]
out["bottom_rows"] = bot

trans = {}
for x in (200, 480, 700, 830):
    for y in range(5, 120):
        if is_gray(px[x, y]) and is_gray(px[x, y + 1]) and is_gray(px[x, y + 2]):
            trans[x] = y
            break
out["gray_transition_cols"] = trans
out["left_stroke_centroid"] = lc
out["right_stroke_centroid"] = rc
out["top_stroke_centroid"] = top_c

# --- detectors for content -------------------------------------------------
def is_blue(p):    # dark blue border/text (0000CC-class)
    r, g, b = p
    return b > 110 and (b - r) > 60 and (b - g) > 40


def is_navy(p):    # navy fill 000080
    r, g, b = p
    return b > 90 and b < 190 and r < 70 and g < 70


def is_green(p):   # border green 00A000-class
    r, g, b = p
    return g > 100 and (g - r) > 40 and (g - b) > 30


def is_lgreen(p):  # light green fill D5EED5
    r, g, b = p
    return 195 < r < 240 and 220 < g < 250 and 195 < b < 240 and g > r and g > b


def is_lblue(p):   # light blue/lavender fill C9D7F0
    r, g, b = p
    return 180 < r < 225 and 195 < g < 235 and b > 225 and b > r


def is_yellow(p):  # FFFFE0 fill / FFFF00 text
    r, g, b = p
    return r > 230 and g > 220 and b < 200


def is_tan(p):     # tan connector/border E6C896-class
    r, g, b = p
    return 190 < r < 245 and 160 < g < 215 and 110 < b < 175 and r > b


def bbox(det, x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, min(y1, H)) for x in range(x0, min(x1, W)) if det(px[x, y])]
    if not pts:
        return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts),
            len(pts)]


# --- 2. title ---------------------------------------------------------------
out["title_red"] = bbox(is_red, 250, 640, 45, 100)          # "[1] Position"
out["title_blue"] = bbox(is_blue, 480, 720, 45, 100)       # "Encoding"
out["title_all"] = bbox(lambda p: is_red(p) or is_blue(p), 150, 850, 40, 105)

# --- 3. diagram blue box border (thin dark blue, thin strokes) --------------
# horizontal border rows: count blue px per row in x 100..860
brow = [(y, sum(1 for x in range(100, 860) if is_blue(px[x, y]))) for y in range(100, 380)]
out["blue_rows_top"] = [(y, n) for y, n in brow if n > 400][:6]
bcol = [(x, sum(1 for y in range(110, 370) if is_blue(px[x, y]))) for x in range(60, 920)]
out["blue_cols_left"] = [(x, n) for x, n in bcol if n > 100][:8]
out["blue_cols_right"] = [(x, n) for x, n in bcol if n > 100][-8:]

# --- 4. row1 band: lane border, boxes, dots ---------------------------------
out["row1_lane"] = bbox(is_blue, 150, 900, 130, 185)       # dashed blue lane
out["row1_boxes_fill"] = bbox(is_lblue, 150, 900, 130, 185)
# dots (gray-blue): scan band between box5 and box N-2
def is_dotgray(p):
    r, g, b = p
    return 100 < r < 190 and 110 < g < 200 and 140 < b < 220 and abs(r - g) < 40
out["row1_dots"] = bbox(is_dotgray, 620, 740, 140, 180)

# --- 5. left labels ----------------------------------------------------------
out["lab_blue"] = bbox(is_blue, 60, 165, 130, 180)          # Position Information
out["lab_red"] = bbox(is_red, 60, 165, 200, 265)           # Positional Encoder

# --- 6. arrows (red) between rows -------------------------------------------
out["arrow1"] = bbox(is_red, 480, 570, 175, 225)
out["arrow2"] = bbox(is_red, 480, 570, 260, 310)

# --- 7. navy bar + yellow/white text ----------------------------------------
out["navy_bar"] = bbox(is_navy, 100, 900, 200, 265)
out["navy_text_yellow"] = bbox(is_yellow, 150, 880, 210, 255)
out["navy_text_white"] = bbox(lambda p: p[0] > 235 and p[1] > 235 and p[2] > 235, 380, 880, 210, 255)

# --- 8. row3 band ------------------------------------------------------------
out["row3_lane"] = bbox(is_green, 150, 900, 275, 340)
out["row3_boxes_fill"] = bbox(is_lgreen, 150, 900, 275, 340)

# --- 9. brace (red, below row3) ----------------------------------------------
out["brace"] = bbox(is_red, 150, 900, 335, 365)

# --- 10. connector line (tan) from function to yellow box --------------------
out["tan_line"] = bbox(is_tan, 250, 420, 245, 400)

# --- 11. yellow note box ------------------------------------------------------
out["yellow_box"] = bbox(is_yellow, 40, 300, 360, 500)
# blue text inside yellow box
out["yellow_box_blue_text"] = bbox(is_blue, 50, 290, 365, 495)
out["yellow_box_red_text"] = bbox(is_red, 50, 290, 365, 495)

# --- 12. green note box -------------------------------------------------------
out["green_box"] = bbox(is_green, 290, 800, 355, 500)
out["green_box_black"] = bbox(lambda p: sum(p) < 200, 300, 790, 360, 495)

print(json.dumps(out, indent=1))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide021/measure1_output.txt", "w") as f:
    f.write(json.dumps(out, indent=1))
