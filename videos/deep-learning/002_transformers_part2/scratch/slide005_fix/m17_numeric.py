# m17_numeric.py — numeric ink extraction: h-circle region + connector endpoints + target edges
from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
W,H = F.size; px = F.load()
def lum(x,y):
    r,g,b = px[x,y]; return 0.299*r+0.587*g+0.114*b
FX0, FY0, SX, SY = 18.0787, 0.4700, 0.961084, 0.957187
def tb(fx,fy): return ((fx-FX0)/SX, (fy-FY0)/SY)

print("=== 1. h-circle region: dark ink clusters x474..504 y326..368 (lum<200) ===")
for y in range(326, 369):
    runs=[]; cur=None
    for x in range(474, 505):
        if lum(x,y)<200:
            if cur is None: cur=x
        else:
            if cur is not None: runs.append((cur,x-1)); cur=None
    if cur is not None: runs.append((cur,504))
    if runs:
        info=[]
        for (a,b) in runs:
            mid=(a+b)//2
            info.append(f"x{a}-{b} rgb{px[mid,y]}")
        print(y, " | ".join(info))

print("\n=== 2. faint interior connector path (lum<240, x478..500 excluding circle y>340) ===")
for y in range(240, 341, 4):
    best=None
    for x in range(478, 501):
        L=lum(x,y)
        if L<240 and (best is None or L<best[1]): best=(x,L)
    if best: print(y, "x",best[0], "lum",round(best[1]), "rgb", px[best[0],y])
    else: print(y, "none")

print("\n=== 3. target edges (frame coords) ===")
# h circle: scan for the tan fill ring D4BCA0-ish / border 8A6A48
print("h circle scan rows 336..366, ink(lum<215) runs in x480..506:")
for y in range(336, 367, 2):
    runs=[]; cur=None
    for x in range(480, 507):
        if lum(x,y)<215:
            if cur is None: cur=x
        else:
            if cur is not None: runs.append((cur,x-1)); cur=None
    if cur is not None: runs.append((cur,506))
    print(" y",y, runs)
