#!/usr/bin/env python3
"""Pass 4: leaders with looser mask, scissors region probe, title center-of-mass, fill modes, underline rows."""
from PIL import Image
import collections

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
im = Image.open(BASE + "unique_slides/slide_008.jpg").convert("RGB")
im6 = Image.open(BASE + "unique_slides/slide_006.jpg").convert("RGB")

def com(img, pred, x0, y0, x1, y1):
    ld = img.load()
    sx = sy = n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(ld[x, y]):
                sx += x; sy += y; n += 1
    return (round(sx / n, 1), round(sy / n, 1), n) if n else None

def redink(p):
    r, g, b = p
    return r > 120 and r - g > 60 and r - b > 60

# title center of mass (x 260..660 band to exclude decoder caption)
print("s8 title com:", com(im, redink, 260, 50, 660, 95))
print("s6 title com:", com(im6, redink, 260, 50, 660, 95))

# clean fill patches
def mode(img, x0, y0, x1, y1):
    c = collections.Counter()
    ld = img.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c[ld[x, y]] += 1
    return c.most_common(5)

print("callout fill (y170..180, x60..300):", mode(im, 60, 170, 300, 180))
print("wait1 fill (y258..261, x60..175):", mode(im, 60, 258, 175, 261))
print("wait2 fill (y257..260, x220..335):", mode(im, 220, 257, 335, 260))

# underline per-row counts, callout x-range, y 195..220
ld = im.load()
def blueink(p):
    r, g, b = p
    return b > 110 and b - r > 40 and g < 140
print("callout rows y195..220 (n, xmin..xmax):")
for y in range(195, 220):
    row = [x for x in range(43, 330) if blueink(ld[x, y])]
    print(f"  y={y}: n={len(row)} {min(row) if row else '-'}..{max(row) if row else '-'}")

# leader pixels: looser blue mask, scan y 228..335, x 0..500
def leaderink(p):
    r, g, b = p
    return b - r > 30 and b > 150 and g < 235 and not (r > 200 and g > 230)
print("leader candidates per row y228..334 (n, xmin..xmax):")
for y in range(228, 335):
    row = [x for x in range(0, 500) if leaderink(ld[x, y])]
    if len(row) >= 2:
        print(f"  y={y}: n={len(row)} {min(row)}..{max(row)}")

# scissors region probe: x 326..365, y 165..235 sample colors
print("probe x330..360, y170..230 — pixels with b-r>20 or gray-dark:")
cnt = 0
for y in range(165, 235):
    for x in range(326, 366):
        p = ld[x, y]
        r, g, b = p
        if (b - r > 20 or (r < 150 and g < 150 and b < 150)):
            if cnt < 40:
                print(f"  ({x},{y}) = {p}")
            cnt += 1
print("probe total:", cnt)
