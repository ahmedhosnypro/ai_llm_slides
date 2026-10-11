from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def cls(y,x):
    R,G,B = r[y,x],g[y,x],b[y,x]
    if R>120 and R-G>40 and R-B>40: return 'R'
    if B-R>60 and B>110: return 'B'
    if B-R>25 and B>150 and R<160: return 'b'   # weak blue
    if R<120 and G<120 and B<120: return 'K'
    if R-G>15 and R>200: return 'p'             # pinkish
    if abs(R-233)<12 and abs(G-233)<12 and abs(B-231)<14: return '.'
    if R>242 and G>242 and B>242: return 'w'
    if R>200 and 110<G<200 and B<110: return 'O' # orange
    return '?'

def show(y0,y1,x0,x1,ystep=2,xstep=4,label=""):
    print(f"--- {label} y{y0}..{y1} x{x0}..{x1}")
    for y in range(y0,y1+1,ystep):
        print(f"{y:4d} " + "".join(cls(y,x0+i*xstep) for i in range((x1-x0)//xstep+1)))

show(180, 240, 60, 905, label="ROW2 full")
