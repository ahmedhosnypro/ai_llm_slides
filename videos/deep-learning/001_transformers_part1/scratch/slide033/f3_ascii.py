#!/usr/bin/env python3
"""Forensics pass 3: coarse ASCII map of the frame via palette classification."""
import numpy as np
from PIL import Image

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W = a.shape[:2]

# candidate palette (measured so far + spec colors, we'll refine)
PAL = {
    ".": (255, 255, 255),   # white
    "p": (247, 226, 205),   # peach panel
    "g": (233, 233, 231),   # gray chrome panel
    "G": (231, 255, 233),   # pale green container
    "Y": (250, 250, 110),   # yellow box
    "y": (255, 255, 204),   # pale yellow pill
    "T": (219, 203, 187),   # taupe
    "O": (248, 222, 251),   # orchid/pink
    "B": (204, 228, 247),   # light blue
    "r": (204, 0, 0),       # red
    "R": (139, 0, 0),       # dark red
    "k": (30, 30, 30),      # black-ish
    "b": (0, 51, 102),      # dark blue
    "M": (255, 0, 255),     # magenta
    "n": (0, 166, 81),      # green border
    "e": (0, 0, 204),       # blue text
    "w": (0, 128, 0),       # green text
    "o": (204, 122, 0),     # orange border
    "s": (180, 160, 200),   # lavender sq
    "q": (240, 220, 140),   # khaki sq
    "h": (245, 190, 200),   # pink sq
    "c": (120, 120, 120),   # mid gray
}

keys = list(PAL.keys())
cols = np.array([PAL[k] for k in keys])

# distance of every pixel to every palette entry
flat = a.reshape(-1, 3)
d = np.abs(flat[:, None, :] - cols[None, :, :]).sum(axis=2)
idx = d.argmin(axis=1)
cls = idx.reshape(H, W)

STEP = 6
rows = []
for y in range(0, H, STEP):
    row = ""
    for x in range(0, W, STEP):
        block = cls[y:y + STEP, x:x + STEP]
        vals, counts = np.unique(block, return_counts=True)
        # pick modal class
        row += keys[vals[counts.argmax()]]
    rows.append(row)

for i, r in enumerate(rows):
    print(f"{i*STEP:3d} {r}")
