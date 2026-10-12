#!/usr/bin/env python3
"""Closed-loop v3: union-ink bbox per window. Strict mask for render; dual mask for orig
(washed thin strokes get the light mask). Tolerance 4px @150dpi."""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide022/render_1.png"
O = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_022.jpg"
S = 2000/960.0
TOL = 4.0

orig = np.asarray(Image.open(O).convert('RGB')).astype(int)
rend = np.asarray(Image.open(R).convert('RGB')).astype(int)

def mask_strict(a):
    r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
    return ((r<150)&(g<150)) | ((r>120)&(r-g>45)&(r-b>35)) | ((b>90)&(b-r>30)) | ((g>150)&(g-r>40)&(b>150)&(b-r>40))
def mask_light(a):  # catches washed thin strokes (excludes bg 232 and white)
    r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
    return ((r<205)&(g<205)&(b<215)) | ((r>120)&(r-g>35)&(r-b>25)) | ((b>95)&(b-r>25)) | ((g>150)&(g-r>30)&(b>150)&(b-r>30))

omi_s, omi_l = mask_strict(orig), mask_light(orig)
rmi = mask_strict(rend)

def union(mask, x0,y0,x1,y1, scale=1.0):
    sub = mask[int(y0):int(y1), int(x0):int(x1)]
    ys,xs = np.nonzero(sub)
    if len(xs)==0: return None
    return ((x0+xs.min())*scale,(y0+ys.min())*scale,(x0+xs.max()+1)*scale,(y0+ys.max()+1)*scale)

