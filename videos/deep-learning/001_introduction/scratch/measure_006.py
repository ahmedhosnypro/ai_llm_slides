#!/usr/bin/env python3
"""PIL ink forensics for slide_006.jpg (960x540, 1px = 1pt)."""
import json
from collections import Counter

import numpy as np
from PIL import Image

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

red = (r > 130) & (g < 100) & (b < 100)
blue = (b > 130) & (r < 130) & (g < 130)
black = (r < 90) & (g < 90) & (b < 90)

def bbox(mask, y0=0, y1=None, x0=0, x1=None):
    m = mask[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if not len(ys):
        return None
    return [int(xs.min()) + x0, int(ys.min()) + y0, int(xs.max()) + x0, int(ys.max()) + y0]

def modal(mask, y0, y1, x0, x1):
    m = mask[y0:y1, x0:x1]
    px = im[y0:y1, x0:x1][m]
    if not len(px):
        return None
    c = Counter(map(tuple, px))
    return [[int(v) for v in col] + [int(n)] for col, n in c.most_common(3)]

out = {}

# ---- title (red ink, y 40..130) ----
tb = bbox(red, 40, 130)
out["title_bbox"] = tb
out["title_modal"] = modal(red, 40, 130, tb[0], tb[1 + 2]) if tb else None
# per-row red ink for cap height
trows = np.where(red[40:130, :].sum(axis=1) > 0)[0] + 40
out["title_rows"] = [int(trows.min()), int(trows.max())]
tcols = np.where(red[40:130, :].sum(axis=0) > 0)[0]
out["title_cols"] = [int(tcols.min()), int(tcols.max())]

# ---- content box border (red ink, y 130..520) ----
# horizontal strokes: rows where red count is large
rowcounts = red[125:525, :].sum(axis=1)
hrows = [int(i) + 125 for i, c in enumerate(rowcounts) if c > 300]
out["box_h_stroke_rows"] = hrows
colcounts = red[150:500, :].sum(axis=0)
vcols = [int(i) for i, c in enumerate(colcounts) if c > 200]
out["box_v_stroke_cols"] = vcols
if hrows and vcols:
    y_top, y_bot = min(hrows), max(hrows)
    x_l, x_r = min(vcols), max(vcols)
    out["box"] = [x_l, y_top, x_r, y_bot]
    out["box_border_modal_top"] = modal(red, y_top - 2, y_top + 4, x_l + 50, x_r - 50)
    out["box_border_modal_left"] = modal(red, 200, 400, x_l - 2, x_l + 4)
    # stroke thickness at left border mid-height
    seg = red[300, max(0, x_l - 4): x_l + 6]
    out["left_stroke_profile_y300"] = [int(v) for v in seg]
    segt = red[ :, x_l + 1][y_top - 4: y_top + 8]
    out["top_stroke_profile_x_mid"] = [int(v) for v in red[y_top - 4: y_top + 8, (x_l + x_r) // 2]]

# ---- inside the box: black (header) and blue (bullets) ink ----
if hrows and vcols:
    ix0, ix1, iy0, iy1 = x_l + 4, x_r - 4, y_top + 4, y_bot - 4
    # black ink rows inside box
    rows_black = black[iy0:iy1, ix0:ix1].sum(axis=1)
    out["black_rows_profile_first40"] = [(int(i) + iy0, int(c)) for i, c in enumerate(rows_black[:60]) if c > 0]
    hbands = []
    s = None
    for i, c in enumerate(rows_black):
        if c > 0 and s is None:
            s = i
        elif c == 0 and s is not None:
            hbands.append((s + iy0, i - 1 + iy0)); s = None
    if s is not None:
        hbands.append((s + iy0, iy1 - 1))
    out["black_bands"] = hbands
    # underline detection: thin dark band with wide horizontal extent under first header line
    for (a, bb) in hbands:
        m = black[a:bb + 1, ix0:ix1]
        widths = m.sum(axis=1)
        out.setdefault("black_band_widths", []).append({"band": [a, bb], "max_run_row_width": int(widths.max())})
    # blue ink bands (bullets)
    rows_blue = blue[iy0:iy1, ix0:ix1].sum(axis=1)
    bbands = []
    s = None
    for i, c in enumerate(rows_blue):
        if c > 2 and s is None:
            s = i
        elif c <= 2 and s is not None:
            bbands.append((s + iy0, i - 1 + iy0)); s = None
    if s is not None:
        bbands.append((s + iy0, iy1 - 1))
    out["blue_band_count"] = len(bbands)
    out["blue_bands"] = []
    for (a, bb) in bbands:
        m = blue[a:bb + 1, :]
        ys, xs = np.where(m)
        out["blue_bands"].append({
            "rows": [a, bb], "x": [int(xs.min()), int(xs.max())],
        })
    out["blue_modal"] = modal(blue, bbands[0][0], bbands[0][1], 100, 800) if bbands else None
    # black markers: black ink left of x=200 inside box, below header
    if bbands:
        first_blue = bbands[0][0]
        mrows = black[first_blue - 5: iy1, : 200]
        ys, xs = np.where(mrows)
        if len(ys):
            # cluster by rows
            yy = sorted(set(ys.tolist()))
            clusters = []
            s = p = yy[0]
            for v in yy[1:]:
                if v <= p + 2:
                    p = v
                else:
                    clusters.append((s, p)); s = p = v
            clusters.append((s, p))
            out["marker_clusters_rows"] = [[int(a) + first_blue - 5, int(bb) + first_blue - 5] for a, bb in clusters]
            mc = []
            for (a, bb) in clusters:
                sub = mrows[a:bb + 1]
                ys2, xs2 = np.where(sub)
                mc.append({"rows": [int(a) + first_blue - 5, int(bb) + first_blue - 5],
                           "x": [int(xs2.min()), int(xs2.max())]})
            out["marker_boxes"] = mc

# ---- footer strip ----
rows_black_full = black[:, 100:900].sum(axis=1)
frows = [int(i) for i, c in enumerate(rows_black_full) if c > 500]
out["footer_rows"] = [min(frows), max(frows)] if frows else None
if frows:
    y0 = min(frows)
    xs = np.where(black[y0 + 2, :])[0]
    out["footer_x"] = [int(xs.min()), int(xs.max())] if len(xs) else None

# ---- background samples ----
out["bg_outside_box"] = [im[300, 20].tolist(), im[20, 480].tolist()]
out["bg_inside_box"] = [im[300, 480].tolist()]
out["panel_sample_left_of_box"] = im[300, 60].tolist()

# ---- canvas/panel chrome measured on THIS frame ----
grayish = (abs(r - 233) < 20) & (abs(g - 233) < 20) & (abs(b - 231) < 22)
row300 = grayish[300]
out["gray_cols_y300"] = [int(np.where(row300)[0].min()), int(np.where(row300)[0].max())] if row300.any() else None
col480 = grayish[:, 480]
out["gray_rows_x480"] = [int(np.where(col480)[0].min()), int(np.where(col480)[0].max())] if col480.any() else None

print(json.dumps(out, indent=1))
