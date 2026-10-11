from PIL import Image

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide041/"
im = Image.open(SRC).convert("RGB")
print("frame", im.size)

# crops in original px (960x540)
crops = {
    "cropA_center_zoom": (270, 195, 540, 540),
    "cropB_right_panel": (555, 95, 915, 540),
    "cropC_left_schematic": (35, 220, 215, 505),
}
for name, box in crops.items():
    c = im.crop(box)
    c2 = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
    c2.save(OUT + name + ".png")
    print(name, box, "->", c2.size)
