#!/usr/bin/env python3
"""Closed-loop checker for the Deep Learning DSAI 308 playlist house chrome.

Compares a 150dpi render (2000x1125 for a 13.333x7.5in slide) against the canonical
chrome measured from videos/deep-learning/001_transformers_part1/unique_slides/
slide_001.jpg (960x540, 1px=1pt). Scale render->frame px: *72/150 (*0.48).

Usage: python3 house_chrome_check.py <render.png> [expected_numeral]
Exit 0 = all checks pass; nonzero = listing of failures.

Checks (tolerance ~8 render-px = ~4 frame-px, the pipeline's closed-loop standard):
  1. panel gray extent (x/y/w) and its bottom reaching the slide bottom
  2. red border presence: bottom stroke fully across + left/right/top strokes
  3. badge: yellow circle center/size + purple ring present
"""
import sys

import numpy as np
from PIL import Image

CANON = {  # frame px (960x540, 1px = 1pt), from slide_001.jpg measurement 2026-10-11
    "panel": {"x0": 42, "x1": 918, "y0": 45},          # bottom at slide edge
    "border_row_bottom": 538,                            # red stroke rows 538-539
    "badge": {"cx": 893, "cy": 71, "d": 36},
}
TOL = 8  # render px at 150dpi (~4 frame px)


def runs(idx):
    out = []
    s = p = None
    for i in idx:
        if s is None:
            s = p = i
        elif i == p + 1:
            p = i
        else:
            out.append((s, p))
            s = p = i
    if s is not None:
        out.append((s, p))
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: house_chrome_check.py <render.png> [expected_numeral]")
    im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
    H, W = im.shape[:2]
    scale = H / 540.0  # render px per frame px (150dpi/960-wide frame -> ~2.083)
    fails = []

    def cv(v):  # canonical frame px -> render px
        return v * scale

    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

    # 1. panel gray extent (sample text-free bands)
    gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
    band_rows = slice(int(cv(CANON["panel"]["y0"])) + 20, int(cv(535)) - 10)
    cols = np.where(gray[band_rows].sum(axis=0) > (band_rows.stop - band_rows.start) * 0.5)[0]
    if not len(cols):
        fails.append("panel: no gray columns found")
    else:
        if abs(cols.min() - cv(CANON["panel"]["x0"])) > TOL:
            fails.append(f"panel left {cols.min()} vs {cv(CANON['panel']['x0']):.0f} (tol {TOL})")
        if abs(cols.max() - cv(CANON["panel"]["x1"])) > TOL:
            fails.append(f"panel right {cols.max()} vs {cv(CANON['panel']['x1']):.0f} (tol {TOL})")
    band_cols = slice(int(cv(CANON["panel"]["x0"])) + 20, int(cv(CANON["panel"]["x0"])) + 120)
    rows = np.where(gray[:, band_cols].sum(axis=1) > (band_cols.stop - band_cols.start) * 0.5)[0]
    if not len(rows):
        fails.append("panel: no gray rows found in left band")
    else:
        if abs(rows.min() - cv(CANON["panel"]["y0"])) > TOL:
            fails.append(f"panel top {rows.min()} vs {cv(CANON['panel']['y0']):.0f} (tol {TOL})")
        if rows.max() < H - int(3 * scale):
            fails.append(f"panel bottom {rows.max()} does not reach slide bottom {H}")

    # 2. red border: bottom stroke across + side strokes
    red = (r > 120) & (g < 110) & (b < 110)
    bot_band = red[int(cv(533)):, :]
    bc = np.where(bot_band.sum(axis=0) > 1)[0]
    if not len(bc) or bc.min() > cv(60) or bc.max() < cv(900):
        fails.append("bottom red stroke missing/not across")
    mid_y = slice(int(cv(270)) - 20, int(cv(270)) + 20)
    left_red = red[mid_y, : int(cv(60))].sum()
    right_red = red[mid_y, int(cv(900)):].sum()
    if left_red < 3:
        fails.append("left red border stroke missing at mid-height")
    if right_red < 3:
        fails.append("right red border stroke missing at mid-height")

    # 3. badge (yellow disc + purple ring) near canonical center
    cx, cy, d = (cv(CANON["badge"][k]) for k in ("cx", "cy", "d"))
    win = np.s_[int(cy - d): int(cy + d), int(cx - d): int(cx + d)]
    wr, wg, wb = r[win], g[win], b[win]
    yel = (wr > 200) & (wg > 200) & (wb < 190)
    pys, pxs = np.where(yel)
    if not len(pys):
        fails.append("badge: no yellow disc found")
    else:
        bcx = win[1].start + (pxs.min() + pxs.max()) / 2
        bcy = win[0].start + (pys.min() + pys.max()) / 2
        if abs(bcx - cx) > TOL or abs(bcy - cy) > TOL:
            fails.append(f"badge center ({bcx:.0f},{bcy:.0f}) vs ({cx:.0f},{cy:.0f}) (tol {TOL})")
        bw = pxs.max() - pxs.min() + 1
        if abs(bw - d) > 1.5 * TOL:
            fails.append(f"badge diameter {bw} vs {d:.0f} (tol {1.5*TOL})")
    pur = (wb > 150) & (wr > 70) & (wr < 180) & (wg < 130)
    if pur.sum() < 10:
        fails.append("badge purple ring missing/faint")

    if fails:
        print("HOUSE CHROME CHECK: FAIL")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("HOUSE CHROME CHECK: PASS "
          f"(panel x {cols.min()}-{cols.max()}, y {rows.min()}-bottom; "
          f"badge center ({bcx:.0f},{bcy:.0f}) d={bw}; all within tol {TOL})")


if __name__ == "__main__":
    main()
