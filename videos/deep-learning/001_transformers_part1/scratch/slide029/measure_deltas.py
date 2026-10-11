#!/usr/bin/env python3
"""PIL forensics: slide_029.jpg (child) vs slide_026.jpg (parent).
Finds the delta regions (structural re-annotation) and measures them.
960x540 frame, 1px = 1pt = 1/72 in.
"""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
a = Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB")
b = Image.open(f"{V}/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(a, dtype=np.int16)
B = np.asarray(b, dtype=np.int16)
print("sizes:", a.size, b.size)

# --- 1. global diff map: which rows/cols differ structurally
D = (np.abs(A - B).sum(axis=2) > 60)  # significant per-pixel diff
rows = D.sum(axis=1)
cols = D.sum(axis=0)
print("\n== rows with >30 diff px ==")
runs = []
inr = False
for y in range(540):
    if rows[y] > 30 and not inr:
        inr, y0 = True, y
    elif rows[y] <= 30 and inr:
        inr = False
        runs.append((y0, y - 1))
if inr:
    runs.append((y0, 539))
for r in runs:
    ys, ye = r
    band = D[ys:ye + 1]
    c = band.sum(axis=0)
    nz = np.nonzero(c)[0]
    if len(nz):
        # split col runs (gap>25 separates regions)
        segs = []
        s = nz[0]
        p = nz[0]
        for x in nz[1:]:
            if x - p > 25:
                segs.append((s, p))
                s = x
            p = x
        segs.append((s, p))
        print(f"y {ys}..{ye}: " + "  ".join(f"x{s}..{e}" for s, e in segs))

def rgb(img, x, y):
    return tuple(img[y, x])

def avg(img, x0, y0, x1, y1):
    return tuple(np.round(img[y0:y1, x0:x1].reshape(-1, 3).mean(axis=0)).astype(int))

def hexc(t):
    return "%02X%02X%02X" % t

# --- 2. sample key inherited regions in BOTH frames (should match)
print("\n== inherited-region color samples (029 | 026) ==")
for name, (x0, y0, x1, y1) in {
    "canvas mid": (600, 300, 640, 330),
    "left stack fill": (80, 260, 120, 280),
    "dotproduct fill": (270, 220, 300, 240),
    "softmax fill": (465, 250, 480, 270),
    "sigma fill": (560, 200, 600, 213),
    "strip fill": (200, 480, 240, 500),
}.items():
    print(f"{name:18s} {hexc(avg(A,x0,y0,x1,y1))} | {hexc(avg(B,x0,y0,x1,y1))}")

# --- 3. measure NEW elements in slide 29 ---
print("\n== slide-029 new elements ==")

def bbox_of(img, x0, y0, x1, y1, pred):
    reg = img[y0:y1, x0:x1]
    m = pred(reg)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())

# cyan callout fill CCFFFF-ish: g,b high and close, r lower
def cyanish(reg):
    r = reg[:, :, 0].astype(int); g = reg[:, :, 1].astype(int); bl = reg[:, :, 2].astype(int)
    return (bl > 200) & (g > 200) & (bl - r > 30) & (g - r > 30)

print("callout1 bbox:", bbox_of(A, 100, 130, 560, 260, cyanish))
print("callout2 bbox:", bbox_of(A, 520, 130, 940, 260, cyanish))
# also in parent for reference (should be none)
print("callout bbox in 026 (expect None/None):", bbox_of(B, 100, 130, 940, 260, cyanish))

# orange Query box FAC090-ish: r high, g mid, b lower
def orangish(reg):
    r = reg[:, :, 0].astype(int); g = reg[:, :, 1].astype(int); bl = reg[:, :, 2].astype(int)
    return (r > 220) & (r - bl > 40) & (g - bl > 30) & (g > 150) & (g < 220)

print("querybox bbox:", bbox_of(A, 80, 400, 560, 470, orangish))
print("querybox in 026 (expect None):", bbox_of(B, 80, 400, 560, 470, orangish))

# result box: white fill + blue border, bottom right; find blue 0000CC-ish pixels
def blueish(reg):
    r = reg[:, :, 0].astype(int); g = reg[:, :, 1].astype(int); bl = reg[:, :, 2].astype(int)
    return (bl > 140) & (bl - r > 60) & (bl - g > 50)

print("resultbox blue bbox:", bbox_of(A, 500, 410, 900, 530, blueish))
print("resultbox white interior avg:", hexc(avg(A, 600, 440, 740, 470)))

# K / V / Q badges: solid red circles C00000-ish
def redish(reg):
    r = reg[:, :, 0].astype(int); g = reg[:, :, 1].astype(int); bl = reg[:, :, 2].astype(int)
    return (r > 140) & (r - g > 70) & (r - bl > 70)

print("K badge bbox (left stack right side):", bbox_of(A, 130, 220, 220, 420, redish))
print("K badge in 026 (expect None):", bbox_of(B, 130, 220, 220, 420, redish))
print("V badge bbox (right stack left side):", bbox_of(A, 700, 220, 780, 420, redish))
print("V badge in 026 (expect None):", bbox_of(B, 700, 220, 780, 420, redish))
print("Q badge bbox (right of query box):", bbox_of(A, 400, 400, 560, 470, redish))
print("Q badge in 026 (expect None):", bbox_of(B, 400, 400, 560, 470, redish))

# title region: yellow highlight (FBF29B-ish / FFFF00-ish)
def yellowish(reg):
    r = reg[:, :, 0].astype(int); g = reg[:, :, 1].astype(int); bl = reg[:, :, 2].astype(int)
    return (r > 215) & (g > 205) & (bl < 190) & (r - bl > 40)

print("title yellow bbox 029:", bbox_of(A, 100, 40, 900, 80, yellowish))
print("title yellow bbox 026:", bbox_of(B, 100, 40, 900, 80, yellowish))
