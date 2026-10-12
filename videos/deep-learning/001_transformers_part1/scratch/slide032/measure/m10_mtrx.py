import numpy as np
from PIL import Image
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
def cls(p):
    r,g,b=int(p[0]),int(p[1]),int(p[2])
    mx,mn=max(p),min(p); s=mx-mn
    if mx>=242 and s<=12: return "."          # white
    if r>=240 and g>=235 and 150<=b<=228 and (r-b)>=18: return "y"   # pale yellow
    if r>=238 and 190<=g<=238 and 195<=b<=242 and (r-b)<18 and s>=10: return "p"  # light pink
    if r>=200 and 150<=g<210 and 160<=b<225 and (r-g)>=35: return "P"  # strong pink border
    if mx<150: return "#"                     # dark ink
    if r>g>b and (r-b)>=35 and mx<200: return "b"  # brown/dark-orange border
    if b>120 and b-r>30: return "B"
    if g>100 and g-r>20 and g-b>20: return "G"
    if r>120 and b>120 and g<r-20 and g<b-10: return "M"
    if r>150 and g<140 and b<140: return "R"
    return "?"
CELL=3
print("matrix zoom x216..378 y82..262, cell=3px; legend: .=white y=yellow p=lightpink P=pinkborder #=ink b=brown B=blue G=green M=magenta R=red")
for y in range(82,263,CELL):
    line=""
    for x in range(216,379,CELL):
        blk=a[y:y+CELL,x:x+CELL].reshape(-1,3)
        line+=cls(np.median(blk,axis=0))
    print(f"{y:3d} {line}")
