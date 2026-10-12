from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[...,0], a[...,1], a[...,2]

reddish = ((r-g)>40) & ((r-b)>40) & (r>110)
dark  = (r<100) & (g<100) & (b<100)
white = (r>230) & (g>230) & (b>230)

print("--- reddish rows 0..120 ---")
for y in range(0, 120):
    c = reddish[y].sum()
    if c>3:
        xs = np.nonzero(reddish[y])[0]
        print(y, c, f"x {xs.min()}..{xs.max()}")

print("--- dark rows 500..540 (bottom bar) ---")
for y in range(500, 540):
    c = dark[y].sum()
    if c>3:
        xs = np.nonzero(dark[y])[0]
        print(y, c, f"x {xs.min()}..{xs.max()}")

# what's the background at various points
print("--- samples ---")
for (x,y) in [(5,5),(200,10),(480,3),(480,20),(480,50),(50,300),(950,300),(480,530),(480,536),(480,539),(20,270),(940,270)]:
    print((x,y), a[y,x])
