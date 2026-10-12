#!/usr/bin/env python3
"""c3_crops.py — crop pairs for dense-region vision comparison (render vs original frame).

Region boxes given in FRAME px; render crop = mapped slide pts * 150/72.
"""
from PIL import Image
import os

VID = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
FR = VID + '/unique_slides/slide_041.jpg'
RN = VID + '/scratch/slide041/render_attempt2.png'
OUT = VID + '/scratch/slide041/crops'
os.makedirs(OUT, exist_ok=True)

SX = lambda fx: 42 + (fx - 58.5) * (919 - 42) / (901 - 58.5)
SY = lambda fy: 45 + (fy - 43.0) * (540 - 45) / (517.0 - 43.0)
S = 150 / 72.0

fr = Image.open(FR)
rn = Image.open(RN)
print('render size', rn.size)

regions = {
    'top_elbow':   (215, 100, 700, 235),   # title bottom + root box + split arrows + parent tops
    'left_branch': (110, 210, 520, 400),   # blue box + spine + cyan 1-2 + arrows
    'right_branch':(540, 195, 820, 400),   # green box + right arrow + leaf box
    'cyan_bottom': (215, 390, 530, 510),   # cyan 3-4 + spine tail + arrows
}
for name, (fx0, fy0, fx1, fy1) in regions.items():
    fc = fr.crop((fx0, fy0, fx1, fy1))
    rx0, ry0, rx1, ry1 = SX(fx0) * S, SY(fy0) * S, SX(fx1) * S, SY(fy1) * S
    rc = rn.crop((int(round(rx0)), int(round(ry0)), int(round(rx1)), int(round(ry1))))
    rc = rc.resize(fc.size, Image.LANCZOS)  # normalize to the frame crop's pixel size
    fc = fc.resize((fc.width * 2, fc.height * 2), Image.LANCZOS)  # x2 upscale both for legibility
    rc = rc.resize((rc.width * 2, rc.height * 2), Image.LANCZOS)
    fc.save('%s/%s_orig.png' % (OUT, name))
    rc.save('%s/%s_rend.png' % (OUT, name))
    print(name, 'orig', fc.size, 'rend', rc.size)
