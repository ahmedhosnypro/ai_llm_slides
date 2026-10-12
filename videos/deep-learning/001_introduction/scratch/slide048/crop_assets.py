#!/usr/bin/env python3
"""Crop the two photo assets from the original frame (slide-040 precedent: photos are
cropped from the ground-truth frame and embedded at exact size). Frame px, 1px=1pt."""
from PIL import Image

src = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')
OUT = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets'

# cat meme (NN row input): measured bbox x 249..360, y 192..251 (112x60)
cat = src.crop((249, 192, 361, 252))
cat.save(f'{OUT}/catmeme_048.png')
print('catmeme_048.png', cat.size, '-> place at (249,192) size 112x60')

# siamese cat (CNN row input, skewed parallelogram): bbox x 129..225, y 319..417
# crop the full bbox incl. white corners (interior below the rule is white -> seamless)
sia = src.crop((128, 318, 227, 419))
sia.save(f'{OUT}/siamese_048.png')
print('siamese_048.png', sia.size, '-> place at (128,318) size 99x101')
