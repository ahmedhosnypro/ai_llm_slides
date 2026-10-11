#!/usr/bin/env python3
"""Measure slide_043.jpg (960x540): find color regions for the five head cards,
output pipeline, concat bar, legend, arrows, chips. 1px = 1pt = 1/72 in."""
import numpy as np
from PIL import Image
import json

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def bbox(mask, name):
    ys, xs = np.where(mask)
    if not len(ys):
        print(f"{name}: NOT FOUND")
        return None
    print(f"{name}: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}  (n={len(ys)})")
    return dict(x0=int(xs.min()), x1=int(xs.max()), y0=int(ys.min()), y1=int(ys.max()), n=int(len(ys)))

def near(c, tol=18):
    return (abs(r-c[0])<tol) & (abs(g-c[1])<tol) & (abs(b-c[2])<tol)

out = {}
# Five head cards (spec palette)
out['card_h1_salmon'] = bbox(near((240,128,128)), 'h1 salmon F08080')
out['card_h2_lavender'] = bbox(near((200,200,240)), 'h2 lavender C8C8F0')
out['card_h3_yellow'] = bbox(near((252,252,176)), 'h3 pale yellow FCFCB0')
out['card_h4_green'] = bbox(near((204,255,204)), 'h4 pale green CCFFCC')
out['card_h5_peach'] = bbox(near((255,228,196)), 'h5 peach FFE4C4')

# Output pipeline
out['lt_box_white'] = bbox((r>245)&(g>245)&(b>245)&(np.arange(H)[:,None]>70)&(np.arange(H)[:,None]<200)&(np.arange(W)[None,:]>280)&(np.arange(W)[None,:]<620), 'white box (Linear Transformation region 70<y<200, 280<x<620)')
out['concat_bar'] = bbox(near((139,0,0),30)&(np.arange(H)[:,None]>115)&(np.arange(H)[:,None]<160), 'darkred in concat bar y115-160')
out['gray_seg'] = bbox(near((64,64,64),25)&(np.arange(H)[:,None]>115)&(np.arange(H)[:,None]<160), 'dark gray segment y115-160')
out['gold_seg'] = bbox(near((255,215,0),35)&(np.arange(H)[:,None]>115)&(np.arange(H)[:,None]<160), 'gold segment y115-160')

# Query row
out['q1_red_bar'] = bbox(near((204,0,0),40)&(np.arange(H)[:,None]>440)&(np.arange(H)[:,None]<480)&(np.arange(W)[None,:]>100)&(np.arange(W)[None,:]<350), 'red q1 bar y440-480 x100-350')
out['x2_magenta'] = bbox(near((255,105,180),35), 'magenta X2 chip FF69B4')

# Heads arrow (dark red swoosh right side)
out['swoosh'] = bbox(near((139,0,0),30)&(np.arange(W)[None,:]>480), 'darkred swoosh x>480')

# Legend
out['legend_fill'] = bbox(near((232,255,232),20)&(np.arange(H)[:,None]>440)&(np.arange(W)[None,:]>700), 'legend pale green E8FFE8 bottom right')
out['legend_yellow'] = bbox(near((255,215,0),40)&(np.arange(H)[:,None]>440)&(np.arange(W)[None,:]>700), 'legend yellow W square')

# weight chips (royal blue 3366CC)
out['blue_chips'] = bbox(near((51,102,204),35), 'royal blue 3366CC chips (all)')

# pink pills (violet EE82EE)
out['pink_pills'] = bbox(near((238,130,238),30), 'violet pills EE82EE')

# tan dot product box
out['tan_box'] = bbox(near((222,184,135),30), 'tan DEB887')

json.dump(out, open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide043/regions.json','w'), indent=1)
