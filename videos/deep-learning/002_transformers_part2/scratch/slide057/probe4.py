#!/usr/bin/env python3
"""Probe 4: gap-fill measurements on 002 slide_057 (read-only vs the frame).
A) Decoder panel vertical row profile (exact y-bands per row type)
B) K / V / Q yellow badge centroids + arrow landing rows
C) Container bboxes: encoder tan container, decoder green container, central striped column
D) Encoder panel row profile (Y / blocks / X / bars / words)
Writes probe4.txt only. No frame files are modified."""
import os
from PIL import Image
BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
OUT = os.path.join(BASE, "scratch", "slide057")
lines = []
def say(s=""):
    lines.append(s); print(s)

im = Image.open(os.path.join(BASE, "unique_slides", "slide_057.jpg")).convert("RGB")
W, H = im.size
px = im.load()
say(f"== probe4 002 slide_057 {W}x{H} ==")

def counts(y, x0, x1):
    red = green = blue = purple = magenta = gray = tan = paleblue = darkpurple = 0
    for x in range(x0, x1):
        r, g, b = px[x, y]
        if 110 < r < 215 and r - g > 55 and r - b > 55: red += 1
        elif g > 120 and g - r > 35 and g - b > 35: green += 1
        elif b > 120 and b - r > 35 and b - g > 25: blue += 1
        elif 85 < r < 150 and g < 80 and 130 < b < 200: purple += 1
        elif r > 195 and b > 175 and g < 110: magenta += 1
        elif 165 < r < 218 and abs(r - g) < 14 and abs(g - b) < 14: gray += 1
        elif r > 235 and 185 < g < 228 and 150 < b < 205: tan += 1
        elif r > 215 and 225 < g < 245 and b > 235: paleblue += 1
        elif 55 < r < 95 and 55 < g < 95 and b > 130: darkpurple += 1
    return dict(red=red, green=green, blue=blue, purple=purple, magenta=magenta,
                gray=gray, tan=tan, paleblue=paleblue, darkpurple=darkpurple)

def bands(cls, thr, y0, y1, x0, x1, min_run=3):
    """contiguous y-bands where cls count >= thr"""
    res, start = [], None
    for y in range(y0, y1):
        c = counts(y, x0, x1)[cls]
        if c >= thr and start is None: start = y
        elif c < thr and start is not None:
            if y - start >= min_run: res.append((start, y - 1))
            start = None
    if start is not None and y1 - start >= min_run: res.append((start, y1 - 1))
    return res

say("\n== A) decoder panel row bands (x 565..850) ==")
for cls, thr, note in [("red", 120, "Residual bars"), ("green", 120, "FFN bars + panel fill"),
                       ("blue", 40, "attention boxes"), ("purple", 25, "Word&Position Encoding bar"),
                       ("magenta", 8, "magenta circle row"), ("gray", 40, "gray squares"),
                       ("darkpurple", 20, "encoder block bars (x 95..445 only)")]:
    if cls == "darkpurple":
        bb = bands(cls, thr, 40, 540, 95, 445)
    else:
        bb = bands(cls, thr, 40, 540, 565, 850)
    say(f"  {cls:10s} thr={thr:3d} {note:38s}: {bb}")

say("\n== B) yellow badge locate (r>200 g>200 b<140 blobs) ==")
def yellow_blob(x0, x1, y0, y1, label):
    xs = ys = n = 0
    minx = miny = 10**9; maxx = maxy = -1
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            if r > 200 and g > 200 and b < 140:
                xs += x; ys += y; n += 1
                minx, miny = min(minx, x), min(miny, y)
                maxx, maxy = max(maxx, x), max(maxy, y)
    if n:
        say(f"  {label}: bbox x {minx}..{maxx} y {miny}..{maxy} centroid=({xs/n:.1f},{ys/n:.1f}) n={n}  ({(xs/n)/W*100:.1f}%W {(ys/n)/H*100:.1f}%H)")
    else:
        say(f"  {label}: none")
