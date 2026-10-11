#!/usr/bin/env python3
"""Self-check attempt 1 — closed-loop ink-bbox comparison, render (150dpi, 2000x1125)
vs original frame (960x540, 1px=1pt; scale 150/72 = 2.08333). Tolerance ~4px @150dpi.
Banks per-element dx/dy/dw/dh in pt units (render_px/2.08333 - orig_px)."""
from PIL import Image
import numpy as np

ORIG = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_034.jpg'
REND = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide034/render_1.png'
S = 150/72.0

o = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
r = np.asarray(Image.open(REND).convert('RGB')).astype(int)
print("render size:", r.shape[1], "x", r.shape[0], "(expect ~2000x1125)")

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
def orange(a):R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]; return (R>200)&(G>110)&(G<210)&(B<130)
def paleyellow(a): R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]; return (R>235)&(G>235)&(B<235)&((R-B)>25)&((R-B)<110)

def cmp(name, obox, rbox):
    if obox is None or rbox is None:
        print(f"{name:26s} MISSING orig={obox} rend={rbox}"); return
    dx = rbox[0]/S - obox[0]; dy = rbox[2]/S - obox[2]
    dw = (rbox[1]-rbox[0])/S - (obox[1]-obox[0]); dh = (rbox[3]-rbox[2])/S - (obox[3]-obox[2])
    flag = "OK " if max(abs(dx),abs(dy),abs(dw),abs(dh)) <= 6 else ">>>"
    print(f"{flag}{name:23s} d(x,y,w,h)=({dx:+5.1f},{dy:+5.1f},{dw:+5.1f},{dh:+5.1f})  orig={obox} rend_px={rbox}")

# scale render crop windows back from orig px windows
def w(x0,x1,y0,y1):
    m=6
    return (int(x0*S)-m, int(x1*S)+m, int(y0*S)-m, int(y1*S)+m)

checks = []
def add(name, cond, x0,x1,y0,y1, use="orig_window"):
    ox0,ox1,oy0,oy1 = x0,x1,y0,y1
    rx0,rx1,ry0,ry1 = w(x0,x1,y0,y1)
    obox = inkbox(o, ox0,ox1,oy0,oy1, cond)
    rbox = inkbox(r, rx0,rx1,ry0,ry1, cond)
    cmp(name, obox, rbox)

add("title", dark, 300,700,50,78)
add("subtitle", dark, 200,830,76,102)
add("subtitle.hl1", yellow, 340,530,74,103)
add("subtitle.hl2", yellow, 550,770,74,103)
add("concept.boxborder", green, 40,400,96,275)
add("concept.eqbox.ink", dark, 70,200,112,160)
add("concept.xi", red, 300,350,110,168)
add("concept.1xd", green, 332,370,148,172)
add("concept.dup", green, 55,100,170,210)
add("concept.uparrow", green, 200,230,170,212)
add("concept.eqsmall.ink", dark, 235,310,175,210)
add("annot.line1", blue, 60,300,215,240)
add("annot.line2", blue, 60,300,239,262)
add("annot.red", red, 265,375,236,258)
add("panel", paleyellow, 40,880,270,535)
add("embbox.border", red, 45,140,275,355)
add("embbox.xi", red, 55,92,283,325)
add("embbox.1xd", green, 88,126,318,342)
add("softmax.label", red, 168,248,295,322)
add("frac.wij", dark, 252,306,300,322)
add("frac.num", dark, 312,380,283,308)
add("frac.den", dark, 300,392,314,342)
add("warning.text", blue, 392,870,286,310)
for i,(hx0,hx1) in enumerate([(125,175),(390,440),(660,725)]):
    add(f"col{i+1}.header", green, hx0,hx1,315,356)
for i,(bx0,bx1) in enumerate([(128,175),(393,443),(661,711)]):
    add(f"col{i+1}.inparen", red, bx0,bx1,355,492)
    add(f"col{i+1}.inbox.fill", paleyellow, bx0+4,bx1-4,362,482)
for i,(px0,px1) in enumerate([(245,315),(513,583),(781,851)]):
    add(f"col{i+1}.outparen", blue, px0,px1,360,485)
for i,(ax0,ax1) in enumerate([(172,250),(440,518),(708,786)]):
    add(f"col{i+1}.arrow", red, ax0,ax1,418,442)
    add(f"col{i+1}.slabel", orange, ax0,ax1,398,422)
    add(f"col{i+1}.caption", dark, 120+(i*270), 340+(i*270), 478,518)
