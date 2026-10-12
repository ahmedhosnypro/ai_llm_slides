#!/usr/bin/env python3
"""Third forensic pass: precise geometry + font metric solving for slide_008."""
from PIL import Image, ImageFont
import numpy as np
from collections import Counter

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_008.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R > 110) & (G < 90) & (B < 90)
dark = (R < 100) & (G < 100) & (B < 100)
white = (R > 240) & (G > 240) & (B > 240)
grayish = (R > 200) & (R < 245) & (G > 200) & (B > 200)

# --- row-by-row top transition ---
print("-- top rows 25..52: white/gray/red/dark counts --")
for y in range(25, 52):
    print(f"  y={y}: white={white[y].sum()} gray={grayish[y].sum()} red={red[y].sum()} dark={dark[y].sum()}")

# --- border extents ---
print("\n-- border geometry --")
for y in (153, 513):
    xs = np.nonzero(red[y])[0]
    print(f"row {y}: x {xs.min()}..{xs.max()} n={len(xs)}")
for x in (58, 70, 460):
    ys = np.nonzero(red[:, x])[0]
    print(f"col {x}: y {ys.min()}..{ys.max()} n={len(ys)}")
# is there any red border on panel (rows 40..50 full width) or sides?
print("red in rows 44..48 total:", red[44:49].sum())
print("red in cols 40..44 total:", red[:, 40:45].sum())
print("red in cols 916..921 total:", red[:, 916:922].sum())

# --- title lines, excluding stray col 58 ---
print("\n-- title line 1 (rows 60..105), excluding col 56..60 --")
t1 = red[60:106].copy()
t1[:, 56:61] = False
ys, xs = np.nonzero(t1)
print(f"  bbox y {ys.min()+60}..{ys.max()+60}, x {xs.min()}..{xs.max()} (adv {xs.max()-xs.min()+1}, center {(xs.min()+xs.max())/2:.1f})")
# row profile to find baseline/descender split
rows1 = t1.sum(axis=1)
prev = 0
for i, c in enumerate(rows1):
    if (c > 60) != (prev > 60):
        print(f"  y={i+60}: count {c} (threshold crossing)")
    prev = c
print("-- title line 2 (rows 106..145), excluding col 56..60 --")
t2 = red[106:146].copy()
t2[:, 56:61] = False
ys, xs = np.nonzero(t2)
print(f"  bbox y {ys.min()+106}..{ys.max()+106}, x {xs.min()}..{xs.max()} (adv {xs.max()-xs.min()+1}, center {(xs.min()+xs.max())/2:.1f})")
rows2 = t2.sum(axis=1)
prev = 0
for i, c in enumerate(rows2):
    if (c > 40) != (prev > 40):
        print(f"  y={i+106}: count {c} (threshold crossing)")
    prev = c

# --- headers precise ---
print("\n-- headers (red, rows 152..513, excluding border cols 56..72 and 458..462, border rows) --")
hr = red.copy()
hr[:152] = False; hr[514:] = False
hr[:, :73] = False; hr[:, 457:] = False
hr[152:156] = False; hr[510:514] = False
rows_h = hr.sum(axis=1)
segs = []
start = None
for y in range(152, H):
    if rows_h[y] > 3 and start is None:
        start = y
    elif rows_h[y] <= 3 and start is not None:
        segs.append((start, y - 1)); start = None
for s, e in segs:
    band = hr[s:e + 1]
    ys2, xs2 = np.nonzero(band)
    print(f"  y {s}..{e} (h {e-s+1}): x {xs2.min()}..{xs2.max()} (adv {xs2.max()-xs2.min()+1})")

# --- bullet lines precise (dark, rows 180..510, x>150) ---
print("\n-- bullet dark bands (x 150..470) --")
db = dark.copy()
db[:180] = False; db[510:] = False
db[:, :150] = False; db[:, 470:] = False
rows_d = db.sum(axis=1)
segs = []
start = None
for y in range(180, H):
    if rows_d[y] > 2 and start is None:
        start = y
    elif rows_d[y] <= 2 and start is not None:
        segs.append((start, y - 1)); start = None
for s, e in segs:
    band = db[s:e + 1]
    ys2, xs2 = np.nonzero(band)
    print(f"  y {s}..{e} (h {e-s+1}): x {xs2.min()}..{xs2.max()}")