yellow_blob(495, 565, 140, 200, "K badge (mid col)")
yellow_blob(495, 565, 240, 300, "V badge (mid col)")
yellow_blob(795, 875, 380, 460, "Q badge (right)")
# red arrow rows landing at decoder left edge x 556..600
say("  red arrow rows at x 558..600 (red px count>=15):")
for y in range(140, 300):
    n = sum(1 for x in range(558, 600) if px[x, y][0] > 150 and px[x, y][0] - px[x, y][1] > 60 and px[x, y][0] - px[x, y][2] > 50)
    if n >= 15: say(f"    y={y} n={n}")
say("  solid blue arrow rows at x 558..600 (blue px count>=15):")
for y in range(280, 430):
    r, g, b = None, None, None
    n = sum(1 for x in range(558, 600) if (lambda c: c[2] > 120 and c[2] - c[0] > 35 and c[2] - c[1] > 25)(px[x, y]))
    if n >= 15: say(f"    y={y} n={n}")

say("\n== C) container bboxes ==")
# decoder green border columns already known (probe2): x=555, 854-855; find rows
gr = [y for y in range(H) if (lambda c: c[1] > 110 and c[1] - c[0] > 35 and c[1] - c[2] > 35)(px[556, y])]
say(f"  green border col x=556: rows {min(gr) if gr else None}..{max(gr) if gr else None} n={len(gr)}")
gr2 = [y for y in range(H) if (lambda c: c[1] > 110 and c[1] - c[0] > 35 and c[1] - c[2] > 35)(px[854, y])]
say(f"  green border col x=854: rows {min(gr2) if gr2 else None}..{max(gr2) if gr2 else None} n={len(gr2)}")
# encoder red container: find red border cols near x 60..70 and 440..460 rows
rr = [y for y in range(H) if (lambda c: c[0] > 120 and c[0] - c[1] > 55 and c[0] - c[2] > 55)(px[448, y])]
say(f"  red col x=448: rows {min(rr) if rr else None}..{max(rr) if rr else None} n={len(rr)}")
rr2 = [y for y in range(H) if (lambda c: c[0] > 120 and c[0] - c[1] > 55 and c[0] - c[2] > 55)(px[64, y])]
say(f"  red col x=64 (tan container left?): rows {min(rr2) if rr2 else None}..{max(rr2) if rr2 else None} n={len(rr2)}")
# tan container fill bbox
tanys = [y for y in range(H) if counts(y, 100, 430)["tan"] > 200]
say(f"  tan fill rows (x 100..430, n>200): {min(tanys) if tanys else None}..{max(tanys) if tanys else None}")
# central striped column: blue px per column x 455..515 at y 150..380
cols = []
for x in range(450, 525):
    n = sum(1 for y in range(150, 380) if (lambda c: c[2] > 120 and c[2] - c[0] > 35 and c[2] - c[1] > 25)(px[x, y]))
    if n > 60: cols.append(x)
say(f"  striped column cols (blue n>60 over y150..380): {min(cols) if cols else None}..{max(cols) if cols else None}")
if cols:
    cx = (min(cols) + max(cols)) // 2
    rows = [y for y in range(H) if (lambda c: c[2] > 120 and c[2] - c[0] > 35 and c[2] - c[1] > 25)(px[cx, y])]
    say(f"  striped column rows @x={cx}: {min(rows) if rows else None}..{max(rows) if rows else None}")

say("\n== D) encoder panel row bands (x 95..445) ==")
for cls, thr, note in [("darkpurple", 20, "Encoder Block bars"),
                       ("tan", 200, "Word Embedding bar"),
                       ("paleblue", 150, "Positional Encoding bar")]:
    say(f"  {cls:10s} thr={thr:3d} {note:24s}: {bands(cls, thr, 40, 540, 95, 445)}")

open(os.path.join(OUT, "probe4.txt"), "w").write("\n".join(lines) + "\n")
print("WROTE probe4.txt")
