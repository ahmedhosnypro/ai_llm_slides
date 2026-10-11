#!/usr/bin/env python3
import numpy as np
from PIL import Image
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
def p(name, x, y):
    px = im[y, x]
    print(f"{name:38s} ({x:3d},{y:3d}) = #{px[0]:02X}{px[1]:02X}{px[2]:02X}")
# small output vector box y48-76 x404-476
for (x,y) in [(410,60),(430,60),(455,60),(465,55),(440,70),(415,52)]:
    p("vecbox", x, y)
# LT box interior
for (x,y) in [(420,100),(480,100),(540,100),(470,92),(470,108)]:
    p("LTbox", x, y)
# concat bar left part (label area?)
for (x,y) in [(200,138),(250,138),(320,136),(380,138),(300,132)]:
    p("bar-left", x, y)
# concat bar segments
for (x,y) in [(445,138),(470,138),(500,138),(530,138),(555,138),(600,138),(620,138),(655,138),(680,138),(710,138),(735,138),(755,138)]:
    p("bar-seg", x, y)
# bar top/bottom edge
for (x,y) in [(500,129),(500,131),(500,146),(500,149),(300,129),(300,149)]:
    p("bar-edge", x, y)
# mystery red y244-251
for (x,y) in [(445,247),(470,247),(490,247),(510,247),(460,244),(460,251)]:
    p("mystery-red", x, y)
# title area
for (x,y) in [(560,60),(700,60),(800,60),(640,90),(760,90)]:
    p("title", x, y)
# badge
for (x,y) in [(893,71),(893,55),(883,71)]:
    p("badge", x, y)
# front card
for (x,y) in [(70,300),(300,290),(500,300),(100,480),(300,500)]:
    p("h1card", x, y)
# ovals on staircase: check white ovals ~ (490,200)? (620,265)?
for (x,y) in [(500,200),(620,262),(560,240),(430,240)]:
    p("oval?", x, y)
