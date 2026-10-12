#!/usr/bin/env python3
"""Slide 038 — m18: decisive glyph grids + underline probes + color censuses.
ASCII grids: '#'=dark red/navy ink, '+'=mid, '-'=pale, '.'=white/bg."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)

def grid(x0, x1, y0, y1, label):
    print(f"== {label} (x{x0}..{x1}, y{y0}..{y1}) ==")
    hdr = "     " + "".join(str(x % 10) for x in range(x0, x1 + 1))
    print(hdr)
    for y in range(y0, y1 + 1):
        row = ""
        for x in range(x0, x1 + 1):
            r, g, b = img[y, x]
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            if lum > 215: row += "."
            elif lum > 170: row += "-"
            elif lum > 110: row += "+"
            else: row += "#"
        print(f"y{y:03d} {row}")

# top-row labels: letter+subscript inside peach cell
grid(194, 220, 258, 280, "TOP col1 label")
grid(268, 294, 258, 280, "TOP col2 label")
grid(488, 512, 258, 280, "TOP col5 label")
grid(746, 772, 258, 280, "TOP col7 label")
grid(820, 846, 258, 280, "TOP col8 label")
# mid-row labels
grid(268, 294, 362, 386, "MID col2 label")
grid(746, 772, 362, 386, "MID col7 label")
grid(820, 846, 362, 386, "MID col8 label")
# X-row labels
grid(194, 220, 465, 488, "X col1 label")
grid(746, 772, 465, 488, "X col7 label")
grid(820, 846, 465, 488, "X col8 label")

print("== gray-bar text underline probe: raw rows 312..322 at x340..350 (text zone) vs x230 (bar-only) ==")
for y in range(312, 323):
    print(f"  y={y}: x230={tuple(img[y,230])} x340={tuple(img[y,340])} x345={tuple(img[y,345])} x500={tuple(img[y,500])} x700={tuple(img[y,700])}")

print("== caption underline probe: raw rows 503..512 at x300/x400/x500 ==")
for y in range(503, 513):
    print(f"  y={y}: x300={tuple(img[y,300])} x400={tuple(img[y,400])} x500={tuple(img[y,500])} x530={tuple(img[y,530])}")

print("== y=286 orange-line mystery: raw RGB at y285..288, x=250,400,600,800 ==")
for y in range(284, 289):
    print(f"  y={y}: " + " ".join(f"x{x}={tuple(img[y,x])}" for x in (250, 400, 600, 800)))

print("== mid-row label color census (dark px in label cells y366..382) ==")
for cx0, cx1, lab in ((268, 290, "mid col2"), (746, 770, "mid col7"), (820, 844, "mid col8")):
    seg = img[366:383, cx0:cx1]
    m = (0.299*seg[:,:,0]+0.587*seg[:,:,1]+0.114*seg[:,:,2]) < 120
    px_ = seg[m]
    if len(px_):
        print(f"  {lab}: n={len(px_)} mean=({px_[:,0].mean():.0f},{px_[:,1].mean():.0f},{px_[:,2].mean():.0f})")
    else:
        print(f"  {lab}: no dark px")

print("== top-row label color census (dark px y260..278) col1/col7/col8 ==")
for cx0, cx1, lab in ((194, 220, "top col1"), (746, 772, "top col7"), (820, 846, "top col8")):
    seg = img[260:279, cx0:cx1]
    m = (0.299*seg[:,:,0]+0.587*seg[:,:,1]+0.114*seg[:,:,2]) < 120
    px_ = seg[m]
    if len(px_):
        print(f"  {lab}: n={len(px_)} mean=({px_[:,0].mean():.0f},{px_[:,1].mean():.0f},{px_[:,2].mean():.0f})")

print("== defbox text ink height re-check (blue mask row extents per line) ==")
blue = (B > 110) & (R < 110) & (G < 110)
for lo, hi, lab in ((112, 135, "L1"), (133, 155, "L2"), (152, 172, "L3"), (192, 212, "L4"), (211, 232, "L5")):
    seg = blue[lo:hi, 100:860]
    rows = np.where(seg.sum(axis=1) > 1)[0]
    if len(rows):
        print(f"  {lab}: y {rows.min()+lo}..{rows.max()+lo} (h={rows.max()-rows.min()+1}) -> slide {invy(rows.min()+lo)}..{invy(rows.max()+lo)}")

print("== title cap-height check: red rows x242..776, y66..96, per-row counts ==")
red = (R > 110) & (G < 110) & (B < 110)
for y in range(66, 97):
    n = int(red[y, 242:777].sum())
    if n: print(f"  y={y}: {n}")
