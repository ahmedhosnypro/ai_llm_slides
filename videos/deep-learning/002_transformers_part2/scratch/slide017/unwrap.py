#!/usr/bin/env python3
"""Un-wash the translucent salmon overlay on h1 card: ratio vs card color, then ASCII map."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(float)

card = np.array([0xF1, 0x8B, 0x96], dtype=float)  # measured h1 salmon core
# ratio vs card; clip; gamma to expand
ratio = a / card[None, None, :]
enh = np.clip(ratio * 150, 0, 255).astype(np.uint8)  # ratio 1.0 -> 150 gray; >1 brighter

Image.fromarray(enh).save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide017/nowash.png")

# ASCII map of the h1 zone (x60..620, y255..515) from the enhanced image
e = enh.astype(int)
PAL = {
    '.': (150,150,150), ' ': (230,230,230),
    'K': (40,40,40), 'k': (90,90,90),
    'W': (255,255,255), 'w': (210,210,210),
    'r': (200,60,60), 'R': (240,120,120),
    'g': (200,170,60), 'G': (230,220,120),
    'b': (60,80,180), 'B': (120,150,220),
    'v': (120,200,120), 'V': (170,230,170),
    'p': (220,120,180), 'P': (240,180,220),
    'l': (150,120,200), 'L': (190,170,230),
    't': (170,130,90), 'T': (210,170,130),
    'y': (230,230,90),
}
names = list(PAL.keys()); cols = np.array([PAL[k] for k in names])
x0, x1, y0, y1 = 60, 620, 255, 515
by, bx = 4, 4
print("    " + "".join(str(((x0 + i*bx)//10) % 10) for i in range((x1-x0)//bx)))
for gy in range((y1-y0)//by):
    row = ""
    for gx in range((x1-x0)//bx):
        block = e[y0+gy*by:y0+(gy+1)*by, x0+gx*bx:x0+(gx+1)*bx].reshape(-1,3).mean(axis=0)
        d = np.abs(cols - block).sum(axis=1)
        row += names[int(d.argmin())]
    print(f"{y0+gy*by:3d} {row}")
