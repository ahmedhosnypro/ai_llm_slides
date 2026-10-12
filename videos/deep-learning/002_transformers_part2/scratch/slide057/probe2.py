#!/usr/bin/env python3
"""Probe 2: panel edges, badge, and clean-row scans for slide_057 chrome."""
import os
from PIL import Image
BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
OUT = os.path.join(BASE, "scratch", "slide057")
im = Image.open(os.path.join(BASE, "unique_slides", "slide_057.jpg")).convert("RGB")
W, H = im.size
px = im.load()
lines = []
def say(s=""):
    lines.append(s); print(s)

say("== gray samples along y=300 (left margin -> panel) ==")
for x in [36, 37, 38, 40, 42, 45, 48, 50, 52, 54, 55, 56, 58, 60, 62, 64, 66]:
    c = px[x, 300]; say(f"  x={x:3d} #{c[0]:02X}{c[1]:02X}{c[2]:02X}")
say("== gray samples along y=300 (right side) ==")
for x in [900, 902, 904, 906, 908, 910, 912, 914, 916, 918, 920, 922, 924]:
    c = px[x, 300]; say(f"  x={x:3d} #{c[0]:02X}{c[1]:02X}{c[2]:02X}")

say("== panel top edge: samples along x=500, y 36..60 ==")
for y in range(36, 61):
    c = px[500, y]; say(f"  y={y:3d} #{c[0]:02X}{c[1]:02X}{c[2]:02X}")

say("== clean row scan: y=516 (above black strip) white->gray transitions ==")
prev = None
for x in range(0, W):
    c = px[x, 516]
    g = "gray" if abs(c[0]-233)<12 and abs(c[1]-233)<12 and abs(c[2]-231)<12 else ("white" if min(c)>238 else "other")
    if g != prev:
        say(f"  x={x}: {prev} -> {g}  #{c[0]:02X}{c[1]:02X}{c[2]:02X}")
        prev = g

say("== badge region probe x 850..905, y 45..100 ==")
# find yellowish: r>200 g>200 100<b<210
minx, miny, maxx, maxy, n, sx, sy = 10**9, 10**9, -1, -1, 0, 0, 0
for y in range(40, 110):
    for x in range(840, 920):
        r, g, b = px[x, y]
        if r > 200 and g > 200 and 100 < b < 210:
            minx = min(minx, x); maxx = max(maxx, x); miny = min(miny, y); maxy = max(maxy, y)
            sx += x; sy += y; n += 1
say(f"  badge-ish bbox x {minx}..{maxx} y {miny}..{maxy} n={n} centroid=({sx/max(n,1):.1f},{sy/max(n,1):.1f})")
# ring color: sample pixels on the bbox perimeter
if n:
    cy = (miny + maxy) // 2
    samples = [px[minx, cy], px[minx+1, cy], px[maxx, cy], px[maxx-1, cy]]
    for i, c in enumerate(samples):
        say(f"  ring sample {i}: #{c[0]:02X}{c[1]:02X}{c[2]:02X}")
    # darkest inside (numeral)
    dark, dpos = (255,)*3, None
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            c = px[x, y]
            if sum(c) < sum(dark):
                dark, dpos = c, (x, y)
    say(f"  darkest (numeral): #{dark[0]:02X}{dark[1]:02X}{dark[2]:02X} at {dpos}")
    # fill sample: middle-right of circle away from numeral
    fill = px[(minx+maxx)//2 + 8, miny + 5]
    say(f"  fill sample: #{fill[0]:02X}{fill[1]:02X}{fill[2]:02X}")

say("== red panel border columns: red count per column x 30..70 and 895..930 ==")
def is_red(c): r,g,b = c; return r>140 and g<90 and b<90
for x in list(range(30, 71)) + list(range(895, 931)):
    n = sum(1 for y in range(40, 520) if is_red(px[x, y]))
    if n > 30:
        say(f"  x={x} red_n={n}")
say("== red panel border rows: red count per row y 36..60 ==")
for y in range(36, 61):
    n = sum(1 for x in range(40, 920) if is_red(px[x, y]))
    if n > 100:
        say(f"  y={y} red_n={n}")
say("== encoder RED container + decoder GREEN container full-height columns ==")
def is_green(c): r,g,b = c; return g>110 and r<110 and b<110
for x in range(W):
    nr = sum(1 for y in range(40, 520) if is_red(px[x, y]))
    ng = sum(1 for y in range(40, 520) if is_green(px[x, y]))
    if nr > 120 or ng > 120:
        say(f"  x={x} red={nr} green={ng}")
open(os.path.join(OUT, "probe2.txt"), "w").write("\n".join(lines) + "\n")
print("WROTE probe2.txt")
