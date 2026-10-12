from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

def map1(x0,y0,x1,y1,label,step=1):
    print(f"== {label} ==")
    print("     " + "".join(str((x//10)%10) for x in range(x0,x1,step)))
    for y in range(y0,y1,step):
        row=""
        for x in range(x0,x1,step):
            rr,gg,bb = a[y,x]
            if rr>130 and rr-gg>45 and rr-bb>35: row+="R"
            elif rr<110 and gg<110 and bb<120: row+="D"
            elif bb>90 and bb-rr>30: row+="B"
            elif rr>235 and gg>235 and bb>235: row+="."
            else: row+=" "
        print(f"{y:4d} "+row)

map1(224, 56, 724, 92, "TITLE full", 2)
