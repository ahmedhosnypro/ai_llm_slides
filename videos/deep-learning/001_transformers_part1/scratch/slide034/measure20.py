from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
print("    " + "".join(str(x%10) for x in range(295,400)))
for y in range(284,345):
    row=""
    for x in range(295,400):
        R,G,B=a[y,x]
        s=R+G+B
        if s<250: row+='#'
        elif s<480: row+='+'
        elif s<660: row+='.'
        else: row+=' '
    print(f"{y:3d} {row}")
