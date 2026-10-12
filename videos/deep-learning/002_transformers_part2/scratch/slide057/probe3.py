#!/usr/bin/env python3
"""Probe 3: precise panel borders + badge mask on 057; panel cross-check on
001 slide_001 (house reference) and 002 slide_049 (sibling)."""
import os
from PIL import Image
BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
OUT = os.path.join(BASE, "002_transformers_part2", "scratch", "slide057")
lines = []
def say(s=""):
    lines.append(s); print(s)

def darkred(c): r, g, b = c; return r > 85 and r - g > 40 and r - b > 30

def panel_edges(path, label):
    im = Image.open(path).convert("RGB")
    W, H = im.size; px = im.load()
    say(f"\n== {label} {W}x{H} ==")
    # left border: for clean rows (y=300,400,480) find dark-red columns near left
    for y in [60, 150, 300, 400, 480, 512]:
        xs = [x for x in range(0, 120) if darkred(px[x, y])]
        say(f"  y={y}: dark-red cols in 0..119: {xs[:12]}")
    for y in [60, 150, 300, 400, 480, 512]:
        xs = [x for x in range(W - 120, W) if darkred(px[x, y])]
        say(f"  y={y}: dark-red cols in {W-120}..{W-1}: {xs[-12:]}")
    # top border row: x=W//2 scan y 30..70
    ys = [y for y in range(30, 71) if darkred(px[W // 2, y])]
    say(f"  x={W//2}: dark-red rows 30..70: {ys}")
    # bottom: last row with gray/panel color near left margin x=50
    col = [px[50, y] for y in range(H)]
    last_nonwhite = max(y for y in range(H) if not all(v > 238 for v in col[y])) if any(not all(v > 238 for v in col[y]) for y in range(H)) else None
    say(f"  x=50: last non-white row = {last_nonwhite}")
    return im

im57 = panel_edges(os.path.join(BASE, "002_transformers_part2", "unique_slides", "slide_057.jpg"), "002 slide_057")
panel_edges(os.path.join(BASE, "002_transformers_part2", "unique_slides", "slide_049.jpg"), "002 slide_049")
panel_edges(os.path.join(BASE, "001_transformers_part1", "unique_slides", "slide_001.jpg"), "001 slide_001 (house reference)")

# ---- badge precise mask on 057 ----
px = im57.load()
say("\n== 057 badge precise mask (pale-yellow fill OR purple ring), region x 850..915 y 40..105 ==")
fx = fy = n = sx = sy = 0
minx, miny, maxx, maxy = 10**9, 10**9, -1, -1
ring_samples, fill_samples = [], []
for y in range(40, 106):
    for x in range(850, 916):
        r, g, b = px[x, y]
        pale_yellow = r > 215 and g > 215 and 120 < b < 205
        purple = 70 < r < 150 and 40 < g < 110 and b > 130
        if pale_yellow or purple:
            minx, miny = min(minx, x), min(miny, y)
            maxx, maxy = max(maxx, x), max(maxy, y)
            sx += x; sy += y; n += 1
            if purple: ring_samples.append((x, y, (r, g, b)))
            else: fill_samples.append((r, g, b))
say(f"  mask bbox x {minx}..{maxx} y {miny}..{maxy} -> d=({maxx-minx+1},{maxy-miny+1}) center=({(minx+maxx)/2:.1f},{(miny+maxy)/2:.1f}) n={n}")
if ring_samples:
    rm = tuple(sum(c[i] for _, _, c in ring_samples) // len(ring_samples) for i in range(3))
    say(f"  ring mean: #{rm[0]:02X}{rm[1]:02X}{rm[2]:02X} (house 6A5ACD)")
if fill_samples:
    fm = tuple(sum(c[i] for c in fill_samples) // len(fill_samples) for i in range(3))
    say(f"  fill mean: #{fm[0]:02X}{fm[1]:02X}{fm[2]:02X} (house FDFD96)")
# numeral darkest
dark, dpos = (255,)*3, None
for y in range(miny, maxy+1):
    for x in range(minx, maxx+1):
        r, g, b = px[x, y]
        if r+g+b < sum(dark) and not (b > 130 and r < 150):  # exclude ring
            dark, dpos = (r, g, b), (x, y)
say(f"  numeral darkest: #{dark[0]:02X}{dark[1]:02X}{dark[2]:02X} at {dpos} (house 333333)")
open(os.path.join(OUT, "probe3.txt"), "w").write("\n".join(lines) + "\n")
print("WROTE probe3.txt")
