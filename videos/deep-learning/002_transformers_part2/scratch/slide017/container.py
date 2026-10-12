from PIL import Image
import numpy as np
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

# mint container fill
mint = (np.abs(r-232)<20)&(np.abs(g-252)<14)&(np.abs(b-232)<20)
# non-mint content inside container
prof = []
for x in range(160, 356):
    col = (~mint[475:499, x]).sum()
    prof.append((x, col))
# print runs where content>6 (strip columns)
runs=[]; inr=False
for x, c in prof:
    if c>6 and not inr: x0=x; inr=True
    elif c<=6 and inr: runs.append((x0, x-1)); inr=False
if inr: runs.append((x0, 355))
print("strip x-ranges in container:", runs)

def rle(y, x0, x1, minrun=1):
    def q(c):
        rr,ggg,bb = c
        if rr>200 and ggg<90 and bb<90: return "RED"
        if rr>140 and ggg<130 and bb<130 and rr-ggg>40: return "dred"
        if rr>215 and ggg>170 and bb<120: return "GOLD"
        if abs(rr-240)<22 and abs(ggg-136)<35 and abs(bb-144)<35: return "SALM"
        if ggg>=rr-6 and ggg>175 and abs(ggg-bb)<30 and ggg-rr>6: return "MINT"
        if rr>205 and ggg>195 and 130<bb<190: return "CREAM"
        if rr>195 and 160<ggg<215 and bb>205: return "PINK"
        if abs(rr-234)<13 and abs(ggg-228)<13 and abs(bb-238)<15: return "LAV"
        if rr>235 and ggg>235 and bb>235: return "WHIT"
        if rr<90 and ggg<90 and bb<90: return "DARK"
        if abs(rr-233)<9 and abs(ggg-233)<9: return "GRAY"
        if rr>235 and ggg>215 and bb>215: return "wcrm"
        return "?"
    out=[]; cur=None; start=x0
    for x in range(x0,x1):
        c=q(a[y,x])
        if c!=cur:
            if cur is not None and x-start>=minrun: out.append((start,x-1,cur))
            cur=c; start=x
    out.append((start,x1-1,cur)); return out

# vertical extent of strips: scan column in each run
for (x0,x1) in runs:
    xm=(x0+x1)//2
    col=[]
    for y in range(470, 502):
        c=~mint[y,xm]
        col.append("X" if c else ".")
    print("x %d..%d (mid %d) vert:" % (x0,x1,xm), "".join(col))
