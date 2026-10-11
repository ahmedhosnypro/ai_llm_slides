#!/usr/bin/env python3
"""Measure pass 3: ASCII classification map + targeted samples."""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_012.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = (r * 299 + g * 587 + b * 114) // 1000
sat = np.max(a, axis=2) - np.min(a, axis=2)

print("== targeted samples (5x5 median) ==")
def med(x, y, k=2):
    p = a[max(0,y-k):y+k+1, max(0,x-k):x+k+1].reshape(-1, 3)
    m = np.median(p, axis=0).astype(int)
    return f"#{m[0]:02X}{m[1]:02X}{m[2]:02X}"
for name, x, y in [
    ("page bg empty (right of abstract)", 740, 420),
    ("page bg (below rule)", 250, 130),
    ("page bg (top right)", 740, 100),
    ("rule line", 400, 92),
    ("rule line 2", 500, 91),
    ("title glyph (thick stroke)", 451, 66),
    ("author name glyph", 285, 165),
    ("email glyph", 300, 192),
    ("abstract glyph", 300, 388),
    ("abstract heading region bg", 480, 320),
    ("watermark gray glyph", 122, 400),
    ("left strip tan (no text)", 125, 220),
    ("left strip tan (no text 2)", 125, 200),
]:
    print(f"  {name}: {med(x, y)}")

print("== container border columns: pixel walks ==")
for x in [93, 94, 95, 96, 794, 795, 796, 797]:
    col = a[44:532, x]
    rr = (col[:, 0] - np.maximum(col[:, 1], col[:, 2]) > 50) & (col[:, 0] > 100)
    print(f"  x={x}: redish rows n={int(rr.sum())}, sample y300={med(x,300)} y150={med(x,150)}")
print("== container border rows extent ==")
for y in [52, 53, 524, 525]:
    row = a[y, :]
    rr = np.where((row[:, 0] - np.maximum(row[:, 1], row[:, 2]) > 50) & (row[:, 0] > 100))[0]
    print(f"  y={y}: redish x extent [{rr.min()},{rr.max()}] n={len(rr)}" if len(rr) else f"  y={y}: none")

# ASCII map at 6px cells
print("== ASCII map (6px cells) W=white page G=gray-panel T=tan P=pink R=red K=dark .=other ==")
def classify(x, y):
    pr, pg, pb = np.median(a[y:y+6, x:x+6].reshape(-1, 3), axis=0)
    pl = (pr*299 + pg*587 + pb*114) / 1000
    ps = max(pr, pg, pb) - min(pr, pg, pb)
    if pr > 235 and pg > 235 and pb > 235: return "W"
    if pl < 110: return "K"
    if pr - max(pg, pb) > 45 and pr > 110: return "R"
    if pr > 225 and 140 < pg < 200 and pb > 210: return "P"   # pink/magenta
    if pr > 225 and pg > 195 and 130 < pb < 205: return "T"   # tan
    if 215 < pl < 242 and ps < 14: return "G"
    return "."
for y in range(0, H, 6):
    line = "".join(classify(x, y) for x in range(0, W, 6))
    print(f"{y:3d} {line}")
