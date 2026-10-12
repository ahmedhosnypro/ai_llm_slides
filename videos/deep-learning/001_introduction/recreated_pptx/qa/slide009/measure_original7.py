# stage 7: per-line x-extents + font solve with real TTFs
from PIL import Image, ImageFont
import numpy as np
from collections import Counter

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_009.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[...,0], a[...,1], a[...,2]

def xext(mask, x0,x1,y0,y1,label):
    m = np.zeros((H,W),bool); m[y0:y1,x0:x1]=True
    mm = mask & m
    ys,xs = np.nonzero(mm)
    if len(xs)==0: print(f"  {label}: EMPTY"); return
    print(f"  {label}: x {xs.min()}..{xs.max()} (w={xs.max()-xs.min()+1})  y {ys.min()}..{ys.max()}")

ink = (r<110)&(g<110)&(b<110)
print("== per-line x-extents (black ink) ==")
xext(ink, 152,246,221,234,"PreProc L1 'Pre'")
xext(ink, 152,246,241,257,"PreProc L2 'processing'")
xext(ink, 297,405,219,235,"Cyan L1 'Feature'")
xext(ink, 297,405,238,254,"Cyan L2 'Extraction'")
xext(ink, 444,556,219,235,"Green L1 'Feature'")
xext(ink, 444,556,238,254,"Green L2 'Selection'")
xext(ink, 760,852,219,235,"Lav L1 'Post'")
xext(ink, 760,852,241,257,"Lav L2 'processing'")
xext(ink, 100,190,148,167,"TD L1 'Training'")
xext(ink, 100,190,169,185,"TD L2 'Data'")
xext(ink, 795,875,314,328,"FR L1")
xext(ink, 795,875,331,346,"FR L2")
for i,(x0,x1) in enumerate([(241,328),(386,473),(537,624),(694,781)],1):
    xext(ink, x0,x1,296,309,f"label{i} L1")
    xext(ink, x0,x1,312,325,f"label{i} L2")

# white text of Classification
whitem = (r>200)&(g>200)&(b>200)
xext(whitem, 590,720,225,250,"Classification white text")

# red title: per-letter columns already known; get title ink with red mask columns
red = (r>120)&(r-np.maximum(g,b)>55)
xext(red, 210,730,66,92,"TITLE red band")

# ---- font solve ----
print("\n== font solve (Liberation Sans = Arial metrics) ==")
import glob
cands = {
 "LiberationSans-Bold": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
 "LiberationSans": "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
 "DejaVuSans-Bold": "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
}
import os
for k,v in list(cands.items()):
    if not os.path.exists(v):
        alt = glob.glob("/usr/share/fonts/**/LiberationSans-Bold.ttf", recursive=True) if "Bold" in k else None
        print("  missing:", k, v)
        del cands[k]
print("  available:", list(cands))

def solve(fontpath, text, target_adv, target_cap, sizes):
    best=[]
    for s in sizes:
        f = ImageFont.truetype(fontpath, s)
        adv = f.getlength(text)
        # cap height via 'T' bbox
        bb = f.getbbox("T")
        cap = bb[3]-bb[1]
        best.append((s, round(adv,1), cap))
    return best

T = "The Complete ML Classification Process"
print("\ntitle targets: advance 496 (x220..715), cap 19")
for k,v in cands.items():
    print(" ", k, solve(v, T, 496, 19, range(24,32)))

print("\n'Classification' target adv 112, cap 12:")
for k,v in cands.items():
    if "Bold" in k: print(" ", k, solve(v, "Classification", 112, 12, range(14,20)))

print("\n'processing' target adv ~? (Lav L2):")
for k,v in cands.items():
    if "Bold" in k: print(" ", k, solve(v, "processing", 91, 12, range(14,20)))

print("\n'Feature' target (Cyan L1):")
for k,v in cands.items():
    if "Bold" in k: print(" ", k, solve(v, "Feature", None, 12, range(14,20)))

print("\nlabels 'Predicted' target ~62 cap 10:")
for k,v in cands.items():
    if "Bold" in k: print(" ", k, solve(v, "Predicted", 62, 10, range(11,16)))

print("\n'Training' target ~70 cap 13:")
for k,v in cands.items():
    if "Bold" in k: print(" ", k, solve(v, "Training", 70, 13, range(15,21)))

print("\n'Result'/'Final' (FR lines):")
for k,v in cands.items():
    if "Bold" in k:
        print(" ", k, "Final:", solve(v, "Final", None, 11, range(14,19)), "Result:", solve(v, "Result", None, 11, range(14,19)))
