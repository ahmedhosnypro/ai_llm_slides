#!/usr/bin/env python3
"""Build labeled montage of dense micro-label zones from the ORIGINAL frame, 3x upscale."""
from PIL import Image, ImageDraw

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg"
img = Image.open(F).convert("RGB")

zones = [
    ("A_top-connection-zone", (376, 470, 240, 300)),
    ("B_mid+bottom-connections", (376, 470, 285, 400)),
    ("C_output-labels-right-of-triangles", (570, 670, 240, 410)),
    ("D_power-supplies-zone", (390, 670, 405, 472)),
    ("E_bluebox-right-edge-labels", (360, 400, 248, 392)),
    ("F_container-top-and-tag", (450, 672, 186, 246)),
]
S = 3
PAD = 8
CROPW = 640
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
    d.text((PAD, y), f"ZONE {name}  (upscaled x{S})", fill=(200, 0, 0))
    y += 26
    m.paste(c, (PAD, y))
    d.rectangle([PAD - 1, y - 1, PAD + c.width, y + c.height], outline=(0, 120, 255))
    y += c.height + PAD
m.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide026/zone_montage.png")
print("saved", m.size)
