#!/usr/bin/env python3
"""Closed-loop check: measure ink bboxes in ORIGINAL (scaled x2000/960) vs RENDER (150dpi).
Tolerance 4px (150dpi space) per the equation alignment law."""
from PIL import Image
import numpy as np
from scipy import ndimage
import sys

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide022/render_1.png"
O = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_022.jpg"
S = 2000/960  # frame px -> 150dpi px

orig = np.asarray(Image.open(O).convert('RGB')).astype(int)
rend = np.asarray(Image.open(R).convert('RGB')).astype(int)

def ink_mask(a, lo=150):
    r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
    return (r<lo)&(g<lo) | ((r>120)&(r-g>45)&(r-b>35)) | ((b>90)&(b-r>30)) | ((g>150)&(g-r>40)&(b>150)&(b-r>40))

omi, rmi = ink_mask(orig), ink_mask(rend)

def bbox(mask, x0,y0,x1,y1, scale=1.0):
    sub = mask[int(y0):int(y1), int(x0):int(x1)]
    ys,xs = np.nonzero(sub)
    if len(xs)==0: return None
    return ( (x0+xs.min())*scale, (y0+ys.min())*scale, (x0+xs.max()+1)*scale, (y0+ys.max()+1)*scale )

# regions: name, orig search window (frame px), render search window (150dpi px = frame*S ± margin)
REG = [
 # name           ox0,oy0,ox1,oy1   (original window, frame px)
 ("title",        200, 50, 760, 95),
 ("eq1 X",         80,150, 102,180),
 ("eq1 =1",        99,155, 116,175),
 ("v1 parenL",    110,110, 120,235),
 ("v1 entries",   119,115, 138,232),
 ("v1 parenR",    136,110, 146,235),
 ("eq1 arrow",    172,152, 200,178),
 ("eq1 X2",       212,152, 235,180),
 ("eq1 =2",       230,155, 250,175),
 ("v2 parenL",    243,100, 253,240),
 ("v2 one(red)",  250,100, 272,125),
 ("v2 entries",   251,125, 271,238),
 ("v2 parenR",    268,100, 280,240),
 ("label1",       290,152, 415,182),
 ("eq2 W",        552,150, 580,180),
 ("eq2 =",        574,155, 592,175),
 ("w parenL",     586,100, 597,240),
 ("w b(red)",     595,100, 618,125),
 ("w entries",    595,125, 618,238),
 ("w parenR",     615,100, 626,240),
 ("label2",       660,152, 770,182),
 ("d(X)",          84,280, 132,308),
 ("eq3 =W^TX",    133,278, 230,308),
 ("eq3 w1x1+",    230,283, 285,308),
 ("eq3 w2x2+",    283,283, 337,308),
 ("eq3 dots5",    335,290, 362,306),
 ("eq3 wnxn+",    360,283, 425,308),
 ("eq3 b*1(red)", 424,283, 460,306),
 ("eq3 arrow",    498,283, 526,304),
 ("brace",        538,262, 556,330),
 ("case1",        550,262, 670,286),
 ("case2",        550,284, 676,308),
 ("case3",        550,306, 745,330),
 ("in x1",        245,350, 268,370),
 ("in 1(red)",    246,485, 266,504),
 ("w col w1",     284,352, 310,372),
 ("w col wn",     284,444, 310,462),
 ("w col b",      284,484, 302,502),
 ("sigma circle", 405,402, 448,436),
 ("block",        466,406, 516,436),
 ("red shaft",    440,414, 578,430),
 ("O/P",          578,410, 614,432),
 ("black bar",     30,512, 930,540),
]
print(f"{'region':14s} {'orig (150dpi)':>26s} {'render':>26s} {'dx0':>5s} {'dy0':>5s} {'dx1':>5s} {'dy1':>5s}  verdict")
fails = []
for name, ox0,oy0,ox1,oy1 in REG:
    ob = bbox(omi, ox0,oy0,ox1,oy1, S)
    m = 12
    rx0,ry0,rx1,ry1 = ox0*S-m, oy0*S-m, ox1*S+m, oy1*S+m
    rb = bbox(rmi, rx0,ry0,rx1,ry1, 1.0)
    if ob is None or rb is None:
        print(f"{name:14s} orig={ob} render={rb}  MISSING"); fails.append(name); continue
    d = [rb[i]-ob[i] for i in range(4)]
    ok = all(abs(v) <= 4.0 for v in d)
    if not ok: fails.append(name)
    print(f"{name:14s} {ob[0]:7.1f} {ob[1]:7.1f} {ob[2]:7.1f} {ob[3]:7.1f} {rb[0]:7.1f} {rb[1]:7.1f} {rb[2]:7.1f} {rb[3]:7.1f} {d[0]:+5.1f} {d[1]:+5.1f} {d[2]:+5.1f} {d[3]:+5.1f}  {'OK' if ok else 'FAIL'}")
print("\nFAILS:", fails if fails else "none")
