#!/usr/bin/env python3
"""forensics14_045.py — full ASCII maps of the annotation-arrow region (original vs render).
Region x596..745, y332..372 frame px. 'r'=red ink, '#'=dark ink, '.'=background."""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg"
ren = np.asarray(Image.open(f"{QA}/render_4.png").convert("RGB")).astype(int)
org = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
s = ren.shape[0] / 540.0

def masks(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    red = (r - g > 25) & (r - b > 15) & (r > 90)
    lum = (r + g + b) / 3
    dark = (lum < 205) & (~red)
    return red, dark

X0, X1, Y0, Y1 = 596, 745, 332, 372
for nm, im, is_r in (("org", org, False), ("ren", ren, True)):
    k = s if is_r else 1
    R, D = masks(im)
    rwin = R[int(Y0*k):int(Y1*k)+1, int(X0*k):int(X1*k)+1]
    dwin = D[int(Y0*k):int(Y1*k)+1, int(X0*k):int(X1*k)+1]
    print(f"== {nm} (left x{X0}, top y{Y0}; 1 char = 1pt wide, 1 row = 1.5pt) ==")
    step = max(1, int(round(1.5 * k)))
    for row in range(0, rwin.shape[0], step):
        line = ""
        for col in range(0, rwin.shape[1], int(k)):
            rc = rwin[row:row+step, col:col+int(k)].sum()
            dc = dwin[row:row+step, col:col+int(k)].sum()
            line += "r" if rc > dc and rc > 0 else ("#" if dc > 0 else ".")
        print(f" y{Y0 + row/k:5.1f} {line}")
