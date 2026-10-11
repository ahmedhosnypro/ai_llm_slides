#!/usr/bin/env python3
"""Per-region top colors (raw pixels, rounded to /8 buckets) to nail TRUE fills."""
import numpy as np
from PIL import Image

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM)

def top(name, x0, y0, x1, y1, k=8):
    reg = A[y0:y1, x0:x1].reshape(-1, 3).astype(int)
    b = (reg // 8) * 8 + 4
    pal, cnt = np.unique(b, axis=0, return_counts=True)
    o = np.argsort(-cnt)[:k]
    s = ", ".join(f"#{pal[i][0]:02X}{pal[i][1]:02X}{pal[i][2]:02X}({100*cnt[i]//len(reg)}%)" for i in o)
    print(f"{name:22s} {s}")

print("== regions: top colors ==")
top("title_band", 100, 40, 860, 100)
top("subtitle_band", 100, 100, 860, 140)
top("peach_canvas", 700, 430, 860, 460)
top("softmax_bar", 455, 210, 495, 390)
top("sigma_box", 505, 190, 655, 222)
top("left_stack", 52, 220, 148, 408)
top("right_stack", 756, 220, 850, 408)
top("strip", 170, 468, 500, 520)
top("dotproduct", 258, 195, 348, 408)
top("Ybox_area", 540, 108, 660, 160)
top("pill_Sim", 250, 158, 360, 190)
top("pill_Prob", 440, 158, 515, 190)
top("pill_WSum", 580, 158, 700, 190)
top("green_arrow", 570, 145, 615, 195)
top("node_region", 510, 230, 800, 380)
top("badge", 876, 55, 910, 87)
