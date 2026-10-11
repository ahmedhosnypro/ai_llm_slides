import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg").convert("RGB")).astype(int)

def runs(axis_vals, label, tol=16, minrun=2):
    print(f"--- {label} ---")
    vals = [tuple(int(v) for v in px) for px in axis_vals]
    start = 0
    cur = list(vals[0])
    out = []
    for i in range(1, len(vals)):
        if abs(vals[i][0]-cur[0])>tol or abs(vals[i][1]-cur[1])>tol or abs(vals[i][2]-cur[2])>tol:
            out.append((start, i-1, tuple(cur)))
            start = i; cur = list(vals[i])
        else:
            for j in range(3): cur[j] = int(cur[j]*0.85 + vals[i][j]*0.15)
    out.append((start, len(vals)-1, tuple(cur)))
    for s,e,c in out:
        if e-s >= minrun:
            name = ""
            cr,cg,cb = c
            if abs(cr-234)<14 and abs(cg-192)<14 and abs(cb-143)<16: name="TAN"
            elif abs(cr-232)<12 and abs(cg-208)<12 and abs(cb-184)<12: name="ENCBROWN"
            elif abs(cr-200)<14 and abs(cg-232)<12 and abs(cb-192)<14: name="DECGREEN"
            elif abs(cr-255)<16 and abs(cg-248)<14 and abs(cb-220)<20: name="PALEYEL"
            elif abs(cr-255)<16 and abs(cg-249)<12 and abs(cb-196)<16: name="SCALEYEL"
            elif abs(cr-197)<16 and abs(cg-202)<16 and abs(cb-233)<16: name="LAVENDER"
            elif abs(cr-248)<14 and abs(cg-187)<16 and abs(cb-208)<16: name="PINK"
            elif abs(cr-200)<14 and abs(cg-230)<12 and abs(cb-201)<14: name="SOFTGRN"
            elif abs(cr-222)<20 and abs(cg-146)<20 and abs(cb-132)<20: name="SALMON"
            elif abs(cr-179)<20 and abs(cg-157)<20 and abs(cb-219)<20: name="PURPLE"
            elif abs(cr-123)<26 and abs(cg-79)<26 and abs(cb-160)<26: name="DKPURPLE"
            elif abs(cr-168)<16 and abs(cg-168)<16 and abs(cb-168)<16: name="GRAY"
            elif abs(cr-200)<14 and abs(cg-154)<14 and abs(cb-106)<16: name="BROWN"
            elif abs(cr-139)<20 and abs(cg-74)<20 and abs(cb-74)<20: name="MAROON"
            elif abs(cr-168)<18 and abs(cg-232)<14 and abs(cb-168)<18: name="LTGREEN"
            elif cr>235 and cg>235 and cb>235: name="WHITE"
            elif cr>230 and 225<cg<250 and 160<cb<215: name="YELHL"
            elif cr>170 and cg<70 and cb<70: name="RED"
            elif cr<80 and cg>85 and cg<130 and cb<80: name="DKGRN"
            elif cr<80 and 130<cg<200 and cb<80: name="GRN"
            elif cr<70 and cg<70 and cb<70: name="BLACK"
            elif abs(cr-232)<10 and abs(cg-233)<10 and abs(cb-231)<10: name="PANELGRAY"
            print(f"  {s:4d}..{e:4d} ({e-s+1:3d}px) rgb{c} {name}")

for x in (110, 405, 440, 470):
    runs(im[:, x, :], f"col x={x}")
for y in (300, 360, 430, 465):
    runs(im[y, :, :], f"row y={y}")
