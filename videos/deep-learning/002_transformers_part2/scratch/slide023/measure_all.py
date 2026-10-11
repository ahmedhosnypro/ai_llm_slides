from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
luma = (0.299*r + 0.587*g + 0.114*b)

def strokes_from_dark(y0, y1, x0, x1, thr, minrows, name):
    m = luma[y0:y1+1, x0:x1+1] < thr
    cp = m.sum(axis=0)
    cols = [x0+i for i in range(x1-x0+1) if cp[i] >= minrows]
    groups=[]
    for c in cols:
        if groups and c-groups[-1][-1] <= 2: groups[-1].append(c)
        else: groups.append([c])
    out = [(g_[0], g_[-1]) for g_ in groups]
    print(f"{name}: {out}")
    return out

print("== BOX vertical strokes (interior bands, text excluded by row count)")
s1 = strokes_from_dark(129, 145, 150, 895, 215, 13, "ROW1 box strokes")
s2 = strokes_from_dark(197, 215, 150, 895, 200, 13, "ROW2 box strokes")
s3 = strokes_from_dark(275, 292, 150, 895, 215, 12, "ROW3 box strokes")

print()
print("== CONTAINER edges")
# ROW1 black dashes
blk = (r<130)&(g<130)&(b<130)
sub = blk[112:165, :]
cp = sub.sum(axis=0)
cols = [x for x in range(150,899) if cp[x] >= 6]
print("ROW1 container dash columns:", cols[:6], "...", cols[-6:] if len(cols)>6 else "")
rp = blk[112:165, 150:899].sum(axis=1)
print("ROW1 container dash rows:", [112+i for i,v in enumerate(rp) if v>=20])
# ROW2 strong blue dashes
bl = (b-r>55)&(b>110)
sub = bl[180:235, :]
rp = sub.sum(axis=1)
print("ROW2 container dash rows:", [180+i for i,v in enumerate(rp) if v>=30])
cp = bl[186:228, :].sum(axis=0)
cols = [x for x in range(145,899) if cp[x] >= 5]
print("ROW2 container dash cols:", cols[:8], "...", cols[-6:] if len(cols)>6 else "")
# ROW3 strong red dashes
rs = (r>120)&(r-g>40)&(r-b>40)
rp = rs[255:312, 150:899].sum(axis=1)
print("ROW3 container dash rows:", [255+i for i,v in enumerate(rp) if v>=30])
cp = rs[258:305, :].sum(axis=0)
cols = [x for x in range(145,899) if cp[x] >= 5]
print("ROW3 container dash cols:", cols[:8], "...", cols[-6:] if len(cols)>6 else "")

print()
print("== DOTS")
# ROW1 gray dots between x 590..740, y 125..150: gray 150-190
graydot = (abs(r-g)<12)&(abs(g-b)<12)&(r>130)&(r<200)
sub = graydot[120:155, 590:745]
rp = sub.sum(axis=1)
print("ROW1 dot rows:", [(120+i, int(v)) for i,v in enumerate(rp) if v>=3])
cp = sub.sum(axis=0)
runs=[]; inr=False
for i,v in enumerate(cp):
    if v>=2 and not inr: s=i; inr=True
    elif v<2 and inr: runs.append((590+s, 590+i-1)); inr=False
print("ROW1 dot col runs:", runs)
# ROW2 blue dots
bd = (b-r>55)&(b>110)
sub = bd[195:222, 590:745]
cp = sub.sum(axis=0)
runs=[]; inr=False
for i,v in enumerate(cp):
    if v>=2 and not inr: s=i; inr=True
    elif v<2 and inr: runs.append((590+s, 590+i-1)); inr=False
rp = sub.sum(axis=1)
print("ROW2 dot rows:", [(195+i, int(v)) for i,v in enumerate(rp) if v>=3])
print("ROW2 dot col runs:", runs)
