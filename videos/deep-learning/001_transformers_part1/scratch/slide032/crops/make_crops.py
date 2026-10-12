# make_crops.py — crop + upscale frame regions for gated reads
from PIL import Image
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
im = Image.open(F).convert("RGB")
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide032/crops/"
def crop(name, box, scale):
    c = im.crop(box)
    c = c.resize((c.width*scale, c.height*scale), Image.LANCZOS)
    c.save(OUT + name, quality=95)
    print(name, c.size)
crop("c1_band.png",      (485, 296, 895, 405), 3)   # band + staircase labels + W_Q
crop("c2_eqpanel.png",   (52, 64, 470, 280), 2)     # whole equation panel
crop("c3_navyhead.png",  (655, 330, 735, 375), 8)   # navy arrowhead zoom
crop("c4_netpanel.png",  (470, 240, 915, 512), 2)   # network panel
