from PIL import Image
import numpy as np
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
def q(c):
    rr,gg,bb = c
    if rr>200 and gg<90 and bb<90: return "RED"
    if rr>140 and gg<130 and bb<130 and rr-gg>40: return "dred"
    if rr>215 and gg>170 and bb<120: return "GOLD"
    if abs(rr-240)<22 and abs(gg-136)<35 and abs(bb-144)<35: return "SALM"
    if gg>=rr-6 and gg>175 and abs(gg-bb)<30 and gg-rr>6: return "MINT"
    if rr>205 and gg>195 and 130<bb<190: return "CREAM"
    if rr>195 and 160<gg<215 and bb>205: return "PINK"
    if abs(rr-234)<13 and abs(gg-228)<13 and abs(bb-238)<15: return "LAV"
    if rr>235 and gg>235 and bb>235: return "WHIT"
    if rr<90 and gg<90 and bb<90: return "DARK"
    return "?"
def rle(y, x0, x1, minrun=2):
    out=[]; cur=None; start=x0
    for x in range(x0,x1):
        c=q(a[y,x])
        if c!=cur:
            if cur is not None and x-start>=minrun: out.append((start,x-1,cur))
            cur=c; start=x
    out.append((start,x1-1,cur)); return out
for y in [323, 350, 377, 404, 314, 392]:
    print("y=%d:" % y)
    for o in rle(y, 415, 615):
        print("   ", o)
