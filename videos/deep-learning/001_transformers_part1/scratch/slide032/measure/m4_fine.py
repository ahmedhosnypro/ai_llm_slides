# m4_fine.py — fine region scans of slide_032.jpg
import numpy as np
from PIL import Image
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
mx = a.max(axis=2); mn = a.min(axis=2); sat = mx - mn

masks = {
  "red":    (R>140) & (G<100) & (B<100),
  "blue":   (B>120) & (B-R>40) & (B-G>25),
  "green":  (G>100) & (G-R>30) & (G-B>30),
  "magenta":(R>150) & (B>150) & (G<140) & (R-G>40),
  "orange": (R>200) & (G>100) & (G<200) & (B<120),
  "dark":   mx<110,
  "yellowish": (R>225) & (G>195) & (B>120) & (B<215) & (R-B>35),
  "pink":   (R>225) & (G>150) & (G<215) & (B>150) & (B<225) & (sat>18) & (R-G>25),
}
try:
    from scipy import ndimage
    HAVE=True
except ImportError:
    HAVE=False
print("scipy:", HAVE)

def comps(mask, min_px=8, region=None):
    m = mask.copy()
    if region:
        x0,y0,x1,y1 = region
        keep = np.zeros_like(m); keep[y0:y1+1, x0:x1+1] = m[y0:y1+1, x0:x1+1]; m = keep
    lab, n = ndimage.label(m)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.where(lab==i)
        if len(xs)<min_px: continue
        out.append((int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()),len(xs)))
    return out

def show(name, lst, limit=25):
    print(f"--- {name} ({len(lst)})")
    for (x0,y0,x1,y1,npx) in sorted(lst,key=lambda c:(c[1],c[0]))[:limit]:
        print(f"   x{x0}..{x1} y{y0}..{y1} w{x1-x0+1} h{y1-y0+1} px={npx}")

# 1) equation panel area
EQ = (40,55,480,290)
show("EQ red comps (border/text/=)", comps(masks["red"], 6, EQ), 40)
show("EQ pink comps (pill/outcells)", comps(masks["pink"], 30, EQ), 20)
show("EQ dark comps (labels)", comps(masks["dark"], 6, EQ), 40)
# 2) title area
TI = (470,105,920,250)
show("TITLE red comps", comps(masks["red"], 6, TI), 30)
show("TITLE blue comps", comps(masks["blue"], 6, TI), 30)
# 3) network panel area
NE = (470,240,925,515)
show("NET blue comps (border/circles/lines)", comps(masks["blue"], 6, NE), 40)
show("NET red comps", comps(masks["red"], 6, NE), 40)
show("NET green comps", comps(masks["green"], 4, NE), 30)
show("NET dark comps (labels)", comps(masks["dark"], 6, NE), 40)
show("NET orange comps", comps(masks["orange"], 4, NE), 20)
