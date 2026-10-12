# m5_fine2.py — targeted fine scans
import numpy as np
from PIL import Image
from scipy import ndimage
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
mx = a.max(axis=2); mn = a.min(axis=2); sat = mx-mn

def comps(mask, min_px=4):
    lab, n = ndimage.label(mask)
    out=[]
    for i in range(1,n+1):
        ys,xs = np.where(lab==i)
        if len(xs)<min_px: continue
        out.append((int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()),len(xs)))
    return sorted(out, key=lambda c:(c[1],c[0]))

def sub(x0,y0,x1,y1): 
    m=np.zeros(a.shape[:2],bool); m[y0:y1+1,x0:x1+1]=True; return m

def show(name,lst,lim=40):
    print(f"--- {name} ({len(lst)})")
    for c in lst[:lim]:
        x0,y0,x1,y1,npx=c
        cx,cy=(x0+x1)//2,(y0+y1)//2
        col=tuple(np.median(a[max(0,y0):y1+1,max(0,x0):x1+1].reshape(-1,3),axis=0).astype(int))
        print(f"   x{x0}..{x1} y{y0}..{y1} w{x1-x0+1} h{y1-y0+1} px={npx} med=#{col[0]:02X}{col[1]:02X}{col[2]:02X} ctr({cx},{cy})")

# 1) pill region: any non-white, non-gray ink
reg = sub(60,92,225,150)
ink = reg & (sat>25)
show("PILL ink comps", comps(ink,6), 30)
# pill fill color at empty spots
for (x,y) in [(80,110),(200,110),(80,135),(200,135),(140,108)]:
    print(f"   pill sample ({x},{y}) #{a[y,x,0]:02X}{a[y,x,1]:02X}{a[y,x,2]:02X}")
# 2) below-pill labels: ink in x60..220 y150..280
reg2 = sub(60,150,220,280)
ink2 = reg2 & ((sat>35)|(mx<120))
show("BELOWPILL ink comps", comps(ink2,5), 30)
# 3) equals region x372..412 y140..220
reg3 = sub(372,140,412,220)
red3 = reg3 & (R>150)&(G<130)&(B<130)
show("EQUALS red comps", comps(red3,3), 20)
# 4) dxd + 1xd areas
show("DXD red comps x330..470 y240..285", comps(sub(330,240,470,285)&(R>150)&(G<130)&(B<130),3), 15)
show("1XD red comps x150..225 y125..175", comps(sub(150,125,225,175)&(R>150)&(G<130)&(B<130),3), 15)
# 5) matrix text colors per cell (cells x[220,260,298,336]+38, y[86,131,172,212]+40)
cols_x=[220,260,298,336]; rows_y=[86,131,172,212]
print("--- MATRIX cell text colors (center 24x24 of each cell, pixels sat>60 or mx<150)")
for ri,y in enumerate(rows_y):
    line=[]
    for ci,x in enumerate(cols_x):
        cx,cy = x+19, y+20
        blk = a[cy-11:cy+12, cx-11:cx+12].reshape(-1,3)
        ink = blk[(blk.max(axis=1)<170) | (blk.max(axis=1)-blk.min(axis=1)>60)]
        if len(ink)==0: line.append("  none  "); continue
        med = np.median(ink,axis=0).astype(int)
        line.append(f"#{med[0]:02X}{med[1]:02X}{med[2]:02X}")
    print(f"   row{ri+1}: " + " ".join(line))
# matrix border color: sample cell edges
print("   matrix border samples:", " ".join(f"#{a[y,x,0]:02X}{a[y,x,1]:02X}{a[y,x,2]:02X}" for (x,y) in [(258,107),(296,150),(335,191),(371,233),(240,86),(240,128),(240,169),(240,210)]))
# 6) band bbox via row/col profiles in x480..908 y240..515
print("--- BAND profile")
graylike = (sat<16)&(mx>200)&(mx<235)
for y in range(240,516,6):
    cnt = int(graylike[y,480:909].sum())
    print(f"   y{y}: gray_px={cnt}")
