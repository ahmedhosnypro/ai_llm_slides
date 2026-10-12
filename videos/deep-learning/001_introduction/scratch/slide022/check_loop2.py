#!/usr/bin/env python3
"""Closed-loop check v2: tight windows, nearest-component matching, bbox+centroid deltas.
Tolerance 4px (150dpi) for solid elements; centroid-based for thin washed ones."""
from PIL import Image
import numpy as np
from scipy import ndimage

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide022/render_1.png"
O = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_022.jpg"
S = 2000/960.0
TOL = 4.0

orig = np.asarray(Image.open(O).convert('RGB')).astype(int)
rend = np.asarray(Image.open(R).convert('RGB')).astype(int)

def ink_mask(a):
    r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
    return ((r<150)&(g<150)) | ((r>120)&(r-g>45)&(r-b>35)) | ((b>90)&(b-r>30)) | ((g>150)&(g-r>40)&(b>150)&(b-r>40))
omi, rmi = ink_mask(orig), ink_mask(rend)

def comps_in(mask, x0,y0,x1,y1, scale):
    sub = mask[int(y0):int(y1), int(x0):int(x1)]
    lab,n = ndimage.label(sub, structure=np.ones((3,3)))
    out=[]
    for i in range(1,n+1):
        ys,xs = np.nonzero(lab==i)
        if len(xs) < 4: continue
        out.append(((x0+xs.min())*scale,(y0+ys.min())*scale,(x0+xs.max()+1)*scale,(y0+ys.max()+1)*scale,
                    (x0+xs.mean())*scale,(y0+ys.mean())*scale, len(xs)))
    return out

def nearest(cl, ref_cx, ref_cy):
    if not cl: return None
    return min(cl, key=lambda c:(c[4]-ref_cx)**2+(c[5]-ref_cy)**2)

