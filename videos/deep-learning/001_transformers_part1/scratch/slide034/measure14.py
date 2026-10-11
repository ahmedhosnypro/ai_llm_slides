from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
dark=(r<160)&(g<160)&(b<160)

def fine(x0,x1,y0,y1,label):
    print(f"== {label}")
    for y in range(y0,y1):
        row=""
        for x in range(x0,x1):
            R,G,B=a[y,x]
            if R+G+B<330: row+='K'
            elif R>150 and R-G>60 and R-B>60: row+='R'
            elif B>110 and B-R>25: row+='B'
            elif G-R>30 and G-B>25 and G>100: row+='G'
            elif R>235 and G>235 and B>225: row+=' '
            else: row+='.'
        print(f"{y:3d} {row}")

# (a) emb box borders: row through middle
print("emb box row y=312:", [(x,tuple(a[312,x])) for x in range(48,60)] , [(x,tuple(a[312,x])) for x in range(84,94)], [(x,tuple(a[312,x])) for x in range(124,142)])
# (b) [X_i] concept symbol
fine(308,368,114,170,"concept [X_i] fine")
