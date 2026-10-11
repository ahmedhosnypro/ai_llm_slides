#!/usr/bin/env python3
"""Measure pass 4: clean logo bbox (exclude frame stroke x>=910), color modes, crop logo."""
from PIL import Image
from collections import Counter

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_001.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
px = im.load()

def is_canvas(r, g, b):
    return 222 <= r <= 240 and 224 <= g <= 242 and 221 <= b <= 239

# clean logo bbox in x 560..908, y 460..534
xs, ys = [], []
for y in range(455, 536):
    for x in range(560, 909):
        if not is_canvas(*px[x, y]):
            xs.append(x); ys.append(y)
print(f"logo ink bbox: x={min(xs)}-{max(xs)} ({min(xs)/72:.3f}-{max(xs)/72:.3f}in) y={min(ys)}-{max(ys)} ({min(ys)/72:.3f}-{max(ys)/72:.3f}in)  w={max(xs)-min(xs)+1} h={max(ys)-min(ys)+1}")

# per-row extents to see panel structure
for y in range(min(ys), max(ys)+1, 2):
    row = [x for x in range(560, 909) if not is_canvas(*px[x, y])]
    if row:
        print(f"  y={y}: x {min(row)}-{max(row)} n={len(row)}")

# color modes: credit name core pixels (blue), english logo line, arabic line
def mode_colors(x0, x1, y0, y1, pred):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = px[x, y]
            if pred(*p): c[p] += 1
    return c.most_common(5)

blue = lambda r, g, b: b > 100 and b - r > 60 and b - g > 40
print("credit-name blue modes:", mode_colors(373, 659, 325, 347, blue))
print("instr-name blue modes:", mode_colors(96, 358, 438, 455, blue))
dark = lambda r, g, b: (r + g + b) < 420
print("logo english-line modes:", mode_colors(690, 900, 500, 516, dark))
print("logo arabic-line modes:", mode_colors(690, 900, 486, 498, dark))
print("logo teal-panel modes:", mode_colors(600, 680, 475, 520, lambda r, g, b: g > 80 and g - r > 20))
red = lambda r, g, b: r > 120 and g < 90 and b < 90
print("title red modes:", mode_colors(254, 677, 135, 190, red))
print("prepared red modes:", mode_colors(460, 571, 301, 320, red))

# crosshair exact
xs, ys = [], []
for y in range(190, 220):
    for x in range(165, 195):
        r, g, b = px[x, y]
        if (231 - r) > 12 and (233 - g) > 12 and (230 - b) > 12:
            xs.append(x); ys.append(y)
print(f"crosshair bbox x={min(xs)}-{max(xs)} ({min(xs)/72:.3f}-{max(xs)/72:.3f}in) y={min(ys)}-{max(ys)} ({min(ys)/72:.3f}-{max(ys)/72:.3f}in)")

# crop logo to ink bbox with no padding, save PNG
x0, x1, y0, y1 = min(xs_l := xs, 0) if False else min(xs), max(xs), min(ys), max(ys)
crop = im.crop((x0, y0, x1 + 1, y1 + 1))
out = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/zewail_logo_slide001.png"
crop.save(out)
print(f"cropped logo {crop.size} -> {out}; embed size in: {crop.size[0]/72:.4f} x {crop.size[1]/72:.4f}")
