from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
def probe(x0,y0,x1,y1,label):
    print(f"== {label} ==")
    for x in range(x0,x1):
        col = a[y0:y1, x]
        ys = np.nonzero(col.sum(axis=1) < 600)[0]
        if len(ys) > 3:
            print(f" x={x}: n={len(ys)} rows {y0+ys.min()}..{y0+ys.max()} sample={tuple(a[y0+ys[len(ys)//2],x])}")
probe(244,100,254,240,"v2 LEFT paren zone (x244..254)")
probe(614,100,626,240,"eq2 RIGHT paren zone (x614..626)")
probe(588,100,598,240,"eq2 LEFT paren zone (x588..598)")
probe(139,115,147,235,"v1 RIGHT paren hooks (x139..147)")
