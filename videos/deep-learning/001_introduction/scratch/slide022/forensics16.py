from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def map1(x0,y0,x1,y1,label):
    print(f"== {label} (x{x0}..{x1}, y{y0}..{y1}) ==")
    hdr = "     " + "".join(str((x//10)%10) for x in range(x0,x1))
    print(hdr)
    for y in range(y0,y1):
        row=""
        for x in range(x0,x1):
            r,g,b = a[y,x]
            if r<100 and g<100 and b<110: row+="D"
            elif r>130 and r-g>45 and r-b>35: row+="R"
            elif b>90 and b-r>30: row+="B"
            elif g>200 and b>200 and r<215 and g-r>20: row+="C"
            elif r>235 and g>235 and b>235: row+="."
            else: row+=" "
        print(f"{y:4d} "+row)

map1(410,406,446,436,"SIGMA CIRCLE")
map1(470,406,512,436,"STEP BLOCK")
map1(556,412,616,432,"O/P zone")
