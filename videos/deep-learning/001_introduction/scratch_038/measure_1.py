from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print("size", W, H)
r, g, b = a[...,0], a[...,1], a[...,2]

# Classify pixels
red   = (r>150) & (g<90) & (b<90)                      # crimson C00000
blue  = (b>150) & (r<110) & (g<110)                    # blue borders/text
dark  = (r<100) & (g<100) & (b<100)                    # black ink
white = (r>230) & (g>230) & (b>230)
gray  = (abs(r-232)<14) & (abs(g-232)<14) & (abs(b-232)<14)

def bbox(mask, name):
    ys, xs = np.nonzero(mask)
    if len(xs)==0:
        print(name, "EMPTY"); return None
    print(f"{name}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  count {len(xs)}")
    return xs.min(), xs.max(), ys.min(), ys.max()

print("--- full-frame masks ---")
bbox(red, "red ALL")
bbox(blue, "blue ALL")
bbox(dark, "dark ALL")

# top rows: find the red rule
print("--- top rule: red pixel count per row (rows 0..80) ---")
for y in range(0, 80):
    c = red[y].sum()
    if c: print(y, c, "xspan", np.nonzero(red[y])[0].min(), np.nonzero(red[y])[0].max())
