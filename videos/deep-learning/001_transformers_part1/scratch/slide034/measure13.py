from PIL import Image
import numpy as np
img = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg').convert('RGB')
a = np.asarray(img).astype(int)
def cls(c):
    R,G,B=c[0],c[1],c[2]
    if R+G+B<330: return 'K'          # dark ink
    if R>150 and R-G>60 and R-B>60: return 'R'
    if R>210 and G>190 and 150<=B<235 and R-B>20: return 'y'   # pale yellow
    if B>110 and B-R>25: return 'B'
    if R>235 and G>235 and B>225: return 'W'
    if 230<R<256 and 205<G<245 and 185<B<235 and R-B>12: return 'p'
    return '?'
def scan(x, y0, y1, label):
    print(f"== col x={x} ({label})")
    prev=None; start=y0
    for y in range(y0,y1):
        k=cls(a[y,x])
        if k!=prev:
            if prev is not None and y-start>=1:
                print(f"   {prev} y {start}..{y-1}  ({y-start}px) mid~{tuple(a[(start+y-1)//2,x])}")
            prev=k; start=y
    print(f"   {prev} y {start}..{y1-1} ({y1-start}px) ~{tuple(a[y1-1,x])}")
scan(148, 355, 490, "input stack col1 (between parens)")
scan(148, 355, 490, "dup") 
scan(281, 355, 490, "output stack col1")
scan(430, 355, 490, "input stack col2")
