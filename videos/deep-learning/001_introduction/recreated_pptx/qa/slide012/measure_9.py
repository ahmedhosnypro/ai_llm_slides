from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
# 2D maps of dot zones x 100..132
for lbl,(y0,y1) in [("dot1",(233,251)),("dot2",(277,295)),("dot3",(320,338)),("dot4",(364,383))]:
    print(f"\n{lbl} rows {y0}..{y1}, cols 100..132 (.' '=light, '#'=<450, '@'=<250):")
    hdr = "     " + "".join(str(x%10) for x in range(100,133))
    print(hdr)
    for y in range(y0,y1):
        line=""
        for x in range(100,133):
            s=a[y,x].sum()
            line += "@" if s<250 else ("#" if s<450 else ".")
        print(f"{y:4d} {line}")
