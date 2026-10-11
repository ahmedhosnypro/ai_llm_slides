#!/usr/bin/env python3
"""Create 2x-upscaled crops of the original for vision reading."""
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')

def crop2x(box, out):
    c = im.crop(box)
    c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
    c.save(out)
    print(out, c.size)

S = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide032/'
crop2x((215, 110, 860, 180), S + 'crop_callout.png')
crop2x((95, 316, 895, 380), S + 'crop_L3L4.png')
crop2x((78, 220, 815, 252), S + 'crop_L1.png')
crop2x((78, 286, 540, 315), S + 'crop_L2.png')
crop2x((78, 382, 890, 412), S + 'crop_L5.png')
crop2x((78, 446, 890, 476), S + 'crop_L6.png')
crop2x((250, 50, 700, 108), S + 'crop_title_sub.png')
crop2x((76, 92, 212, 202), S + 'crop_vector.png')
