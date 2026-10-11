#!/usr/bin/env python3
"""ASCII maps + remaining color pins."""
import numpy as np
from PIL import Image

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_026.jpg").convert("RGB")
A = np.asarray(IM).astype(int)

def classify(c):
    r, g, b = c
    if abs(r-247)+abs(g-227)+abs(b-206) <= 45: return "."
    if r>235 and g>235 and b>235: return "w"
    if abs(r-233)+abs(g-233)+abs(b-231) <= 25: return ","
    if r>240 and g>240 and b<225: return "Y"
    if g>r and g>b and g>200 and r>200: return "m"
    if r>230 and g<220 and b>235: return "L"
    if r>235 and 130<g<215 and b>190: return "P"
    if r<160 and g<160 and b<160: return "K"
    if r-g>50 and r>140: return "R"
    if b-r>40 and b>150: return "B"
    if g-r>25 and g-b>25: return "G"
    if r>180 and g>140 and b>120 and r-b>40: return "t"
    return "?"

def amap(name, x0, x1, y0, y1, step=2):
    print(f"== {name} x{x0}..{x1} y{y0}..{y1} step{step} ==")
    hdr = "     " + "".join(str((x0+i*step)//100 % 10) for i in range((x1-x0)//step))
    hdr2 = "     " + "".join(str((x0+i*step)//10 % 10) for i in range((x1-x0)//step))
    print(hdr); print(hdr2)
    for y in range(y0, y1, step):
        row = "".join(classify(A[y, x0+i*step]) for i in range((x1-x0)//step))
        print(f"y{y:3d} {row}")

amap("SIGMA/Y/ARROW/WSUM", 488, 700, 112, 224, 2)
amap("LINES+NODES upper", 490, 764, 222, 312, 2)
amap("LINES+NODES lower", 490, 764, 312, 396, 2)

print("\n== pill row profiles ==")
for yy in (166, 174, 182):
    print(f"y{yy}: " + "".join(classify(c) for c in A[yy, 250:700]))

print("\n== color pins ==")
def pin(nm, x, y):
    c = A[y, x]; print(f"  {nm:26s} ({x:3d},{y:3d}) #{c[0]:02X}{c[1]:02X}{c[2]:02X}")
pin("Sim_label_ink", 290, 174)
pin("Prob_label_ink", 470, 172)
pin("WSum_label_ink", 620, 160)
pin("sigma_glyph", 582, 206)
pin("sigma_fill", 540, 205)
pin("dot1_core", 330, 246)
pin("dot2_core", 314, 287)
pin("W_label_ink", 502, 231)
pin("softmax_label_ink", 473, 280)
pin("dotprod_label_ink", 290, 205)
pin("dotprod_label2_ink", 290, 220)
pin("X1_label_L1", 96, 246)
pin("X2_highlight_border_top", 298, 474)
pin("X2_highlight_border_left", 264, 490)
pin("X2_fill_core", 290, 492)
pin("strip_X1_label", 245, 494)
pin("red_query_core", 298, 430)
pin("red_token_X2_sub_core", 412, 88)
pin("dashed_border_green_L", 57, 300)
pin("ybox_mid_block", 578, 131)
pin("ybox_left_block", 558, 131)
pin("ybox_right_block", 588, 131)
pin("green_arrow_core2", 560, 158)
pin("badge_ring", 876, 71)
pin("title_ink2", 262, 66)
pin("subtitle_ink2", 205, 88)
