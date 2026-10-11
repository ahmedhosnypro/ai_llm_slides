from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]

# fill color profile: rows across concept box interior
for y in [115, 150, 170, 215, 245, 256]:
    row = a[y, 55:390]
    print(f"concept row y={y}: median {tuple(np.median(row,axis=0).astype(int))}")

def cmap(x0,x1,y0,y1,label,step=2):
    print(f"== {label} ({x0}..{x1}, {y0}..{y1}) step{step}")
    classes = {
      'K': lambda c: c.sum()<260,                      # dark ink
      'R': lambda c: c[0]>150 and c[0]-c[1]>60 and c[0]-c[2]>60,   # red
      'O': lambda c: c[0]>200 and 120<c[1]<205 and c[2]<130,       # orange
      'Y': lambda c: c[0]>210 and c[1]>190 and c[2]<150,           # yellow
      'B': lambda c: c[2]>120 and c[2]-c[0]>40 and c[0]<170,       # blue
      'G': lambda c: c[1]-c[0]>30 and c[1]-c[2]>25 and c[1]>100,   # green
      'W': lambda c: c[0]>235 and c[1]>235 and c[2]>225,           # white
      'P': lambda c: 230<c[0]<255 and 205<c[1]<245 and 185<c[2]<235 and c[0]-c[2]>15, # peach
      'y': lambda c: c[0]>235 and c[1]>235 and 200<c[2]<235,       # pale-yellow fill
      '.': lambda c: True,
    }
    order=['K','R','O','Y','B','G','W','P','y','.']
    for y in range(y0,y1,step):
        line=""
        for x in range(x0,x1,step):
            c=a[y,x]
            for k in order:
                if k!='.' and classes[k](c): line+=k; break
            else: line+='.'
        print(f"{y:4d} {line}")

# annotation region
cmap(60,395,208,262,"annotation region",2)
