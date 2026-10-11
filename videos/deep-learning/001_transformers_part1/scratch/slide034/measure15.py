from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
def fine(x0,x1,y0,y1,label,step=1):
    print(f"== {label}")
    for y in range(y0,y1,step):
        row=""
        for x in range(x0,x1,step):
            R,G,B=a[y,x]
            if R+G+B<330: row+='K'
            elif R>150 and R-G>60 and R-B>60: row+='R'
            elif B>110 and B-R>25: row+='B'
            elif G-R>30 and G-B>25 and G>100: row+='G'
            elif R>235 and G>235 and B>225: row+=' '
            else: row+='.'
        print(f"{y:3d} {row}")
fine(220,400,162,218,"small eq box region")
