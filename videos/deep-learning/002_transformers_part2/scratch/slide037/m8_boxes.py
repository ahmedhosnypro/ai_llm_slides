#!/usr/bin/env python3
"""Batch 2: exact mode colors + bboxes of inset elements on the ORIGINAL frame."""
from PIL import Image
from collections import Counter
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg").convert("RGB")
px = img.load()
AX, SX = 17.101, 0.962329
BY, SY = -0.224, 0.96053
def mx(fx): return round((fx-AX)/SX, 1)
def my(fy): return round((fy-BY)/SY, 1)
out = {}

def bbox_of(pred, x0,y0,x1,y1):
    xs=[];ys=[]
    for y in range(y0,y1):
        for x in range(x0,x1):
            if pred(px[x,y]): xs.append(x);ys.append(y)
    if not xs: return None
    return (min(xs),min(ys),max(xs),max(ys))

def slide_bbox(b):
    if b is None: return None
    return (mx(b[0]),my(b[1]),mx(b[2]),my(b[3]))

def mode_in(x0,y0,x1,y1,pred):
    c = Counter()
    for y in range(y0,y1):
        for x in range(x0,x1):
            p = px[x,y]
            if pred(p): c[p]+=1
    return c.most_common(3)

# --- LEFT inset interior boxes: mask by fill family
lav = lambda p: 175<p[0]<215 and 165<p[1]<205 and 195<p[2]<235
yel = lambda p: p[0]>235 and p[1]>235 and 165<p[2]<215
pnk = lambda p: 210<p[0]<245 and 175<p[1]<215 and 195<p[2]<235
sft = lambda p: 150<p[0]<200 and 205<p[1]<240 and 150<p[2]<195   # softmax light green A5D6A7-ish
wht = lambda p: p[0]>243 and p[1]>243 and p[2]>240
blk = lambda p: p[0]<80 and p[1]<80 and p[2]<80
red = lambda p: p[0]>120 and (p[0]-p[1])>60 and (p[0]-p[2])>60
blu = lambda p: p[2]>120 and (p[2]-p[1])>60 and p[0]<110

out["L_matmul_top"] = slide_bbox(bbox_of(lav, 60, 270, 200, 320))
out["L_mask"]       = slide_bbox(bbox_of(pnk, 60, 340, 200, 385))
out["L_scale"]      = slide_bbox(bbox_of(yel, 60, 380, 200, 415))
out["L_matmul_bot"] = slide_bbox(bbox_of(lav, 60, 400, 200, 460))
out["L_softmax"]    = slide_bbox(bbox_of(sft, 60, 300, 200, 350))
out["L_white_fill"] = slide_bbox(bbox_of(wht, 50, 230, 210, 520))
out["L_circ_red"]   = slide_bbox(bbox_of(red, 60, 440, 200, 500))
out["L_circ_blue"]  = slide_bbox(bbox_of(blu, 60, 440, 200, 500))
out["L_black_ink"]  = slide_bbox(bbox_of(blk, 60, 265, 200, 500))

# left inset mode colors (exact)
out["L_lav_mode"] = mode_in(95, 285, 170, 310, lav)
out["L_pnk_mode"] = mode_in(80, 355, 160, 380, pnk)
out["L_yel_mode"] = mode_in(90, 385, 150, 412, yel)
out["L_sft_mode"] = mode_in(80, 315, 160, 345, sft)
out["L_white_mode"] = mode_in(100, 430, 180, 465, wht)
out["L_frame_mode"] = mode_in(78, 300, 81, 400, lambda p: p[1]>90 and (p[1]-p[0])>40 and (p[1]-p[2])>40)

# --- CENTER inset
out["C_sdpa_mauve"] = slide_bbox(bbox_of(lambda p: 170<p[0]<205 and 130<p[1]<165 and 160<p[2]<195, 290, 330, 500, 400))
out["C_concat_yel"] = slide_bbox(bbox_of(yel, 290, 295, 500, 330))
out["C_linear_row"] = slide_bbox(bbox_of(wht, 295, 390, 480, 430))
out["C_circ_red"]   = slide_bbox(bbox_of(red, 300, 470, 480, 520))
out["C_circ_blue"]  = slide_bbox(bbox_of(blu, 300, 470, 480, 520))
out["C_shadows"]    = slide_bbox(bbox_of(lambda p: 215<p[0]<240 and 215<p[1]<240 and 215<p[2]<240, 290, 250, 500, 520))
out["C_sdpa_mode"]  = mode_in(310, 355, 470, 395, lambda p: 170<p[0]<205 and 130<p[1]<165 and 160<p[2]<195)
out["C_concat_mode"]= mode_in(360, 305, 420, 325, yel)

print(json.dumps(out, indent=1, default=str))
