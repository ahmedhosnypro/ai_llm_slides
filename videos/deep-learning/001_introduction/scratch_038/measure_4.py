from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[...,0], a[...,1], a[...,2]
ink   = ((r<160)|(g<160)|(b<160))  # any ink
reddish = ((r-g)>40) & ((r-b)>40) & (r>110)
bluish  = ((b-r)>40) & ((b-g)>20) & (b>110)
greenish= ((g-r)>30) & ((g-b)>30) & (g>90)
dark  = (r<100) & (g<100) & (b<100)

# Formula box interior: x 94..876, y 121..231
print("--- formula box ink rows ---")
for y in range(121, 232):
    c = ink[y, 94:877].sum()
    if c>3:
        xs = np.nonzero(ink[y, 94:877])[0] + 94
        # color composition
        rd = reddish[y, 94:877].sum(); bl = bluish[y, 94:877].sum(); gr = greenish[y, 94:877].sum(); dk = dark[y, 94:877].sum()
        print(f"y={y} ink={c} r={rd} b={bl} g={gr} dk={dk} x {xs.min()}..{xs.max()}")
