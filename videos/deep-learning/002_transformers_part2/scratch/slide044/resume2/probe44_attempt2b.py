#!/usr/bin/env python3
import numpy as np
from PIL import Image
BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
orig = np.asarray(Image.open(f'{BASE}/unique_slides/slide_044.jpg').convert('RGB')).astype(int)
r0,g0,b0 = orig[:,:,0], orig[:,:,1], orig[:,:,2]
redL = (r0>150)&(r0-g0>30)&(r0-b0>30)
redS = (r0>150)&(g0<90)&(b0<90)

def rows(mask,x0,x1,y0,y1,lbl):
    print(f'-- {lbl} --')
    for y in range(y0,y1):
        xs=np.where(mask[y,x0:x1])[0]
        if len(xs): print(f'  y{y}: x {xs.min()+x0}..{xs.max()+x0} n={len(xs)}')

print('== FV label strip (x664..686, y140..360) ==')
rows(redL,664,686,140,360,'FV-label redL')
print('== FV heads: top y120..152, bottom y340..370 (x648..676) ==')
rows(redL,648,676,120,152,'FV-top')
rows(redL,648,676,340,370,'FV-bottom')
print('== left Channels label strict red (x88..164 y428..448) ==')
rows(redS,88,164,428,448,'chL-label redS')
rows(redL,55,200,424,434,'chL-arrow redL fine')
print('== pixel samples ==')
pts = [('LY-top-border',(300,455)),('LY-top2',(600,455)),('LY-top3',(800,455)),
 ('LY-left',(63,470)),('LY-left2',(64,478)),('LY-right',(905,470)),('LY-right2',(904,485)),
 ('LY-bot',(300,501)),('LY-bot2',(600,501)),('LY-bot3',(800,501)),
 ('LY-fill1',(200,470)),('LY-fill2',(400,490)),('LY-fill3',(700,470)),('LY-fill4',(300,485)),
 ('GN-top',(300,372)),('GN-top2',(420,373)),('GN-bot',(300,444)),('GN-bot2',(420,444)),
 ('GN-left',(260,400)),('GN-right',(448,400)),('GN-fill',(300,437)),
 ('IN-top',(500,363)),('IN-top2',(700,363)),('IN-bot',(500,441)),('IN-bot2',(700,441)),
 ('IN-left',(469,400)),('IN-right',(864,400)),('IN-fill',(520,433)),
 ('chL-color',(110,437)),('chL-color2',(140,438)),('chL-arrow',(100,428)),('chL-arrow2',(150,429)),
 ('FV-shaft',(660,250)),('FV-label',(672,260)),
 ('title-bar-y455-left',(80,455)),('title-in-oval-zone',(800,455))]
for lbl,(x,y) in pts: print(f'  orig({x},{y}) {lbl}: {tuple(int(v) for v in orig[y,x])}')
