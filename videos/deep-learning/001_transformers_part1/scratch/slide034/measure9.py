from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
def cmap(x0,x1,y0,y1,label,step=3):
    print(f"== {label} x{x0}..{x1} y{y0}..{y1} step{step}")
    def cls(c):
        R,G,B=c[0],c[1],c[2]
        if R+G+B<250: return 'K'
        if R>150 and R-G>60 and R-B>60: return 'R'
        if R>200 and 110<G<205 and B<120: return 'O'
        if R>210 and G>190 and B<150: return 'Y'
        if B>120 and B-R>40 and R<170: return 'B'
        if G-R>30 and G-B>25 and G>100: return 'G'
        if R>235 and G>235 and B>225: return 'W'
        if 230<R<256 and 205<G<245 and 185<B<235 and R-B>15: return 'p'
        return '.'
    print("     "+"".join(str(((x0+i*step)//10)%10) for i in range((x1-x0)//step)))
    for y in range(y0,y1,step):
        print(f"{y:4d} "+"".join(cls(a[y,x]) for x in range(x0,x1,step)))

cmap(55,250,103,175,"concept: large eq box",2)
cmap(240,395,103,175,"concept: [X_i] symbol region",2)
