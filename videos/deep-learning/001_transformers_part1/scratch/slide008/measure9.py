#!/usr/bin/env python3
"""Pass 9: stem-based italic slant test. Italic => stem x-center DECREASES as y increases
(top leans right). Upright => slope ~ 0. Also compare against slide 6's known-italic
labels (softmax/o1) and known-upright ctx-box text as calibration."""
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"

def stems(img, x0, x1, y0, y1, pred, min_rows, max_w=4):
    ld = img.load()
    # column presence
    cols = {}
    for x in range(x0, x1):
        ys = [y for y in range(y0, y1) if pred(ld[x, y])]
        if len(ys) >= min_rows:
            cols[x] = ys
    # group adjacent columns
    groups, cur = [], []
    for x in sorted(cols):
        if cur and x - cur[-1] > 1:
            groups.append(cur); cur = []
        cur.append(x)
    if cur: groups.append(cur)
    out = []
    for g in groups:
        if len(g) > max_w: continue
        rows = sorted(set(min(cols[x]) for x in g) | set(max(cols[x]) for x in g))
        y0g, y1g = min(min(cols[x]) for x in g), max(max(cols[x]) for x in g)
        if y1g - y0g < min_rows: continue
        pts = []
        for y in range(y0g, y1g + 1):
            xs = [x for x in g if y in cols[x]]
            if xs:
                pts.append((y, sum(xs) / len(xs)))
        if len(pts) < min_rows - 2: continue
        n = len(pts)
        my = sum(p[0] for p in pts) / n
        mx = sum(p[1] for p in pts) / n
        num = sum((p[0] - my) * (p[1] - mx) for p in pts)
        den = sum((p[0] - my) ** 2 for p in pts)
        slope = num / den if den else 0
        out.append((g[0], g[-1], y0g, y1g, round(slope, 3)))
    return out

def blueink(p):
    r, g, b = p
    return b > 110 and b - r > 40 and g < 140

def redink(p):
    r, g, b = p
    return r > 120 and r - g > 60 and r - b > 60

def oliveink(p):
    r, g, b = p
    return 100 < r < 190 and 90 < g < 180 and b < 120 and r > b + 30

im = Image.open(BASE + "unique_slides/slide_008.jpg").convert("RGB")
im6 = Image.open(BASE + "unique_slides/slide_006.jpg").convert("RGB")

print("CALIBRATION slide6 'Decoder (RNN)' caption (Arial bold ITALIC, certified):")
print(" ", stems(im6, 670, 835, 85, 115, redink, 8))
print("CALIBRATION slide6 'softmax' (Times italic):")
print(" ", stems(im6, 480, 560, 168, 190, oliveink, 8))
print("CALIBRATION slide6 'Context Vector...' box text (drawn upright, certified):")
print(" ", stems(im6, 570, 830, 410, 436, redink, 8))
print("TEST slide8 '(Challenges)' (x 392..520, exclude parens):")
print(" ", stems(im, 392, 520, 88, 112, blueink, 8))
print("TEST slide8 callout line1 'Sequential Processing' (x 92..283):")
print(" ", stems(im, 92, 283, 182, 198, blueink, 7))
print("TEST slide8 callout line2 'Can NOT do processing in Parallel' (x 62..310):")
print(" ", stems(im, 62, 310, 201, 214, blueink, 7))
print("TEST slide8 wait1 line2 'Till Processing X1' (x 64..175):")
print(" ", stems(im, 64, 175, 276, 290, blueink, 6))
