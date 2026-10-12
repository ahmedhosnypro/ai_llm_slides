#!/usr/bin/env python3
"""Comprehensive geometry measurement of slide_049.jpg (960x540, 1px=1pt).
Measures every element group the build needs: title, Y row, green arrows, container,
bars, red arrows, blue dots, X row, blue arrows, embedding bars, gray arrows,
word row, left column. Prints compact results and saves JSON."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_049.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

out = {}

def comps(mask, min_px=6):
    lab, n = ndimage.label(mask)
    res = []
    for sl in ndimage.find_objects(lab):
        y0, y1 = sl[0].start, sl[0].stop - 1
        x0, x1 = sl[1].start, sl[1].stop - 1
        npx = int(mask[sl].sum())
        if npx < min_px:
            continue
        res.append((x0, x1, y0, y1, npx))
    return sorted(res, key=lambda t: (t[2], t[0]))

def merge_x(items, gap=6):
    """merge components into clusters by x-overlap (for segmented rows)"""
    items = sorted(items, key=lambda t: t[0])
    clusters = []
    for it in items:
        if clusters and it[0] <= clusters[-1][1] + gap:
            c = clusters[-1]
            clusters[-1] = (c[0], max(c[1], it[1]), min(c[2], it[2]), max(c[3], it[3]), c[4] + it[4])
        else:
            clusters.append((it[0], it[1], it[2], it[3], it[4]))
    return clusters

# ---------- color classes ----------
red_ink = (r > 120) & (g < 90) & (b < 90) & (r - g > 60) & (r - b > 60)          # C00000-ish text/borders
dark_blue = (b > 120) & (b - r > 60) & (b - g > 60) & (r < 110) & (g < 110)      # 2E3192-ish
med_blue = (b - r > 40) & (b - g > 30) & (b > 130) & (r > 40) & (r < 160) & (g < 140)  # 3355BB-ish arrows
green = (g - r > 40) & (g - b > 40) & (g > 110)                                   # 00B050 / 92D050
tan = (r > 200) & (r - b > 40) & (g > 190) & (g - b > 30) & (b < 220)             # FDE9D9 bar
cyan = (b > 200) & (g > 200) & (r < 210) & (b - r > 20) & (g - r > 20)            # CCFFFF bar
gray_ink = (abs(r - g) < 14) & (abs(g - b) < 14) & (r > 120) & (r < 205)          # A6A6A6-ish
yellow_ink = (r > 215) & (g > 185) & (b < 170) & (r - b > 60)                     # FFE699 cells
pink_ink = (r > 200) & (b > 160) & (g < 200) & (r - g > 25) & (b - g > 15)        # F4B8C8 cells

# ---------- title ----------
tb = comps(red_ink[40:82, 100:800], 20)
tb = [(x0+100, x1+100, y0+40, y1+40, n) for (x0, x1, y0, y1, n) in tb]
out["title_red_ink"] = merge_x(tb, gap=40)

# ---------- Y row band (y 80..110) ----------
band = slice(78, 112)
redb = comps(red_ink[band, :], 10)
redb = [(x0, x1, y0+78, y1+78, n) for (x0, x1, y0, y1, n) in redb]
out["yrow_red_borders"] = merge_x(redb, gap=4)
yellowb = comps(yellow_ink[band, :], 15)
yellowb = [(x0, x1, y0+78, y1+78, n) for (x0, x1, y0, y1, n) in yellowb]
out["yrow_yellow_cells"] = merge_x(yellowb, gap=8)
greenb = comps(green[band, :], 15)
greenb = [(x0, x1, y0+78, y1+78, n) for (x0, x1, y0, y1, n) in greenb]
out["yrow_green_cells"] = merge_x(greenb, gap=8)
pinkb = comps(pink_ink[band, :], 15)
pinkb = [(x0, x1, y0+78, y1+78, n) for (x0, x1, y0, y1, n) in pinkb]
out["yrow_pink_cells"] = merge_x(pinkb, gap=8)
out["yrow_blue_dots"] = merge_x(comps(dark_blue[band, :], 4), gap=5)

# ---------- green arrows ----------
gb = comps(green[100:130, 150:900], 15)
gb = [(x0+150, x1+150, y0+100, y1+100, n) for (x0, x1, y0, y1, n) in gb]
out["green_arrows"] = gb

# ---------- container ----------
# light blue fill C9DFF0: high b, mid r/g
lb = (b > 215) & (r > 165) & (r < 215) & (g > 195) & (g < 235)
cb = comps(lb[:, :], 400)
out["pale_blue_regions"] = cb[:8]
# container dark-blue border: vertical/horizontal dark blue lines
dbv = comps(dark_blue[:, :], 100)
out["dark_blue_big"] = [t for t in dbv if (t[1]-t[0] > 50 or t[3]-t[2] > 50)][:10]

# ---------- red arrows between bars (y 160..237 has dots; red arrows y 267..283, 312..329) ----------
for name, (yy0, yy1) in {"red_arrows_b21": (266, 285), "red_arrows_b10": (311, 331)}.items():
    rb = comps(red_ink[yy0:yy1, 150:900], 4)
    rb = [(x0+150, x1+150, y0+yy0, y1+yy0, n) for (x0, x1, y0, y1, n) in rb]
    out[name] = merge_x(rb, gap=8)

# ---------- X row band (y 372..402) ----------
band = slice(370, 404)
redb = comps(red_ink[band, :], 10)
redb = [(x0, x1, y0+370, y1+370, n) for (x0, x1, y0, y1, n) in redb]
out["xrow_red_borders"] = merge_x(redb, gap=4)
yellowb = comps(yellow_ink[band, :], 15)
yellowb = [(x0, x1, y0+370, y1+370, n) for (x0, x1, y0, y1, n) in yellowb]
out["xrow_yellow_cells"] = merge_x(yellowb, gap=8)
greenb = comps(green[band, :], 15)
greenb = [(x0, x1, y0+370, y1+370, n) for (x0, x1, y0, y1, n) in greenb]
out["xrow_green_cells"] = merge_x(greenb, gap=8)
pinkb = comps(pink_ink[band, :], 15)
pinkb = [(x0, x1, y0+370, y1+370, n) for (x0, x1, y0, y1, n) in pinkb]
out["xrow_pink_cells"] = merge_x(pinkb, gap=8)
out["xrow_green_dots"] = merge_x(comps(green[band, 560:760], 4), gap=5)
out["xrow_green_dots"] = [(x0+560, x1+560, y0+370, y1+370, n) for (x0, x1, y0, y1, n) in out["xrow_green_dots"]]

# ---------- blue arrows (y 396..419) ----------
bb = comps(med_blue[394:420, 150:900], 8)
bb = [(x0+150, x1+150, y0+394, y1+394, n) for (x0, x1, y0, y1, n) in bb]
out["blue_arrows"] = merge_x(bb, gap=6)

# ---------- embedding bars ----------
tanb = comps(tan[:, :], 500)
out["tan_bar"] = tanb[:4]
cyb = comps(cyan[:, :], 500)
out["cyan_bar"] = cyb[:4]

# ---------- gray arrows (between cyan bar and word row) ----------
gab = comps(gray_ink[455:478, 150:900], 8)
gab = [(x0+150, x1+150, y0+455, y1+455, n) for (x0, x1, y0, y1, n) in gab]
out["gray_arrows"] = merge_x(gab, gap=6)

# ---------- word row ----------
band = slice(470, 520)
redb = comps(red_ink[band, :], 10)
redb = [(x0, x1, y0+470, y1+470, n) for (x0, x1, y0, y1, n) in redb]
out["wordrow_red_borders"] = merge_x(redb, gap=4)
out["wordrow_gray_dots"] = merge_x(comps(gray_ink[band, 560:780], 4), gap=6)
out["wordrow_gray_dots"] = [(x0+560, x1+560, y0+470, y1+470, n) for (x0, x1, y0, y1, n) in out["wordrow_gray_dots"]]

# ---------- left column (x 55..165) ----------
lc = slice(0, 540)
redb = comps(red_ink[lc, 55:165], 10)
redb = [(x0+55, x1+55, y0, y1, n) for (x0, x1, y0, y1, n) in redb]
out["leftcol_red"] = redb
blueb = comps((b - r > 40) & (b - g > 20) & (b > 120) & (r < 120)[:, :] [:, 55:165] if False else ((b - r > 40) & (b - g > 20) & (b > 120) & (r < 120))[lc, 55:165], 15)
blueb = [(x0+55, x1+55, y0, y1, n) for (x0, x1, y0, y1, n) in blueb]
out["leftcol_blue_text"] = merge_x(blueb, gap=12)

# black strip bottom
strip = ((r < 60) & (g < 60) & (b < 60))[500:540, :]
rows = np.where(strip.mean(axis=1) > 0.5)[0]
out["black_strip_rows_500plus"] = [int(rr)+500 for rr in rows]

# bar colors sampled
def cc(y, x):
    return tuple(int(v) for v in a[y, x])
out["samples"] = {
    "bar_block0": cc(344, 520), "bar_block1": cc(297, 520), "bar_block2": cc(252, 520), "bar_blockM": cc(146, 520),
    "container_fill": cc(220, 200), "container_border": cc(129, 520),
    "tan_fill": cc(430, 520), "cyan_fill": cc(453, 520),
    "title_red": cc(62, 400), "green_arrow": cc(115, 205), "blue_arrow": cc(410, 280),
    "red_arrow": cc(275, 205), "blue_dot": cc(194, 204), "gray_arrow": cc(467, 240),
    "yellow_cell": cc(390, 474), "green_cell": cc(390, 455), "pink_cell": cc(390, 495),
    "word_border": cc(480, 240), "canvas": cc(20, 480), "badge_fill": cc(67, 876),
}

print(json.dumps(out, indent=1, default=int))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide049/measure_full_out.json", "w") as f:
    json.dump(out, f, indent=1, default=int)
