#!/usr/bin/env python3
"""Slide 033 pass W2: classified ASCII maps per region -> meas/w2_maps.txt"""
from PIL import Image
import numpy as np

IM = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg').convert('RGB')
A = np.asarray(IM).astype(int)


def cls(px):
    r, g, b = px
    mx, mn = max(r, g, b), min(r, g, b)
    if mx < 100:
        return 'K'                                   # near-black ink
    if r > 150 and r - g > 60 and r - b > 45 and g < 120:
        return 'R'                                   # strong red ink
    if r > 140 and r - g > 30 and r - b > 18 and g >= 120:
        return 'r'                                   # soft red/pink-red (ink AA, salmon)
    if r > 180 and 60 < r - g <= 60 and b < 120 and g > 80:
        return 'O'                                   # orange/brown border
    if g - r > 18 and g - b > 8 and g > 110 and r < 190:
        return 'G'                                   # green ink/border
    if b - r > 30 and b > 90:
        return 'B'                                   # blue ink
    if b > 150 and r > 140 and g < 140 and b - g > 40:
        return 'M'                                   # magenta/violet
    if r > 200 and g < 190 and b > 200:
        return 'S'                                   # softmax pink
    if r > 195 and g > 195 and b < 185:
        return 'Y'                                   # yellow/chartreuse
    if r > 205 and g > 195 and 175 <= b <= 215 and r - b > 22:
        return 'T'                                   # DP tan fill
    if mx - mn > 26:
        return '?'                                   # other saturated
    return '.'                                       # pale/peach/white


def region(name, x0, x1, y0, y1, step=2):
    print(f"\n=== {name} (x{x0}..{x1}, y{y0}..{y1}) step{step} ===")
    hdr = "     " + "".join(str((x // 10) % 10) if x % 10 == 0 else (str(x % 5) if x % 5 == 0 else ' ') for x in range(x0, x1 + 1, step))
    print(hdr)
    for y in range(y0, y1 + 1, step):
        row = "".join(cls(A[y, x]) for x in range(x0, x1 + 1, step))
        print(f"{y:4d} {row}")


if __name__ == "__main__":
    import sys
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "kcol"):
        region("K column: W_k boxes+vectors+labels", 140, 265, 220, 400, 2)
    if which in ("all", "dp"):
        region("Dot Product box", 248, 350, 188, 412, 2)
    if which in ("all", "mid"):
        region("Softmax bar", 440, 500, 190, 410, 2)
    if which in ("all", "sum"):
        region("Circles + Sigma", 500, 665, 190, 400, 2)
    if which in ("all", "vcol"):
        region("V column: labels+vectors+W_v", 660, 770, 220, 400, 2)
    if which in ("all", "y2"):
        region("Y2 widget + arrows", 535, 665, 108, 200, 1)
    if which in ("all", "q"):
        region("q2 + W_q", 260, 350, 400, 470, 1)
    if which in ("all", "pills"):
        region("Stage pills", 260, 700, 152, 192, 2)
    if which in ("all", "title"):
        region("Title", 180, 790, 50, 102, 2)
    if which in ("all", "sent"):
        region("Sentence row", 168, 500, 462, 539, 2)
    if which in ("all", "legend"):
        region("Legend", 728, 912, 458, 539, 1)
    if which in ("all", "conn"):
        region("Connectors L/R verticals", 60, 130, 380, 480, 2)
        region("connector R", 770, 912, 380, 480, 2)
        region("connector horizontal", 480, 780, 478, 512, 2)
    if which in ("all", "lcol"):
        region("Left container rows", 52, 145, 220, 400, 2)
    if which in ("all", "rcol"):
        region("Right container rows", 755, 850, 220, 400, 2)
