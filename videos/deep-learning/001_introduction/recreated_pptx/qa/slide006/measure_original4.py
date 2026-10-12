#!/usr/bin/env python3
# measure_original4.py — title density (bold vs regular), blue median, box right edge,
# chrome border positions in the original frame.
from PIL import Image, ImageFont
import numpy as np

ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (r > 110) & (r - g > 45) & (r - b > 35)
blue_loose = (b - r > 25) & (b - g > 25) & (b > 110) & (r < 160)

print("== title ink density (slide_005 empirical: ArialReg ~5.1, ArialBold ~7.19 px/pt-adv) ==")
n = int(red[84:126, 142:834].sum())
print(f"  title red px = {n}, advance 692 -> density {n/692:.2f}")

print("== bullet line density sanity (regular expected ~5) ==")
n2 = int(blue_loose[223:240, 205:563].sum())
print(f"  b2 blue px = {n2}, adv 353 -> density {n2/353:.2f}")
n3 = int(blue_loose[197:214, 205:312].sum())
print(f"  b1 blue px = {n3}, adv 107 -> density {n3/107:.2f}")

print("== blue median (core px, b-r>50 & b-g>50) y 197..476 x 204..565 ==")
reg = a[197:476, 204:565]
rr, gg, bb2 = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
core = (bb2 - rr > 50) & (bb2 - gg > 50)
px = reg[core]
print(f"  n core px: {len(px)}, median r,g,b: {np.median(px, axis=0)}")
# strongest 200 by (b - (r+g)/2)
sats = bb2[core] - (rr[core] + gg[core]) / 2
idx = np.argsort(-sats)[:200]
print(f"  top-200 saturated median: {np.median(px[idx], axis=0)}")

print("== box right border: cols 835..860, red any threshold, y 140..500 ==")
red_loose = (r - g > 20) & (r - b > 20) & (r > 100)
for x in range(835, 861):
    c = int(red_loose[140:500, x].sum())
    c2 = int(red[140:500, x].sum())
    if c > 30 or c2 > 30:
        print(f"  col {x}: loose {c} strict {c2}")
print("== box top border rows 128..138, x 100..800 strict count ==")
for y in range(128, 139):
    print(f"  row {y}: {int(red[y, 100:800].sum())}")

print("== chrome borders in ORIGINAL frame ==")
print("  left cols x 38..48 (loose red, y 50..500):")
for x in range(38, 49):
    c = int(red_loose[50:500, x].sum())
    if c > 100:
        print(f"    col {x}: {c}")
print("  right cols x 910..925:")
for x in range(910, 926):
    c = int(red_loose[50:500, x].sum())
    if c > 100:
        print(f"    col {x}: {c}")
print("  top rows y 40..50 (loose red, x 50..900):")
for y in range(40, 51):
    c = int(red_loose[y, 50:900].sum())
    if c > 300:
        print(f"    row {y}: {c}")

print("== header L1 phrase-end check: underline run ends 467; TimesB24 phrase adv + x93 ==")
ftB = ImageFont.truetype("/usr/share/fonts/TTF/Timesbd.TTF", 24)
print(f"  TimesB24 'Broadly applicable in many domains' adv = {ftB.getlength('Broadly applicable in many domains'):.1f} -> end x {93 + ftB.getlength('Broadly applicable in many domains'):.1f}")
print("== gap between phrase end and '(e.g.,' — check for a space before '(': ==")
ftR = ImageFont.truetype("/usr/share/fonts/TTF/Times.TTF", 24)
for rest in [" (e.g., finance, robotics,", "(e.g., finance, robotics,"]:
    print(f"  rest '{rest}' adv = {ftR.getlength(rest):.1f}; L1 total = {93 + ftB.getlength('Broadly applicable in many domains') + ftR.getlength(rest):.1f} (target end 692)")

print("== L2 start/end check ==")
l2 = "bioinformatics, vision, natural language, etc.). Some applications:"
print(f"  Times24 L2 adv = {ftR.getlength(l2):.1f} (target 626, x 94..719)")

print("== bullet-12 exact text-left and advance (dark px, y 485..498, x 186..360) ==")
dark = a.max(axis=2) < 150
sub = dark[485:498, 186:360]
ys, xs = np.where(sub)
print(f"  ink x {xs.min()+186}..{xs.max()+186} (text-left excl dot)")
cols = dark[485:498, 186:360].sum(axis=0)
first_ink = 186 + int(np.argmax(cols > 0))
print(f"  first ink col: {first_ink}")
ftA = ImageFont.truetype("/usr/share/fonts/TTF/Arial.TTF", 17.5)
print(f"  Arial17.5 '.. and many more' adv = {ftA.getlength('.. and many more'):.1f}; from 205 -> end {205 + ftA.getlength('.. and many more'):.1f} (measured end ~340)")
print(f"  Arial17.5 '.' adv = {ftA.getlength('.'):.1f}, ' ' adv = {ftA.getlength(' '):.1f}")
