#!/usr/bin/env python3
"""m03_body.py — body color-region analysis for slide_051 frame.
Finds the spec's palette regions and tests whether the banked Fig 1 raster palette
appears in bulk (raster-present test). All coords reported in FRAME px and slide pt.
"""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_051.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = im.shape

def bbox_of(mask, label):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(f"{label}: NONE")
        return None
    print(f"{label}: count={len(xs)} bbox x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}")
    return (xs.min(), xs.max(), ys.min(), ys.max())

def near(rgb, tol):
    return np.abs(im - np.array(rgb)).max(axis=2) <= tol

# spec palette targets
tests = [
    ("peach FBE5D6", (251, 229, 214), 12),
    ("orange ED7D31", (237, 125, 49), 25),
    ("bright green 00E100", (0, 225, 0), 60),
    ("light green CCFFCC", (204, 255, 204), 15),
    ("blue 4472C4", (68, 114, 196), 25),
    ("gray 7F7F7F", (127, 127, 127), 20),
    ("pink FFC7CE", (255, 199, 206), 15),
    ("purple C9A0DC", (201, 160, 220), 25),
    ("teal 66CCCC", (102, 204, 204), 25),
    ("yellow FFFF00", (255, 255, 0), 40),
    ("brown A0622D", (160, 98, 45), 25),
    ("white 255", (255, 255, 255), 6),
]
for name, rgb, tol in tests:
    m = near(rgb, tol)
    # restrict to slide body (frame y 46..515, x 62..898)
    mm = np.zeros_like(m)
    mm[46:515, 62:898] = m[46:515, 62:898]
    bbox_of(mm, name)

# paper-figure palette probe: sample the banked Fig 1's most common non-white colors
fig = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/slide_18_source/The Transformer - model architecture..png").convert("RGB")).astype(int)
q = (fig // 16 * 16).reshape(-1, 3)
colors, counts = np.unique(q, axis=0, return_counts=True)
order = np.argsort(counts)[::-1]
print("\nFig1 top colors (quantized /16):")
for i in order[:18]:
    c = colors[i]
    if counts[i] < 5000:
        break
    m = near(c, 10)
    mm = np.zeros((H, W), bool)
    mm[46:515, 62:898] = m[46:515, 62:898]
    n = mm.sum()
    print(f"  fig{tuple(int(v) for v in c)} n={counts[i]:8d}  -> frame n={n:7d}")
