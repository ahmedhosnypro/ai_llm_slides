# m7_zoommaps.py — zoomed ASCII maps of matrix, arrow, circles/band
import numpy as np
from PIL import Image
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
mx=a.max(axis=2); mn=a.min(axis=2); sat=mx-mn
R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]

def cls(p):
    r,g,b=p
    m=max(p); s=m-min(p)
    if m>238 and s<14: return " "         # white
    if 200<m<=238 and s<16: return "-"     # light gray fill (band)
    if s<25 and m<=200: return "g"         # mid gray (C0C0C0)
    if m<110: return "#"                   # dark
    if r>150 and g<110 and b<110: return "R"
    if r>170 and 110<=g<165 and b<150 and r-g>40: return "o"  # soft red/pink-red
    if r>215 and g>185 and b>150 and r-b>30 and r-g<50: return "y"  # pale yellow
    if r>200 and g>140 and b>140 and r-g>45 and abs(g-b)<40: return "p"  # pink
    if b>120 and b-r>35: return "B"
    if g>110 and g-r>25 and g-b>25: return "G"
    if r>150 and b>150 and g<150 and r-g>30 and b-g>30: return "M"
    return "?"

def zoom(x0,y0,x1,y1,cell=2,label=""):
    print(f"=== {label} x{x0}..{x1} y{y0}..{y1} cell={cell}")
    hdr="     "+"".join(str((x0+c*cell)//10%10) if c%5==0 else " " for c in range((x1-x0)//cell+1))
    print(hdr)
    for r in range((y1-y0)//cell+1):
        y=y0+r*cell
        line=""
        for c in range((x1-x0)//cell+1):
            x=x0+c*cell
            blk=a[y:y+cell,x:x+cell].reshape(-1,3)
            med=np.median(blk,axis=0)
            line+=cls(tuple(med))
        print(f"{y:4d} {line}")

zoom(214,80,380,264,2,"MATRIX")
zoom(474,132,590,248,2,"ARROW")
