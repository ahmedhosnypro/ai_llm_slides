#!/usr/bin/env python3
"""Slide 038 forensics pass 10: annotation zooms (7s, 3, pencil, 3 dims, 735 weights)."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def cls(p):
    rr, gg, bb = p
    if rr > 235 and gg > 235 and bb > 235: return '.'
    if abs(rr - 232) < 12 and abs(gg - 232) < 12: return ' '
    if rr < 110 and gg < 110 and bb < 110: return '#'
    if rr < 185 and gg < 165: return 'd'
    if rr > 170 and gg < 100 and bb < 100: return 'R'
    if rr > 150 and gg > 95 and gg < 185 and bb < 115 and (rr - bb) > 40: return 'o'
    if rr > 190 and gg > 170 and bb < 150: return 'y'
    if gg > 120 and (gg - rr) > 30 and (gg - bb) > 15: return 'G'
    if bb > 130 and gg > 120 and rr < 140: return 'c'
    if rr > 80 and bb > 110 and gg < 100: return 'P'
    return '+'

def zoom(x0, x1, y0, y1, step=1, label=""):
    print(f"=== {label}: x{x0}..{x1} y{y0}..{y1} ===")
    for y in range(y0, y1, step):
        print(f"{y:3d} " + ''.join(cls(a[y, x]) for x in range(x0, x1, step)))

zoom(395, 470, 326, 344, 1, "A: above cyan slab / '7' above stack?")
zoom(455, 560, 300, 340, 1, "B: above stack right / '7' above stack")
zoom(186, 285, 318, 352, 1, "C: '3 dims' + arrow region")
zoom(225, 265, 360, 400, 1, "D: '7' left edge of slab")
zoom(235, 320, 438, 478, 1, "E: '7' below slab bottom")
zoom(545, 618, 380, 460, 1, "F: '7' right of purple slab")
zoom(355, 425, 378, 445, 1, "G: '3' + pencil below-left of stack")
