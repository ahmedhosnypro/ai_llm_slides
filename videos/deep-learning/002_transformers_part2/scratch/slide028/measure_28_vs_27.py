#!/usr/bin/env python3
"""PIL-measure slide_028.jpg vs slide_027.jpg (parent) — geometry diff for the
dependency-gated build. All coordinates in FRAME px (960x540). The frame->slide
mapping is fitted from each frame's own chrome landmarks (L/R red border cols,
T red border row) per the 002 capture convention: fx = MX + SX*slide_x,
fy = SY*slide_y."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"

def near(img, rgb, tol):
    return (np.abs(img[:, :, 0].astype(int) - rgb[0]) <= tol) & \
           (np.abs(img[:, :, 1].astype(int) - rgb[1]) <= tol) & \
           (np.abs(img[:, :, 2].astype(int) - rgb[2]) <= tol)

def measure(path):
    img = np.array(Image.open(path).convert("RGB"))
    H, W = img.shape[:2]
    out = {"frame": path.split("/")[-1], "size": [W, H]}

    # --- chrome landmarks: red border C00000 columns/rows (strong red, low green/blue)
    red = (img[:, :, 0].astype(int) > 150) & (img[:, :, 1].astype(int) < 70) & (img[:, :, 2].astype(int) < 70)
    colcount = red.sum(axis=0)
    rowcount = red.sum(axis=1)
    # border columns: near-full-height red columns at the panel edges
    border_cols = [x for x in range(W) if colcount[x] > H * 0.7]
    border_rows = [y for y in range(H) if rowcount[y] > W * 0.7]
    out["chrome"] = {
        "border_cols": border_cols[:6] + border_cols[-6:] if len(border_cols) > 12 else border_cols,
        "border_rows": border_rows[:6] + border_rows[-6:] if len(border_rows) > 12 else border_rows,
    }
    L = min(border_cols) if border_cols else None
    R = max(border_cols) if border_cols else None
    T = min(border_rows) if border_rows else None
    out["landmarks"] = {"L": L, "R": R, "T": T}

    # --- circle: pale yellow FBFCC9 (251,252,201)
    circ = near(img, (251, 252, 201), 14)
    ys, xs = np.nonzero(circ)
    if len(xs):
        # largest connected component only
        lab, n = ndimage.label(circ)
        sizes = ndimage.sum(circ, lab, range(1, n + 1))
        big = (np.argmax(sizes) + 1)
        ys, xs = np.nonzero(lab == big)
        out["circle"] = {"x0": int(xs.min()), "x1": int(xs.max()), "y0": int(ys.min()), "y1": int(ys.max()),
                         "cx": float((xs.min() + xs.max()) / 2), "cy": float((ys.min() + ys.max()) / 2),
                         "rx": float((xs.max() - xs.min()) / 2), "ry": float((ys.max() - ys.min()) / 2),
                         "npix": int(len(xs))}

    # --- word chips: mint CCFFCC (204,255,204)
    chip = near(img, (204, 255, 204), 16)
    lab, n = ndimage.label(chip)
    chips = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 400:  # chips ~65x22 = ~1400px; reject specks
            continue
        chips.append({"cx": float((xs.min() + xs.max()) / 2), "cy": float((ys.min() + ys.max()) / 2),
                      "x0": int(xs.min()), "x1": int(xs.max()), "y0": int(ys.min()), "y1": int(ys.max()),
                      "w": int(xs.max() - xs.min() + 1), "h": int(ys.max() - ys.min() + 1), "n": int(len(xs))})
    chips.sort(key=lambda c: (c["cy"], c["cx"]))
    out["chips"] = chips

    # --- arrowheads: orange E06010 (224,96,16)
    ah = near(img, (224, 96, 16), 40)
    lab, n = ndimage.label(ah)
    heads = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 25:
            continue
        heads.append({"cx": float((xs.min() + xs.max()) / 2), "cy": float((ys.min() + ys.max()) / 2),
                      "w": int(xs.max() - xs.min() + 1), "h": int(ys.max() - ys.min() + 1), "n": int(len(xs))})
    heads.sort(key=lambda c: (c["cy"], c["cx"]))
    out["heads"] = heads

    # --- '+w' labels: saturated red CC0000 text OUTSIDE circle & title area
    # strong red but NOT the border cols/rows and not the faded pink spokes
    lbl = (img[:, :, 0].astype(int) > 170) & (img[:, :, 1].astype(int) < 60) & (img[:, :, 2].astype(int) < 60)
    lbl[:, :60] = False           # title zone x
    lbl[:150, :360] = False       # title zone
    if L and R:
        lbl[:, max(0, L - 3):L + 4] = False
        lbl[:, R - 3:R + 4] = False
    if T:
        lbl[T - 3:T + 4, :] = False
    lab, n = ndimage.label(lbl)
    blobs = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 30:
            continue
        blobs.append({"cx": float((xs.min() + xs.max()) / 2), "cy": float((ys.min() + ys.max()) / 2),
                      "x0": int(xs.min()), "x1": int(xs.max()), "y0": int(ys.min()), "y1": int(ys.max()), "n": int(len(xs))})
    out["redblobs"] = blobs

    # --- formula box: FFFFCC (255,255,204) left half
    fb = near(img, (255, 255, 204), 12)
    fb[:, 400:] = False
    lab, n = ndimage.label(fb)
    best, bestn = None, 0
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) > bestn:
            bestn, best = len(xs), (xs.min(), xs.max(), ys.min(), ys.max())
    if best:
        out["formula_box"] = {"x0": int(best[0]), "x1": int(best[1]), "y0": int(best[2]), "y1": int(best[3])}

    # --- title ink: red text rows in x 60..360, y 40..150
    ti = (img[:, :, 0].astype(int) > 150) & (img[:, :, 1].astype(int) < 80) & (img[:, :, 2].astype(int) < 80)
    ti = ti[40:150, 60:360]
    rows = np.nonzero(ti.sum(axis=1) > 2)[0] + 40
    # group into lines
    lines = []
    if len(rows):
        s = rows[0]
        p = rows[0]
        for r in rows[1:]:
            if r - p > 4:
                lines.append([int(s), int(p)])
                s = r
            p = r
        lines.append([int(s), int(p)])
    out["title_lines_y"] = lines

    # --- vertical extent of panel (bottom black bar row)
    dark = (img[:, :, 0].astype(int) < 40) & (img[:, :, 1].astype(int) < 40) & (img[:, :, 2].astype(int) < 40)
    rowdark = dark.sum(axis=1)
    bar_rows = [y for y in range(H) if rowdark[y] > W * 0.8]
    out["black_bar_rows"] = [min(bar_rows), max(bar_rows)] if bar_rows else None
    return out

r27 = measure(f"{BASE}/unique_slides/slide_027.jpg")
r28 = measure(f"{BASE}/unique_slides/slide_028.jpg")
print(json.dumps({"slide_027": r27, "slide_028": r28}, indent=1))
