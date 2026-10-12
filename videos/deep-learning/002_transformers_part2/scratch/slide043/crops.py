#!/usr/bin/env python3
"""Slide 043: crop title band + callout + right stack top for visual inspection."""
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
im.crop((150, 40, 900, 110)).resize((1500, 140), Image.LANCZOS).save("crop_title.png")
im.crop((290, 140, 700, 310)).resize((820, 340), Image.LANCZOS).save("crop_callout.png")
im.crop((60, 80, 340, 340)).resize((560, 520), Image.LANCZOS).save("crop_leftstack.png")
im.crop((600, 70, 920, 350)).resize((640, 560), Image.LANCZOS).save("crop_rightstack.png")
im.crop((60, 340, 900, 510)).resize((1680, 340), Image.LANCZOS).save("crop_bottom.png")
print("crops saved")
