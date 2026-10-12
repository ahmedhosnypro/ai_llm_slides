#!/usr/bin/env python3
"""Crop the pencil glyph from the original frame (faithful pixel import, ml-intro
figure-crop precedent). Region covers pencil ink x245..280 y206..231 + margin."""
from PIL import Image
im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_019.jpg").convert("RGB")
crop = im.crop((241, 203, 285, 237))  # 44x34
crop.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/pencil_crop_019.png")
print("pencil_crop_019.png", crop.size, "bbox=(241,203)-(285,237)")
