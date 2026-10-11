#!/usr/bin/env python3
"""ASCII map of the paper's Figure 1 (ModalNet-21.png) to ground the topology."""
import numpy as np
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/slide_18_source/The Transformer - model architecture..png').convert('RGB')
A = np.asarray(im).astype(int)
H, W, _ = A.shape
print(f"paper fig {W}x{H}")

def cls(px):
    r, g, b = px
    if r < 100 and g < 100 and b < 100: return '#'
    if r > 200 and g < 120 and b < 120: return 'R'
    if b > 150 and b-r > 40: return 'B'
    if r > 200 and g > 150 and b < 120: return 'O'  # orange
    if r > 200 and g > 200 and b < 150: return 'Y'
    if r > 230 and g > 230 and b > 230: return '.'
    return '?'

step = 14
print('     ' + ''.join(str((i*step)//100 % 10) if (i*step) % 100 < step else ' ' for i in range(W//step+1)))
for y in range(0, H-1, step):
    line = []
    for x in range(0, W-1, step):
        c = Counter()
        for dy in range(0, step, 3):
            for dx in range(0, step, 3):
                if y+dy < H and x+dx < W:
                    c[cls(A[y+dy, x+dx])] += 1
        line.append(c.most_common(1)[0][0])
    print(f"{y:4d} {''.join(line)}")
