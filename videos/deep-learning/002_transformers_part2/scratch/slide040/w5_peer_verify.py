from PIL import Image
import numpy as np
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg"
im = np.array(Image.open(FR).convert("RGB")).astype(int)
def runs_of(mask, x0):
    out=[];s=None
    for i,v in enumerate(mask):
        if v and s is None: s=i
        if not v and s is not None: out.append((x0+s,x0+i-1)); s=None
    if s is not None: out.append((x0+s,x0+len(mask)-1))
    return out
print("== 'learn parameters' green underline claim: frame y156..159, x 385..545 ==")
for y in range(155,161):
    row = im[y,385:546]
    dark = row.mean(axis=1)<215
    rr=[(a,b) for a,b in runs_of(dark,385) if b-a>=20]
    for a,b in rr:
        print(f"  y={y}: run {a}..{b} med {np.median(im[y,a:b+1],axis=0).astype(int)}")
print("== L1 blue underline claim: NO underline (rows 130..140 x 530..820 sparse?) ==")
for y in range(130,141):
    row = im[y,530:821]
    dark = row.mean(axis=1)<215
    rr=[(a,b) for a,b in runs_of(dark,530) if b-a>=25]
    if rr: print(f"  y={y}: long runs {rr}")
print("(no output above = no long runs = NO L1 blue underline, claim confirmed)")
print("== stem slant m27-E spot check: 'mean' (blue L1) leftmost-stem x per row ==")
for y in range(126,140):
    row = im[y,634:676]
    r,g,b = row[:,0],row[:,1],row[:,2]
    m = (b>r+40)&(b>90)&(r<150)
    idx=np.where(m)[0]
    if len(idx): print(f"  y={y}: leftmost {634+idx[0]} rightmost {634+idx[-1]}")
