from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

dark = (r<140)&(g<140)&(b<150)
redink = (r>120)&(r>g+60)&(r>b+60)
blueink = (b>100)&(b>r+40)&(g<b+10)

def inkmap(x0,y0,x1,y1,cell=2):
    print(f"--- ink map x{x0}..{x1} y{y0}..{y1} cell={cell} (D=dark R=red B=blue .=bg) ---")
    hdr = "     " + "".join(str(((x0+i*cell)//10)%10) for i in range((x1-x0)//cell))
    print(hdr)
    for y in range(y0, y1, cell):
        row = ""
        for x in range(x0, x1, cell):
            cd = dark[y:y+cell, x:x+cell].sum()
            cr = redink[y:y+cell, x:x+cell].sum()
            cb = blueink[y:y+cell, x:x+cell].sum()
            n = cell*cell
            if cr > n*0.15: row += "R"
            elif cb > n*0.15: row += "B"
            elif cd > n*0.15: row += "D"
            else: row += "."
        print(f"{y:4d} " + row)

inkmap(84, 88, 430, 246, 2)      # left box
