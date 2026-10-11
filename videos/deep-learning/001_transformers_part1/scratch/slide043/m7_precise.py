#!/usr/bin/env python3
"""Precise runs: find exact edges of key shapes by scanning colors along lines."""
import numpy as np
from PIL import Image
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
H,W = im.shape[:2]
r,g,b = im[:,:,0], im[:,:,1], im[:,:,2]

def seg(y, pred, label):
    xs = np.where(pred(y))[0]
    if len(xs)==0: print(f"y={y} {label}: none"); return
    # print runs
    runs=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x==p+1: p=x
        else: runs.append((s,p)); s=p=x
    runs.append((s,p))
    runs = [rn for rn in runs if rn[1]-rn[0]>=1]
    print(f"y={y} {label}: {runs}")

def segv(x, pred, label):
    ys = np.where(pred(x))[0]
    if len(ys)==0: print(f"x={x} {label}: none"); return
    runs=[]; s=ys[0]; p=ys[0]
    for y in ys[1:]:
        if y==p+1: p=y
        else: runs.append((s,p)); s=p=y
    runs.append((s,p))
    print(f"x={x} {label}: {runs}")

white = lambda y: (r[y]>240)&(g[y]>240)&(b[y]>240)
black = lambda y: (r[y]<80)&(g[y]<80)&(b[y]<80)
paleyellow = lambda y: (r[y]>245)&(g[y]>245)&(b[y]>180)&(b[y]<230)

print("--- LT box white border rows (y90,y114) cols 300-600")
seg(90, white, 'white')
seg(114, white, 'white')
print("--- LT box white cols (x340, x540)")
segv(340, white, 'white')
#segv(540, white, 'white')
print("--- concat bar top/bottom (dark border) at x=500")
segv(500, black, 'black')
print("--- concat bar segments at y=138: classify each x")
def cls(c):
    rr,gg,bb=c
    if rr>240 and gg>240 and bb>240: return 'white'
    if rr<90 and gg<90 and bb<90: return 'black'
    if rr>140 and rr<230 and gg<120 and bb<60: return 'orange'
    if rr>200 and gg>200 and bb<120: return 'yellow'
    if gg>200 and rr<200 and bb<160: return 'green'
    if abs(rr-64)<40 and abs(gg-64)<40 and abs(bb-64)<40: return 'gray'
    if rr>180 and gg<120 and bb<120: return 'red'
    if rr>230 and gg>180 and bb>200: return 'pink'
    if abs(rr-222)<40 and abs(gg-184)<40 and abs(bb-135)<45: return 'tan'
    if abs(rr-139)<30 and gg<60 and bb<60: return 'darkred'
    return f"?{rr//32}{gg//32}{bb//32}"
row = im[138]
s = ""
prev = None
for x in range(160, 800):
    c = cls(row[x])
    if c != prev:
        s += f"[{x}:{c}]"
        prev = c
print(s)
