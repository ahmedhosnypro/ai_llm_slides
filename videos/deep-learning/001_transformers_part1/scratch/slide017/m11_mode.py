#!/usr/bin/env python3
"""Mode fill color per candidate box region (excluding dark ink)."""
import numpy as np
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im)

def mode_fill(name, x0, y0, x1, y1):
    r = A[y0:y1+1, x0:x1+1].reshape(-1, 3).astype(int)
    # exclude dark ink
    keep = ~((r[:, 0] < 140) & (r[:, 1] < 140) & (r[:, 2] < 140))
    r = r[keep]
    q = (r // 8 * 8)
    c = Counter(map(tuple, q))
    top = c.most_common(3)
    tot = len(r)
    s = ", ".join(f"{col}x{n}({100*n//tot}%)" for col, n in top)
    print(f"{name:34s} [{x0},{y0}..{x1},{y1}]: {s}")

# encoder boxes
mode_fill("enc box1 (y268-284)", 632, 269, 722, 283)
mode_fill("enc box2 (y288-314)", 632, 289, 722, 313)
mode_fill("enc box3 top (y318-340)", 632, 319, 722, 339)
mode_fill("enc box3 bot (y370-392)", 632, 371, 722, 391)
mode_fill("enc box4 (y411-443)", 658, 412, 720, 442)
mode_fill("enc box5 (y447-470)", 644, 448, 722, 469)
mode_fill("enc box6 (y473-481)", 644, 474, 722, 480)
mode_fill("enc Nx ellipse", 598, 335, 618, 375)
# decoder
mode_fill("dec MHA? (y283-303)", 754, 284, 818, 302)
mode_fill("dec yellow band (y309-321)", 790, 310, 812, 320)
mode_fill("dec purple (y345-360)", 766, 346, 782, 358)
mode_fill("dec box (y419-442)", 752, 420, 818, 441)
mode_fill("dec box (y449-468)", 752, 450, 818, 467)
mode_fill("dec box (y475-480)", 752, 475, 818, 479)
mode_fill("dec olive top (y205-243)", 760, 207, 820, 242)
mode_fill("dec region (y153-197)", 760, 155, 820, 195)
mode_fill("dec Nx badge", 850, 304, 862, 316)
mode_fill("dec stripe x834-838 y210-320", 834, 210, 838, 320)
mode_fill("dec top yellow (y113-127)", 768, 115, 820, 125)
mode_fill("dec top red (y117-139)", 744, 118, 751, 138)
# linear/softmax candidates right of stripe?
mode_fill("dec right x845-895 y150-250", 845, 150, 895, 250)
mode_fill("dec right x845-895 y255-330", 845, 255, 895, 330)
# paper: Linear/Softmax at top. check y150-200 x845+
mode_fill("callout1 yellow", 110, 125, 520, 178)
mode_fill("callout2 pink", 190, 218, 480, 271)
mode_fill("callout3 tan", 110, 343, 515, 386)
mode_fill("callout4 tan", 95, 472, 525, 512)
