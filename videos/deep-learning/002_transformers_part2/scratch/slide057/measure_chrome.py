#!/usr/bin/env python3
"""Slide 057 chrome landmarks + global structure (read-only PIL forensics).
Frame: videos/deep-learning/002_transformers_part2/unique_slides/slide_057.jpg (960x540).
House-chrome reference (playlist law, from 001 slide_001):
  white canvas FFFFFF; gray panel E9E9E7 x 42..918, y 45 -> bottom;
  red C00000 border panel left/right/top; badge d~36 centered (893,71),
  fill FDFD96, ring 6A5ACD, numeral 333333.
Outputs (this dir): chrome_landmarks.txt, chrome_landmarks.json
"""
import json, os
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
OUT = os.path.join(BASE, "scratch", "slide057")
im = Image.open(os.path.join(BASE, "unique_slides", "slide_057.jpg")).convert("RGB")
W, H = im.size
px = im.load()
lines = []

def say(s=""):
    lines.append(s)
    print(s)

say(f"FRAME {W}x{H} slide_057.jpg  (1 px = 1 pt at 72dpi mapping: 960px=13.33in)")

# ---------- corner / canvas colors ----------
corners = {"TL": (3, 3), "TR": (W - 4, 3), "BL": (3, H - 4), "BR": (W - 4, H - 4),
           "TL_in": (8, 8), "TR_in": (W - 9, 8), "mid_left_margin": (20, 270),
           "mid_right_margin": (W - 21, 270)}
say("\n== canvas corner samples ==")
corner_rgb = {}
for k, (x, y) in corners.items():
    c = px[x, y]
    corner_rgb[k] = c
    say(f"  {k:16s} ({x:3d},{y:3d}) = #{c[0]:02X}{c[1]:02X}{c[2]:02X}")

# ---------- gray panel bbox ----------
# gray panel ~ E9E9E7 (233,233,231). Find per-column fraction of gray pixels; panel cols are mostly gray (excluding content? panel is the backdrop).
def is_gray(c, tol=10):
    r, g, b = c
    return abs(r - 233) <= tol and abs(g - 233) <= tol and abs(b - 231) <= tol

col_gray = [0] * W
row_gray = [0] * H
for y in range(H):
    for x in range(W):
        if is_gray(px[x, y]):
            col_gray[x] += 1
            row_gray[y] += 1

# panel columns = columns with a substantial gray count; but content covers panel too.
# Instead find LEFT/RIGHT edges: first/last column whose gray count > 200 (out of 540).
panel_cols = [x for x in range(W) if col_gray[x] > 200]
panel_rows = [y for y in range(H) if row_gray[y] > 400]
pl, pr = (panel_cols[0], panel_cols[-1]) if panel_cols else (None, None)
pt, pb = (panel_rows[0], panel_rows[-1]) if panel_rows else (None, None)
say("\n== gray panel E9E9E7 bbox (col_gray>200 / row_gray>400) ==")
say(f"  columns {pl}..{pr}   rows {pt}..{pb}")
say(f"  vs house law: x 42..918, y 45..bottom(538) -> delta L={pl-42 if pl else None} R={pr-918 if pr else None} T={pt-45 if pt else None}")

# red border of panel: scan for saturated red columns near panel edges
def is_red(c):
    r, g, b = c
    return r > 140 and g < 80 and b < 80

red_cols = []
for x in range(W):
    n = sum(1 for y in range(0, H) if is_red(px[x, y]))
    if n > 300:
        red_cols.append((x, n))
say("\n== near-full-height RED columns (panel border candidates) ==")
for x, n in red_cols:
    say(f"  x={x} red_px={n}")

red_rows = []
for y in range(H):
    n = sum(1 for x in range(W) if is_red(px[x, y]))
    if n > 500:
        red_rows.append((y, n))
say("== near-full-width RED rows ==")
for y, n in red_rows:
    say(f"  y={y} red_px={n}")

