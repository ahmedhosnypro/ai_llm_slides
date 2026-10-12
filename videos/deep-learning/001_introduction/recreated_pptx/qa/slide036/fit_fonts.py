#!/usr/bin/env python3
# fit_fonts.py — PIL metric fit for slide 036 text blocks (frame px, 1px=1pt).
from PIL import ImageFont

ARIAL_B = "/usr/share/fonts/TTF/Arialbd.TTF"
COMIC = "/usr/share/fonts/TTF/Comic.TTF"

def ink(font, s):
    bb = font.getbbox(s)
    return bb  # (x0,y0,x1,y1) ink box incl bearings-origin

print("== TITLE L1: 'How many Parameters are  in the  RGB' target ink w=643 (x157..799), cap+desc band 62..92 (31px), pitch 39 ==")
s1 = "How many Parameters are  in the  RGB"
for size in range(28, 39):
    f = ImageFont.truetype(ARIAL_B, size)
    bb = f.getbbox(s1)
    w = bb[2] - bb[0]
    capH = f.getbbox("H")[3] - f.getbbox("H")[1]
    desc = f.getbbox("y")[3] - f.getbbox("y")[1]
    band = f.getbbox(s1)[3] - 0  # top-relative
    print(f"  {size}pt: ink w={w} (bb x0={bb[0]}), H cap={capH}, y-desc={desc}, ink h={bb[3]-bb[1]}")

print("== TITLE L2: 'Image filter  ( K=3 )' target ink w=308 (x329..636), band 101..131 (31px) ==")
s2 = "Image filter  ( K=3 )"
for size in range(28, 39):
    f = ImageFont.truetype(ARIAL_B, size)
    bb = f.getbbox(s2)
    print(f"  {size}pt: ink w={bb[2]-bb[0]} (x0={bb[0]}), ink h={bb[3]-bb[1]}")

print("== QUESTION Comic Sans: 'How many weights for this neuron?' target ink w=638 (x157..794) ==")
sq = "How many weights for this neuron?"
for size in range(24, 36):
    f = ImageFont.truetype(COMIC, size)
    bb = f.getbbox(sq)
    capH = f.getbbox("H")[3] - f.getbbox("H")[1]
    print(f"  {size}pt: ink w={bb[2]-bb[0]} (x0={bb[0]}), H cap={capH}, ink h={bb[3]-bb[1]}")

# ---- frame's own chrome border scan (for ground-rule note) ----
from PIL import Image
import numpy as np
im = np.array(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_036.jpg").convert("RGB")).astype(int)
red = (im[:, :, 0] > 130) & (im[:, :, 1] < 80) & (im[:, :, 2] < 80)
print("== frame chrome: red cols x 30..120 & 850..930 (y 150..450), red rows y 35..70 (x 200..800) ==")
for x in list(range(30, 121)) + list(range(850, 931)):
    n = red[150:450, x].sum()
    if n > 100:
        print(f"  col x={x}: n={n}")
for y in range(35, 71):
    n = red[y, 200:800].sum()
    if n > 100:
        print(f"  row y={y}: n={n} (x 200..800)")
# gray panel extent at row 300: first/last non-white col
row = im[300]
nw = np.where(row.mean(axis=1) < 240)[0]
print(f"  row300 non-white cols: {nw.min()}..{nw.max()}" if len(nw) else "  row300 all white")
# box border core color
print("  box top border core (y156, x300..310):", [tuple(im[156, x]) for x in (300, 305, 310)])
# box interior vs panel flat samples
print("  box interior (500,430):", tuple(im[430, 500]), " (200,180):", tuple(im[180, 200]), " (700,350):", tuple(im[350, 700]))
print("  panel outside box (80,300):", tuple(im[300, 80]), " (880,300):", tuple(im[300, 880]))
