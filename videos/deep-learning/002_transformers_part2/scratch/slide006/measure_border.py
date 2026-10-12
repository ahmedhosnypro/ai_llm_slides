#!/usr/bin/env python3
"""Refine: chrome border strokes + mapping fit for slide_006.jpg."""
from PIL import Image
import numpy as np

p = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(p).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
red = (R - G > 55) & (R - B > 55) & (R > 110)

# vertical strokes: scan columns, count red px within panel interior band y 110..510
colprof = red[110:510, :].sum(axis=0)
cand = [x for x in range(W) if colprof[x] >= 100]
def groups(idxs):
    out, g = [], []
    for i in idxs:
        if g and i == g[-1] + 1: g.append(i)
        else:
            if g: out.append(g)
            g = [i]
    if g: out.append(g)
    return out
def centers(idxs, prof):
    res = []
    for g in groups(idxs):
        ws = np.array([prof[i] for i in g], float)
        c = float((np.array(g) * ws).sum() / ws.sum())
        res.append((round(c,2), g[0], g[-1], int(ws.sum())))
    return res
print("VERT strokes (center,x0,x1,mass):", centers(cand, colprof) if cand else "none")

# horizontal strokes: rows, red px within x 70..890
rowprof = red[:, 70:890].sum(axis=1)
candr = [y for y in range(H) if rowprof[y] >= 100]
print("HORIZ strokes (center,y0,y1,mass):", centers(candr, rowprof) if candr else "none")
