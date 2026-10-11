from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def fine(y0,y1,x0,x1,label):
    print(f"--- {label} y{y0}..{y1} x{x0}..{x1}")
    for y in range(y0,y1+1):
        line=""
        for x in range(x0,x1+1):
            R,G,B = r[y,x],g[y,x],b[y,x]
            if R>120 and R-G>40 and R-B>40: c='R'
            elif B-R>60 and B>110: c='B'
            elif B-R>28 and B>150: c='b'
            elif R<120 and G<120 and B<120: c='K'
            elif R-G>12 and R>200: c='p'
            elif abs(R-205)<14 and abs(G-205)<14 and B>235: c='l'
            elif abs(R-233)<12 and abs(G-233)<12 and abs(B-231)<14: c='.'
            elif R>242 and G>242 and B>242: c='w'
            else: c='?'
            line+=c
        print(f"{y:4d} {line}")

fine(184, 232, 148, 245, "ROW2 box1+gap zone")
fine(256, 312, 150, 250, "ROW3 box1+gap zone")
