#!/usr/bin/env python3
"""PIL forensics pass 4 — slide_047.jpg final details."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_047.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)

red = lambda s: (s[:,:,0] > 120) & (s[:,:,0] - s[:,:,1] > 60) & (s[:,:,0] - s[:,:,2] > 60)

def ascii_map(x0, x1, y0, y1, pred, label=""):
    print(f"  {label} x {x0}..{x1} y {y0}..{y1}:")
    hdr = "      " + "".join(str((x // 10) % 10) for x in range(x0, x1))
    print(hdr)
    for y in range(y0, y1):
        row = "".join("#" if pred(a[y:y+1, x:x+1])[0][0] else "." for x in range(x0, x1))
        print(f"  y={y:3d} {row}")

loose = lambda s: (s.sum(axis=2) < 650)
notred = lambda s: ~red(s)
dk_loose = lambda s: (s.sum(axis=2) < 650) & notred(s)

# 1. full arrow
print("-- ARROW full map --")
ascii_map(735, 795, 414, 445, dk_loose, "arrow")

# 2. eq3 full
print("\n-- EQ3 full map --")
ascii_map(315, 545, 282, 314, dk_loose, "eq3")

# 3. eq4 full
print("\n-- EQ4 full map --")
ascii_map(315, 500, 318, 362, dk_loose, "eq4")

# 4. grid numeral '1' cell TL
print("\n-- grid cell TL numeral (1) --")
ascii_map(571, 612, 363, 396, lambda s: s.sum(axis=2) < 260, "num1")
print("cell fill away from numeral:", a[370, 578].tolist(), a[390, 578].tolist())

# 5. ring marker color
print("\n-- marker ring color samples --")
# marker1 ring at y 230..237 x 91..101
for (yy, xx) in [(230, 96), (231, 94), (233, 92), (234, 101), (236, 95)]:
    print(f"  ({xx},{yy}) =", a[yy, xx].tolist())
# bullet text color mid-stroke
print("  text stroke (231,120) =", a[231, 120].tolist(), " (232,117) =", a[232, 117].tolist())

# 6. label box1 text map
print("\n-- label box1 'Activation function:' text --")
ascii_map(112, 320, 289, 312, lambda s: (s[0,0,2] > 100) & (s[0,0,2] - s[0,0,0] > 30), "blue-ink")

# 7. intro line 2 left portion (check glyphs)
print("\n-- intro line2 map x 78..320, y 155..178 (red-ish) --")
ascii_map(78, 320, 155, 178, lambda s: (s[0,0,0] - s[0,0,1] > 40) & (s[0,0,0] > 120), "red-ink")

# 8. legend border color more samples
print("\n-- legend border samples --")
for (yy, xx) in [(348, 500), (349, 520), (474, 500), (475, 520), (400, 455), (400, 456), (400, 565), (400, 566)]:
    print(f"  ({xx},{yy}) =", a[yy, xx].tolist())

# 9. x=58 red line: verify width and endpoints
print("\n-- x=58 red line --")
for x in (56, 57, 58, 59, 60, 61):
    ys = np.nonzero(red(a[200:510, x:x+1])[:, 0])[0]
    print(f"  x={x}: n={len(ys)}", f"y {200+ys.min()}..{200+ys.max()}" if len(ys) else "")

# 10. label box border color samples (box1 + box2)
print("\n-- label box borders --")
for (yy, xx) in [(287, 200), (313, 200), (300, 110), (300, 310), (323, 200), (350, 200), (337, 110), (337, 310)]:
    print(f"  ({xx},{yy}) =", a[yy, xx].tolist())

# 11. content box border exact color (multiple)
print("\n-- content box border colors --")
for (yy, xx) in [(220, 300), (220, 600), (486, 300), (487, 600), (350, 82), (350, 874)]:
    print(f"  ({xx},{yy}) =", a[yy, xx].tolist())

# 12. title color samples (core strokes)
print("\n-- title stroke samples --")
for (yy, xx) in [(80, 148), (85, 165), (75, 460), (85, 480), (80, 600), (85, 780)]:
    print(f"  ({xx},{yy}) =", a[yy, xx].tolist())

# 13. intro line colors core
print("\n-- intro line core samples --")
for (yy, xx) in [(138, 90), (140, 200), (165, 90), (170, 300), (195, 90), (195, 400)]:
    print(f"  ({xx},{yy}) =", a[yy, xx].tolist())
