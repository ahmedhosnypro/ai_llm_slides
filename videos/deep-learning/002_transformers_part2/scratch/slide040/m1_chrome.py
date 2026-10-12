#!/usr/bin/env python3
"""Stage 1: chrome landmarks of slide_040.jpg + frame->slide mapping fit + badge cross-check.
Slide chrome (playlist law): panel x 42..918, top y 45, bottom border stroke rows 538-539;
badge circle d36 center (893,71) fill FDFD96.
"""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
H, W, _ = im.shape
print('frame size', W, H)

def is_gray(px):
    r, g, b = px
    return abs(r-0xE9) < 14 and abs(g-0xE9) < 14 and abs(b-0xE7) < 14

def is_white(px):
    r, g, b = px
    return r > 242 and g > 242 and b > 242

# --- panel left edge: first column from left where a run of gray starts (scan row y=300)
row = 300
xs_gray = [x for x in range(0, 200) if is_gray(im[row, x])]
print('row300 first gray x:', xs_gray[:3])
# --- panel right edge
xs_gray_r = [x for x in range(W-1, W-120, -1) if is_gray(im[row, x])]
print('row300 last gray x:', xs_gray_r[:3])

# --- panel top edge: scan column x=500 from top for first gray run
col = 500
ys_gray = [y for y in range(0, 120) if is_gray(im[y, col])]
print('col500 first gray y:', ys_gray[:3])

# --- red border rows: the C00000 strokes. Find red pixels (r>150, g<70, b<70)
red = (im[:,:,0] > 150) & (im[:,:,1] < 70) & (im[:,:,2] < 70)
# left border column at row 300
redcols = np.where(red[row, :300])[0]
print('row300 red cols (left border):', redcols[:8])
redcols_r = np.where(red[row, 850:])[0] + 850
print('row300 red cols (right border):', redcols_r[-8:])
# top border row at col 500
redrows = np.where(red[:120, col])[0]
print('col500 red rows (top border):', redrows[:8])
# bottom border: red rows near bottom at col 500 (excluding letterbox black)
redrows_b = np.where(red[490:540, col])[0] + 490
print('col500 red rows (bottom border):', redrows_b)

# --- badge: yellow-ish pixels (high R,G, low-ish B) in top-right quadrant
yellow = (im[:,:,0] > 220) & (im[:,:,1] > 220) & (im[:,:,2] < 190)
ys, xs = np.where(yellow[:150, 800:])
if len(xs):
    print('badge yellow bbox: x', xs.min()+800, '..', xs.max()+800, ' y', ys.min(), '..', ys.max())
    print('badge center', (xs.min()+xs.max())/2+800, (ys.min()+ys.max())/2)

# --- letterbox: black rows at bottom
dark_rows = [y for y in range(500, H) if (im[y, 100:900].mean(axis=(0,1)) < 60)]
print('letterbox dark rows:', dark_rows[:3], '..', dark_rows[-3:] if dark_rows else None)

# --- mapping fit (slide 1px=1pt): panel edges left 42, right 918(+1=919 border outer?), top 45,
# bottom border stroke rows 538-539 -> visible bottom ~539.  Use left/right/top + bottom stroke.
# landmark frame values printed above are substituted manually after run.
