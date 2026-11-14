#!/usr/bin/env python3
# PIL check of render_5.png (v5 build) vs original slide_024.jpg, normalized to 960x540.
from PIL import Image
import sys

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
orig = Image.open(f"{NS}/unique_slides/slide_024.jpg").convert("RGB")
rend = Image.open(f"{NS}/recreated_pptx/qa/slide024/render_5.png").convert("RGB")
rend = rend.resize((960, 540), Image.LANCZOS)

def px(img, x, y):
    return img.getpixel((x, y))

def region_ink(img, x0, y0, x1, y1, pred):
    n = 0
    for y in range(max(0, y0), min(540, y1)):
        for x in range(max(0, x0), min(960, x1)):
            if pred(img.getpixel((x, y))):
                n += 1
    return n

def is_red(p):
    r, g, b = p
    return r > 120 and r > g + 50 and r > b + 50

def is_dark(p):
    r, g, b = p
    return r < 100 and g < 100 and b < 100

def is_gray_ink(p):
    r, g, b = p
    return abs(r - g) < 25 and abs(g - b) < 25 and 60 < r < 200

print("== 1. Threshold box containment (box x691-731 y110-188) ==")
# red label ink above box top (y 100-109) within x 672-750 would be overflow
above = region_ink(rend, 672, 100, 750, 110, is_red)
inside = region_ink(rend, 691, 110, 731, 188, is_red)
print(f"render: red-ink above box top = {above}px, red-ink inside box = {inside}px")
above_o = region_ink(orig, 672, 100, 750, 110, is_red)
inside_o = region_ink(orig, 691, 110, 731, 188, is_red)
print(f"orig  : red-ink above box top = {above_o}px, red-ink inside box = {inside_o}px")

print("== 2. Matrix gutters ==")
# upper matrix label col x86-109 y96-141; Actual rotated at x67.5-97.5 y122-130
# check P/N row labels present in label col (dark ink at row centers y~118, y~133)
for name, (x0, y0, x1, y1) in {
    "upper label col": (86, 96, 109, 141),
    "upper Actual zone": (60, 110, 86, 140),
    "lower label col": (92, 163, 129, 243),
    "lower Actual zone": (55, 200, 92, 240),
}.items():
    print(f"  {name}: render dark-ink={region_ink(rend, x0, y0, x1, y1, is_dark)} orig dark-ink={region_ink(orig, x0, y0, x1, y1, is_dark)}")

print("== 3. Plane sizes (body width ~0.68*110=75px) ==")
for (cx, cy) in [(128, 266), (282, 296), (572, 299), (855, 356)]:
    # count gray-ink pixels in a 90x40 window around plane center
    n_r = region_ink(rend, cx - 45, cy - 20, cx + 45, cy + 20, is_gray_ink)
    n_o = region_ink(orig, cx - 45, cy - 20, cx + 45, cy + 20, is_gray_ink)
    print(f"  plane({cx},{cy}): render gray-ink={n_r} orig gray-ink={n_o}")

print("== 4. Aircraft/table collision (matrix bottom y=243, plane0 top ~248) ==")
strip_r = region_ink(rend, 90, 243, 170, 249, is_gray_ink)
strip_o = region_ink(orig, 90, 243, 170, 249, is_gray_ink)
print(f"  gap strip y243-249 x90-170: render gray-ink={strip_r} orig gray-ink={strip_o}")

print("== 5. Class oval fills ==")
for name, (x, y) in {"Class I": (816, 134), "Class II": (816, 174)}.items():
    print(f"  {name}: render px={px(rend, x, y)} orig px={px(orig, x, y)}")

print("== 6. House chrome ==")
print(f"  bg render={px(rend, 400, 300)} orig={px(orig, 400, 300)}")
print(f"  frame render={px(rend, 11, 270)} orig={px(orig, 11, 270)}")
print(f"  badge render={px(rend, 950, 25)} orig={px(orig, 950, 25)}")
