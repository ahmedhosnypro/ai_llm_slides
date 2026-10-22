#!/usr/bin/env python3
"""Closed-loop checker for the 03_ridger_regression_gradient_descent house chrome.

Compares a 150dpi render (2001x1125 for a 13.333x7.5in slide) against the canonical
chrome measured from this video's unique_slides/slide_003.jpg (960x540, 1px=1pt)
and verified constant across slides 001/005/009/018/040. Scale render->frame px: *72/150.

Usage: python3 house_chrome_check.py <render.png> [expected_numeral]
Exit 0 = all checks pass; nonzero = listing of failures.

Checks (tolerance ~8 render-px = ~4 frame-px, the pipeline's closed-loop standard):
  1. panel gray extent (x/y/w) and its bottom reaching the slide bottom
  2. strokes: bottom stroke fully across + left/right strokes at mid-height
     + **NO TOP STROKE** (this deck differs from lecture 02: top must be bare)
  3. badge: yellow circle center/size + purple ring present
"""
import sys

import numpy as np
from PIL import Image

CANON = {  # frame px (960x540, 1px = 1pt), from slide_003.jpg measurement 2026-10-19
    "panel": {"x0": 54, "x1": 903, "y0": 45},          # bottom at slide edge
    "bottom_stroke_row": 538,                            # rows 537-539, half-visible
    "left_stroke_x": 58,                                 # cols 58-59
    "right_stroke_x": 901,
    "badge": {"cx": 876, "cy": 73, "d": 35},
}
TOL = 8  # render px at 150dpi (~4 frame px)


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: house_chrome_check.py <render.png> [expected_numeral]")
    im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(int)
    H, W = im.shape[:2]
    scale = H / 540.0  # render px per frame px (150dpi -> ~2.083)
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
        # gray may legitimately end at the bottom STROKE band (rows ~537-539 on the
        # original: the half-visible red stroke replaces gray there) — self-derivation
        # on slide_003.jpg shows gray to y=536 with the stroke below it.
        if rows.max() < int(cv(536)) - TOL:
            fails.append(f"panel bottom {rows.max()} stops short of the bottom stroke band")

    # 2. strokes: bottom across + left/right at mid-height + NO top stroke.
    # Stroke mask covers BOTH the drawn C00000 and the original's JPEG-darkened
    # maroon cores — left (114,40,51), right (107,47,56), bottom (125,0,19):
    # r>90, R-G>40, R-B>10 matches all three while rejecting gray/yellow/white.
    red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
    bot_band = red[int(cv(533)):, :]
    bc = np.where(bot_band.sum(axis=0) > 1)[0]
    if not len(bc) or bc.min() > cv(70) or bc.max() < cv(890):
        fails.append("bottom red stroke missing/not across")
    mid_y = slice(int(cv(270)) - 20, int(cv(270)) + 20)
    # stroke windows cover the measured stroke x +-3 (learned from 02's latent
    # window bug: a window that stops short of the drawn stroke false-FAILs).
    left_red = red[mid_y, : int(cv(CANON["left_stroke_x"] + 3))].sum()
    right_red = red[mid_y, int(cv(CANON["right_stroke_x"] - 3)):].sum()
    if left_red < 3:
        fails.append("left red border stroke missing at mid-height")
    if right_red < 3:
        fails.append("right red border stroke missing at mid-height")
    # NO TOP STROKE law (measured 0 red px in the top band on 5 frames):
    top_band = red[int(cv(44)): int(cv(52)), int(cv(80)): int(cv(880))]
    if top_band.sum() > 30:
        fails.append(f"TOP STROKE PRESENT ({int(top_band.sum())} red px) — this deck has NO top stroke")

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

    # 4. optional numeral presence check
    if len(sys.argv) > 2 and sys.argv[2] != "":
        numwin = np.s_[int(cy - d / 2): int(cy + d / 2), int(cx - d / 2): int(cx + d / 2)]
        dark = (im[numwin].sum(axis=2) < 300).sum()
        if dark < 12:
            fails.append(f"badge numeral ink too sparse ({int(dark)} px) — numeral '{sys.argv[2]}' missing?")

    if fails:
        print("HOUSE CHROME CHECK: FAIL")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("HOUSE CHROME CHECK: PASS "
          f"(panel x {cols.min()}-{cols.max()}, y {rows.min()}-bottom; "
          f"strokes L/R/bottom present, top bare; "
          f"badge center ({bcx:.0f},{bcy:.0f}) d={bw}; all within tol {TOL})")


if __name__ == "__main__":
    main()
