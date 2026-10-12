from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[...,0], a[...,1], a[...,2]

brown = ((r-g)>40)&((g-b)>25)&(r>120)&(b<130)
purple = (r>90)&(r<170)&(b>90)&(b<180)&(g<90)
blue = (b>190)&(r>70)&(r<160)&(g>110)&(g<200)
for m, name in [(brown,'brown'),(purple,'purple'),(blue,'blue')]:
    m2 = m.copy(); m2[:256]=False; m2[512:]=False
    ys, xs = np.nonzero(m2)
    print(f"--- {name} column profile (x: count) ---")
    # coarse: bucket by 20px
    import collections
    buck = collections.Counter((x//20)*20 for x in xs)
    print(sorted(buck.items()))
    print(f"--- {name} row profile (y: count) ---")
    bucky = collections.Counter((y//10)*10 for y in ys)
    print(sorted(bucky.items()))
