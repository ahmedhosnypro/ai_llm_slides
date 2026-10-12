#!/usr/bin/env python3
"""Chrome landmark + content measurement for slide_060 (960x540 frame, 1 frame px ~ 1pt * scale).

Landmarks (playlist chrome, from shared_patterns/house_chrome.js TRUE slide coords):
  panel left border x=42, right border x=918(+1), top border y=45, bottom stroke rows 538-539
  badge circle d=36 center (893,71) in slide pts.
Fit frame = a + s * slide (x and y separately) from the four red border landmarks,
cross-check with badge bbox center. Then measure content ink and map to slide pts.
"""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_060.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide060"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()

def reddish(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50

def blueish(p):
    r, g, b = p
    return b > 110 and (b - r) > 40 and (b - g) > 30

out = {"size": (W, H)}

# ---- red border columns/rows (chrome landmarks)
red_cols = [(x, sum(1 for y in range(0, H, 2) if reddish(px[x, y]))) for x in range(W)]
red_cols = [c for c in red_cols if c[1] > 40]
red_rows = [(y, sum(1 for x in range(0, W, 2) if reddish(px[x, y]))) for y in range(H)]
red_rows = [r for r in red_rows if r[1] > 60]
out["red_cols"] = red_cols
out["red_rows"] = red_rows

# ---- black letterbox strip
blk_rows = [y for y in range(H) if all(sum(px[x, y]) < 160 for x in (100, 300, 500, 700, 900))]
out["black_strip_rows"] = (min(blk_rows), max(blk_rows)) if blk_rows else None

# ---- badge bbox: non-white, non-panel, non-red-border px in top-right region
pts = []
for y in range(30, 130):
    for x in range(820, 955):
        r, g, b = px[x, y]
        if reddish((r, g, b)):
            continue
        if abs(r - 233) < 20 and abs(g - 233) < 20 and abs(b - 231) < 20:
            continue
        if r > 242 and g > 242 and b > 242:
            continue
        pts.append((x, y))
if pts:
    bx0, by0 = min(p[0] for p in pts), min(p[1] for p in pts)
    bx1, by1 = max(p[0] for p in pts), max(p[1] for p in pts)
    out["badge_bbox"] = (bx0, by0, bx1, by1)
    out["badge_center"] = ((bx0 + bx1) / 2, (by0 + by1) / 2)
    out["badge_wh"] = (bx1 - bx0 + 1, by1 - by0 + 1)
    dark = [(x, y) for (x, y) in pts if sum(px[x, y]) < 330]
    if dark:
        out["badge_numeral_bbox"] = (min(d[0] for d in dark), min(d[1] for d in dark),
                                     max(d[0] for d in dark), max(d[1] for d in dark))

# ---- mapping fit: frame landmarks <-> slide pts
# left border: red column(s) near left; right: near right; top: red row near top
lm = {}
if red_cols:
    left = [c for c in red_cols if c[0] < 100]
    right = [c for c in red_cols if c[0] > 850]
    lm["left_cols"] = [c[0] for c in left]
    lm["right_cols"] = [c[0] for c in right]
if red_rows:
    top = [r for r in red_rows if r[0] < 80]
    bot = [r for r in red_rows if r[0] > 480]
    lm["top_rows"] = [r[0] for r in top]
    lm["bot_rows"] = [r[0] for r in bot]
out["landmarks"] = lm

# slide-side values: border stroke center at x=42 means the border LINE straddles 42
# (rect edge). For fitting use stroke center vs slide edge value.
# From slide_002 fit: frame_x = 18.63 + 0.96123*slide_x ; frame_y = 0.95556*slide_y
# Recompute independently:
if red_cols and red_rows:
    fx_l = sum(lm["left_cols"]) / len(lm["left_cols"])
    fx_r = sum(lm["right_cols"]) / len(lm["right_cols"])
    fy_t = sum(lm["top_rows"]) / len(lm["top_rows"])
    fy_b = sum(lm["bot_rows"]) / len(lm["bot_rows"])
    # slide landmarks: left 42, right 918(+1 edge ~918.5), top 45, bottom stroke 538.5
    sx = (fx_r - fx_l) / (918.5 - 42.0)
    ix = fx_l - sx * 42.0
    sy = (fy_b - fy_t) / (538.5 - 45.0)
    iy = fy_t - sy * 45.0
    out["fit"] = {"sx": sx, "ix": ix, "sy": sy, "iy": iy,
                  "fx_l": fx_l, "fx_r": fx_r, "fy_t": fy_t, "fy_b": fy_b}
    # badge cross-check
    if "badge_center" in out:
        bx, by = out["badge_center"]
        mx = (bx - ix) / sx
        my = (by - iy) / sy
        out["badge_mapped_to_slide"] = (mx, my)
        out["badge_delta_vs_house"] = (mx - 893.0, my - 71.0)

def to_slide_x(fx): return (fx - out["fit"]["ix"]) / out["fit"]["sx"]
def to_slide_y(fy): return (fy - out["fit"]["iy"]) / out["fit"]["sy"]

# ---- content ink: title (red) rows between top border and box top
rows = {}
for y in range(int(fy_t) + 4, H - 4):
    xs = [x for x in range(int(fx_l) + 4, int(fx_r) - 3) if reddish(px[x, y])]
    if xs:
        rows[y] = (min(xs), max(xs))
# group into lines
lines = []
cur = None
for y in sorted(rows):
    if cur and y <= cur[1] + 3:
        cur[1] = y
        cur[2].append(rows[y])
    else:
        cur = [y, y, [rows[y]]]
        lines.append(cur)
red_lines = []
for y0, y1, seg in lines:
    xs0 = min(s[0] for s in seg); xs1 = max(s[1] for s in seg)
    red_lines.append({"fy": (y0, y1), "fx": (xs0, xs1),
                      "slide_y": (round(to_slide_y(y0), 1), round(to_slide_y(y1), 1)),
                      "slide_x": (round(to_slide_x(xs0), 1), round(to_slide_x(xs1), 1))})
out["red_ink_lines"] = red_lines

# ---- blue ink lines (box border will be a tall run; text lines short runs)
brows = {}
for y in range(int(fy_t) + 4, H - 4):
    xs = [x for x in range(int(fx_l) + 4, int(fx_r) - 3) if blueish(px[x, y])]
    if xs:
        brows[y] = (min(xs), max(xs))
blines = []
cur = None
for y in sorted(brows):
    if cur and y <= cur[1] + 3:
        cur[1] = y
        cur[2].append(brows[y])
    else:
        cur = [y, y, [brows[y]]]
        blines.append(cur)
blue_lines = []
for y0, y1, seg in blines:
    xs0 = min(s[0] for s in seg); xs1 = max(s[1] for s in seg)
    blue_lines.append({"fy": (y0, y1), "fx": (xs0, xs1), "n_rows": y1 - y0 + 1,
                       "slide_y": (round(to_slide_y(y0), 1), round(to_slide_y(y1), 1)),
                       "slide_x": (round(to_slide_x(xs0), 1), round(to_slide_x(xs1), 1))})
out["blue_ink_lines"] = blue_lines

# ---- color census: sample regions
def census(x0, y0, x1, y1, key):
    from collections import Counter
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = px[x, y]
            c[(p[0] // 8 * 8, p[1] // 8 * 8, p[2] // 8 * 8)] += 1
    return [(k, v) for k, v in c.most_common(key)]

out["census_title"] = None
if red_lines:
    L = red_lines[0]
    out["census_title"] = census(L["fx"][0], L["fy"][0], L["fx"][1] + 1, L["fy"][1] + 1, 6)

# box border color: strongest blue line
boxb = max(blue_lines, key=lambda L: L["n_rows"]) if blue_lines else None
out["box_border_line"] = boxb
if boxb:
    y0, y1 = boxb["fy"]
    x0, x1 = boxb["fx"]
    out["census_boxborder"] = census(x0, y0, x1 + 1, y1 + 1, 6)

with open(f"{OUT}/measure1_out.json", "w") as f:
    json.dump(out, f, indent=1, default=str)
for k in ("size", "red_cols", "red_rows", "black_strip_rows", "badge_bbox", "badge_center",
          "badge_wh", "badge_numeral_bbox", "landmarks", "fit", "badge_mapped_to_slide",
          "badge_delta_vs_house"):
    print(k, "=", out.get(k))
print("--- red lines ---")
for L in red_lines:
    print(L)
print("--- blue lines (first 30) ---")
for L in blue_lines[:30]:
    print(L)
print("census_title", out["census_title"])
print("census_boxborder", out["census_boxborder"])