# --- dots: dark px in x160..179 per line ---
print("\n-- dot bboxes (dark x158..180, rows 180..510) --")
db2 = dark.copy()
db2[:180] = False; db2[510:] = False
db2[:, :158] = False; db2[:, 180:] = False
ys, xs = np.nonzero(db2)
# cluster by y
if len(ys):
    order = np.argsort(ys)
    ys, xs = ys[order], xs[order]
    clusters = []
    cur = [0]
    for i in range(1, len(ys)):
        if ys[i] - ys[i - 1] > 5:
            clusters.append(cur); cur = []
        cur.append(i)
    clusters.append(cur)
    for cl in clusters:
        cy = ys[cl]; cx = xs[cl]
        print(f"  dot y {cy.min()}..{cy.max()} (d {cy.max()-cy.min()+1}), x {cx.min()}..{cx.max()} (d {cx.max()-cx.min()+1}), center ({(cx.min()+cx.max())/2:.1f},{(cy.min()+cy.max())/2:.1f})")

# --- x-height probe: 'o' of Python (x220..227), 'o' of Gensim etc. ---
def probe_band(x0, x1, y0, y1, label, mask):
    band = mask[y0:y1, x0:x1]
    ys2, xs2 = np.nonzero(band)
    if len(ys2):
        print(f"  {label}: y {ys2.min()+y0}..{ys2.max()+y0} (h {ys2.max()-ys2.min()+1}), x {xs2.min()+x0}..{xs2.max()+x0}")
    else:
        print(f"  {label}: empty")

print("\n-- glyph probes --")
probe_band(220, 228, 180, 205, "Python 'o'", dark)
probe_band(183, 193, 180, 205, "Python 'P'", dark)
probe_band(183, 196, 205, 230, "R glyph", dark)
probe_band(97, 107, 158, 185, "hdr1 'P'", red)
probe_band(97, 118, 158, 185, "hdr1 'Po'", red)
probe_band(64, 100, 55, 105, "title 'Pr'", red)

# --- font metric solving with Liberation fonts ---
print("\n-- font metric solving (Liberation Sans = Arial metrics) --")
LSB = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
LSR = "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"

def adv(fontpath, px_size, text):
    f = ImageFont.truetype(fontpath, px_size)
    return f.getlength(text)

print("title line1 'Programming Languages, Platforms,'")
for s in (38, 39, 40, 41, 42):
    print(f"  bold {s}px adv={adv(LSB, s, 'Programming Languages, Platforms,'):.1f}")
print("title line2 'and Libraries'")
for s in (38, 39, 40, 41, 42):
    print(f"  bold {s}px adv={adv(LSB, s, 'and Libraries'):.1f}")
print("hdr1 'Popular Languages for ML/DL'")
for s in (16, 17, 17.5, 18, 19):
    print(f"  bold {s}px adv={adv(LSB, int(s*2)/2 if False else round(s), 'Popular Languages for ML/DL'):.1f}")
print("hdr2 'Popular Platforms for ML/DL'")
for s in (17, 18):
    print(f"  bold {s}px adv={adv(LSB, s, 'Popular Platforms for ML/DL'):.1f}")
print("hdr3 'Popular Libraries (for python)'")
for s in (17, 18):
    print(f"  bold {s}px adv={adv(LSB, s, 'Popular Libraries (for python)'):.1f}")
print("bullets regular:")
for s in (13, 14, 15, 16):
    print(f"  {s}px: Python={adv(LSR, s, 'Python'):.1f} Matlab={adv(LSR, s, 'Matlab'):.1f} Tensor Flow={adv(LSR, s, 'Tensor Flow'):.1f} Pytorch={adv(LSR, s, 'Pytorch'):.1f} SciKit Learn={adv(LSR, s, 'SciKit Learn'):.1f} SciPy={adv(LSR, s, 'SciPy'):.1f} NLTK={adv(LSR, s, 'NLTK'):.1f} Spacy={adv(LSR, s, 'Spacy'):.1f} Gensim={adv(LSR, s, 'Gensim'):.1f} OpenCV={adv(LSR, s, 'OpenCV'):.1f}")

# measured advances of bullet lines (text only, x>=175)
print("\n-- measured bullet text advances (dark, x>=175) --")
db3 = dark.copy()
db3[:180] = False; db3[510:] = False
db3[:, :175] = False; db3[:, 470:] = False
rows_d3 = db3.sum(axis=1)
segs = []
start = None
for y in range(180, H):
    if rows_d3[y] > 2 and start is None:
        start = y
    elif rows_d3[y] <= 2 and start is not None:
        segs.append((start, y - 1)); start = None
names = ["Python", "R", "Matlab", "Tensor Flow", "Pytorch", "SciKit Learn", "SciPy", "NLTK", "Spacy", "Gensim", "OpenCV"]
for i, (s, e) in enumerate(segs):
    band = db3[s:e + 1]
    ys2, xs2 = np.nonzero(band)
    nm = names[i] if i < len(names) else "?"
    print(f"  {nm}: y {s}..{e}, x {xs2.min()}..{xs2.max()} (adv {xs2.max()-xs2.min()+1})")
