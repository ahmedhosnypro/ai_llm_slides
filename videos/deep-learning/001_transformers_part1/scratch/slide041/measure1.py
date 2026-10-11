import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
print("frame size", W, H)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def bbox(mask, label):
    ys, xs = np.where(mask)
    if not len(xs):
        print(f"{label}: EMPTY"); return None
    print(f"{label}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  n={len(xs)}")
    return xs.min(), xs.max(), ys.min(), ys.max()

# title: red-ish text in top area y<60
red_title = (r>140)&(g<90)&(b<90)
red_title[:25,:] = False
red_title[70:,:] = False
bbox(red_title, "title-red-ink(top)")

# badge: yellow near top right
yel = (r>200)&(g>200)&(b<190)
yel[:, :800] = False; yel[100:,:] = False
bbox(yel, "badge-yellow")

# tan center container EAC08F ~ (234,192,143)
tan = (abs(r-234)<20)&(abs(g-192)<22)&(abs(b-143)<25)
bbox(tan, "tan-container(EAC08F)")

# right panel interior: tan-brown E8D0B8 ~ (232,208,184)
enc = (abs(r-232)<14)&(abs(g-208)<14)&(abs(b-184)<16)
enc[:, :540] = False
bbox(enc, "encoder-half(E8D0B8)")

# pale green decoder C8E8C0 ~ (200,232,192)
dec = (abs(r-200)<14)&(abs(g-232)<14)&(abs(b-192)<14)
dec[:, :540] = False
bbox(dec, "decoder-half(C8E8C0)")

# dark green border 006400 ~ (0,100,0)
dg = (r<90)&(g>75)&(g<130)&(b<80)
bbox(dg, "darkgreen(006400) all")

# bright green border 00A000
bg = (r<90)&(g>130)&(b<90)
bbox(bg, "brightgreen(00A000)")

# purple B39DDB masked MHA
pur = (abs(r-179)<25)&(abs(g-157)<25)&(abs(b-219)<25)
pur[:, :540] = False
bbox(pur, "maskedMHA-purple(B39DDB)")