# (name, orig win frame px, expected center frame px (cx,cy), mode)  mode: bbox|centroid
REG = [
 ("title",      (210,52,750,90),   (473,71),  "bbox"),
 ("eq1 X",      (83,155,101,176),  (92,165),  "bbox"),
 ("eq1 =1",     (99,158,115,173),  (107,165), "bbox"),
 ("v1 parenL",  (112,115,121,232), (116.5,172),"centroid"),
 ("v1 x1",      (119,117,138,136), (128,126), "bbox"),
 ("v1 x2",      (119,142,138,158), (128,150), "bbox"),
 ("v1 dots1",   (119,171,138,183), (127,176), "bbox"),
 ("v1 dots2",   (119,192,138,204), (127,197), "bbox"),
 ("v1 xn",      (119,206,138,226), (128,215), "bbox"),
 ("v1 parenR",  (136,115,146,232), (139.5,172),"centroid"),
 ("eq1 arr",    (175,156,198,175), (186,165), "bbox"),
 ("eq1 X2",     (214,155,234,176), (224,165), "bbox"),
 ("eq1 =2",     (231,158,249,173), (240,165), "bbox"),
 ("v2 parenL",  (245,100,254,240), (249,170), "centroid"),
 ("v2 one",     (251,102,268,124), (261,113), "bbox"),
 ("v2 x1",      (251,128,270,148), (260,138), "bbox"),
 ("v2 x2",      (251,151,270,172), (260,162), "bbox"),
 ("v2 dots1",   (251,181,270,192), (259,186), "bbox"),
 ("v2 dots2",   (251,202,270,213), (259,207), "bbox"),
 ("v2 xn",      (251,217,270,236), (260,227), "bbox"),
 ("v2 parenR",  (269,100,279,240), (272.5,170),"centroid"),
 ("label1",     (294,155,411,180), (352,166), "bbox"),
 ("eq2 W",      (555,155,578,178), (567,166), "bbox"),
 ("eq2 =",      (575,158,592,173), (583,165), "bbox"),
 ("w parenL",   (589,100,597,240), (593,170), "centroid"),
 ("w b",        (595,102,615,124), (607,113), "bbox"),
 ("w w1",       (595,128,618,148), (606,138), "bbox"),
 ("w w2",       (595,151,618,172), (606,162), "bbox"),
 ("w dots1",    (595,181,614,192), (603,187), "bbox"),
 ("w dots2",    (595,202,614,213), (603,207), "bbox"),
 ("w wn",       (595,217,618,236), (606,227), "bbox"),
 ("w parenR",   (616,100,624,240), (619,170), "centroid"),
 ("label2",     (664,155,766,180), (715,166), "bbox"),
 ("d(X) d(",    (84,282,105,306),  (93,294),  "bbox"),
 ("d(X) X(red)",(105,282,124,307), (115,294), "bbox"),
 ("d(X) )",     (124,283,131,305), (127,294), "bbox"),
 ("eq3 =1",     (134,288,150,300), (142,294), "bbox"),
 ("eq3 WT",     (153,278,184,305), (168,293), "bbox"),
 ("eq3 X",      (189,283,209,305), (199,294), "bbox"),
 ("eq3 =2",     (212,288,228,300), (220,294), "bbox"),
 ("eq3 w1x1",   (230,287,254,308), (242,297), "bbox"),
 ("eq3 x1",     (253,287,272,308), (261,297), "bbox"),
 ("eq3 +1",     (270,286,284,302), (277,294), "bbox"),
 ("eq3 w2x2",   (283,287,300,308), (291,297), "bbox"),
 ("eq3 x2",     (305,287,324,308), (312,297), "bbox"),
 ("eq3 +2",     (322,286,336,302), (329,294), "bbox"),
 ("eq3 dots5",  (335,294,361,304), (348,299), "bbox"),
 ("eq3 +3",     (360,286,374,302), (367,294), "bbox"),
 ("eq3 wnxn",   (373,287,395,308), (384,297), "bbox"),
 ("eq3 xn",     (394,286,413,308), (404,297), "bbox"),
 ("eq3 +4",     (412,286,426,302), (419,294), "bbox"),
 ("eq3 b*1",    (424,283,459,305), (441,294), "bbox"),
 ("eq3 arr",    (499,284,525,302), (512,293), "bbox"),
 ("brace",      (540,264,560,326), (550,295), "centroid"),
 ("case1 >0",   (551,264,577,285), (564,274), "bbox"),
 ("case1 arr",  (583,267,604,283), (593,275), "bbox"),
 ("case1 word", (611,264,670,285), (640,274), "bbox"),
 ("case2 <0",   (551,286,577,307), (564,296), "bbox"),
 ("case2 word", (611,286,676,307), (643,296), "bbox"),
 ("case3 =0",   (551,308,577,329), (564,318), "bbox"),
 ("case3 word", (611,308,745,329), (677,318), "bbox"),
 ("in x1",      (247,352,266,370), (256,361), "bbox"),
 ("in x2",      (247,375,266,391), (256,383), "bbox"),
 ("in x3",      (247,397,266,414), (256,405), "bbox"),
 ("in dots1",   (247,426,264,435), (255,430), "bbox"),
 ("in dots2",   (247,448,264,457), (255,453), "bbox"),
 ("in xn",      (247,465,268,483), (257,474), "bbox"),
 ("in 1",       (249,486,260,503), (254,494), "bbox"),
 ("wt w1",      (286,354,308,371), (296,362), "bbox"),
 ("wt w2",      (286,373,308,389), (296,380), "bbox"),
 ("wt w3",      (286,395,308,411), (296,402), "bbox"),
 ("wt wn",      (286,446,308,462), (296,453), "bbox"),
 ("wt b",       (286,485,300,501), (292,493), "bbox"),
 ("sigma",      (412,407,436,433), (423,420), "bbox"),
 ("block",      (468,408,515,435), (491,421), "centroid"),
 ("O/P",        (580,412,612,431), (596,421), "bbox"),
 ("callout L1", (645,404,802,425), (723,414), "bbox"),
 ("callout L2", (680,422,767,442), (723,431), "bbox"),
 ("blackbar",   (30,514,930,541),  (480,528), "bbox"),
]
print(f"{'region':12s} | {'orig bbox(cFramePt)':>24s} | {'render bbox':>24s} | {'dL':>5s} {'dT':>5s} {'dR':>5s} {'dB':>5s} | verdict")
fails=[]
for name,(wx0,wy0,wx1,wy1),(cx,cy),mode in REG:
    oc = comps_in(omi, wx0,wy0,wx1,wy1, S)
    ob = nearest(oc, cx*S, cy*S)
    # render window: expected placement +- 8 frame px, in render px
    m = 8
    rc = comps_in(rmi, (wx0*S if mode!="bbox" else cx*S-14), (wy0*S if mode!="bbox" else cy*S-14),
                  (wx1*S if mode!="bbox" else cx*S+14), (wy1*S if mode!="bbox" else cy*S+14), 1.0)
    rb = nearest(rc, cx*S, cy*S)
    if ob is None or rb is None:
        print(f"{name:12s} | orig={ob is not None} render={rb is not None} | MISSING"); fails.append(name); continue
    if mode=="centroid":
        dx, dy = rb[4]-ob[4], rb[5]-ob[5]
        ok = abs(dx)<=TOL and abs(dy)<=TOL
        d = (dx,dy,None,None)
        print(f"{name:12s} | c=({ob[4]:6.1f},{ob[5]:6.1f}) | c=({rb[4]:6.1f},{rb[5]:6.1f}) | {dx:+5.1f} {dy:+5.1f}          | {'OK' if ok else 'FAIL'}")
    else:
        d = [rb[i]-ob[i] for i in range(4)]
        ok = all(abs(v)<=TOL for v in d)
        print(f"{name:12s} | {ob[0]:6.1f} {ob[1]:6.1f} {ob[2]:6.1f} {ob[3]:6.1f} | {rb[0]:6.1f} {rb[1]:6.1f} {rb[2]:6.1f} {rb[3]:6.1f} | {d[0]:+5.1f} {d[1]:+5.1f} {d[2]:+5.1f} {d[3]:+5.1f} | {'OK' if ok else 'FAIL'}")
    if not ok: fails.append(name)
print("\nFAILS:", fails if fails else "none")
