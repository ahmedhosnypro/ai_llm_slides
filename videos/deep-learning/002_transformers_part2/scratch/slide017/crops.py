from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
def crop(name, box, scale=2):
    im = F.crop(box)
    im = im.resize((im.width*scale, im.height*scale), Image.LANCZOS)
    im.save("crops/%s.png" % name)
    print(name, box, "->", im.size)
crop("leftcol",  (55, 258, 212, 515))      # input strips + gold boxes + K zone
crop("dotprod",  (195, 283, 305, 432))     # tan box + K,q + scaling
crop("midright", (300, 283, 625, 432))     # softmax, sigma, nodes, V, W_v, X cells
crop("queryrow", (55, 428, 625, 518))      # W_q, q bar, token container
crop("toppipe",  (180, 38, 725, 205))      # vecbox, LT box, concat bar
crop("title",    (495, 45, 915, 110))      # title + badge
crop("rightswoosh", (580, 165, 810, 465))  # swoosh, +H* Heads, panels
crop("legend",   (695, 428, 915, 520))     # bottom-right legend
