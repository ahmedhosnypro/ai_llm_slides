#!/usr/bin/env python3
"""Scanline + nearest-palette forensics on slide_011.jpg."""
import numpy as np
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_011.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

PALETTE = {
    "WHITE": (255, 255, 255),
    "PANEL": (233, 233, 231),   # E9E9E7
    "ORANGE": (247, 161, 99),   # F7A163
    "YELLOW": (255, 255, 0),
    "LAV": (214, 214, 242),     # D6D6F2
    "BEIGE": (240, 237, 228),   # F0EDE4
    "GRAY": (191, 191, 191),    # BFBFBF
    "RED": (224, 0, 0),         # E00000 / C00000
    "BLUE": (34, 34, 204),      # 2222CC
    "PINK": (255, 158, 158),    # FF9E9E
    "DARK": (26, 26, 26),
    "OTHER": None,
}

names = list(PALETTE.keys())
cols = np.array([PALETTE[n] if PALETTE[n] else (0, 0, 0) for n in names[:-1]] + [(128, 128, 128)])
flat = a.reshape(-1, 3)
d = np.linalg.norm(flat[:, None, :] - cols[None, :, :], axis=2)
cls = d.argmin(axis=1).reshape(H, W)
# cap assignment: if min distance > 60 -> OTHER
mind = d.min(axis=1).reshape(H, W)
cls[mind > 60] = len(names) - 1

def region(name, tol_idx):
    m = cls == tol_idx
    ys, xs = np.where(m)
    if not len(xs):
        print(f"{name}: none"); return
    print(f"{name}: n={len(xs)} x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
    # row profile: rows with >=20 px
    rc = np.bincount(ys, minlength=H)
    rows = np.where(rc >= 20)[0]
    if len(rows):
        # contiguous runs
        runs = []
        s = p = rows[0]
        for y in rows[1:]:
            if y == p + 1: p = y
            else: runs.append((int(s), int(p))); s = p = y
        runs.append((int(s), int(p)))
        runs = [(s, e) for (s, e) in runs if e - s >= 2]
        for (s, e) in runs:
            band = m[s:e+1, :]
            cbc = band.sum(axis=0)
            ccols = np.where(cbc >= 3)[0]
            if len(ccols):
                print(f"   run y[{s},{e}] h={e-s+1} x[{ccols.min()},{ccols.max()}]")

for n in ["PANEL", "ORANGE", "YELLOW", "LAV", "BEIGE", "GRAY", "RED", "BLUE", "PINK"]:
    region(n, names.index(n))

# scanlines
def scan(row):
    print(f"scanline y={row}: ", end="")
    prev = None; start = 0
    for x in range(W):
        c = names[cls[row, x]]
        if c != prev:
            if prev is not None and x - start > 3:
                print(f"{prev}[{start}-{x-1}]", end=" ")
            prev = c; start = x
    print(f"{prev}[{start}-{W-1}]")

for row in [20, 50, 75, 100, 130, 165, 200, 240, 280, 320, 360, 400, 440, 470, 495, 505, 515, 525, 535, 539]:
    scan(row)
