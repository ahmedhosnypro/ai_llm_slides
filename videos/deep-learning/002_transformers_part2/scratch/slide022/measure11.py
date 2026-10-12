from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)

def amap(y0, y1, x0, x1, step=1):
    print(f"== map y[{y0},{y1}] x[{x0},{x1}] (1px, x tens header) ==")
    print("    " + "".join(str((x//10)%10) for x in range(x0, x1, step)))
    for y in range(y0, y1):
        line = []
        for x in range(x0, x1, step):
            r,g,b = im[y,x]
            if r<100 and g<100: ch='K'
            elif r-g>45 and r-b>45: ch='R'
            elif b-r>50 and b-g>25: ch='B'
            elif r>235 and g>225 and b<212: ch='Y'
            elif r>215 and g>235 and b>235 and g-r>5: ch='C'
            elif r>230 and g>215 and b>195 and r-b>15: ch='y'
            elif abs(r-g)<20 and abs(g-b)<20: ch = '.' if r>238 else ('-' if r>150 else '#')
            else: ch='?'
        # build line
            line.append(ch)
        print(f"{y:3d} " + "".join(line))

amap(258, 315, 160, 320)   # row3 left part incl box1-2 gap and +delta
amap(258, 315, 780, 892)   # row3 right part: box7-8 gap, +delta, N-2/N-1 boxes
