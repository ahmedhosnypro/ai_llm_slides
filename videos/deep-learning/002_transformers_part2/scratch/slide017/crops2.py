from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
def crop(name, box, scale):
    im = F.crop(box)
    im = im.resize((im.width*scale, im.height*scale), Image.LANCZOS)
    im.save("crops/%s.png" % name)
    print(name, box, "->", im.size)
crop("micro_ltlabel", (480, 82, 570, 118), 5)     # LT box right part + dHxd label
crop("micro_concat_l", (300, 124, 500, 156), 4)   # concat segments 1-3 labels
crop("micro_concat_r", (490, 124, 690, 156), 4)   # concat segments 4-5 labels
crop("micro_vlabels", (430, 315, 485, 430), 5)    # V label column + nodes
crop("micro_wq", (170, 448, 270, 505), 5)         # q label + W_q box
crop("micro_chips", (280, 235, 520, 305), 4)      # Probabilities oval + climbing chips zone
crop("micro_seg2", (413, 127, 447, 151), 8)
crop("micro_seg4", (561, 127, 595, 151), 8)
