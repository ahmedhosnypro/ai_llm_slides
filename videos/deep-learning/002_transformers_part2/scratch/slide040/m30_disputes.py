#!/usr/bin/env python3
"""m30: settle w1-vs-m26 disputes with corrected masks + control-anchored slant test."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
lum = (r+g+b)/3.0

print("== A. red-dominant underline scan (mask r-g>35 & r>140 — catches muted red (184,118,125)) ==")
def rowscan(y0,y1,x0,x1,label):
    print(f"-- {label} rows {y0}..{y1} x {x0}..{x1}")
    for y in range(y0,y1):
        m = (r[y,x0:x1]-g[y,x0:x1]>35) & (r[y,x0:x1]>140)
        idx = np.where(m)[0]
        if len(idx)<5: continue
        d = np.diff(idx); gaps = int((d>2).sum())
        seg = im[y, x0+idx[0]:x0+idx[-1]+1]
        print(f"   y={y}: n={len(idx)} span {x0+idx[0]}..{x0+idx[-1]} gaps>2px:{gaps} med {np.median(seg,axis=0).round(0)}")
rowscan(150,164,660,832,"L2 red run 'convert the mean and' (text band ~143..156)")
rowscan(170,190,100,440,"L3 red 'variance...Loss.' (text band ~167..183)")
print()
print("== B. green underline scan under 'learn parameters' (mask g-r>25 & g>100 & g<200) ==")
for y in range(150,166):
    m = (g[y,385:545]-r[y,385:545]>25) & (g[y,385:545]>100) & (g[y,385:545]<200)
    idx = np.where(m)[0]
    if len(idx)<5: continue
    d = np.diff(idx); gaps = int((d>2).sum())
    seg = im[y, 385+idx[0]:385+idx[-1]+1]
    print(f"   y={y}: n={len(idx)} span {385+idx[0]}..{385+idx[-1]} gaps>2px:{gaps} med {np.median(seg,axis=0).round(0)}")
print()
print("== C. control-anchored italic slant (column-profile cross-correlation) ==")
def slant(x0,x1,y0,y1,label,hue=None):
    reg = im[y0:y1, x0:x1]
    rr,gg,bb = reg[:,:,0],reg[:,:,1],reg[:,:,2]
    if hue=='blue': m = (bb-rr>35)&(bb>100)
    elif hue=='red': m = (rr-gg>35)&(rr>140)
    elif hue=='green': m = (gg-rr>25)&(gg>90)
    else: m = lum[y0:y1,x0:x1]<150
    h = m.shape[0]
    top = m[:h//2].sum(axis=0).astype(float)
    bot = m[h//2:].sum(axis=0).astype(float)
    top -= top.mean(); bot -= bot.mean()
    best=(1e18,0)
    for s in range(-6,7):
        if s>=0: a,b2 = top[s:], bot[:len(bot)-s if s else len(bot)]
        else: a,b2 = top[:s], bot[-s:]
        n=min(len(a),len(b2))
        if n<10: continue
        d = float(np.sum((a[:n]-b2[:n])**2))
        if d<best[0]: best=(d,s)
    print(f"   {label:28s} shift(top vs bot) = {best[1]:+d}px  ({'TOP RIGHT of bottom = italic lean' if best[1]<0 else 'top LEFT = backslant' if best[1]>0 else 'vertical = upright'})")
print("  L1 (band 117..135):")
slant(536,586,117,135,"blue 'strictly' (italic control)",'blue')
slant(592,632,117,135,"blue 'Zero' (bold, should be 0)",'blue')
slant(648,670,117,135,"blue 'mean' (disputed)",'blue')
slant(680,700,117,135,"blue 'and' (disputed)",'blue')
slant(778,826,117,135,"blue 'variance,' (disputed)",'blue')
slant(105,530,117,135,"black L1 words (control)",None)
print("  L2 (band 142..160):")
slant(88,380,142,160,"black L2 'Normalization...to' (control)",None)
slant(388,532,142,160,"green 'learn parameters' (disputed)",'green')
slant(535,547,142,160,"gamma (red, disputed)",'red')
slant(663,700,142,160,"red 'conv' (disputed)",'red')
slant(754,830,142,160,"red 'mean and' (disputed)",'red')
print("  L3 (band 167..185):")
slant(104,200,167,185,"red 'variance to' (disputed)",'red')
slant(230,330,167,185,"red 'Minimizes' (disputed bold)",'red')
slant(330,436,167,185,"red 'Loss.' (disputed bold)",'red')
print()
print("== D. eq3 rect edge weights (w1: bottom 2px (131,128,165) vs top 1px (191,189,211)) ==")
for y in list(range(397,403))+list(range(443,450)):
    m = lum[y,164:288]<235
    idx=np.where(m)[0]
    if len(idx)>100:
        seg=im[y,164+idx[0]:164+idx[-1]+1]
        print(f"   y={y}: n={len(idx)} med {np.median(seg,axis=0).round(0)}")
print()
print("== E. highlight fill MODES (w1: panel B0E8B0, intro D8F8D8) ==")
def fillmode(y0,y1,x0,x1,label):
    reg = im[y0:y1,x0:x1].reshape(-1,3)
    # keep only clearly-fill pixels: all channels > 140 and low saturation-to-white
    keep = reg[(reg.min(axis=1)>140)]
    if len(keep)==0: print(f"   {label}: none"); return
    vals, counts = np.unique(keep, axis=0, return_counts=True)
    o = np.argsort(-counts)[:3]
    print(f"   {label}: top modes " + " | ".join(f"{vals[i]} x{counts[i]}" for i in o))
fillmode(228,247,205,420,"panel params green fill")
fillmode(147,156,392,425,"intro learn-params green fill")
fillmode(455,470,213,222,"eq4 gamma green fill")
fillmode(455,470,262,272,"eq4 beta green fill")
