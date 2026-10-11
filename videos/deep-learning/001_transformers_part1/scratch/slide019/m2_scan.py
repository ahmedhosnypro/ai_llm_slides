#!/usr/bin/env python3
"""m2_scan.py — callout zone map + full gap scan + unquantized box modes."""
from PIL import Image
import collections

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg").convert("RGB")
px = IM.load()

def q(c, s=32):
    return (c[0] // s * s, c[1] // s * s, c[2] // s * s)

# --- callout zone ASCII map (x40..570, y60..260), 4px cells --------------------
print("== callout zone map (x40..570 step4, y60..260 step4); legend: .=bg W=white-ish B=blue-ish G=green-ish Y=yellow-ish R=red-ish D=dark K=gray-ish ?=other")
def cls(c):
    r, g, b = c
    if r > 235 and g > 235 and b > 235: return "."
    if abs(r - g) < 26 and abs(g - b) < 26:
        if r < 90: return "D"
        return "K" if r < 215 else "."
    if b > r + 24 and b > g + 8: return "B"
    if g > r + 18 and g >= b: return "G"
    if r > 200 and g > 200 and b < 140: return "Y"
    if r > g + 40 and r > b + 40: return "R"
    if r + g + b < 300: return "D"
    return "?"
for y in range(60, 260, 4):
    row = ""
    for x in range(40, 572, 4):
        row += cls(px[x, y])
    print(f"{y:3d} {row}")

# --- unquantized modes of candidate solid regions ------------------------------
def mode_exact(x0, y0, x1, y1, topn=8):
    cnt = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            cnt[px[x, y]] += 1
    return cnt.most_common(topn)

print("\n== exact modes, rows through callout zone ==")
for y in [95, 105, 125, 145, 165, 185, 205, 225, 240]:
    print(f"y={y}:", mode_exact(60, y, 560, y + 1, 6))

# --- full gap scan x455..578, y90..530 ------------------------------------------
print("\n== gap scan x455..578: rows with ink (excluding fig-frame edge x570..578) ==")
for y in range(90, 532):
    xs = [x for x in range(455, 570) if sum(px[x, y]) < 620]
    if xs:
        print(f"y={y:3d}: x {min(xs)}..{max(xs)} n={len(xs)} first={px[xs[0], y]} mid={px[xs[len(xs)//2], y]}")
