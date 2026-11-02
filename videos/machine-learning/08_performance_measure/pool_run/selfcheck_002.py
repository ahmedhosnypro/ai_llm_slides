import os
from PIL import Image
import numpy as np

NS = os.environ.get("NS", "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
orig = np.array(Image.open(f"{NS}/unique_slides/slide_002.jpg").convert("RGB")).astype(int)
ren = np.array(Image.open(f"{NS}/recreated_pptx/qa/slide002/render_1.png").convert("RGB")).astype(int)
print("render size", ren.shape, "orig", orig.shape)
S = ren.shape[1] / 960.0
print("scale", S)

def ink(mask): return int(mask.sum())
def rmask(a): R,G,B = a[...,0],a[...,1],a[...,2]; return (R>140)&(R-G>60)&(R-B>60)

# 1. house frame: red pixels near expected border in render
rf = rmask(ren)
# expected frame centerline: x=0.15in*150=22.5, right edge (0.15+13.03)*150=1979.5, y=22.5, bottom (0.15+7.2)*150=1102.5
col = rf[:, 18:28].sum(); print("frame left col ink", col)
col = rf[:, 1975:1985].sum(); print("frame right col ink", col)
row = rf[18:28, :].sum(); print("frame top row ink", row)
row = rf[1098:1108, :].sum(); print("frame bottom row ink", row)

# 2. badge: yellowish pixels in badge box
R,G,B = ren[...,0],ren[...,1],ren[...,2]
yellow = (R>230)&(G>220)&(B<200)
bx0,bx1 = int(12.48*150), int((12.48+0.5)*150)
by0,by1 = int(0.30*150), int((0.30+0.5)*150)
print("badge yellow px", ink(yellow[by0:by1, bx0:bx1]), "of", (by1-by0)*(bx1-bx0))

# 3. pane images present: dark ink inside pane interiors of render
def darkfrac(a, x0,y0,x1,y1, s):
    reg = a[int(y0*s):int(y1*s), int(x0*s):int(x1*s)]
    d = (reg[...,0]<120)&(reg[...,1]<120)&(reg[...,2]<120)
    return d.mean()
print("render pos pane dark frac", round(darkfrac(ren, 90,150,230,495, S),4), " orig", round(darkfrac(orig, 90,150,230,495, 1.0),4))
print("render neg pane dark frac", round(darkfrac(ren, 340,150,475,495, S),4), " orig", round(darkfrac(orig, 340,150,475,495, 1.0),4))

# 4. sigmoid present in activation panel render
reg = ren[int(96*S):int(160*S), int(706*S):int(876*S)]
R,G,B = reg[...,0],reg[...,1],reg[...,2]
mag = (R>110)&(B>110)&(G<R-40)&(G<B-40)
print("render sigmoid magenta px", ink(mag), " orig", end=" ")
reg = orig[96:160, 706:876]
R,G,B = reg[...,0],reg[...,1],reg[...,2]
mag = (R>110)&(B>110)&(G<R-40)&(G<B-40)
print(ink(mag))

# 5. broken-image placeholder check: LibreOffice placeholder text is gray box w/ text; check for large uniform gray rect where images go
for name,(x0,y0,x1,y1) in {"pos pane":(84,140,235,502),"neg pane":(336,140,480,502),"sigmoid":(706,96,876,160)}.items():
    reg = ren[int(y0*S):int(y1*S), int(x0*S):int(x1*S)].reshape(-1,3)
    uniq = len(np.unique(reg//32, axis=0))
    print(name, "unique color buckets", uniq, "mean", reg.mean(axis=0).round(1))

# 6. caption text present under model boxes: dark-on-red? caption is white text on red box in build; check red box exists
redfill = (ren[...,0]>120)&(ren[...,0]-ren[...,1]>60)&(ren[...,0]-ren[...,2]>60)
reg = redfill[int(245*S):int(305*S), int(613*S):int(736*S)]
print("model train red fill frac", round(reg.mean(),3))
reg = redfill[int(422*S):int(463*S), int(613*S):int(736*S)]
print("model eval red fill frac", round(reg.mean(),3))
