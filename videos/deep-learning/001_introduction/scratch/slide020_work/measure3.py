from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]

def vscan(x, y0, y1, label, step=1):
    print(f"-- vscan x={x} {label}")
    prev=None
    for y in range(y0,y1,step):
        px=a[y,x]; c=f"{px[0]:02X}{px[1]:02X}{px[2]:02X}"
        if c!=prev: print(f"   y={y} #{c}"); prev=c
def hscan(y, x0, x1, label, step=1):
    print(f"-- hscan y={y} {label}")
    prev=None
    for x in range(x0,x1,step):
        px=a[y,x]; c=f"{px[0]:02X}{px[1]:02X}{px[2]:02X}"
        if c!=prev: print(f"   x={x} #{c}"); prev=c

vscan(847, 206, 262, "SamplesLabels vert")
vscan(772, 165, 180, "PredError top")
vscan(772, 293, 306, "PredError bottom")
hscan(230, 750, 760, "PredError left")
hscan(230, 786, 796, "PredError right")
vscan(120, 208, 218, "InputSamples top")
vscan(120, 250, 262, "InputSamples bottom")
hscan(235, 78, 88, "InputSamples left")
vscan(300, 334, 346, "greenbox top")
vscan(300, 372, 384, "greenbox bottom")
hscan(358, 258, 270, "greenbox left")
hscan(358, 736, 748, "greenbox right")
vscan(419, 104, 118, "ellipse top edge")
vscan(419, 152, 162, "ellipse bottom edge")
