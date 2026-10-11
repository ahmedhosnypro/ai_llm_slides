#!/usr/bin/env python3
"""Cube-wall structure maps: middle grid + left stack vertical/column scans,
label-box text line color segmentation, right box right border."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def cls(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if R > 235 and G > 235 and B > 230: return "."   # white
    if G > 150 and G - R > 50 and G - B > 80: return "F"  # bright front green
    if G > 60 and G - R > 20 and G - B > 30 and G <= 150: return "t"  # dark top green
    if R > 120 and B > 120 and G < 100: return "M"
    if R > 150 and G < 110 and B < 110: return "R"
    return "?"

print("=== MIDDLE GRID 2px map x372..522, y248..428 ===")
print("     " + "".join(str((x // 10) % 10) for x in range(372, 523, 2)))
for y in range(248, 429, 2):
    print(f"{y:4d} " + "".join(cls(a[y, x]) for x in range(372, 523, 2)))

print()
print("=== LEFT STACK 2px map x160..236, y252..436 ===")
print("     " + "".join(str((x // 10) % 10) for x in range(160, 237, 2)))
for y in range(252, 437, 2):
    print(f"{y:4d} " + "".join(cls(a[y, x]) for x in range(160, 237, 2)))

print()
print("=== TEXT LINE COLOR SEGMENTATION (per-x dominant hue of dark-ish text pixels) ===")
def line_hue(name, y0, y1, x0, x1):
    print(f"  {name} y{y0}..{y1}:")
    out = []
    for x in range(x0, x1):
        col = a[y0:y1, x]
        rr = gg = bb = kk = mm = 0
        for px in col:
            R, G, B = int(px[0]), int(px[1]), int(px[2])
            if R > 235 and G > 235 and B > 230: continue
            if R > 120 and B > 120 and G < 110: mm += 1
            elif B > R + 30 and B > G + 20: bb += 1
            elif G > R + 30 and G > B + 20: gg += 1
            elif R > G + 40 and R > B + 40: rr += 1
            elif R < 120 and G < 120 and B < 120: kk += 1
        tot = rr + gg + bb + kk + mm
        if tot < 2: out.append(" ")
        elif mm >= rr and mm >= gg and mm >= bb and mm >= kk: out.append("M")
        elif bb >= rr and bb >= gg and bb >= kk: out.append("B")
        elif gg >= rr and gg >= bb and gg >= kk: out.append("G")
        elif kk >= rr: out.append("K")
        else: out.append("R")
    # compress runs
    s = "".join(out)
    runs = []
    prev = None; st = 0
    for i, c in enumerate(s):
        if c != prev:
            if prev is not None: runs.append((x0 + st, x0 + i - 1, prev))
            prev = c; st = i
    runs.append((x0 + st, x0 + len(s) - 1, prev))
    print("    " + " | ".join(f"{c} x{a_}..{b_}" for a_, b_, c in runs if c != " " or b_ - a_ > 2))

line_hue("LEFT box L1", 200, 213, 75, 340)
line_hue("LEFT box L2", 216, 230, 75, 340)
line_hue("MID box L1", 199, 213, 335, 620)
line_hue("MID box L2", 216, 230, 335, 620)
line_hue("RIGHT box L1", 170, 184, 620, 890)
line_hue("RIGHT box L2", 187, 203, 620, 890)
line_hue("RIGHT box L3", 204, 220, 620, 890)

print()
print("=== RIGHT BOX right border: row y=195, x870..890 raw")
print("  ", [tuple(a[195, x]) for x in range(870, 891)])
print("=== MIDDLE BOX right border: row y=210, x595..625 raw")
print("  ", [tuple(a[210, x]) for x in range(595, 626)])
print("=== MIDDLE BOX left border recheck: row y=210, x336..348 raw")
print("  ", [tuple(a[210, x]) for x in range(336, 349)])
print("=== LEFT BOX borders: col x=200, y190..200 and y232..242 raw")
print("  top:", [tuple(a[y, 200]) for y in range(190, 201)])
print("  bot:", [tuple(a[y, 200]) for y in range(232, 243)])
print("=== LEFT BOX right border: row y=210, x322..336 raw")
print("  ", [tuple(a[210, x]) for x in range(322, 337)])
