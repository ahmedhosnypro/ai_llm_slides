#!/usr/bin/env python3
"""Head orientation check: for each head, row-width profile of orange ink.
Down-pointing triangle = widest at TOP, narrowing downward (monotone decreasing).
Up-pointing = widest at BOTTOM. Compare 028's certified heads (ground truth for the
family convention) vs 029's new heads k=8,9,10."""
import numpy as np
from PIL import Image
BASE="/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
def profile(img, fxc, fyc, tag):
    x0,x1,y0,y1 = int(fxc)-9, int(fxc)+10, int(fyc)-9, int(fyc)+10
    sub = img[y0:y1, x0:x1]
    m = (sub[:,:,0]>170)&((sub[:,:,0]-sub[:,:,1])>55)&(sub[:,:,1]<170)&(sub[:,:,2]<110)
    widths = m.sum(axis=1)
    rows = [(i+y0, int(w)) for i,w in enumerate(widths) if w>0]
    if not rows: print(f" {tag}: no ink"); return
    top = rows[0]; bot = rows[-1]
    maxrow = max(rows, key=lambda r: r[1])
    print(f" {tag}: top row {top[0]} w{top[1]} | widest row {maxrow[0]} w{maxrow[1]} | bottom row {bot[0]} w{bot[1]}"
          f"  => {'DOWN-pointing' if maxrow[0] <= (top[0]+bot[0])/2 else 'UP-pointing'}")
A = np.asarray(Image.open(f"{BASE}/unique_slides/slide_028.jpg").convert("RGB")).astype(int)
B = np.asarray(Image.open(f"{BASE}/unique_slides/slide_029.jpg").convert("RGB")).astype(int)
def f(sx,sy): return (18.63+0.96123*sx, 0.95556*sy)
print("== 028 certified heads (family convention ground truth) ==")
for k,(sx,sy) in {0:(776.4,188.4),4:(385.7,185.1),5:(357.0,292.0),6:(385.5,405.2),7:(470.3,493.2)}.items():
    fx,fy = f(sx,sy); profile(A,fx,fy,f"028 head{k}")
print("== 029 new heads ==")
for k,(sx,sy) in {8:(576.2,522.7),9:(689.1,493.4),10:(777.0,408.7)}.items():
    fx,fy = f(sx,sy); profile(B,fx,fy,f"029 head{k}")
print("== 029 inherited heads (control) ==")
for k,(sx,sy) in {4:(385.7,185.1),7:(470.3,493.2)}.items():
    fx,fy = f(sx,sy); profile(B,fx,fy,f"029 head{k}")
