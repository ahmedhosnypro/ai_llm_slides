#!/usr/bin/env python3
"""Side-by-side probe composites: ORIGINAL 002:37 frame (slide space) vs PARENT render
(imported 001:19 composition, base_960.png). Same slide-space window per zone, so the
two halves align. 2x LANCZOS. Labels name the zone and the axis."""
from PIL import Image, ImageDraw

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/base_960.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/slide037_slide_space.png"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/probes"

base = Image.open(BASE).convert("RGB")
orig = Image.open(ORIG).convert("RGB")

ZONES = {
    "p1_pin_circle":  ((565, 140, 780, 480), 2.0),
    "p2_arch_top":    ((560, 95, 905, 300), 2.0),
    "p3_arch_bottom": ((560, 300, 905, 530), 2.0),
    "p4_funnel":      ((185, 225, 660, 465), 1.5),
    "p5_title_legend":((40, 40, 560, 215), 1.5),
    "p6_insets":      ((48, 205, 520, 520), 1.5),
}

def stack(name, box, zoom):
    a = orig.crop(box)
    b = base.crop(box)
    w = int((box[2] - box[0]) * zoom)
    h = int((box[3] - box[1]) * zoom)
    a = a.resize((w, h), Image.LANCZOS)
    b = b.resize((w, h), Image.LANCZOS)
    LAB = 22
    out = Image.new("RGB", (w, LAB * 2 + h * 2 + 8), (255, 255, 255))
    d = ImageDraw.Draw(out)
    d.rectangle([0, 0, w, LAB - 1], fill=(0, 120, 0))
    d.text((6, 4), f"TOP = ORIGINAL 002:37 frame  zone slide x{box[0]}-{box[2]} y{box[1]}-{box[3]}", fill=(255, 255, 255))
    out.paste(a, (0, LAB))
    y2 = LAB + h + 4
    d.rectangle([0, y2, w, y2 + LAB - 1], fill=(150, 0, 0))
    d.text((6, y2 + 4), "BOTTOM = PARENT RENDER (certified 001:19 composition)", fill=(255, 255, 255))
    out.paste(b, (0, y2 + LAB))
    out.save(f"{OUT}/{name}.png")
    print(name, out.size)

for n, (box, z) in ZONES.items():
    stack(n, box, z)
