# stage 6: remaining details
from PIL import Image, ImageFont
import numpy as np
from collections import Counter

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_009.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[...,0], a[...,1], a[...,2]

def modal(x0,x1,y0,y1,n=5):
    reg = a[y0:y1, x0:x1].reshape(-1,3)
    return Counter(map(tuple, (reg//2*2))).most_common(n)

def bbox_of(mask):
    ys, xs = np.nonzero(mask)
    if len(xs)==0: return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(mask.sum()))

def amap(x0,x1,y0,y1,step=2,label=""):
    print(f"--- map {label} x{x0}..{x1} y{y0}..{y1} step{step} ---")
    print("     " + "".join(str((x//10)%10) for x in range(x0,x1,step)))
    for y in range(y0,y1,step):
        row = "".join(cls(a[y,x]) for x in range(x0,x1,step))
        print(f"y{y:4d} {row}")

def cls(p):
    R,G,B = p
    if R>235 and G>235 and B>235:
        if R>248 and G>248 and B>248: return "W"
        return "w"
    if abs(R-G)<14 and abs(G-B)<14:
        v=(R+G+B)//3
        if v<60: return "K"
        if v<150: return "D"
        if v<205: return "G"
        if v<228: return "g"
        return "h"
    if R>140 and R-np.maximum(G,B)>60 and G<110: return "R"
    if G>140 and G-np.maximum(R,B)>25: return "N"
    if R>190 and G>190 and B<120: return "y"
    if B>200 and R>190 and G<225 and B-np.maximum(R,G)>10: return "L"
    if R>200 and G>170 and B>130 and R>G>B: return "P"
    return "?"

# green box: fill mask + bbox
green = (g>240)&(g-r>8)&(g-b>8)&(abs(g-b)<25)
mm = np.zeros((H,W),bool); mm[200:275, 425:575]=True
print("green fill bbox:", bbox_of(green & mm))
print("green fill modal:", modal(460,540,215,228))
# green box border: top edge
print("green border top edge modal (x460..540, y207..212):", modal(460,540,207,212,8))
print("green border left edge modal (x440..445, y225..250):", modal(440,445,225,250,8))

# classification border check + white text bbox inside fill
print("\nclassification left edge (x584..589, y225..250):", modal(584,589,225,250,8))
print("classification top edge (x600..700, y207..212):", modal(600,700,207,212,8))
whitem = (r>190)&(g>190)&(b>190)
mm4 = np.zeros((H,W),bool); mm4[212:263, 589:721]=True
print("classification white-text bbox (inside fill):", bbox_of(whitem & mm4))

# post-processing text ink modal (is it black?)
inkm = (r<110)&(g<110)&(b<110)
mm5 = np.zeros((H,W),bool); mm5[219:257, 758:852]=True
ys,xs = np.nonzero(inkm & mm5)
print("\npostproc text ink bbox:", bbox_of(inkm & mm5), "ink modal:", Counter(map(tuple,(a[inkm & mm5]//2*2))).most_common(3))
print("mystery (825..829, 234..238):", modal(825,829,234,238,8))

# per-line text bboxes helper
def lines(x0,x1,y0,y1,label,mask=None):
    m = (mask if mask is not None else ((r<110)&(g<110)&(b<110)))
    print(f"-- {label} line profile (x{x0}..{x1}, y{y0}..{y1}) --")
    sub = m[y0:y1, x0:x1]
    prof = sub.sum(axis=1)
    inline = False
    for i,c in enumerate(prof):
        if c>0 and not inline: start=i; inline=True
        if c==0 and inline:
            print(f"   line y {y0+start}..{y0+i-1} (h={i-start})")
            inline=False
    if inline: print(f"   line y {y0+start}..{y0+len(prof)-1}")
    # horizontal extents per line
    return

lines(152,246,213,261,"PreProc text")
lines(297,405,213,261,"Cyan text")
lines(444,556,213,261,"Green text")
lines(760,852,215,258,"Lav text")
lines(100,190,145,190,"TrainingData text")
lines(795,875,315,346,"FinalResult text")
for i,(x0,x1) in enumerate([(241,328),(386,473),(537,624),(694,781)],1):
    lines(x0+2,x1-2,293,330,f"label{i} text")

# final ellipse border + fill hist
print("\nfinal ellipse: border modal (y312..316, x820..850):", modal(820,850,312,316,8))
print("final ellipse fill fine modal (x820..870, y322..340):", Counter(map(tuple,(a[322:340,820:870].reshape(-1,3)//2*2))).most_common(6))
print("final ellipse bottom edge (y344..348, x820..850):", modal(820,850,344,348,8))

# training ellipse outline: scan across left edge y=165
row=a[165]; seg=[(x,tuple(row[x])) for x in range(76,100)]
print("\ntraining ellipse left edge y=165 x76..100:", seg)

# ASCII map of curved arrow 2 region
amap(820, 895, 228, 315, 2, "curved arrow 2 + final ellipse top")

# title: stroke core color + font solve
print("\ntitle stroke modal (T stem x224..229, y70..85):", modal(224,229,70,85))
print("title ink bbox rows:")
lines(215,720,60,95,"title")
