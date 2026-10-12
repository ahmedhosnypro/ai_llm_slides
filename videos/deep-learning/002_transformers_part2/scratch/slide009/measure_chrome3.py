#!/usr/bin/env python3
"""Chrome landmarks v3 — find top border and right border precisely."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_009.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# softer red: r dominates but allow dimmer
red = (r > 100) & (r - g > 40) & (r - b > 40)

top_limit = 518
# top border: rows 0..72, red run width
print('rows 0..72 red-run:')
print({y: int(red[y, :].sum()) for y in range(0, 72) if red[y, :].sum() > 100})

# right border: red-run per column x 880..940
print('right columns x 880..940 red-run:')
print({x: int(red[:top_limit, x].sum()) for x in range(880, 941) if red[:top_limit, x].sum() > 30})
