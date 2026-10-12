from PIL import Image
import numpy as np
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)

def q(c):
    r,g,b = c
    if r>200 and g<90 and b<90: return "RED"
    if r>140 and g<130 and b<130 and r-g>40: return "dred"
    if r>215 and g>170 and b<120: return "GOLD"
    if abs(r-240)<22 and abs(g-136)<35 and abs(b-144)<35: return "SALM"
    if g>=r-6 and g>175 and abs(g-b)<30 and g-r>6: return "MINT"
    if r>205 and g>195 and 130<b<190: return "CREAM"
    if r>195 and 160<g<215 and b>205: return "PINK"
    if abs(r-234)<13 and abs(g-228)<13 and abs(b-238)<15: return "LAV"
    if r>235 and g>235 and b>235: return "WHIT"
    if r<90 and g<90 and b<90: return "DARK"
    if abs(r-233)<9 and abs(g-233)<9 and abs(b-231)<9: return "GRAY"
    if r>235 and g>215 and b>215: return "wcrm"
    return "?"

def rle(y, x0, x1, minrun=2):
    out=[]; cur=None; start=x0
    for x in range(x0, x1):
        c = q(a[y, x])
        if c != cur:
            if cur is not None and x-start >= minrun: out.append((start, x-1, cur))
            elif cur is not None: 
                if out and out[-1][2]==cur: pass
                else: out.append((start, x-1, cur))
            cur=c; start=x
    out.append((start, x1-1, cur))
    return [o for o in out if o[2] not in ("WHIT",) or o[1]-o[0]>3]

for y in [436, 452, 468, 483, 497, 472]:
    print("y=%d:" % y, rle(y, 90, 360))
