from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)
R, G, B = im[:,:,0], im[:,:,1], im[:,:,2]
lum = im.mean(axis=2)

print("== cyan panel text bands y[350,506] x[70,885] (darkfrac>0.06) ==")
band = None
for y in range(350, 507):
    f = (lum[y, 70:885] < 185).mean()
    if f > 0.06:
        if band is None: band = [y, y]
        else: band[1] = y
    else:
        if band: 
            sub = lum[band[0]:band[1]+1, 70:885]
            m = sub < 185
            xs = np.where(m.any(axis=0))[0]
            # dominant text color: dark pixels
            reg = im[band[0]:band[1]+1, 70:885]
            dk = reg[sub]
            redpx = ((dk[:,0]-dk[:,1]>40)&(dk[:,0]-dk[:,2]>40)).sum()
            bluepx = ((dk[:,2]-dk[:,0]>40)).sum()
            darkpx = ((abs(dk[:,0]-dk[:,1])<30)&(abs(dk[:,1]-dk[:,2])<30)&(dk[:,0]<120)).sum()
            print(f"  band y[{band[0]},{band[1]}] x[{xs.min()+70},{xs.max()+70}] red={redpx} blue={bluepx} dark={darkpx}")
            band = None
if band: print(f"  band y[{band[0]},{band[1]}] (open)")

print("== row2 dots: dark px in gap x[610,730] y[193,222] ==")
sub = lum[193:222, 610:730]
ys, xs = np.where(sub < 165)
if len(xs):
    import collections
    cols = sorted(set(xs))
    runs, s, p = [], None, None
    for x in cols:
        if s is None: s = x; p = x; continue
        if x - p > 3: runs.append((s+610, p+610)); s = x
        p = x
    runs.append((s+610, p+610))
    print("  dot x-runs:", runs, " y extent:", ys.min()+193, ys.max()+193)
else: print("  none")

print("== row1/2/3 container side dashes ==")
for lbl, ys in [("row1", [130, 140, 150]), ("row2", [195, 205, 215]), ("row3", [270, 280, 290])]:
    for y in ys:
        l = im[y, 160:175].mean(axis=1); r = im[y, 880:895].mean(axis=1)
        print(f"  {lbl} y={y} left min {l.min():.0f}@x{160+int(l.argmin())}  right min {r.min():.0f}@x{880+int(r.argmin())}")

print("== dash cores ==")
print("row1 top dash y119:", [im[119,x].tolist() for x in (300, 420, 540, 660)])
print("row3 top dash y263:", [im[263,x].tolist() for x in (200, 300, 400, 500)])
print("row2 top dash y188:", [im[188,x].tolist() for x in (200, 300, 400, 500)])
print("row1 box border y127 x300:", im[127,300].tolist(), " y147:", im[147,300].tolist())
print("row2 box border y195 x300:", im[195,300].tolist(), " y216:", im[216,300].tolist())
print("row3 box border y272 x300:", im[272,300].tolist(), " y293:", im[293,300].tolist())
print("== navy rule x extent at y111 ==")
row = lum[111, :]
dk = np.where(row < 160)[0]
print("  dark cols:", dk.min(), dk.max(), "n=", len(dk), " im[111,62]:", im[111,62].tolist(), " im[111,896]:", im[111,896].tolist())
print("== navy side borders continuity ==")
for y in (113, 200, 300, 342, 346, 348, 400, 470, 500):
    print(f"  y={y}: x64-66 {[im[y,x].tolist() for x in (64,65,66)]} x891-893 {[im[y,x].tolist() for x in (891,892,893)]}")
print("== title/subtitle bboxes (excl chrome) ==")
def bbox(y0,y1,x0=70,x1=890,cond=None):
    reg = im[y0:y1, x0:x1]
    rr,gg,bb = reg[:,:,0],reg[:,:,1],reg[:,:,2]
    if cond=='red': m = (rr-gg>45)&(rr-bb>45)
    elif cond=='blue': m = (bb-rr>45)&(bb-gg>25)
    else: m = reg.mean(axis=2)<150
    ys,xs = np.where(m)
    if not len(xs): return None
    return (xs.min()+x0, ys.min()+y0, xs.max()+x0, ys.max()+y0)
print("  title red bbox:", bbox(55, 84, cond='red'))
print("  subtitle blue bbox:", bbox(84, 108, cond='blue'))
print("  title dark-ish bbox:", bbox(55, 84))
