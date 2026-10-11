import numpy as np
from PIL import Image
from scipy import ndimage

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def largest(mask, label, k=3):
    lab, n = ndimage.label(mask)
    if n == 0:
        print(f"{label}: EMPTY"); return
    sizes = ndimage.sum(mask, lab, range(1, n+1))
    order = np.argsort(sizes)[::-1][:k]
    for i in order:
        if sizes[i] < 30: continue
        ys, xs = np.where(lab == i+1)
        print(f"{label}[{i}] n={int(sizes[i])}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}")

# tan center container
tan = (abs(r-234)<18)&(abs(g-192)<18)&(abs(b-143)<20)
largest(tan, "tan-zoom-container", 2)

# encoder interior tan-brown E8D0B8
enc = (abs(r-232)<12)&(abs(g-208)<12)&(abs(b-184)<14)
largest(enc, "encoder-interior", 2)

# decoder interior pale-green C8E8C0
dec = (abs(r-200)<14)&(abs(g-232)<12)&(abs(b-192)<14)
largest(dec, "decoder-interior", 2)

# masked MHA purple
pur = (abs(r-179)<25)&(abs(g-157)<25)&(abs(b-219)<28)
largest(pur, "maskedMHA", 2)

# gray A8A8A8 blocks (Multi-Head Attention / Add&Norm / Feed Forward / Linear?)
gray = (abs(r-168)<22)&(abs(g-168)<22)&(abs(b-168)<22)
largest(gray, "gray-block", 6)

# maroon output embedding 8B4A4A
mar = (abs(r-139)<22)&(abs(g-74)<20)&(abs(b-74)<20)
largest(mar, "maroon", 2)

# brown input embedding C89A6A
br = (abs(r-200)<18)&(abs(g-154)<18)&(abs(b-106)<20)
largest(br, "brown-input-emb", 2)

# light green A8E8A8 (Linear/Softmax decoder)
lg = (abs(r-168)<20)&(abs(g-232)<16)&(abs(b-168)<20)
largest(lg, "lightgreen-linear/softmax", 4)
