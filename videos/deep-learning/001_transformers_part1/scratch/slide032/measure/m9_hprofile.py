import numpy as np
from PIL import Image
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
def hp(y, x0=214, x1=382):
    print(f"=== horizontal y={y}")
    runs=[]
    prev=None
    for x in range(x0,x1):
        r,g,b = a[y,x]
        v = f"#{r:02X}{g:02X}{b:02X}"
        if r>245 and g>245 and b>240: k="WHT"
        elif r>245 and g>235 and 150<b<225: k="YEL"
        elif r>200 and g<190 and b<210 and r-b>25: k="PNK"
        elif max(r,g,b)<150: k="INK"
        else: k="mid"
        if k!=prev: runs.append([x,x,k,v]); prev=k
        else: runs[-1][1]=x; runs[-1][3]=v
    for (xs,xe,k,v) in runs:
        print(f"  x{xs}..{xe} {k} {v}")
hp(95)   # row1 above textbox
hp(103)  # textbox top border row1
hp(107)  # row1 text
hp(95-0)
