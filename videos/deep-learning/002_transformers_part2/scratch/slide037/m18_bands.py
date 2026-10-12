#!/usr/bin/env python3
"""Per-row dominant-color bands inside the encoder container and decoder stack
(original frame coords; excludes rows dominated by text ink)."""
from PIL import Image
from collections import Counter
img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg").convert("RGB")
px = img.load()
AX, SX = 17.101, 0.962329
BY, SY = -0.224, 0.96053
def SY_(fy): return round((fy-BY)/SY,1)

def bands(x0, x1, y0, y1, label, skip=None):
    print(f"== {label} (frame x{x0}-{x1}) ==")
    prev=None; start=y0
    res=[]
    for y in range(y0,y1):
        c = Counter()
        for x in range(x0,x1):
            p = px[x,y]
            key=(p[0]//10*10, p[1]//10*10, p[2]//10*10)
            c[key]+=1
        top = c.most_common(1)[0][0]
        tot = sum(c.values())
        if top in (skip or ()):  # skip background families
            top = ('BG',)+()
        if top != prev:
            if prev is not None and y-start>=2:
                res.append((start,y-1,prev))
            prev=top; start=y
    res.append((start,y1-1,prev))
    for a,b,c in res:
        if isinstance(c, tuple) and len(c)==3:
            print(f"  frame y{a}-{b}  slide y{SY_(a)}-{SY_(b)}  mode~{c}")
        else:
            print(f"  frame y{a}-{b}  slide y{SY_(a)}-{SY_(b)}  {c}")

# encoder container interior (frame x652-716 => slide ~659-725)
bands(652, 716, 255, 420, "ENCODER container", skip=None)
print()
# decoder stack interior (frame x748-806)
bands(748, 806, 195, 320, "DECODER stack", skip=None)
print()
# decoder low container (purple) frame x748-806 y318-412
bands(748, 806, 318, 412, "DECODER low (purple)", skip=None)
