#!/usr/bin/env python3
"""Side-by-side comparison montage: ORIGINAL (left) vs RENDER (right) per dense zone, 2.5x."""
from PIL import Image, ImageDraw

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg"
RR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide026/render_1.png"
orig = Image.open(FR).convert("RGB")
rend = Image.open(RR).convert("RGB")

K = 150 / 72.0
MX, SXX, SYY = 18.628, 0.96123, 0.95556

def crop_render(fx0, fy0, fx1, fy1):
    rx0 = (fx0 - MX) / SXX * K; ry0 = fy0 / SYY * K
    rx1 = (fx1 - MX) / SXX * K; ry1 = fy1 / SYY * K
    return rend.crop((int(rx0), int(ry0), int(rx1), int(ry1)))

zones = [
    ("Z1_bluebox+labels", (225, 232, 400, 392)),
    ("Z2_toppath+corridor", (405, 183, 672, 296)),
    ("Z3_mid+comparators", (405, 284, 672, 405)),
    ("Z4_powersupplies", (350, 405, 672, 470)),
    ("Z5_rightrect", (655, 183, 862, 470)),
    ("Z6_title+subtitle", (180, 48, 760, 110)),
    ("Z7_captions", (300, 470, 800, 520)),
    ("Z8_posarrow", (125, 282, 240, 352)),
]
S = 2
PAD = 10
pairs = []
for name, (x0, y0, x1, y1) in zones:
    o = orig.crop((x0, y0, x1, y1)).resize(((x1 - x0) * S, (y1 - y0) * S), Image.LANCZOS)
    r = crop_render(x0, y0, x1, y1).resize(((x1 - x0) * S, (y1 - y0) * S), Image.LANCZOS)
    pairs.append((name, o, r))

W = max(o.width + r.width + 3 * PAD for _, o, r in pairs)
H = sum(max(o.height, r.height) + 40 + PAD for _, o, r in pairs) + PAD
m = Image.new("RGB", (W, H), (230, 230, 230))
d = ImageDraw.Draw(m)
y = PAD
for name, o, r in pairs:
    d.text((PAD, y), f"{name}  |  LEFT=ORIGINAL FRAME  RIGHT=RECREATION (attempt 1)", fill=(150, 0, 0))
    y += 30
    m.paste(o, (PAD, y))
    m.paste(r, (PAD * 2 + o.width, y))
    d.rectangle([PAD - 1, y - 1, PAD + o.width, y + o.height], outline=(0, 90, 200))
    d.rectangle([PAD * 2 + o.width - 1, y - 1, PAD * 2 + o.width + r.width, y + r.height], outline=(200, 90, 0))
    y += max(o.height, r.height) + PAD
m.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide026/compare_1.png")
print("saved", m.size)
