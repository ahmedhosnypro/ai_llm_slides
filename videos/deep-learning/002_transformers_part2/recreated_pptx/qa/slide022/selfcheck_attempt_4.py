#!/usr/bin/env python3
# selfcheck_attempt_4.py — resumed worker. Render-vs-ORIGINAL closed loop on MY measured regions.
# render px = slide_pt * 150/72 ; slide_x = (frame_x-17.753)/0.962235 ; slide_y = frame_y/0.955556
from PIL import Image
import numpy as np, json, sys

V = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
ren = np.asarray(Image.open(f'{V}/recreated_pptx/qa/slide022/render_1.png').convert('RGB')).astype(int)
org = np.asarray(Image.open(f'{V}/unique_slides/slide_022.jpg').convert('RGB')).astype(int)
RH, RW, _ = ren.shape
FX = lambda fx: (fx - 17.753) / 0.962235
FY = lambda fy: fy / 0.955556
RX = lambda fx: FX(fx) * 150 / 72
RY = lambda fy: FY(fy) * 150 / 72

def ink_bbox(img, y0, y1, x0, x1, thr):
    m = img[y0:y1, x0:x1].mean(axis=2) < thr
    ys, xs = np.where(m)
    if not len(ys): return None
    return [int(xs.min()+x0), int(ys.min()+y0), int(xs.max()+x0), int(ys.max()+y0)]

def cmp_region(name, fbox, thr=170, pad=6):
    # fbox = [fx0, fy0, fx1, fy1] search window in FRAME coords
    rx0, ry0 = int(RX(fbox[0]))-pad, int(RY(fbox[1]))-pad
    rx1, ry1 = int(RX(fbox[2]))+pad, int(RY(fbox[3]))+pad
    got = ink_bbox(ren, max(0,ry0), min(RH,ry1), max(0,rx0), min(RW,rx1), thr)
    exp = [RX(fbox[0]), RY(fbox[1]), RX(fbox[2]), RY(fbox[3])]
    if got is None:
        return name, "EMPTY", got, exp
    d = max(abs(got[0]-exp[0]), abs(got[1]-exp[1]), abs(got[2]-exp[2]), abs(got[3]-exp[3]))
    return name, ("OK " if d <= 14 else f"FAIL max|d|={d:.1f}"), got, [round(v,1) for v in exp]

out = {}
# title / subtitle (frame ink bboxes measured: title [339,60,688,81], subtitle [322,86,719,105])
out['title'] = cmp_region('title', [330, 52, 700, 86])
out['subtitle'] = cmp_region('subtitle', [312, 80, 730, 110])
# diagram panel navy border: top rule y111, sides x65/x892, bottom y341.5
out['dpanel_top_rule'] = cmp_region('dpanel_top', [70, 106, 880, 116])
out['dpanel_bottom'] = cmp_region('dpanel_bottom', [70, 336, 880, 347])
# row lanes (dashed containers) x[166,888]
out['lane1'] = cmp_region('lane1', [160, 114, 894, 162])
out['lane2'] = cmp_region('lane2', [160, 183, 894, 230])
out['lane3'] = cmp_region('lane3', [160, 257, 894, 307])
# row box top-border bands (y127/y195/y272) x[170,890]
out['r1_boxes'] = cmp_region('r1_boxes', [170, 121, 890, 153])
out['r2_boxes'] = cmp_region('r2_boxes', [170, 189, 890, 221])
out['r3_boxes'] = cmp_region('r3_boxes', [170, 266, 890, 298])
# dots bands
out['dots1'] = cmp_region('dots1', [628, 130, 716, 148])
out['dots2'] = cmp_region('dots2', [628, 199, 716, 217])
# cyan panel: top y349.5, bottom y502.5
out['cpanel'] = cmp_region('cpanel', [60, 344, 897, 508])
# summary / problems / bullets (frame ink: summary [80,366,825,383]; problems [81,390,160,401];
# b1 [80,411,884,445]; b2 [80,454,879,470]; b3 [80,476,743,491])
out['summary'] = cmp_region('summary', [70, 362, 835, 388])
out['problems'] = cmp_region('problems', [74, 386, 170, 405])
out['b1'] = cmp_region('b1', [74, 407, 894, 449])
out['b2'] = cmp_region('b2', [74, 450, 889, 473])
out['b3'] = cmp_region('b3', [74, 472, 753, 495])
# left labels: lab1 [79,115,159,157], lab2 [77,192,164,220], lab3 [75,264,156,289]
out['lab1'] = cmp_region('lab1', [70, 111, 165, 161])
out['lab2'] = cmp_region('lab2', [70, 188, 170, 224])
out['lab3'] = cmp_region('lab3', [70, 260, 162, 293])
# +delta band: orange marks y[292,306] x[265,850]; delta texts y[313,330] x[210,880]
out['dmarks'] = cmp_region('dmarks', [260, 289, 855, 309])
out['dtexts'] = cmp_region('dtexts', [205, 311, 885, 332])

for k, (name, verdict, got, exp) in out.items():
    print(f"{k:16s} {verdict:30s} got={got} exp={exp}")
