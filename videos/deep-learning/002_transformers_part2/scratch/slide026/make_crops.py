#!/usr/bin/env python3
"""Create ×2 upscaled crops of dense micro-regions for gate reads."""
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg').convert('RGB')
OUT = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide026/'

crops = {
    'orig_R1_blueedge':  (345, 240, 420, 395),   # blue right edge: SPI/12-bit ADC/eQEP + 3 connection labels
    'orig_R2_upperpath': (440, 212, 665, 300),   # 16bit box, Dual ADC, triangle, output labels
    'orig_R3_midpath':   (440, 295, 665, 400),   # analog path, triangle, comparator, Comparators
    'orig_R4_psu':       (388, 408, 665, 470),   # 24V, PSU, 5V, 3.3V, Encoder supply
    'orig_R5_panel':     (678, 188, 862, 470),   # right panel: diff box, wires, labels, motor, sincos
    'orig_R6_sb1':       (228, 250, 382, 292),   # sub-block 1 text
    'orig_R7_sb23':      (228, 302, 382, 390),   # sub-blocks 2+3 text
    'orig_R8_hostconn':  (390, 248, 672, 392),   # host box + encoder connector (vertical labels)
}
for name, (x0, y0, x1, y1) in crops.items():
    c = im.crop((x0, y0, x1, y1))
    w, h = c.size
    c = c.resize((w*3, h*3), Image.LANCZOS)
    c.save(OUT + name + '.png')
    print(name, c.size)
