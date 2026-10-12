#!/usr/bin/env python3
"""Dense-region crop PAIRS: original (left) vs render (right), same regions, 2x upscale.
Render px = ((fx-18.63)/0.96123, fy/0.95556) * 150/72."""
from PIL import Image, ImageDraw

ORIG = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg").convert("RGB")
REN = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide054/render_1.png").convert("RGB")
X0, SX, SY, K = 18.63, 0.96123, 0.95556, 150/72.0

regions = [
    ("R1 fraction K,q/sqrt(d)", (408, 178, 458, 228)),
    ("R2 mask column + cells",  (450, 186, 490, 372)),
    ("R3 top-right legend",     (722, 48, 850, 96)),
    ("R4 bottom-right legend",  (718, 442, 895, 516)),
    ("R5 W_k boxes + K strips", (168, 220, 265, 378)),
    ("R6 nodes + V strips",     (538, 214, 712, 378)),
    ("R7 W_q + q2 + Z2 arrow",  (252, 388, 348, 514)),
]
SC = 2.4
tiles = []
for name, (fx0, fy0, fx1, fy1) in regions:
    oc = ORIG.crop((fx0, fy0, fx1, fy1)).resize((int((fx1-fx0)*SC), int((fy1-fy0)*SC)), Image.LANCZOS)
    rx0, ry0 = (fx0 - X0)/SX*K, fy0/SY*K
    rx1, ry1 = (fx1 - X0)/SX*K, fy1/SY*K
    rc = REN.crop((int(rx0), int(ry0), int(rx1), int(ry1))).resize(oc.size, Image.LANCZOS)
    tiles.append((name, oc, rc))

pad, labh = 10, 22
colw = max(max(oc.width, rc.width) for _, oc, rc in tiles) + pad*2
W = colw*2 + pad*3
H = sum(max(oc.height, rc.height) + labh + pad for _, oc, rc in tiles) + pad
canvas = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(canvas)
y = pad
for name, oc, rc in tiles:
    d.text((pad, y), f"{name}  --  LEFT=original frame, RIGHT=recreation render", fill=(180, 0, 0))
    y += labh - 6
    canvas.paste(oc, (pad, y))
    d.rectangle([pad-1, y-1, pad+oc.width, y+oc.height+1], outline=(0, 0, 0))
    canvas.paste(rc, (colw + pad*2, y))
    d.rectangle([colw + pad*2-1, y-1, colw + pad*2 + rc.width, y+rc.height+1], outline=(0, 0, 0))
    y += max(oc.height, rc.height) + pad
canvas.save("crop_pairs.png")
print("saved crop_pairs.png", canvas.size)
