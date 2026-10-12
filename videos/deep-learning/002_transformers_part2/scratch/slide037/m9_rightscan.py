#!/usr/bin/env python3
"""Right panel vertical strips (encoder/decoder column centers) + exact fill modes per band."""
from PIL import Image
from collections import Counter
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg").convert("RGB")
px = img.load()
AX, SX = 17.101, 0.962329
BY, SY = -0.224, 0.96053
def my(fy): return round((fy-BY)/SY, 1)
def mx(fx): return round((fx-AX)/SX, 1)
out = {}

def scan_col(x, y0, y1, label, minrun=2):
    runs = []
    prev = None; start = y0
    for y in range(y0, y1):
        p = px[x, y]
        key = (p[0]//12*12, p[1]//12*12, p[2]//12*12)
        if key != prev:
            if prev is not None and y-start >= minrun:
                runs.append((start, y-1, prev, my(start), my(y-1)))
            prev = key; start = y
    runs.append((start, y1-1, prev, my(start), my(y1-1)))
    out[label] = [[a, b, list(c)] for a, b, c, _, _ in runs if b-a >= minrun-1]

# encoder column center in frame coords: slide 699 -> fx = 17.101+0.962329*699 = 689.9
scan_col(690, 100, 519, "enc_col_x690")
# decoder column center: slide 808 -> fx = 794.8
scan_col(795, 100, 519, "dec_col_x795")
# also x=660 (left part of encoder container), x=845 (right decoder)
scan_col(660, 100, 519, "enc_x660")
scan_col(845, 100, 519, "dec_x845")

# panel fill split: where does peach end / green begin? scan row y=150 (slide 156)
row = []
prev=None; start=530
for x in range(530, 960):
    p = px[x,150]
    key=(p[0]//12*12,p[1]//12*12,p[2]//12*12)
    if key!=prev:
        if prev is not None and x-start>=2: row.append((start,x-1,list(prev),mx(start),mx(x-1)))
        prev=key; start=x
row.append((start,959,list(prev),mx(start),mx(959)))
out["row150_runs"] = [[a,b,c] for a,b,c,_,_ in row if b-a>=1]
# row y=480 (slide 501) lower area
row = []
prev=None; start=530
for x in range(530, 960):
    p = px[x,480]
    key=(p[0]//12*12,p[1]//12*12,p[2]//12*12)
    if key!=prev:
        if prev is not None and x-start>=2: row.append((start,x-1,list(prev),mx(start),mx(x-1)))
        prev=key; start=x
row.append((start,959,list(prev),mx(start),mx(959)))
out["row480_runs"] = [[a,b,c] for a,b,c,_,_ in row if b-a>=1]

print(json.dumps(out, indent=0, default=str))
