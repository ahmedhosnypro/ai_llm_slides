#!/usr/bin/env python3
# measure_regions.py — slide_025 frame structural probes (960x540, 1px=1pt)
# Round 1: global band scans for title / magenta boxes / dash / panel / rows /
# output / error / class / blockarrows / callouts / equation boxes / blackbar.
from PIL import Image
import sys

F = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg'
im = Image.open(F).convert('RGB')
W, H = im.size
px = im.load()

def runs_row(y, pred, x0=0, x1=W):
    out = []
    start = None
    for x in range(x0, x1):
        if pred(px[x, y]):
            if start is None: start = x
        else:
            if start is not None:
                out.append((start, x - 1)); start = None
    if start is not None: out.append((start, x1 - 1))
    return out

def runs_col(x, pred, y0=0, y1=H):
    out = []
    start = None
    for y in range(y0, y1):
        if pred(px[x, y]):
            if start is None: start = y
        else:
            if start is not None:
                out.append((start, y - 1)); start = None
    if start is not None: out.append((start, y1 - 1))
    return out

def isred(p):    r,g,b = p; return r > 150 and g < 80 and b < 80
def isdarkred(p):r,g,b = p; return 100 < r < 190 and g < 40 and b < 40
def isbeige(p):  r,g,b = p; return abs(r-218) < 18 and abs(g-208) < 18 and abs(b-196) < 20
def isblack(p):  r,g,b = p; return r < 60 and g < 60 and b < 60
def ismag(p):    r,g,b = p; return r > 200 and g < 120 and b > 170
def iscream(p):  r,g,b = p; return r > 235 and g > 235 and 170 < b < 225

print("== title band (red ink rows x300..660) ==")
for y in range(40, 110):
    rr = runs_row(y, isred, 200, 760)
    if rr:
        tot = sum(b-a+1 for a,b in rr)
        if tot > 8: print(y, rr[:6], 'tot', tot)

print("== magenta boxes (rows 90..135) ==")
for y in range(90, 140):
    rr = runs_row(y, ismag, 40, 940)
    if rr and sum(b-a+1 for a,b in rr) > 20: print(y, rr)

print("== dash line row scan (magenta 990099-ish) ==")
def isdash(p): r,g,b=p; return 120<r<190 and g<60 and 120<b<190
for y in range(100, 130):
    rr = runs_row(y, isdash, 100, 900)
    if rr and sum(b-a+1 for a,b in rr) > 60: print('dashrow', y, 'n', len(rr), 'tot', sum(b-a+1 for a,b in rr))

print("== panel bbox (beige) ==")
ys = [y for y in range(H) if sum(1 for x in range(60, 900, 4) if isbeige(px[x,y])) > 40]
print('beige rows', ys[0] if ys else None, '..', ys[-1] if ys else None)
ymid = (ys[0]+ys[-1])//2 if ys else 250
xs = [x for x in range(W) if isbeige(px[x, ymid])]
print('beige cols at y%d'%ymid, xs[0] if xs else None, '..', xs[-1] if xs else None)

print("== error bar (dark red tall) ==")
def iserr(p): r,g,b=p; return 130<r<185 and g<35 and b<35
cols = [x for x in range(500, 750) if sum(1 for y in range(150, 400) if iserr(px[x,y])) > 80]
print('err cols', cols[0] if cols else None, '..', cols[-1] if cols else None)
if cols:
    xc = (cols[0]+cols[-1])//2
    rr = runs_col(xc, iserr)
    print('err rows at x%d'%xc, rr)

print("== class boxes (pale green) ==")
def isclass(p): r,g,b=p; return 200<r<245 and g>245 and 190<b<230
for x in (660, 680, 700):
    rr = runs_col(x, isclass, 150, 400)
    if rr: print('class col x%d'%x, rr)

print("== black bottom bar ==")
for y in range(500, 540):
    rr = runs_row(y, isblack, 0, W)
    if rr and sum(b-a+1 for a,b in rr) > 400: print(y, rr)

print("== equation boxes (cream) rows 440..520 ==")
for y in range(430, 525, 2):
    rr = runs_row(y, iscream, 40, 940)
    if rr and sum(b-a+1 for a,b in rr) > 50: print(y, rr)
