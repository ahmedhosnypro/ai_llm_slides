#!/usr/bin/env python3
"""Montage 2: remaining dense micro-zones at 4x upscale."""
from PIL import Image, ImageDraw

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg"
img = Image.open(F).convert("RGB")

zones = [
    ("G_mystery-band-under-dual-adc", (412, 610, 278, 298)),
    ("H_midpath-output-and-R-labels", (570, 672, 330, 372)),
    ("I_5V-3.3V-and-encoder-supply", (455, 672, 408, 470)),
    ("J_24V-label-and-gray-box", (350, 425, 415, 450)),
    ("K_comparators-block", (455, 610, 348, 405)),
    ("L_wires-and-labels-encoder-connector", (640, 745, 265, 400)),
    ("M_caption-line1", (300, 800, 476, 496)),
    ("N_bluebox-labels-horiz", (355, 400, 250, 392)),
]
S = 4
PAD = 8
crops = []
for name, (x0, x1, y0, y1) in zones:
    c = img.crop((x0, y0, x1, y1))
    c = c.resize(((x1 - x0) * S, (y1 - y0) * S), Image.LANCZOS)
    crops.append((name, c))

W = max(c.width for _, c in crops) + 2 * PAD
H = sum(c.height + 34 + PAD for _, c in crops) + PAD
m = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(m)
y = PAD
for name, c in crops:
    d.text((PAD, y), f"ZONE {name}  (x{S})", fill=(200, 0, 0))
    y += 26
    m.paste(c, (PAD, y))
    d.rectangle([PAD - 1, y - 1, PAD + c.width, y + c.height], outline=(0, 120, 255))
    y += c.height + PAD
m.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide026/zone_montage2.png")
print("saved", m.size)
