#!/usr/bin/env python3
"""Forensics pass 6: ink density (bold/serif discrimination), border cores, matrix internals."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

D = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
a = np.asarray(Image.open(os.path.join(D, "unique_slides/slide_031.jpg")).convert("RGB")).astype(int)
lum = a.mean(axis=2)

LIB = "/usr/share/fonts/liberation"
FONTS = {
    "TNR-B": f"{LIB}/LiberationSerif-Bold.ttf",
    "TNR-R": f"{LIB}/LiberationSerif-Regular.ttf",
    "Arial-B": f"{LIB}/LiberationSans-Bold.ttf",
    "Arial-R": f"{LIB}/LiberationSans-Regular.ttf",
}
fcache = {}
def load(fp, s):
    k = (fp, round(s, 1))
    if k not in fcache: fcache[k] = ImageFont.truetype(fp, int(round(s * 4)))
    return fcache[k]

def cand_density(fname, size, text):
    """render at 4x on white, downsample to 1x, count px <190, per pt of advance"""
    f = load(FONTS[fname], size)
    W = int(f.getlength(text) / 4) + 20
    img = Image.new("L", (W, int(size * 4) + 20), 255)
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, font=f, fill=0)
    small = img.resize((W // 4, img.height // 4), Image.LANCZOS)
    s = np.asarray(small).astype(int)
    ink = (s < 190).sum()
    adv = f.getlength(text) / 4.0
    return ink / adv

def meas_density(y0, y1, x0, x1):
    seg = lum[y0:y1 + 1, x0:x1 + 1]
    return (seg < 190).sum() / (x1 - x0)

print("== density: measured vs candidates (ink px per pt of advance) ==")
m_title = meas_density(87, 120, 179, 778)
print(f"title meas {m_title:.2f} | Arial-B35 {cand_density('Arial-B',35,'Where to Get Filters for Recognition'):.2f} | TNR-B38.5 {cand_density('TNR-B',38.5,'Where to Get Filters for Recognition'):.2f} | TNR-B38 {cand_density('TNR-B',38,'Where to Get Filters for Recognition'):.2f} | TNR-R40.5 {cand_density('TNR-R',40.5,'Where to Get Filters for Recognition'):.2f} | Arial-R37.5 {cand_density('Arial-R',37.5,'Where to Get Filters for Recognition'):.2f}")
L1 = "There are Several, handcrafted filters in computer vision"
m1 = meas_density(145, 164, 108, 676)
print(f"line1 meas {m1:.2f} | TNR-B23.5 {cand_density('TNR-B',23.5,L1):.2f} | TNR-R25 {cand_density('TNR-R',25,L1):.2f} | Arial-R23 {cand_density('Arial-R',23,L1):.2f} | Arial-B21 {cand_density('Arial-B',21,L1):.2f}")
mq = meas_density(302, 323, 134, 468)
print(f"q1 meas {mq:.2f} | TNR-B23.5 {cand_density('TNR-B',23.5,'Are they optimal for recognition?'):.2f} | TNR-R25 {cand_density('TNR-R',25,'Are they optimal for recognition?'):.2f} | Arial-B21 {cand_density('Arial-B',21,'Are they optimal for recognition?'):.2f} | Arial-R23 {cand_density('Arial-R',23,'Are they optimal for recognition?'):.2f}")
mfp = meas_density(445, 463, 389, 595)
print(f"fp meas {mfp:.2f} | TNR-B27 {cand_density('TNR-B',27,'Filter Parameters'):.2f} | Arial-B25 {cand_density('Arial-B',25,'Filter Parameters'):.2f} | TNR-R27 {cand_density('TNR-R',27,'Filter Parameters'):.2f} | Arial-R27 {cand_density('Arial-R',27,'Filter Parameters'):.2f}")

print("\n== border cores ==")
print("chrome line col58 @y300:", tuple(a[300, 57]), tuple(a[300, 58]), tuple(a[300, 59]))
print("title core @ (105,300):", tuple(a[105, 300]), " @ (100,400):", tuple(a[100, 400]))
print("content border (99,300):", tuple(a[300, 99]), " (885,300):", tuple(a[300, 885]), "(886,300):", tuple(a[300, 886]))
print("fp border (378,455):", tuple(a[455, 378]), " (606,455):", tuple(a[455, 606]), " top(500,436):", tuple(a[436, 500]))
print("matrix border (623,450):", tuple(a[450, 623]), " (841,450):", tuple(a[450, 841]), " top(700,387):", tuple(a[387, 700]))

print("\n== matrix internals: entry bands (x between brackets 640..828) ==")
mb = lum[392:500, 640:828]
rowink = (mb < 150).sum(axis=1)
bands = []
y = 0
while y < len(rowink):
    if rowink[y] > 0:
        y2 = y
        while y2 < len(rowink) - 1 and rowink[y2 + 1] > 0: y2 += 1
        bands.append((392 + y, 392 + y2)); y = y2 + 1
    else: y += 1
for b in bands:
    seg = lum[b[0]:b[1] + 1, 640:828]
    xs = np.where((seg < 150).any(axis=0))[0]
    print(f"  row band {b}: x {640+xs.min()}..{640+xs.max()}")
# column runs in the middle row band to see the 3 columns
if bands:
    b = bands[len(bands)//2]
    seg = lum[b[0]:b[1]+1, 640:828]
    colink = (seg < 150).sum(axis=0)
    runs = []
    x = 0
    while x < len(colink):
        if colink[x] > 0:
            x2 = x
            while x2 < len(colink)-1 and (colink[x2+1] > 0 or (x2+3 < len(colink) and colink[x2+1:x2+4].any())): x2 += 1
            runs.append((640+x, 640+x2)); x = x2+1
        else: x += 1
    print("  col runs mid band:", runs)
# bracket tick geometry: rows of horizontal ticks at top/bottom of brackets (x 634..640)
print("bracket left col634-637 y-extent:", np.where((lum[390:500, 634:638] < 150).any(axis=1))[0].min()+390, np.where((lum[390:500, 634:638] < 150).any(axis=1))[0].max()+390)
