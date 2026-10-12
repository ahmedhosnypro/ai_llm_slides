#!/usr/bin/env python3
"""Landmark census on 002:slide_008.jpg vs 001:slide_033.jpg (both 960x540).

Finds color-mask bboxes for the diagram's big elements in each frame, pairs them,
and fits per-axis affine  frame008 = A + S * frame033  (least squares over pairs).
Also prints a classification grid of the badge region of frame008.
"""
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
f8 = np.asarray(Image.open(f"{ROOT}/002_transformers_part2/unique_slides/slide_008.jpg").convert("RGB")).astype(int)
f33 = np.asarray(Image.open(f"{ROOT}/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")).astype(int)


def mask(im, hexcol, tol):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    cr, cg, cb = int(hexcol[0:2], 16), int(hexcol[2:4], 16), int(hexcol[4:6], 16)
    return (abs(r - cr) < tol) & (abs(g - cg) < tol) & (abs(b - cb) < tol)


def bbox(m, minpix=40):
    ys, xs = np.where(m)
    if len(xs) < minpix:
        return None
    return xs.min(), xs.max(), ys.min(), ys.max(), len(xs)


LANDMARKS = [
    # name, hex, tol, description
    ("peach_panel", "F7E2CD", 14, "diagram panel fill"),
    ("dp_box", "DCCBBB", 12, "dot product box fill"),
    ("softmax", "F8DDFC", 12, "softmax bar fill"),
    ("sigma", "EAFEFC", 12, "sigma box fill"),
    ("container", "E7FFE9", 12, "green dashed containers"),
    ("band_yellow", "F7F96B", 20, "yellow W bands"),
]

print("== per-frame landmark bboxes (x0..x1, y0..y1, npix) ==")
results = {}
for name, hexc, tol, desc in LANDMARKS:
    b8 = bbox(mask(f8, hexc, tol))
    b33 = bbox(mask(f33, hexc, tol))
    results[name] = (b8, b33)
    print(f"{name:12s} f8: {b8}   f33: {b33}   ({desc})")

# fit affine from pairable bboxes: use centers and extents
pairs = []
for name, (b8, b33) in results.items():
    if b8 and b33:
        c8x = (b8[0] + b8[1]) / 2
        c33x = (b33[0] + b33[1]) / 2
        c8y = (b8[2] + b8[3]) / 2
        c33y = (b33[2] + b33[3]) / 2
        w8 = b8[1] - b8[0]
        w33 = b33[1] - b33[0]
        h8 = b8[3] - b8[2]
        h33 = b33[3] - b33[2]
        pairs.append((name, c8x, c33x, c8y, c33y, w8, w33, h8, h33))

if len(pairs) >= 2:
    xs8 = np.array([p[1] for p in pairs]); xs33 = np.array([p[2] for p in pairs])
    ys8 = np.array([p[3] for p in pairs]); ys33 = np.array([p[4] for p in pairs])
    A_x = np.polyfit(xs33, xs8, 1)
    A_y = np.polyfit(ys33, ys8, 1)
    print("\n== affine fit (centers): frame8_x = %.3f + %.5f * frame33_x ; frame8_y = %.3f + %.5f * frame33_y" % (A_x[1], A_x[0], A_y[1], A_y[0]))
    print("residuals x:", ["%s:%+.1f" % (p[0], p[1] - (A_x[1] + A_x[0] * p[2])) for p in pairs])
    print("residuals y:", ["%s:%+.1f" % (p[0], p[3] - (A_y[1] + A_y[0] * p[4])) for p in pairs])
    # implied inverse (frame8 -> slide px, since frame33 == slide px 1:1)
    sx = 1 / A_x[0]; ax = -A_x[1] / A_x[0]
    sy = 1 / A_y[0]; ay = -A_y[1] / A_y[0]
    print("inverse: slide_x = %.3f + %.5f * frame8_x  (i.e. XI = (fx - %.3f)/%.5f/72)" % (ax, sx, ax, sx))
    print("inverse: slide_y = %.3f + %.5f * frame8_y  (i.e. YI = (fy - %.3f)/%.5f/72)" % (ay, sy, ay, sy))
    # width/height ratios
    print("size ratios w (f8/f33):", ["%s:%.3f" % (p[0], p[5] / p[6]) for p in pairs])
    print("size ratios h (f8/f33):", ["%s:%.3f" % (p[0], p[7] / p[8]) for p in pairs])

# badge region grid of frame8 (x 830..920, y 40..130), 4px cells
print("\n== badge region grid f8 (R=reddish, Y=yellow, P=purple-ish, G=gray, .=other) ==")
for y in range(40, 132, 4):
    row = ""
    for x in range(830, 921, 4):
        R, G, B = f8[y, x]
        if R > 200 and G > 200 and B < 190:
            c = "Y"
        elif R > 140 and G < 110 and B < 110:
            c = "R"
        elif B > 150 and R < 180 and G < 140:
            c = "P"
        elif abs(R - 233) < 20 and abs(G - 233) < 20 and abs(B - 231) < 22:
            c = "g"
        elif R < 60 and G < 60 and B < 60:
            c = "#"
        else:
            c = "."
        row += c
    print(f"{y:3d} {row}")
print("     " + "".join(str((x // 10) % 10) for x in range(830, 921, 4)))

# chrome strokes f8 with loose red
r, g, b = f8[:, :, 0], f8[:, :, 1], f8[:, :, 2]
red = (r > 110) & (r - g > 40) & (r - b > 40)
mid = red[250:300, :]
print("\nleft border cols (loose):", np.where(mid[:, :80].sum(axis=0) > 10)[0].tolist())
print("right border cols (loose):", (880 + np.where(mid[:, 880:].sum(axis=0) > 10)[0]).tolist())
topr = red[:70, 300:700]
print("top border rows (loose):", np.where(topr.sum(axis=1) > 80)[0].tolist())
botr = red[490:530, 300:700]
print("bottom border rows 490-530 (loose):", (490 + np.where(botr.sum(axis=1) > 80)[0]).tolist())
# gray panel top row at left band
gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
rows = np.where(gray[:, 60:140].sum(axis=1) > 60)[0]
print("gray rows left band:", rows.min(), "..", rows.max())
cols = np.where(gray[100:500, :].sum(axis=0) > 300)[0]
print("gray cols:", cols.min(), "..", cols.max())
