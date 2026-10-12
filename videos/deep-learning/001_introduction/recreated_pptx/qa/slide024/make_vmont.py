#!/usr/bin/env python3
"""Build labeled montages for the slide_024 vision reads (labels A/B, neurons, fan+arrows)."""
from PIL import Image, ImageDraw

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide024/"
IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_024.jpg").convert("RGB")

def stack(crops, out, scale=1):
    imgs = []
    for label, box in crops:
        c = IM.crop(box)
        if scale > 1:
            c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
        imgs.append((label, c))
    w = max(i.width for _, i in imgs) + 120
    h = sum(i.height + 16 for _, i in imgs) + 16
    M = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(M)
    y = 16
    for label, c in imgs:
        d.text((8, y + c.height // 2 - 6), label, fill=(200, 0, 0))
        M.paste(c, (110, y))
        d.rectangle([110, y, 110 + c.width - 1, y + c.height - 1], outline=(180, 180, 180))
        y += c.height + 16
    M.save(QA + out)
    print(out, M.size)

def side(crops, out, scale=1):
    imgs = []
    for label, box in crops:
        c = IM.crop(box)
        if scale > 1:
            c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
        imgs.append((label, c))
    w = sum(i.width + 90 for _, i in imgs) + 20
    h = max(i.height for _, i in imgs) + 30
    M = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(M)
    x = 20
    for label, c in imgs:
        d.text((x, 4), label, fill=(200, 0, 0))
        M.paste(c, (x, 24))
        d.rectangle([x, 24, x + c.width - 1, 24 + c.height - 1], outline=(180, 180, 180))
        x += c.width + 90
    M.save(QA + out)
    print(out, M.size)

# 1+2: the six blue weight labels (already-banked crops re-used for A; fresh zoom for montage clarity)
stack([("A1", (315, 188, 365, 218)), ("A2", (312, 218, 352, 252)), ("A3", (320, 252, 355, 292))], "vmont_A.png", 6)
stack([("B1", (478, 190, 522, 218)), ("B2", (480, 218, 520, 255)), ("B3", (483, 252, 515, 292))], "vmont_B.png", 6)
# 3: neuron internals col2/col3/col5 row1 + col1 row2
side([("N-col2", (238, 186, 292, 238)), ("N-col3", (401, 186, 455, 238)), ("N-col5", (650, 190, 704, 240)), ("N-col1", (134, 260, 188, 312))], "vmont_neurons.png", 5)
# 4: fan region + block arrows j,k (with letters)
stack([("FAN", (58, 232, 152, 396)), ("ARROW-j", (392, 376, 468, 442)), ("ARROW-k", (552, 376, 628, 442))], "vmont_fan.png", 3)
