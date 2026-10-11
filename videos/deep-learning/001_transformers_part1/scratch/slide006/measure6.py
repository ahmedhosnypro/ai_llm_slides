#!/usr/bin/env python3
"""measure6: fine 1px zooms of curve regions + true ink colors via min-luminance."""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)

def ascii_map(x0, y0, x1, y1, ref, tol, step=1, label=""):
    print(f"\n== {label} ({x0},{y0})-({x1},{y1}) step={step} ==")
    print("     " + "".join(str((x0 + i * step) // 100 % 10) for i in range((x1 - x0) // step)))
    print("     " + "".join(str((x0 + i * step) // 10 % 10) for i in range((x1 - x0) // step)))
    for y in range(y0, y1, step):
        row = ""
        for x in range(x0, x1, step):
            blk = a[y:y + step, x:x + step].reshape(-1, 3)
            d = np.abs(blk - np.array(ref)).sum(axis=1)
            f = (d > tol).mean()
            row += "#" if f > 0.6 else ("+" if f > 0.3 else ("." if f > 0.1 else " "))
        print(f"{y:4d} {row}")

# curve1: top area between shaft1 and green bar2
ascii_map(545, 180, 660, 226, (253, 255, 133), 80, 1, "curve1 zone x545-660 y180-226")
# feedback1 below barB1/B2
ascii_map(580, 258, 710, 300, (253, 255, 133), 80, 1, "feedback1 zone x580-710 y258-300")

def darkest(x0, y0, x1, y1, label):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    lum = reg.sum(axis=1)
    i = int(np.argmin(lum))
    r, g, b = reg[i]
    # also 10th percentile darkest median
    idx = np.argsort(lum)[: max(6, len(lum) // 50)]
    med = np.median(reg[idx], axis=0).astype(int)
    print(f"  {label}: darkest #{r:02x}{g:02x}{b:02x}  dark-median #{med[0]:02x}{med[1]:02x}{med[2]:02x}")

print("\n== true ink colors (darkest pixels per region) ==")
darkest(547, 130, 560, 140, "o1 label")
darkest(679, 130, 692, 140, "o2 label")
darkest(810, 130, 823, 140, "o3 label")
darkest(488, 168, 548, 185, "softmax col1")
darkest(619, 168, 680, 185, "softmax col2")
darkest(211, 312, 225, 327, "h1 label")
darkest(341, 312, 357, 327, "h2 label")
darkest(62, 362, 155, 380, "embedding x1")
darkest(194, 362, 287, 380, "embedding x2")
darkest(325, 362, 418, 380, "embedding x3")
darkest(613, 272, 626, 282, "s1 label")
darkest(744, 272, 758, 282, "s2 label")
darkest(874, 272, 890, 282, "s3 label")
darkest(152, 472, 168, 485, "x1 label")
darkest(284, 472, 300, 485, "x2 label")
darkest(415, 472, 430, 485, "x3 label")
darkest(265, 58, 642, 81, "title")
darkest(676, 90, 830, 108, "decoder caption")
darkest(222, 508, 370, 527, "encoder caption")
darkest(578, 415, 820, 432, "callout text")
darkest(556, 400, 840, 406, "callout top border")
darkest(556, 438, 840, 445, "callout bottom border")
darkest(556, 402, 562, 442, "callout left border")
darkest(204, 326, 250, 332, "h1 arrow line")
darkest(335, 326, 381, 332, "h2 arrow line")
darkest(62, 326, 119, 332, "encoder in-arrow")
darkest(597, 261, 641, 268, "s1 arrow line")
darkest(728, 261, 771, 268, "s2 arrow line")
darkest(860, 261, 882, 268, "s3 arrow line")
darkest(505, 148, 560, 198, "decoder up-arrow col1")
darkest(553, 219, 560, 254, "decoder down-arrow col1")
darkest(159, 342, 165, 402, "encoder emb-arrow col1")
darkest(157, 428, 168, 470, "encoder x-arrow col1")
darkest(466, 255, 518, 310, "context arc zone")
darkest(480, 330, 556, 402, "leader line zone")
darkest(466, 322, 474, 331, "encoder red dot")
darkest(509, 258, 518, 267, "decoder red dot")
