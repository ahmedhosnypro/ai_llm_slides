#!/usr/bin/env python3
"""probe10 — what actually spans between col1 (x282) and col2 (x407)?"""
from PIL import Image
import numpy as np

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)

def runs(m):
    idx = np.where(m)[0]
    if len(idx) == 0: return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v == p+1: p = v
        else: out.append((int(s), int(p))); s = p = v
    out.append((int(s), int(p)))
    return out

beige = (abs(a[:,:,0]-218)<14) & (abs(a[:,:,1]-208)<14) & (abs(a[:,:,2]-196)<14)
nonbg = ~beige

print("== non-beige runs in x285..404, sampled rows y150..375 ==")
for y in range(150, 376, 5):
    rr = runs(nonbg[y, 285:405])
    rr = [(s+285, e+285) for s, e in rr if e-s >= 0]
    if rr and len(rr) < 12:
        print(f"  y{y}: {rr}")

print("== per-column non-beige counts x285..404 (sum over y150..380) ==")
cnt = nonbg[150:380, 285:405].sum(axis=0)
for i in range(0, 120, 4):
    xs = 285+i
    print(f"  x{xs}..{xs+3}: {list(cnt[i:i+4])}")
