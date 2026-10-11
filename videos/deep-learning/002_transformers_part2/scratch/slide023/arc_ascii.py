from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def cls(y,x):
    R,G,B = int(r[y,x]), int(g[y,x]), int(b[y,x])
    if R-B>60 and R-G>25 and R>150:
        return 'O' if G>90 else 'R'   # orange vs strong red
    if R-G>35 and R-B>35: return 'r'  # weak red
    if R<140 and G<140 and B<140: return 'K'
    return '.'

print("arc zone arrow1: y292..334, x196..312 (1char/2px)")
for y in range(292, 335):
    line = "".join(cls(y, x) for x in range(196, 313, 2))
    print(f"{y:3d} {line}")
