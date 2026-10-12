from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[...,0], a[...,1], a[...,2]
black = (r<120)&(g<120)&(b<120)
def show(y0,y1,x0,x1,cell=1,label=""):
    print(f"--- {label} y{y0}..{y1} x{x0}..{x1} cell={cell} ---")
    print("     " + "".join(str((x//10)%10) for x in range(x0, x1, cell)))
    for y in range(y0, y1, cell):
        row=""
        for x in range(x0, x1, cell):
            row += "#" if black[y:y+cell, x:x+cell].sum()>0 else "."
        print(f"{y:4d} {row}")
show(340, 404, 344, 404, 2, "dashed zone glyphs (7s?) ORIGINAL")
show(288, 342, 274, 344, 2, "3dims arrow region ORIGINAL")
