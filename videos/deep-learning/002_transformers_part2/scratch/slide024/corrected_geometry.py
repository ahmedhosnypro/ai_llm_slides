#!/usr/bin/env python3
"""Corrected final geometry: mapping Sx=(fx-17.628)/0.961231, Sy=fy/0.955556.
Recompute all delta elements + measure frame23's box border cols for comparison."""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
img24 = np.asarray(Image.open(f"{V}/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
img23 = np.asarray(Image.open(f"{V}/unique_slides/slide_023.jpg").convert("RGB")).astype(int)

def Sx(fx): return (fx - 17.628) / 0.961231
def Sy(fy): return fy / 0.955556
def Fx(sv): return 17.628 + 0.961231 * sv

# frame23 box border cols (scan row 430 — text-free zone? use row 360 like before)
for name, img in (("f23", img23), ("f24", img24)):
    row = img[360]
    darks = [x for x in range(40, 930) if row[x][2] < 190 and row[x][2] > row[x][0] + 20]
    print(f"{name} row360 blue-dark cols: {darks[:8]}...{darks[-8:] if len(darks)>8 else ''}")
    # left border core = min col cluster, right = max cluster
    if darks:
        print(f"   left core ~{darks[0]}-{darks[min(3,len(darks)-1)]}  right core ~{darks[-4:]}")

print("\n=== corrected slide-coord geometry (Sx=(fx-17.628)/0.961231, Sy=fy/0.955556) ===")
print(f"subtitle yellow strip: fx 301..741 fy 81..107 -> x {Sx(301):.1f}..{Sx(741):.1f} (w {Sx(741)-Sx(301):.1f}) y {Sy(81):.1f}..{Sy(107):.1f} (h {Sy(107)-Sy(81):.1f})")
print(f"subtitle ink:          fx 295..746 fy 86..105 -> x {Sx(295):.1f}..{Sx(746):.1f} (w {Sx(746)-Sx(295):.1f}) y {Sy(86):.1f}..{Sy(105):.1f} (h {Sy(105)-Sy(86):.1f}) center {(Sx(295)+Sx(746))/2:.1f}")
print(f"rules box border: left core ~74.5 right ~886 top core 349 bottom core 502")
print(f"   -> x {Sx(74.5):.1f}..{Sx(886):.1f} (w {Sx(886)-Sx(74.5):.1f}) y {Sy(349):.1f}..{Sy(502):.1f} (h {Sy(502)-Sy(349):.1f})")
print(f"   parent certified box: x 54.5..907.6 y 363.9..525.9 (w 853.1 h 162.0)")
print(f"   -> frame cols fx {Fx(54.5):.1f}..{Fx(907.6):.1f} rows fy {0.955556*363.9:.1f}..{0.955556*525.9:.1f}")

# text lines: band tops/lefts (from earlier scans) with corrected mapping
bands = [
    ("L1", 363, 386, 79, 640),   # frame x extremes measured: ink fx 79.1..639.6?? recompute from slide: L1 ink 63.9..611.4 was WRONG mapping
]
# Recompute line ink extents with correct mapping from frame measurements:
# earlier measured (wrong map) slide values -> recompute from frame:
# L1 ink frame x: from word scan: Sx_old(63.9)=fx?? I need raw frame extents. Re-scan here:
def line_extent(img, y0, y1, x0=78, x1=884):
    reg = img[y0:y1, x0:x1]
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    ink = ((b > 100) & (b > r + 30)) | ((r > 110) & (r > b + 40) & (g < r - 30))
    cols = np.where(ink.any(axis=0))[0]
    rows = np.where(ink.any(axis=1))[0]
    return cols[0] + x0, cols[-1] + x0, rows[0] + y0, rows[-1] + y0

LINES = [
    ("L1", 363, 386), ("L2", 386, 408), ("L3", 408, 431),
    ("L4", 430, 452), ("L5", 452, 474), ("L6", 474, 496),
]
for tag, y0, y1 in LINES:
    fx0, fx1, fy0, fy1 = line_extent(img24, y0, y1)
    print(f"{tag}: ink frame x {fx0}..{fx1} y {fy0}..{fy1} -> slide x {Sx(fx0):.1f}..{Sx(fx1):.1f} (w {Sx(fx1)-Sx(fx0):.1f}) y {Sy(fy0):.1f}..{Sy(fy1):.1f}")
