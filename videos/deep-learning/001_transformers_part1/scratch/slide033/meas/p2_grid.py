#!/usr/bin/env python3
"""Slide 033 forensics pass 2: coarse mode-color grid + probe samples."""
from PIL import Image
import numpy as np
from collections import Counter

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")
A = np.asarray(IM)

def mode_hex(region):
    x0, y0, x1, y1 = region
    sub = A[y0:y1+1, x0:x1+1].reshape(-1, 3)
    q = (sub // 8) * 8 + 4
    c = Counter(map(tuple, q))
    return c.most_common(3)

# 12-col x 9-row grid over the slide
print("=== grid: cell -> top-3 mode colors (quantized /8) ===")
for gy in range(9):
    row = []
    for gx in range(12):
        x0, x1 = gx*80, min((gx+1)*80-1, 959)
        y0, y1 = gy*60, min((gy+1)*60-1, 539)
        top = mode_hex((x0, y0, x1, y1))
        s = " | ".join(f"#{r:02X}{g:02X}{b:02X}:{n}" for (r, g, b), n in top[:2])
        row.append(f"({gx},{gy}) {s}")
    print("\n".join(row))
    print("---")

print("=== targeted probes ===")
probes = {
    "peach interior": (300, 440, 340, 470),
    "peach interior 2": (700, 180, 740, 200),
    "dot product fill": (265, 360, 290, 390),
    "dot product fill 2": (310, 300, 330, 330),
    "softmax bar": (465, 250, 482, 300),
    "sigma box": (525, 202, 640, 214),
    "left container fill": (62, 260, 66, 275),
    "left container top": (62, 232, 66, 240),
    "right container fill": (766, 260, 770, 275),
    "sentence fill": (300, 480, 320, 490),
    "legend fill": (760, 475, 790, 485),
    "left mini sq1": (69, 242, 77, 252),
    "left mini sq2": (84, 242, 96, 252),
    "left mini sq3": (100, 242, 112, 252),
    "W box guess a": (152, 250, 185, 280),
    "W box guess b": (150, 290, 190, 320),
    "W box guess c": (155, 240, 190, 285),
    "pill Similarity": (280, 165, 330, 180),
    "badge area": (875, 55, 910, 88),
    "title L1": (300, 55, 320, 70),
}
for name, r in probes.items():
    print(f"{name:22s} {r}: {mode_hex(r)}")
