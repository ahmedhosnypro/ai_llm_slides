from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[...,0], a[...,1], a[...,2]
ink = (r<175)&(g<175)&(b<175)  # any dark-ish ink

def show(y0,y1,x0,x1,cell=4,label=""):
    print(f"--- {label} y{y0}..{y1} x{x0}..{x1} cell={cell} (col=x start {x0}, step {cell}) ---")
    hdr = "     " + "".join(str(((x0+c*cell)//10)%10) for c in range((x1-x0)//cell))
    print(hdr)
    for y in range(y0, y1, cell):
        row=""
        for x in range(x0, x1, cell):
            row += "#" if ink[y:y+cell, x:x+cell].sum()>0 else "."
        print(f"{y:4d} {row}")

show(255, 300, 150, 400, 4, "TOP: RGB / 3 dims labels")
show(300, 445, 348, 392, 3, "X + dashed lines between slab and stack")
show(295, 445, 380, 560, 4, "stack annotations (7s, 3, pencil)")
show(440, 512, 380, 560, 4, "735 weights + arrows")
