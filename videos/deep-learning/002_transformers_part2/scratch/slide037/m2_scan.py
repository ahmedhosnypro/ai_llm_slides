#!/usr/bin/env python3
"""m2_scan.py — precise element measurements on 002:37 frame (960x540, 1px=1pt)."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg"
img = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W, _ = img.shape

def near(rgb, tol):
    return (np.abs(img - np.array(rgb)).sum(axis=2) <= tol)

def bbox(mask, label, x0=0, x1=W, y0=0, y1=H):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        print(f"{label}: EMPTY in [{x0},{x1})x[{y0},{y1})")
        return
    print(f"{label}: x {x0+xs.min()}-{x0+xs.max()} y {y0+ys.min()}-{y0+ys.max()} n={len(xs)} cx={x0+xs.mean():.1f} cy={y0+ys.mean():.1f}")

# --- title (top-left, exclude badge & architecture): red ink y40-100 x60-600
red = near((204, 0, 0), 100) | near((210, 40, 40), 70)
bbox(red, "TITLE red", 60, 600, 40, 100)
rowc = red[:100, 60:600].sum(axis=1)
bands = []
s = None
for i, v in enumerate(rowc):
    if v > 2 and s is None: s = i
    elif v <= 2 and s is not None: bands.append((s, i-1)); s = None
if s is not None: bands.append((s, 99))
print("TITLE row bands (y<100):", [b for b in bands if b[1]-b[0] > 2])

# --- badge: yellow FDFD96
badge = near((253, 253, 150), 45)
bbox(badge, "BADGE yellow", 820, 960, 30, 120)

# --- left box borders: green mask along columns x=140 and x=100
green = near((46, 125, 50), 110) | near((27, 114, 63), 110) | near((20, 130, 30), 110)
for cx in (90, 140, 190):
    col = green[:, cx]
    runs = []
    s = None
    for y, v in enumerate(col):
        if v and s is None: s = y
        elif not v and s is not None:
            if y - s >= 2: runs.append((s, y-1))
            s = None
    print(f"GREEN runs col x={cx}:", runs)
for cx in (330, 400, 480):
    col = green[:, cx]
    runs = []
    s = None
    for y, v in enumerate(col):
        if v and s is None: s = y
        elif not v and s is not None:
            if y - s >= 2: runs.append((s, y-1))
            s = None
    print(f"GREEN runs col x={cx}:", runs)
for cy in (250, 300, 400, 480):
    row = green[cy, :]
    runs = []
    s = None
    for x, v in enumerate(row):
        if v and s is None: s = x
        elif not v and s is not None:
            if x - s >= 2: runs.append((s, x-1))
            s = None
    print(f"GREEN runs row y={cy}:", runs)

# --- left box interior fill mode
from collections import Counter
sub = img[300:480, 90:190].reshape(-1, 3)
print("LEFT box interior mode:", Counter(map(tuple, sub)).most_common(3))
sub = img[300:480, 320:500].reshape(-1, 3)
print("CENTER box interior mode:", Counter(map(tuple, sub)).most_common(3))

# --- architecture panels
peach = near((251, 229, 214), 26)
mint = near((206, 255, 224), 26)
bbox(peach, "PEACH panel", 560, 900, 95, 515)
bbox(mint, "MINT panel", 560, 900, 95, 515)
sub = img[460:500, 745:870].reshape(-1, 3)
print("DEC panel low mode:", Counter(map(tuple, sub)).most_common(3))

# --- red highlight circle + yellow glow (region around encoder MHA)
hlred = near((210, 47, 47), 70) | near((190, 30, 30), 70)
bbox(hlred, "HL circle red", 590, 760, 230, 420)
glow = near((255, 217, 102), 60)
bbox(glow, "GLOW yellow", 590, 780, 230, 420)

# --- pin (red balloon) above the circle
bbox(hlred, "PIN red", 560, 780, 130, 240)

# --- white WE ARE HERE text inside pin
wt = near((255, 255, 255), 40)
bbox(wt, "PIN white text", 600, 700, 150, 215)

# --- title/header texts in diagrams (red italic)
bbox(red, "LEFT hdr", 55, 230, 195, 245)
bbox(red, "CENTER hdr", 280, 530, 200, 240)

# --- encoder/decoder labels
bbox(red, "ENC label", 575, 700, 105, 140)
bbox(red, "DEC label", 800, 895, 105, 140)

# --- orange boxes
orange = near((232, 163, 61), 55)
bbox(orange, "ORANGE all", 560, 900, 95, 515)

# --- tan boxes
tan = near((201, 166, 107), 55)
bbox(tan, "TAN all", 560, 900, 95, 515)

# --- Nx circle: gray A6A6A6
ggray = near((166, 166, 166), 45)
bbox(ggray, "Nx gray circle", 815, 885, 270, 360)

# --- decoder-stack region scan rows (through the arch, fine classes)
def cls(p):
    r, g, b = p
    def d(rgb): return abs(int(r)-rgb[0])+abs(int(g)-rgb[1])+abs(int(b)-rgb[2])
    if d((46,125,50)) <= 100 or d((27,114,63)) <= 100: return "G"
    if d((251,229,214)) <= 22: return "P"
    if d((206,255,224)) <= 22: return "M"
    if d((232,163,61)) <= 50: return "O"
    if d((201,166,107)) <= 45: return "T"
    if d((216,160,184)) <= 45: return "V"
    if d((179,157,219)) <= 45: return "L"
    if d((255,217,102)) <= 50: return "Y"
    if d((165,214,167)) <= 40: return "S"
    if d((255,251,197)) <= 35: return "y"
    if r > 240 and g > 240 and b > 240: return "."
    if d((253,253,150)) <= 40: return "B"
    if r < 75 and g < 75 and b < 75: return "#"
    if d((210,47,47)) <= 80: return "R"
    if d((204,0,0)) <= 90: return "R"
    return " "
for cy in (110, 130, 160, 190, 250, 270, 310, 330, 350, 370, 390, 410, 430, 450, 470, 490):
    row = img[cy]
    segs = []
    cur = cls(row[560]); start = 560
    for x in range(561, 900):
        c = cls(row[x])
        if c != cur:
            if x - start >= 2: segs.append(f"{start}-{x-1}:{cur}")
            cur = c; start = x
    if 900 - start >= 2: segs.append(f"{start}-899:{cur}")
    print(f"ARCH row y={cy}:", " ".join(segs))