# panel top red border: scan rows 30..70 for mostly-red spans between x pl..pr
say("\n== panel top border detail: red run-length on rows 30..80 ==")
for y in range(30, 81):
    run = 0; best = 0
    for x in range(W):
        if is_red(px[x, y]):
            run += 1
            best = max(best, run)
        else:
            run = 0
    if best > 400:
        say(f"  y={y}: longest red run {best}")

# ---------- badge ----------
# search top-right for the yellow circle
minx, miny, maxx, maxy, n = 10**9, 10**9, -1, -1, 0
sx = sy = 0
for y in range(0, 140):
    for x in range(W - 160, W):
        r, g, b = px[x, y]
        if r > 210 and g > 190 and b < 130:  # yellowish
            minx = min(minx, x); maxx = max(maxx, x)
            miny = min(miny, y); maxy = max(maxy, y)
            sx += x; sy += y; n += 1
say("\n== slide-number badge (yellowish blob in top-right 160x140) ==")
if n:
    cx, cy = sx / n, sy / n
    bw, bh = maxx - minx + 1, maxy - miny + 1
    say(f"  bbox x {minx}..{maxx} y {miny}..{maxy}  (w={bw} h={bh}) centroid=({cx:.1f},{cy:.1f}) n={n}")
    say(f"  vs house law center (893,71) d~36 -> delta center=({cx-893:+.1f},{cy-71:+.1f}) d={bw} vs 36")
    # ring color: sample the extreme edges of bbox; numeral color: darkest pixel inside
    edge = px[minx + 1, (miny + maxy) // 2]
    # darkest pixel inside central region
    dark = (255, 255, 255); darkpos = None
    for y in range(miny + 4, maxy - 3):
        for x in range(minx + 4, maxx - 3):
            c = px[x, y]
            if sum(c) < sum(dark):
                dark = c; darkpos = (x, y)
    say(f"  ring sample @left edge: #{edge[0]:02X}{edge[1]:02X}{edge[2]:02X}")
    say(f"  darkest inside: #{dark[0]:02X}{dark[1]:02X}{dark[2]:02X} at {darkpos}")
    badge = {"bbox": [minx, miny, maxx, maxy], "center": [round(cx, 1), round(cy, 1)],
             "diam": [bw, bh], "ring": edge, "numeral": dark}
else:
    say("  NO yellowish blob found")
    badge = None

# ---------- black bottom strip ----------
dark_rows = []
for y in range(H):
    n = sum(1 for x in range(0, W, 2) if sum(px[x, y]) < 150)
    if n > (W // 2) * 0.9:
        dark_rows.append(y)
say("\n== black bottom strip (rows >90% dark) ==")
say(f"  rows {dark_rows[0]}..{dark_rows[-1]}" if dark_rows else "  none")

# ---------- left white margin width ----------
# first non-white column from left (excluding red border)
first_content_x = None
for x in range(W):
    for y in range(H):
        c = px[x, y]
        if not (c[0] > 235 and c[1] > 235 and c[2] > 235):
            first_content_x = x; break
    if first_content_x is not None:
        break
say(f"\nfirst non-white pixel column from left: x={first_content_x}")
# top margin likewise
first_content_y = None
for y in range(H):
    for x in range(W):
        c = px[x, y]
        if not (c[0] > 235 and c[1] > 235 and c[2] > 235):
            first_content_y = y; break
    if first_content_y is not None:
        break
say(f"first non-white pixel row from top:    y={first_content_y}")

json.dump({"frame": [W, H], "corners": {k: list(v) for k, v in corner_rgb.items()},
           "panel": {"cols": [pl, pr], "rows": [pt, pb]},
           "badge": badge, "black_rows": [dark_rows[0], dark_rows[-1]] if dark_rows else None,
           "first_ink": [first_content_x, first_content_y]},
          open(os.path.join(OUT, "chrome_landmarks.json"), "w"), indent=1)
open(os.path.join(OUT, "chrome_landmarks.txt"), "w").write("\n".join(lines) + "\n")
print("\nWROTE chrome_landmarks.txt / .json")
