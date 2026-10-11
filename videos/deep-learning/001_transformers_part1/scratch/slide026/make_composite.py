#!/usr/bin/env python3
"""Build a labeled composite of ambiguous regions for ONE vision analysis call."""
from PIL import Image, ImageDraw

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")

PANELS = [
    ("A left-stack glyphs x52-148 y220-400", (52, 220, 148, 400), 3),
    ("B nodes+W-labels x488-700 y220-300", (488, 220, 700, 300), 3),
    ("C Ybox+arrow+Sigma x480-700 y110-230", (480, 110, 700, 230), 3),
    ("D strip glyphs+X2 x170-350 y462-525", (170, 462, 350, 525), 3),
    ("E bottom-left curve x50-200 y380-500", (50, 380, 200, 500), 2),
    ("F bottom-right curve x480-870 y380-512", (480, 380, 870, 512), 2),
    ("G box-to-bar zone x335-470 y190-410", (335, 190, 470, 410), 3),
    ("H red block arrow x250-320 y495-540", (250, 495, 320, 540), 4),
]

W = 1750
tiles = []
y = 0
for label, box, sc in PANELS:
    crop = IM.crop(box)
    crop = crop.resize((crop.width * sc, crop.height * sc), Image.LANCZOS)
    tiles.append((label, crop))
    y += crop.height + 34

comp = Image.new("RGB", (W, y + 10), (255, 255, 255))
d = ImageDraw.Draw(comp)
y = 0
for label, crop in tiles:
    d.rectangle([0, y, W, y + 24], fill=(230, 230, 250))
    d.text((6, y + 5), label, fill=(0, 0, 0))
    comp.paste(crop, (0, y + 28))
    y += crop.height + 34

comp.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide026/composite.png")
print("saved", comp.size)