# name, orig window (frame px), mask, render pad (frame px around same window scaled)
REG = [
 ("title",      (222,54,724,90),   "L", 4),
 ("eq1 X",      (84,156,100,175),  "S", 4),
 ("eq1 =1",     (100,159,114,171), "S", 4),
 ("v1 parenL",  (113,118,120,230), "L", 4),
 ("v1 x1",      (120,118,137,136), "S", 4),
 ("v1 x2",      (120,143,137,157), "S", 4),
 ("v1 dots1",   (120,172,137,181), "L", 4),
 ("v1 dots2",   (120,193,137,202), "L", 4),
 ("v1 xn",      (120,207,137,226), "S", 4),
 ("v1 parenR",  (137,118,145,230), "L", 4),
 ("eq1 arr",    (176,158,196,174), "S", 4),
 ("eq1 X2",     (216,156,233,175), "S", 4),
 ("eq1 =2",     (232,159,248,171), "S", 4),
 ("v2 parenL",  (246,102,252,238), "L", 4),
 ("v2 one",     (255,104,267,122), "S", 4),
 ("v2 x1",      (252,129,270,148), "S", 4),
 ("v2 x2",      (252,152,270,171), "S", 4),
 ("v2 dots1",   (252,182,270,191), "S", 4),
 ("v2 dots2",   (252,203,270,212), "S", 4),
 ("v2 xn",      (252,218,270,236), "S", 4),
 ("v2 parenR",  (270,102,278,238), "L", 4),
 ("label1",     (295,156,410,178), "S", 4),
 ("eq2 W",      (557,156,577,176), "S", 4),
 ("eq2 =",      (576,159,591,171), "S", 4),
 ("w parenL",   (590,101,596,238), "L", 4),
 ("w b",        (600,103,614,123), "S", 4),
 ("w w1",       (596,129,617,148), "S", 4),
 ("w w2",       (596,152,617,171), "S", 4),
 ("w dots1",    (596,182,612,191), "S", 4),
 ("w dots2",    (596,203,612,212), "S", 4),
 ("w wn",       (596,218,617,236), "S", 4),
 ("w parenR",   (616,100,623,238), "L", 4),
 ("label2",     (666,156,765,178), "S", 4),
 ("d(X) d(",    (85,283,104,304),  "S", 4),
 ("d(X) X(red)",(106,283,124,306), "S", 4),
 ("d(X) )",     (125,284,131,304), "S", 4),
 ("eq3 =1",     (135,289,149,299), "S", 4),
 ("eq3 WT",     (154,280,183,304), "S", 4),
 ("eq3 X",      (190,284,208,304), "S", 4),
 ("eq3 =2",     (213,289,227,299), "S", 4),
 ("eq3 w1x1",   (231,288,253,308), "S", 4),
 ("eq3 x1",     (254,288,271,308), "S", 4),
 ("eq3 +1",     (271,287,284,302), "S", 4),
 ("eq3 w2x2",   (284,287,300,308), "S", 4),
 ("eq3 x2",     (306,288,324,308), "S", 4),
 ("eq3 +2",     (323,287,336,302), "S", 4),
 ("eq3 dots5",  (336,295,361,304), "S", 4),
 ("eq3 +3",     (361,287,374,302), "S", 4),
 ("eq3 wnxn",   (374,288,395,308), "S", 4),
 ("eq3 xn",     (395,287,413,308), "S", 4),
 ("eq3 +4",     (413,287,426,302), "S", 4),
 ("eq3 b*1",    (425,284,458,304), "S", 4),
 ("eq3 arr",    (500,285,524,301), "S", 4),
 ("brace",      (541,266,559,324), "L", 4),
 ("case1 >0",   (552,265,576,284), "S", 4),
 ("case1 arr",  (584,268,603,282), "S", 4),
 ("case1 word", (612,265,668,284), "S", 4),
 ("case2 <0",   (552,287,576,306), "S", 4),
 ("case2 arr",  (584,290,603,304), "S", 4),
 ("case2 word", (612,287,674,306), "S", 4),
 ("case3 =0",   (552,309,576,328), "S", 4),
 ("case3 arr",  (584,312,603,326), "S", 4),
 ("case3 word", (612,309,743,328), "S", 4),
 ("in x1",      (249,354,265,369), "S", 4),
 ("in x2",      (249,376,266,391), "S", 4),
 ("in x3",      (249,399,266,414), "S", 4),
 ("in dots1",   (249,427,263,434), "S", 4),
 ("in dots2",   (249,449,263,457), "S", 4),
 ("in xn",      (249,466,267,482), "S", 4),
 ("in 1",       (250,487,259,502), "S", 4),
 ("wt w1",      (287,355,307,370), "S", 4),
 ("wt w2",      (287,373,307,388), "S", 4),
 ("wt w3",      (287,395,307,410), "S", 4),
 ("wt wn",      (287,446,308,461), "S", 4),
 ("wt b",       (287,485,299,501), "S", 4),
 ("sigma",      (414,408,434,432), "S", 6),
 ("O/P",        (581,413,611,430), "S", 4),
 ("callout L1", (646,405,801,424), "S", 4),
 ("callout L2", (681,423,766,441), "S", 4),
 ("blackbar",   (36,516,924,540),  "S", 6),
]
print(f"{'region':12s} | {'orig bbox (frame pt)':>26s} | {'render bbox (frame pt)':>26s} | {'dL':>5s} {'dT':>5s} {'dR':>5s} {'dB':>5s} | verdict")
fails=[]
for name,(wx0,wy0,wx1,wy1),mk,pad in REG:
    om = omi_l if mk=="L" else omi_s
    ob = union(om, wx0,wy0,wx1,wy1, 1.0)  # frame px == frame pt
    m = pad*S
    rb = union(rmi, wx0*S-m, wy0*S-m, wx1*S+m, wy1*S+m, 1/S)
    if ob is None or rb is None:
        print(f"{name:12s} | orig={'None' if ob is None else 'ok':>4s} render={'None' if rb is None else 'ok':>4s} | MISSING"); fails.append(name); continue
    d = [rb[i]-ob[i] for i in range(4)]
    ok = all(abs(v)<=TOL for v in d)
    if not ok: fails.append(name)
    print(f"{name:12s} | {ob[0]:6.1f} {ob[1]:6.1f} {ob[2]:6.1f} {ob[3]:6.1f} | {rb[0]:6.1f} {rb[1]:6.1f} {rb[2]:6.1f} {rb[3]:6.1f} | {d[0]:+5.1f} {d[1]:+5.1f} {d[2]:+5.1f} {d[3]:+5.1f} | {'OK' if ok else 'FAIL'}")
print("\nFAILS:", fails if fails else "none")
