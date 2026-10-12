#!/usr/bin/env python3
"""Build labeled contact sheets of slide_017.jpg dense regions for gate vision analysis."""
from PIL import Image, ImageDraw

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide017"
im = Image.open(F).convert("RGB")

def crop(x0, y0, x1, y1, scale):
    c = im.crop((x0, y0, x1, y1))
    return c.resize((c.width * scale, c.height * scale), Image.LANCZOS)

def sheet(name, crops):
    """crops: list of (label, PIL image)"""
    W = max(c.width for _, c in crops) + 20
    H = sum(c.height + 34 for _, c in crops) + 10
    s = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(s)
    y = 5
    for label, c in crops:
        d.text((10, y), label, fill=(200, 0, 0))
        y += 24
        s.paste(c, (10, y))
        d.rectangle([9, y - 1, 10 + c.width, y + c.height], outline=(0, 120, 255))
        y += c.height + 10
    s.save(f"{OUT}/{name}.png")
    print(f"{name}.png {s.size}")

# Sheet A: top pipeline
sheet("sheetA_top", [
    ("A1 title+badge zone x495..910 y42..108 (2x)", crop(495, 42, 910, 108, 2)),
    ("A2 top embedding strip x395..505 y44..80 (5x)", crop(395, 44, 505, 80, 5)),
    ("A3 LT box full x310..570 y80..125 (3x)", crop(310, 80, 570, 125, 3)),
    ("A4 LT box bottom-right corner x420..565 y90..125 (6x)", crop(420, 90, 565, 125, 6)),
    ("A5 concat bar full x180..700 y118..155 (2x)", crop(180, 118, 700, 155, 2)),
    ("A6 concat bar left label x182..320 y122..152 (4x)", crop(182, 122, 320, 152, 4)),
    ("A7 concat bar right half + Y chips x430..700 y122..152 (4x)", crop(430, 122, 700, 152, 4)),
    ("A8 drop-lines zone x395..620 y148..195 (4x)", crop(395, 148, 620, 195, 4)),
])

# Sheet B: h1 layer internals
sheet("sheetB_h1", [
    ("B1 left inputs+Wboxes+Kstrips x66..270 y280..465 (3x)", crop(66, 280, 270, 465, 3)),
    ("B2 Dot Product box x150..270 y285..460 (4x)", crop(150, 285, 270, 460, 4)),
    ("B3 ovals+pills zone x255..545 y270..320 (4x)", crop(255, 270, 545, 320, 4)),
    ("B4 Scaling+Softmax pills x255..400 y295..470 (3x)", crop(255, 295, 400, 470, 3)),
    ("B5 Sigma + circle-x nodes x330..545 y295..470 (3x)", crop(330, 295, 545, 470, 3)),
    ("B6 V labels + W_v boxes + output strips x540..700 y290..475 (3x)", crop(540, 290, 700, 475, 3)),
])

# Sheet C: rear heads, bottom, legend, swoosh
sheet("sheetC_misc", [
    ("C1 rear head h2/h3 bottom edges W chips x420..660 y215..270 (4x)", crop(420, 215, 660, 270, 4)),
    ("C2 rear head right edge X strips x690..780 y190..450 (3x)", crop(690, 190, 780, 450, 3)),
    ("C3 rear heads Similarity/WeightedSUM ovals x430..770 y180..320 (2x)", crop(430, 180, 770, 320, 2)),
    ("C4 bottom sequence strip + magenta cell x150..370 y470..510 (4x)", crop(150, 470, 370, 510, 4)),
    ("C5 W_q box + q strip + red arrow x180..320 y440..515 (4x)", crop(180, 440, 320, 515, 4)),
    ("C6 legend box x715..905 y430..515 (3x)", crop(715, 430, 905, 515, 3)),
    ("C7 swoosh + label x560..870 y280..520 (1.5x->2x)", crop(560, 280, 870, 520, 2)),
    ("C8 h=1 black pill zoom x550..600 y262..292 (8x)", crop(550, 262, 600, 292, 8)),
    ("C9 gold bar top zone x480..560 y180..230 (5x)", crop(480, 180, 560, 230, 5)),
])
