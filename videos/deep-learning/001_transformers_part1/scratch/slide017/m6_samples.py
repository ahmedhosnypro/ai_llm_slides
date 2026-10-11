#!/usr/bin/env python3
"""Precise pixel sampling at key diagram locations of slide_017.jpg."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)

def avg(x0, y0, x1, y1):
    r = A[y0:y1+1, x0:x1+1].reshape(-1, 3)
    return tuple(int(v) for v in r.mean(axis=0))

pts = [
    # encoder stack boxes (x range ~629..725)
    ("enc box A (y268-285)", 640, 270, 660, 283),
    ("enc box B (y293-314)", 640, 295, 660, 312),
    ("enc box C (y324-351)", 640, 326, 660, 349),
    ("enc box D (y360-381)", 640, 362, 660, 379),
    ("enc box E (y386-407)", 640, 388, 660, 405),
    ("enc box F (y417-444)", 640, 419, 660, 442),
    ("enc box G (y447-470)", 640, 449, 660, 468),
    ("enc box H (y474-480)", 640, 475, 660, 479),
    # Nx badges
    ("Nx enc badge", 603, 336, 615, 348),
    ("Nx dec badge", 849, 305, 861, 317),
    # decoder stack (x range ~749..830)
    ("dec box 1 (y279-294)", 758, 281, 775, 292),
    ("dec box 2 (y300-321)", 758, 302, 775, 319),
    ("dec purple (y327-408)", 760, 350, 775, 365),
    ("dec purple 2", 795, 395, 810, 405),
    ("dec box (y417-444)", 758, 419, 775, 442),
    ("dec box (y447-470)", 758, 449, 775, 468),
    ("dec box (y474-480)", 758, 475, 775, 479),
    # panels
    ("enc panel bg", 590, 200, 600, 210),
    ("dec panel bg", 880, 200, 890, 210),
    # title
    ("title ink", 280, 70, 284, 74),
    # blue circles
    ("blue enc V", 660, 398, 666, 403),
    ("blue dec (y387-399)", 750, 390, 755, 396),
    ("blue dec (y311-321)", 749, 313, 753, 319),
    # red circles
    ("red enc Q", 711, 398, 715, 403),
    ("red dec Q (y387)", 815, 390, 818, 396),
    ("red dec Q (y311)", 807, 313, 810, 319),
    # callout fills
    ("callout1 yellow", 200, 130, 220, 140),
    ("callout2 pink", 250, 230, 270, 240),
    ("callout3 tan", 200, 350, 220, 360),
    ("callout4 tan", 200, 480, 220, 490),
    # margins/backgrounds
    ("white margin", 20, 300, 30, 310),
    ("panel gray", 300, 200, 310, 210),
    # leader line pixels (left margin)
    ("leader y150", 563, 149, 570, 151),
    ("leader y252", 563, 251, 570, 253),
    ("leader y372", 563, 371, 570, 373),
    # highlights
    ("Y band crossing", 700, 260, 710, 270),
    ("Y outputs", 770, 495, 790, 505),
    # block arrows
    ("block arrow enc", 656, 495, 665, 505),
    ("block arrow dec out", 790, 495, 800, 505),
]
for name, x0, y0, x1, y1 in pts:
    print(f"{name:26s} [{x0},{y0}..{x1},{y1}] = {avg(x0,y0,x1,y1)}")
