#!/usr/bin/env python3
"""Probe 2 for slide_006.jpg: raw color sampling, glyph extents, 12th bullet."""
import json
from collections import Counter

import numpy as np
from PIL import Image

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
out = {}

def modal_px(region_mask, y0, y1, x0, x1, n=5):
    m = region_mask[y0:y1, x0:x1]
    px = im[y0:y1, x0:x1][m]
    if not len(px):
        return None
    return [[int(v) for v in c] + [int(k)] for c, k in Counter(map(tuple, px)).most_common(n)]

# 1. title color: saturated red pixels (r - max(g,b) > 60)
redish = (r - np.maximum(g, b)) > 60
out["title_modal"] = modal_px(redish, 80, 128, 143, 833)

# 2. box border raw profiles
out["left_border_raw_y300_x84_94"] = [[int(v) for v in im[300, x]] for x in range(84, 95)]
out["top_border_raw_x465_y129_140"] = [[int(v) for v in im[y, 465]] for y in range(129, 141)]
out["bottom_border_raw_x465_y499_510"] = [[int(v) for v in im[y, 465]] for y in range(499, 511)]
out["right_border_raw_y300_x838_848"] = [[int(v) for v in im[300, x]] for x in range(838, 849)]

# 3. bullet blue core: darkest 10% pixels by luma in line 1 and line 11
def dark_modal(y0, y1, x0, x1, frac=0.15):
    reg = im[y0:y1, x0:x1].reshape(-1, 3)
    luma = reg @ [299, 587, 114] / 1000.0
    idx = np.argsort(luma)[: max(1, int(len(luma) * frac))]
    return [[int(v) for v in c] + [1] for c, _ in Counter(map(tuple, reg[idx])).most_common(5)]

out["bullet1_dark"] = dark_modal(197, 213, 205, 312)
out["bullet11_dark"] = dark_modal(459, 475, 205, 522)
out["bullet12_dark"] = dark_modal(483, 500, 175, 350)
out["header_dark"] = dark_modal(140, 187, 100, 800)

# 4. bullet 12 extent: any non-background ink rows 480..502
bg = (abs(r - 255) < 12) & (abs(g - 255) < 12) & (abs(b - 253) < 14)
ink12 = ~bg[480:503, 90:840]
ys, xs = np.where(ink12)
out["bullet12_ink_bbox"] = ([int(xs.min()) + 90, int(ys.min()) + 480, int(xs.max()) + 90, int(ys.max()) + 480] if len(ys) else None)
if len(ys):
    sel = im[480:503, 90:840][ink12]
    out["bullet12_ink_modal"] = [[int(v) for v in c] + [int(k)] for c, k in Counter(map(tuple, sel)).most_common(6)]

# 5. markers raw extent (threshold <170 any channel)
darkish = (r < 170) & (g < 170) & (b < 170)
mrows = darkish[195:210, 172:195]
ys, xs = np.where(mrows)
out["marker1_raw_bbox"] = ([int(xs.min()) + 172, int(ys.min()) + 195, int(xs.max()) + 172, int(ys.max()) + 195] if len(ys) else None)
out["marker1_modal"] = modal_px(darkish, 195, 210, 172, 195, 4)
# marker vertical extent via column through its center
if len(ys):
    cx = int(xs.min()) + 172 + 1
    out["marker_col_raw"] = [[int(v) for v in im[y, cx]] for y in range(196, 210)]

# 6. underline extent: dark run rows 157..162
und = (r < 140) & (g < 140) & (b < 140)
for yy in range(155, 164):
    xs2 = np.where(und[yy, 90:840])[0]
    out.setdefault("underline_rows", []).append([yy, int(xs2.min()) + 90, int(xs2.max()) + 90, len(xs2)] if len(xs2) else [yy, None, None, 0])

# 7. header line extents
def ink_x_extent(y0, y1, thr=120):
    m = (r[y0:y1] < thr) & (g[y0:y1] < thr) & (b[y0:y1] < thr)
    xs3 = np.where(m.sum(axis=0) > 0)[0]
    return [int(xs3.min()), int(xs3.max()), int(len(xs3))] if len(xs3) else None

out["header_line1_x"] = ink_x_extent(140, 158)
out["header_line2_x"] = ink_x_extent(163, 187)
out["header_l1_left_cols"] = [[x, int(und[150, x])] for x in range(95, 130)]

# 8. cap heights: title 'M' (first glyph col range), bullet 'S', header 'B'
def col_extent(x0, x1, y0, y1, mask):
    m = mask[y0:y1, x0:x1]
    ys4, _ = np.where(m)
    return [int(ys4.min()) + y0, int(ys4.max()) + y0] if len(ys4) else None

out["title_M_extent"] = col_extent(143, 175, 80, 128, redish)  # 'M' of Machine
out["bullet_S_extent"] = col_extent(205, 214, 195, 215, (b - np.maximum(r, g)) > 40)  # 'S' of Spam
out["header_B_extent"] = col_extent(96, 108, 135, 165, (r < 120) & (g < 120) & (b < 120))
out["title_row_profile"] = [(int(yy), int(redish[yy, 143:833].sum())) for yy in range(82, 128, 2)]

# 9. gap: box bottom stroke rows vs bullet12
out["box_bottom_rows_raw"] = [[int(v) for v in im[y, 465]] for y in range(500, 508)]

# 10. bullet x-left per line and marker centers (dark cores)
blue = (b > 130) & (r < 130) & (g < 130)
bands = [(197, 212), (223, 239), (250, 265), (276, 290), (302, 313), (328, 343), (355, 366), (382, 392), (406, 422), (433, 445), (459, 474), (483, 500)]
out["line_lefts_blue"] = []
for (a, bb) in bands:
    m = blue[a:bb + 1, :]
    xs5 = np.where(m.sum(axis=0) > 0)[0]
    out["line_lefts_blue"].append([a, int(xs5.min()), int(xs5.max())] if len(xs5) else [a, None, None])

print(json.dumps(out, indent=1))
