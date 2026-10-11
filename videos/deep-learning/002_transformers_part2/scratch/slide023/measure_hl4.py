from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
X0, X1 = 75, 884   # inside box borders

def runs_of(mask1d, minw=2, merge=8):
    runs=[]; inr=False
    for i, v in enumerate(mask1d):
        if v and not inr: s=i; inr=True
        elif not v and inr:
            if i-s>=minw: runs.append([s,i-1])
            inr=False
    if inr: runs.append([s, len(mask1d)-1])
    mg=[]
    for rn in runs:
        if mg and rn[0]-mg[-1][1]<=merge: mg[-1][1]=rn[1]
        else: mg.append(rn)
    return [(a+X0, bb+X0) for a,bb in mg]

# text line bands: dark ink in x 160..880 (text only), rows 352..505
luma = (0.299*r + 0.587*g + 0.114*b)
ink = luma < 195
prof = ink[:, 160:881].sum(axis=1)
bands=[]; prev=False
for y in range(352, 506):
    v = prof[y] >= 4
    if v and not prev: s=y
    if not v and prev: bands.append((s, y-1))
    prev=v
if prev: bands.append((s,505))
print("text line bands (x160..880):", bands)

for (y0,y1) in bands:
    red  = ((r-g>45)&(r-b>45))[y0:y1+1, X0:X1+1].any(axis=0)
    mag  = ((r-g>60)&(b-g>60))[y0:y1+1, X0:X1+1].any(axis=0)
    blue = ((b-r>45)&(b-g>25))[y0:y1+1, X0:X1+1].any(axis=0)
    inkc = (luma[y0:y1+1, X0:X1+1] < 195).any(axis=0)
    print(f"\nband y{y0}..{y1}:")
    print("  ink x:", runs_of(inkc, 2, 14))
    print("  RED  :", runs_of(red))
    print("  MAG  :", runs_of(mag))
    print("  BLUE :", runs_of(blue))
# bullet dot column zone: x 95..160 for each band
print("\nbullet-zone ink (x90..160) per band:")
for (y0,y1) in bands:
    sub = (luma[y0:y1+1, 90:161] < 195)
    cols = np.where(sub.any(axis=0))[0]
    if len(cols): print(f"  y{y0}..{y1}: x {90+cols.min()}..{90+cols.max()}")
