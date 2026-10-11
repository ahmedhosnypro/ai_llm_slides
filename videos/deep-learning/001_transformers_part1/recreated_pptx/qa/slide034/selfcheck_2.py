#!/usr/bin/env python3
"""Self-check round 2 — border-excluding ink windows, proper peach mask."""
from PIL import Image
import numpy as np

ORIG = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg'
REND = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide034/render_1.png'
S = 150/72.0

o = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
r = np.asarray(Image.open(REND).convert('RGB')).astype(int)

def inkbox(a, x0, x1, y0, y1, cond):
    sub = cond(a[y0:y1, x0:x1])
    ys, xs = np.where(sub)
    if len(xs) == 0: return None
    return (xs.min()+x0, xs.max()+x0, ys.min()+y0, ys.max()+y0)

def dark(a):  R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]; return (R<150)&(G<150)&(B<150)
def red(a):   R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]; return (R>140)&((R-G)>60)&((R-B)>60)
def blue(a):  R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]; return (B>120)&((B-R)>40)&(R<170)
def green(a): R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]; return ((G-R)>30)&((G-B)>25)&(G>100)
def yellow(a):R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]; return (R>200)&(G>190)&(B<160)
def orange(a):R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]; return (R>200)&(G>110)&(G<215)&(B<140)
def peach(a): R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]; return (R>235)&(G>210)&(G<245)&(B>180)&(B<235)&((R-B)>18)

def cmp(name, obox, rbox):
    if obox is None or rbox is None:
        print(f"{name:26s} MISSING orig={obox} rend={rbox}"); return
    dx = rbox[0]/S - obox[0]; dy = rbox[2]/S - obox[2]
    dw = (rbox[1]-rbox[0])/S - (obox[1]-obox[0]); dh = (rbox[3]-rbox[2])/S - (obox[3]-obox[2])
    flag = "OK " if max(abs(dx),abs(dy),abs(dw),abs(dh)) <= 6 else ">>>"
    print(f"{flag}{name:23s} d(x,y,w,h)=({dx:+5.1f},{dy:+5.1f},{dw:+5.1f},{dh:+5.1f})  orig={obox} rend_px={rbox}")

def add(name, cond, x0,x1,y0,y1, inset=0):
    ox0,ox1,oy0,oy1 = x0+inset,x1-inset,y0+inset,y1-inset
    m=6
    rx0,rx1,ry0,ry1 = int(x0*S)-m, int(x1*S)+m, int(y0*S)-m, int(y1*S)+m
    obox = inkbox(o, ox0,ox1,oy0,oy1, cond)
    rbox = inkbox(r, rx0,rx1,ry0,ry1, cond)
    cmp(name, obox, rbox)

add("title", dark, 300,700,50,78)
add("subtitle.dark", dark, 340,530,76,102)          # "Vector Dimension" black-on-yellow
add("subtitle.red1", red, 200,350,76,102)           # "(Embedding"
add("subtitle.hl1", yellow, 335,530,72,103)
add("subtitle.hl2", yellow, 550,775,72,103)
add("concept.boxborder", green, 40,400,96,275)
add("concept.eq.ink", dark, 74,190,118,155, inset=4)   # inside eq box, excl border
add("concept.xi", red, 305,352,112,168)
add("concept.1xd", green, 338,370,150,172)
add("concept.eqsmall.ink", dark, 233,350,180,203, inset=4)
add("annot.line1", blue, 60,300,216,239)
add("annot.line2.blue", blue, 60,268,240,262)
add("annot.line2.red", red, 266,375,237,258)
add("panel", peach, 40,880,268,538)
add("embbox.border", red, 46,136,276,353)
add("embbox.1xd", green, 86,128,316,344)
add("softmax.label", red, 166,250,294,322)
add("frac.wij", dark, 252,303,302,321, inset=2)
add("frac.bar", dark, 300,390,306,315, inset=2)
add("frac.num", dark, 312,380,284,306, inset=2)
add("frac.den", dark, 300,392,315,341, inset=2)
add("warning.text", blue, 400,868,286,312)
for i,(hx0,hx1) in enumerate([(125,175),(390,440),(660,725)]):
    add(f"col{i+1}.header", green, hx0,hx1,315,356)
for i,(bx0,bx1) in enumerate([(128,175),(393,443),(661,711)]):
    add(f"col{i+1}.inparen", red, bx0,bx1,355,492)
for i,(px0,px1) in enumerate([(245,315),(513,583),(781,851)]):
    add(f"col{i+1}.outparen", blue, px0,px1,360,485)
for i,(ax0,ax1) in enumerate([(172,250),(440,518),(708,786)]):
    add(f"col{i+1}.arrow", red, ax0,ax1,419,443)
    add(f"col{i+1}.slabel", orange, ax0,ax1,397,421)
    add(f"col{i+1}.caption.w", dark, 125+i*270, 178+i*270, 492,518)
    add(f"col{i+1}.caption.txt", dark, 180+i*270, 320+i*270, 492,518)
