#!/usr/bin/env python3
"""Attempt-2 self-check v2: containment excl chrome ring, tighter anchors."""
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide041/"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg"
ren = Image.open(QA + "render_3.png").convert("RGB")
org = Image.open(ORIG).convert("RGB")
rp, op = ren.load(), org.load()
RW, RH = ren.size
ok = True

# 1) containment: ink in the white margin EXCLUDING a 5px band along the chrome
# panel border (x 87..1913, y 94..1125 render px)
def content_ink(c):
    r, g, b = c
    return not (r > 235 and g > 235 and b > 235)
def is_chrome_red(c):
    r, g, b = c
    return r > 130 and g < 90 and b < 90

stray = 0
samples = []
for y in range(0, 94):
    for x in range(0, RW):
        if content_ink(rp[x, y]) and not (87 - 5 <= x <= 1913 + 5) and not is_chrome_red(rp[x, y]):
            stray += 1
            if len(samples) < 5: samples.append((x, y, rp[x, y]))
for y in range(94, RH):
    for x in range(0, 87 - 5):
        if content_ink(rp[x, y]) and not is_chrome_red(rp[x, y]):
            stray += 1
            if len(samples) < 5: samples.append((x, y, rp[x, y]))
    for x in range(1913 + 5, RW):
        if content_ink(rp[x, y]) and not is_chrome_red(rp[x, y]):
            stray += 1
            if len(samples) < 5: samples.append((x, y, rp[x, y]))
print(f"containment (chrome ring excluded): {stray} stray ink px; samples {samples}")
if stray > 150: ok = False; print("[FAIL] containment")
else: print("[PASS] frame-containment")

# 2) anchors with tight predicates (match attempt-1 methodology)
def bbox(pixels, pred, x0, y0, x1, y1):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(pixels[x, y]):
                xs.append(x); ys.append(y)
    if not xs: return None
    return (min(xs), min(ys), max(xs), max(ys), len(xs))

# center container TAN FILL ONLY (tight, like attempt-1: measured orig (286,208)-(521,525))
tan_tight = lambda c: abs(c[0]-223) < 18 and abs(c[1]-170) < 22 and abs(c[2]-117) < 28
rb = bbox(rp, tan_tight, 560, 400, 1120, 1120)
ob = bbox(op, tan_tight, 270, 195, 545, 540)
fb = tuple(round(v * 960 / 2000, 1) for v in rb[:4])
d = max(abs(fb[i] - ob[i]) for i in range(4))
print(f"anchor center container: render {fb} vs orig {ob[:4]} maxD {d:.1f} -> {'PASS' if d <= 6 else 'FAIL'}")
if d > 6: ok = False
# left schematic border: dark-green stroke (tight)
grn_tight = lambda c: c[1] > 70 and c[1] > c[0] + 40 and c[1] > c[2] + 40 and c[0] < 120
rb = bbox(rp, grn_tight, 100, 520, 420, 1060)
ob = bbox(op, grn_tight, 45, 250, 210, 500)
fb = tuple(round(v * 960 / 2000, 1) for v in rb[:4])
d = max(abs(fb[i] - ob[i]) for i in range(4))
print(f"anchor left schematic: render {fb} vs orig {ob[:4]} maxD {d:.1f} -> {'PASS' if d <= 6 else 'FAIL'}")
if d > 6: ok = False

print("RESULT:", "ALL CHECKS PASS" if ok else "CHECKS FAILED")
