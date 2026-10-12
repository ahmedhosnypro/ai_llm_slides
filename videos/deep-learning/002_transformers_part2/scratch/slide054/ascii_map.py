#!/usr/bin/env python3
"""ASCII color-class maps of slide_054 regions (2px sampling)."""
from PIL import Image
import numpy as np
import sys

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg"
img = Image.open(SRC).convert("RGB")
A = np.asarray(img).astype(int)
H, W, _ = A.shape
R, G, B = A[..., 0], A[..., 1], A[..., 2]

def classify(y, x):
    r, g, b = A[y, x]
    if r < 110 and g < 110 and b < 110: return "K"          # dark/black ink
    if r - g >= 70 and r - b >= 60 and r >= 150: return "R" # red ink
    if b - r >= 60 and b >= 130: return "B"                 # blue ink
    if r >= 190 and b >= 190 and g <= 175 and r - g >= 40: return "M"  # magenta
    if r >= 235 and g >= 235 and b <= 215 and r - b >= 35: return "Y"  # yellow
    if g - r >= 14 and g - b >= 14 and g >= 228: return "G" # light green fill
    if abs(r-245)<=10 and abs(g-209)<=12 and abs(b-246)<=10: return "P"  # panel pink
    if abs(r-216)<=15 and abs(g-200)<=15 and abs(b-185)<=15: return "T"  # tan
    if abs(r-247)<=8 and abs(g-212)<=10 and abs(b-215)<=10: return "S"   # pale pink (scaling)
    if r >= 238 and g >= 238 and b >= 238: return "W"       # near-white
    if abs(r-231)<=6 and abs(g-231)<=6 and abs(b-231)<=6: return "E"     # chrome gray
    return "."

def dump(x0, x1, y0, y1, step=2, label=""):
    print(f"\n### {label} frame x{x0}..{x1} y{y0}..{y1} step{step} (cols: 1 char = {step}px)")
    hdr = "     " + "".join(str((x0 + i*step) // 100 % 10) for i in range((x1 - x0)//step))
    hdr2 = "     " + "".join(str((x0 + i*step) // 10 % 10) for i in range((x1 - x0)//step))
    print(hdr); print(hdr2)
    for y in range(y0, y1, step):
        row = "".join(classify(y, x) for x in range(x0, x1, step))
        print(f"{y:4d} {row}")

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "title"):
        dump(66, 560, 56, 96, 2, "TITLE + top area")
    if which in ("all", "legend"):
        dump(690, 910, 45, 100, 2, "TOP-RIGHT LEGEND + badge")
    if which in ("all", "left"):
        dump(62, 270, 205, 395, 2, "LEFT: container + W_k + K strips + dot-product left edge")
    if which in ("all", "dotprod"):
        dump(255, 425, 180, 400, 2, "DOT PRODUCT + SCALING")
    if which in ("all", "mask"):
        dump(440, 545, 180, 445, 2, "MASK + SOFTMAX columns + ellipse")
