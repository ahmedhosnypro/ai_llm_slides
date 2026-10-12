from PIL import Image
import numpy as np
from collections import Counter
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)

def amap(y0, y1, x0, x1):
    print(f"== y[{y0},{y1}] x[{x0},{x1}] ==")
    print("    " + "".join(str((x//10)%10) for x in range(x0, x1)))
    for y in range(y0, y1):
        line = []
        for x in range(x0, x1):
            r,g,b = im[y,x]
            if r<100 and g<100: ch='K'
            elif r-b>70 and r-g>70 and g>85 and g<160: ch='O'   # orange
            elif r-g>40 and r-b>40: ch='R'
            elif b-r>50 and b-g>25: ch='B'
            elif abs(r-g)<20 and abs(g-b)<20: ch = '.' if r>238 else ('-' if r>150 else '#')
            else: ch='?'
            line.append(ch)
        print(f"{y:3d} " + "".join(line))
amap(286, 308, 254, 300)

def hist(y0,y1,x0,x1,lbl):
    q = im[y0:y1, x0:x1].reshape(-1,3)//8*8
    c = Counter(map(tuple, q))
    print(lbl, c.most_common(5))

hist(130, 145, 244, 254, "ROW1 between-box gap fill:")
hist(129, 134, 262, 306, "ROW1 box2 top strip fill:")
hist(199, 204, 260, 300, "ROW2 box1 top strip fill:")
hist(199, 204, 242, 248, "ROW2 gap fill:")
hist(276, 281, 256, 300, "ROW3 box2 top strip fill:")
hist(276, 281, 238, 248, "ROW3 gap fill:")
hist(136, 142, 700, 720, "ROW1 dots zone:")
hist(203, 209, 560, 600, "ROW2 dots zone:")
hist(430, 470, 100, 800, "CYAN panel fill:")
hist(380, 390, 100, 400, "CYAN summary-line zone:")
# borders cores
hist(119, 120, 300, 800, "ROW1 container top dash:")
hist(156, 158, 300, 800, "ROW1 container bottom dash:")
hist(187, 189, 300, 800, "ROW2 container top dash:")
hist(224, 226, 300, 800, "ROW2 container bottom dash:")
hist(262, 264, 300, 800, "ROW3 container top dash:")
hist(300, 302, 300, 700, "ROW3 container bottom dash:")
hist(111, 112, 200, 800, "NAVY rule:")
hist(341, 342, 200, 800, "CYAN panel top border:")
hist(349, 350, 200, 800, "CYAN panel 2nd line:")
hist(502, 503, 200, 800, "CYAN panel bottom border:")
hist(65, 66, 130, 500, "NAVY panel left border col:")
hist(892, 893, 130, 500, "NAVY panel right border col:")
