from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]

def modal(x0,y0,x1,y1,label,q=8):
    reg = a[y0:y1, x0:x1].reshape(-1,3)
    qq = (reg//q*q)
    cnt = Counter(map(tuple, qq))
    (c,n) = cnt.most_common(1)[0]
    core = tuple(int(v)+q//2 for v in c)
    print(f"{label:30s} modal#{core[0]:02X}{core[1]:02X}{core[2]:02X} {core} n={n}/{len(reg)}")

modal(90,218,150,252,"InputSamples fill")
modal(212,215,275,222,"PreProcessing fill top strip")
modal(338,215,398,222,"FeatExtraction fill")
modal(435,215,508,222,"FeatSelection fill")
modal(540,213,625,228,"Classification fill")
modal(663,215,736,220,"PredictedLabels fill")
modal(757,175,788,185,"PredError fill top")
modal(812,218,880,252,"SamplesLabels fill")
modal(380,118,460,126,"ellipse fill")
modal(270,345,300,372,"green box fill left")
modal(715,385,745,400,"starburst fill upper")
modal(300,60,600,66,"title band bg")
modal(48,300,55,400,"outer panel left of frame? x48..55")
modal(63,300,68,400,"panel strip x63..68")

# borders: vertical scans
def vscan(x, y0, y1, label):
    print(f"-- vscan x={x} {label}")
    prev=None
    for y in range(y0,y1):
        px=a[y,x]; c=f"#{px[0]:02X}{px[1]:02X}{px[2]:02X}"
        if c!=prev: print(f"   y={y} {c}"); prev=c
def hscan(y, x0, x1, label):
    print(f"-- hscan y={y} {label}")
    prev=None
    for x in range(x0,x1):
        px=a[y,x]; c=f"#{px[0]:02X}{px[1]:02X}{px[2]:02X}"
        if c!=prev: print(f"   x={x} {c}"); prev=c
vscan(242, 202, 268, "PreProcessing box vertical (borders)")
hscan(235, 200, 212, "PreProcessing left border")
vscan(580, 200, 270, "Classification vertical")
vscan(700, 205, 268, "PredictedLabels vertical")
vscan(772, 165, 185, "PredError top border")
vscan(772, 290, 305, "PredError bottom border")
hscan(230, 748, 760, "PredError left border")
hscan(230, 786, 798, "PredError right border")
vscan(847, 206, 262, "SamplesLabels vertical")
vscan(120, 208, 262, "InputSamples vertical")
vscan(300, 334, 384, "green box vertical")
hscan(360, 258, 270, "green box left border")
vscan(419, 106, 120, "ellipse top")
vscan(419, 150, 165, "ellipse bottom")
hscan(134, 368, 378, "ellipse left edge+dot")
