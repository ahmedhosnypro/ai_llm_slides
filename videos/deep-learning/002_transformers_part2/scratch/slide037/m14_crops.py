#!/usr/bin/env python3
"""Create 2x-upscaled crops of dense regions for vision probes."""
from PIL import Image
img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg").convert("RGB")
CROPS = {
  "crop_enc_stack":   (628, 253, 742, 420),
  "crop_enc_pe":      (575, 370, 745, 505),
  "crop_dec_stack":   (733, 190, 852, 320),
  "crop_dec_mid":     (733, 285, 852, 425),
  "crop_dec_pe":      (735, 395, 900, 505),
  "crop_dec_top":     (728, 100, 862, 210),
  "crop_pin":         (570, 145, 700, 295),
  "crop_highlight":   (625, 305, 775, 465),
  "crop_funnel":      (185, 230, 660, 460),
  "crop_enc_nx":      (580, 300, 655, 375),
  "crop_left_top":    (48, 220, 215, 335),
  "crop_brace":       (470, 240, 545, 430),
  "crop_enc_circles": (638, 368, 745, 418),
  "crop_right_full":  (560, 95, 905, 525),
}
for name,(x0,y0,x1,y1) in CROPS.items():
    c = img.crop((x0,y0,x1,y1))
    c = c.resize(((x1-x0)*2, (y1-y0)*2), Image.LANCZOS)
    c.save(f"{name}.png")
    print(name, c.size)
