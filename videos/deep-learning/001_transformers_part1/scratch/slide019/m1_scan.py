#!/usr/bin/env python3
"""m1_scan.py — fine scanline profiles of slide_019.jpg: stack internals, circles, callouts."""
from PIL import Image
import collections

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg").convert("RGB")
px = IM.load()
W, H = IM.size

def q(c, s=24):
    return (c[0] // s * s, c[1] // s * s, c[2] // s * s)

def runs_along_y(x, y0, y1, minrun=3):
    out = []
    cur = None; start = y0
    for y in range(y0, y1):
        k = q(px[x, y])
        if cur is None:
            cur = k; start = y; n = 1
        elif k == cur:
            n += 1
        else:
            if n >= minrun: out.append((start, y - 1, cur, n))
            cur = k; start = y; n = 1
    if cur is not None and n >= minrun: out.append((start, y1 - 1, cur, n))
    return out

def runs_along_x(y, x0, x1, minrun=3):
    out = []
    cur = None; start = x0; n = 0
    for x in range(x0, x1):
        k = q(px[x, y])
        if cur is None:
            cur = k; start = x; n = 1
        elif k == cur:
            n += 1
        else:
            if n >= minrun: out.append((start, x - 1, cur, n))
            cur = k; start = x; n = 1
    if cur is not None and n >= minrun: out.append((start, x1 - 1, cur, n))
    return out

def dump_y(label, x, y0, y1):
    print(f"\n-- vertical x={x} {label}")
    for a, b, k, n in runs_along_y(x, y0, y1):
        print(f"  y {a:3d}..{b:3d} ({n:3d}px) rgb~{k}")

def dump_x(label, y, x0, x1):
    print(f"\n-- horizontal y={y} {label}")
    for a, b, k, n in runs_along_x(y, x0, x1):
        print(f"  x {a:3d}..{b:3d} ({n:3d}px) rgb~{k}")

# encoder stack internals
dump_y("enc stack left-of-center", 640, 255, 420)
dump_y("enc stack center", 676, 255, 420)
dump_y("enc stack right", 715, 255, 420)
# decoder stack internals
dump_y("dec stack", 760, 190, 420)
dump_y("dec stack 2", 800, 190, 420)
# horizontal through the compartments
dump_x("enc row y275 (A&N top)", 275, 620, 740)
dump_x("enc row y300 (FF)", 300, 620, 740)
dump_x("enc row y335 (A&N mid)", 335, 620, 740)
dump_x("dec row y210 (A&N top)", 210, 735, 855)
dump_x("dec row y235 (FF)", 235, 735, 855)
dump_x("dec row y257 (A&N mid)", 257, 735, 855)
dump_x("dec row y337 (purple A&N)", 337, 735, 855)
