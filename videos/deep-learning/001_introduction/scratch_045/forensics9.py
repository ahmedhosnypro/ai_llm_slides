#!/usr/bin/env python3
"""forensics9.py — arrow raw-pixel segments + starburst fill grid. Banked to qa/slide045/forensics9_out.txt."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def reddish(px):
    rr, gg, bb = px
    return (rr - gg > 30 and rr - bb > 20 and rr > 100)

print("== ARROW1: raw segment (736,378) -> (692,350), sample every 2px ==")
for t in np.linspace(0, 1, 24):
    x = int(round(736 + t * (692 - 736))); y = int(round(378 + t * (350 - 378)))
    win = im[y-2:y+3, x-2:x+3].reshape(-1, 3)
    best = win[np.argmax(win[:, 0] - win[:, 1])]
    print(f"  ({x},{y}) center={tuple(im[y,x])} reddest-5x5={tuple(best)} reddish={reddish(best)}")

print("\n== ARROW1 alt: horizontal segment (736,364) -> (700,352) ==")
for t in np.linspace(0, 1, 12):
    x = int(round(736 + t * (700 - 736))); y = int(round(364 + t * (352 - 364)))
    win = im[y-2:y+3, x-2:x+3].reshape(-1, 3)
    best = win[np.argmax(win[:, 0] - win[:, 1])]
    print(f"  ({x},{y}) center={tuple(im[y,x])} reddest-5x5={tuple(best)} reddish={reddish(best)}")

print("\n== ARROW2: raw region x676..738 y415..455 — max redness per row ==")
redness = r - (g + b) / 2
for yy in range(415, 456):
    row = redness[yy, 676:739]
    if row.max() > 25:
        xs = np.where(row > 25)[0] + 676
        print(f"  y={yy}: x{xs.min()}..{xs.max()} max_redness={row.max():.0f} at x{xs[np.argmax(row[xs-676])]}")

print("\n== ARROW2 inside panel x600..695 y415..465 — max redness per row ==")
for yy in range(415, 466):
    row = redness[yy, 600:696]
    if row.max() > 30:
        xs = np.where(row > 30)[0] + 600
        print(f"  y={yy}: x{xs.min()}..{xs.max()} max={row.max():.0f}")

print("\n== ARROW1 inside panel x600..695 y330..370 — max redness per row ==")
for yy in range(330, 371):
    row = redness[yy, 600:696]
    if row.max() > 30:
        xs = np.where(row > 30)[0] + 600
        print(f"  y={yy}: x{xs.min()}..{xs.max()} max={row.max():.0f}")

print("\n== STARBURST fill grid (median color per 12px cell) ==")
print("     " + "".join(f"x{c:<14}" for c in range(786, 895, 12)))
for yy in range(50, 152, 12):
    cells = []
    for xx in range(786, 895, 12):
        cell = im[yy:yy+12, xx:xx+12].reshape(-1, 3)
        cells.append(str(tuple(np.median(cell, axis=0).astype(int))))
    print(f"y{yy:<4}" + " ".join(f"{c:>13}" for c in cells))

print("\n== starburst yellow-coverage: count cells dominated by pale-yellow ==")
# pale yellow: r>230,g>215,b<225, r-b>15
py = (r > 230) & (g > 215) & (r - b > 15) & (b < 230)
ys, xs = np.where(py[45:160, 775:905])
if len(ys):
    print(f" pale-yellow bbox: x{xs.min()+775}..{xs.max()+775} y{ys.min()+45}..{ys.max()+45} n={len(ys)}")
    import collections
    print(" row histogram:", {yy: int((py[yy, 775:905]).sum()) for yy in range(45, 160, 8) if py[yy, 775:905].sum()})

print("\n== badge window pollution check (original has no badge, starburst zone) ==")
win = np.s_[35:108, 857:930]
pyw = py[win]
print(f" pale-yellow px in badge window: {pyw.sum()}")
