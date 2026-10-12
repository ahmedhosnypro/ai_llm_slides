#!/usr/bin/env python3
"""Pass 2 — trace faint stem shafts + hunt Softmax-side feeds (read-only)."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_008.jpg").convert("RGB")).astype(int)
R, G, B = frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]
# loosest reddish: any pixel notably redder than the peach bg (bg ~ (245,220,200))
reddish = (R - G >= 25) & (R - B >= 25) & (R >= 150)

def contig(xs):
    if len(xs) == 0:
        return []
    runs, s = [], xs[0]
    for i in range(1, len(xs)):
        if xs[i] != xs[i - 1] + 1:
            runs.append((int(s), int(xs[i - 1]))); s = xs[i]
    runs.append((int(s), int(xs[-1])))
    return runs

def amap(x0, x1, y0, y1):
    """1px ASCII map; '#'=strong red, '+'=reddish, '.'=faint, ' '=bg."""
    for y in range(y0, y1 + 1):
        line = []
        for x in range(x0, x1 + 1):
            r, g, b = frame[y, x]
            if (R - G >= 25) and (R - B >= 25) and R >= 150:
                line.append("#" if (R - G >= 60) else "+")
            elif r < 225 and (r - g) >= 12:
                line.append(".")
            else:
                line.append(" ")
        print(f"{y:3d} " + "".join(line))

print("=== A) FEED ZONE: reddish row profile x 455..514, y 195..395 (n>=4) ===")
for y in range(195, 395):
    xs = np.nonzero(reddish[y, 455:514])[0] + 455
    if len(xs) >= 4:
        print(f"y{y:3d}: n={len(xs):3d} x {xs.min()}..{xs.max()}  runs: "
              + " ".join(f"{a}-{b}" for a, b in contig(xs)))

print("\n=== B) SOFTMAX PILL right edge: column x 486..496 reddish counts y 195..390 ===")
for x in range(484, 500):
    ys = np.nonzero(reddish[195:390, x])[0] + 195
    if len(ys) >= 4:
        print(f"x{x:3d}: n={len(ys):3d} y {ys.min()}..{ys.max()}")

print("\n=== C) STEM SHAFTS: reddish column profiles x 526..622, y 210..390 ===")
for x in range(526, 623):
    ys = np.nonzero(reddish[210:390, x])[0] + 210
    if len(ys) >= 6:
        print(f"x{x:3d}: n={len(ys):3d} runs: " + " ".join(f"{a}-{b}" for a, b in contig(ys)))

print("\n=== D) color probe along stem centerlines (x531/560/588/617, y step 10) ===")
for x in (531, 560, 588, 589, 617):
    vals = []
    for y in range(212, 372, 10):
        r, g, b = frame[y, x]
        vals.append(f"y{y}:({r},{g},{b})")
    print(f"x{x}: " + " ".join(vals))

print("\n=== E) fine 1px ASCII map: arrowhead band x 524..542, y 209..226 ===")
amap(524, 542, 209, 226)

print("\n=== F) fine 1px ASCII map: stem-3 region x 580..596, y 209..300 ===")
amap(580, 596, 209, 300)

print("\n=== G) fine 1px ASCII map: stem-4 region x 610..624, y 209..340 ===")
amap(610, 624, 209, 340)

print("\n=== H) ring tops vs stem bottoms: does each stem REACH its ring? ===")
for name, (x0, x1) in [("s1", (528, 534)), ("s2", (556, 563)), ("s3", (584, 591)), ("s4", (613, 621))]:
    for y in range(210, 380):
        xs = np.nonzero(reddish[y, x0:x1 + 1])[0]
        if len(xs):
            pass
    # print last reddish row (bottom end of shaft)
    rows = [y for y in range(210, 380) if reddish[y, x0:x1 + 1].any()]
    if rows:
        # find contiguous blocks
        blocks, s = [], rows[0]
        for i in range(1, len(rows)):
            if rows[i] != rows[i - 1] + 1:
                blocks.append((s, rows[i - 1])); s = rows[i]
        blocks.append((s, rows[-1]))
        print(f"{name} x{x0}-{x1}: blocks " + " ".join(f"{a}-{b}" for a, b in blocks))
