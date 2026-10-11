#!/usr/bin/env python3
"""Pass 4: template-match inherited parent blocks (from slide_006.jpg) onto slide_009.jpg
to get exact per-block (dx,dy); plus focused scans for labels/softmax/arrows."""
from PIL import Image
import numpy as np

A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_006.jpg"
B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(A).convert("L"), dtype=np.float32)
b = np.asarray(Image.open(B).convert("L"), dtype=np.float32)

def match(name, x, y, w, h, search=18):
    """Find (dx,dy) minimizing SSD of parent crop placed at (x+dx, y+dy) in slide9."""
    best = None
    crop = a[y:y+h, x:x+w]
    for dy in range(-search, search + 1):
        for dx in range(-search, search + 1):
            yy, xx = y + dy, x + dx
            if yy < 0 or xx < 0 or yy + h > 540 or xx + w > 960:
                continue
            ssd = float(((b[yy:yy+h, xx:xx+w] - crop) ** 2).mean())
            if best is None or ssd < best[0]:
                best = (ssd, dx, dy)
    ssd, dx, dy = best
    print(f"  {name}: dx={dx:+d} dy={dy:+d} (ssd={ssd:.1f})")
    return dx, dy

print("== TEMPLATE MATCH (parent region -> slide9 offset) ==")
match("dec container", 479, 117, 423, 165, 16)
match("dec green bar1", 516, 199, 77, 20, 16)
match("dec green bar2", 647, 199, 77, 20, 16)
match("dec green bar3", 778, 199, 77, 20, 16)
match("dec hidden bar1", 516, 255, 77, 20, 16)
match("dec hidden bar2", 647, 255, 77, 20, 16)
match("dec hidden bar3", 778, 255, 77, 20, 16)
match("dec uparrow1", 550, 146, 8, 52, 16)
match("dec uparrow2", 681, 146, 8, 52, 16)
match("dec uparrow3", 811, 146, 8, 52, 16)
match("dec downarrow1", 550, 219, 8, 35, 16)
match("dec downarrow2", 681, 219, 8, 35, 16)
match("dec downarrow3", 811, 219, 8, 35, 16)
match("dec sarrow1", 597, 262, 51, 7, 16)
match("dec sarrow2", 728, 262, 51, 7, 16)
match("dec sarrow3", 860, 262, 40, 7, 16)
match("dec o1 label", 548, 123, 13, 24, 14)
match("dec s1 label", 613, 268, 14, 19, 14)
match("dec softmax1", 445, 170, 101, 16, 16)
match("dec softmax2", 576, 170, 101, 16, 16)
match("dec softmax3", 706, 170, 101, 16, 16)
match("dec curve_a", 550, 183, 101, 76, 16)
match("dec curve_b", 681, 183, 101, 76, 16)
match("dec dot", 507, 256, 13, 13, 14)
match("dec caption", 672, 87, 160, 24, 16)
print("== ENCODER ==")
match("enc container", 46, 306, 442, 190, 16)
match("enc pink bar1", 123, 319, 77, 20, 16)
match("enc pink bar2", 253, 319, 77, 20, 16)
match("enc pink bar3", 384, 319, 77, 20, 16)
match("enc tan bar1", 123, 406, 77, 19, 16)
match("enc tan bar2", 253, 406, 77, 19, 16)
match("enc tan bar3", 384, 406, 77, 19, 16)
match("enc harrow entry", 63, 326, 56, 7, 16)
match("enc harrow h1", 204, 326, 47, 7, 16)
match("enc harrow h2", 335, 326, 47, 7, 16)
match("enc h1 label", 211, 307, 14, 25, 14)
match("enc embarrow1", 157, 342, 8, 60, 16)
match("enc embarrow2", 287, 342, 8, 60, 16)
match("enc embarrow3", 418, 342, 8, 60, 16)
match("enc emblabel1", 52, 362, 100, 17, 16)
match("enc emblabel2", 184, 362, 100, 17, 16)
match("enc emblabel3", 315, 362, 100, 17, 16)
match("enc xarrow1", 157, 428, 8, 42, 16)
match("enc xarrow2", 287, 428, 8, 42, 16)
match("enc xarrow3", 418, 428, 8, 42, 16)
match("enc xlabel1", 155, 468, 10, 21, 14)
match("enc xlabel2", 286, 468, 10, 21, 14)
match("enc xlabel3", 417, 468, 10, 21, 14)
match("enc dot", 462, 320, 14, 13, 14)
match("enc caption", 215, 505, 160, 24, 16)
match("ctx_arc", 464, 257, 48, 73, 16)
match("title L1", 260, 55, 390, 28, 10)
