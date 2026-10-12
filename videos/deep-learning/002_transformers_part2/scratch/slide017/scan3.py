#!/usr/bin/env python3
"""ASCII color map + card bbox detection for slide_017.jpg."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

# named palette for the map
PAL = {
    '.': (232,232,232), ' ': (255,255,255),
    'r': (200,30,30), 'R': (240,140,150),   # red ink / salmon card h1
    'L': (197,193,244), 'Y': (248,255,154), 'G': (212,255,229), 'P': (247,226,205),  # h2..h5 cards
    'K': (20,20,20), 'k': (90,90,90),
    'g': (245,194,66),                       # gold
    'T': (216,200,184),                      # tan
    'p': (242,184,198),                      # pink
    'l': (201,160,220),                      # lilac
    'e': (232,252,230), 'E': (216,248,232),  # pale greens
    'y': (255,224,102), 'c': (244,204,204), 'v': (182,215,168),  # strip cells
    'b': (60,90,200), 'B': (130,170,220),    # blues
    'm': (255,105,180),                      # magenta
    'd': (89,89,89),
}
names = list(PAL.keys()); cols = np.array([PAL[k] for k in names])

# 5px blocks
by, bx = 5, 5
gh, gw = H // by, W // bx
out = []
for gy in range(gh):
    row = ""
    for gx in range(gw):
        block = a[gy*by:(gy+1)*by, gx*bx:(gx+1)*bx].reshape(-1,3).mean(axis=0)
        d = np.abs(cols - block).sum(axis=1)
        row += names[int(d.argmin())]
    out.append(row)
print("   " + "".join(str((i*bx)//100 % 10) for i in range(gw)))
for gy, row in enumerate(out):
    print(f"{gy*by:3d} {row}")
