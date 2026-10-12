from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[...,0], a[...,1], a[...,2]
ink = (r<175)&(g<175)&(b<175)

def show(y0,y1,x0,x1,cell=2,label=""):
    print(f"--- {label} y{y0}..{y1} x{x0}..{x1} cell={cell} ---")
    print("     " + "".join(str(((x0+c*cell)//10)%10) for c in range((x1-x0)//cell)))
    for y in range(y0, y1, cell):
        row=""
        for x in range(x0, x1, cell):
            row += "#" if ink[y:y+cell, x:x+cell].sum()>0 else "."
        print(f"{y:4d} {row}")

show(262, 340, 282, 400, 2, "RGB + 3 dims + arrow")
show(330, 400, 346, 400, 2, "X sign + dashes fine")
show(320, 360, 390, 480, 2, "above-stack 7 + slab tops")
