#!/usr/bin/env python3
"""Darkest-core ink color sampler: median of the darkest N pixels per region."""
import numpy as np
from PIL import Image

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)

def ink(name, y0, y1, x0, x1, n=25):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    lum = sub.sum(axis=1)
    idx = np.argsort(lum)[:n]
    med = np.median(sub[idx], axis=0).astype(int)
    print(f"{name:28s} ink=#{med[0]:02X}{med[1]:02X}{med[2]:02X}  {tuple(med)}  (region x{x0}..{x1} y{y0}..{y1})")

ink("title black 'Self'", 58, 73, 222, 460)
ink("title blue '(Linear'", 59, 73, 500, 700)
ink("title red X2", 81, 96, 404, 425)
ink("title line2 black", 81, 95, 186, 400)
ink("W_k box1 text", 233, 250, 158, 195, 40)
ink("W_k box2 text", 274, 290, 158, 195, 40)
ink("W_v box1 text", 233, 250, 705, 742, 40)
ink("W_q box text", 432, 465, 276, 316, 40)
ink("pill1 'Similarity'", 162, 184, 276, 340, 40)
ink("pill2 'Probabilities'", 162, 184, 432, 505, 40)
ink("pill3 'Weighted SUM'", 162, 186, 600, 680, 40)
ink("K label row1", 240, 252, 305, 325, 20)
ink("K label row4", 369, 376, 256, 268, 20)
ink("V label row1", 229, 241, 638, 650, 20)
ink("V label row4", 356, 368, 638, 650, 20)
ink("q2 label", 404, 430, 290, 305, 20)
ink("DotProduct title", 200, 225, 265, 335, 40)
ink("K2q corner", 243, 250, 311, 323, 12)
ink("Y2 green", 148, 168, 548, 576, 25)
ink("Sigma glyph", 198, 216, 575, 596, 30)
ink("band1 tiny text", 242, 251, 512, 546, 30)
ink("band2 tiny text", 283, 292, 543, 612, 30)
ink("band4 tiny text", 368, 378, 602, 645, 30)
ink("legend 'd: Embedding'", 505, 515, 790, 865, 30)
ink("legend W black", 483, 495, 795, 820, 20)
ink("legend red 1^d", 483, 500, 770, 792, 20)
ink("sentence X labels", 487, 501, 188, 205, 20)
ink("left box X row1", 238, 253, 90, 104, 15)
ink("right box X row1", 238, 253, 795, 808, 15)
ink("softmax vert text", 240, 360, 466, 484, 40)
ink("block arrow red", 508, 528, 262, 290, 25)
ink("emphasis circle", 305, 333, 215, 252, 40)
