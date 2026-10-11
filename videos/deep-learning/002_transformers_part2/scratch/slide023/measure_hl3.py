from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
luma = (0.299*r + 0.587*g + 0.114*b)

bands = [("L?", 352,386),("P", 388,406),("B1", 410,430),("B2", 432,452),("B3", 454,474),("B4", 476,500)]
for name, y0, y1 in bands:
    red  = (r[y0:y1+1]-g[y0:y1+1]>45)&(r[y0:y1+1]-b[y0:y1+1]>45)
    mag  = (r[y0:y1+1]-g[y0:y1+1]>60)&(b[y0:y1+1]-g[y0:y1+1]>60)
    blue = (b[y0:y1+1]-r[y0:y1+1]>45)&(b[y0:y1+1]-g[y0:y1+1]>25)&(luma[y0:y1+1]<185)
    for cname, m in (("RED",red),("MAG",mag),("BLU",blue)):
        cols = np.where(m.any(axis=0))[0]
        if len(cols)==0: continue
        # x runs
        runs=[]; inr=False
        for x in range(74, 890):
            v = m[:, x-74].sum() if x-74 < m.shape[1] else 0
            if v>0 and not inr: s=x; inr=True
            elif v==0 and inr:
                if x-s>=2: runs.append((s,x-1))
                inr=False
        if inr: runs.append((s,889))
        # merge runs with gaps<8
        mg=[]
        for rn in runs:
            if mg and rn[0]-mg[-1][1]<=8: mg[-1]=(mg[-1][0], rn[1])
            else: mg.append(list(rn)); mg[-1]=tuple(mg[-1])
            mg[-1]=list(mg[-1])
        mg=[tuple(x) for x in mg]
        print(f"{name} {cname}: runs {mg}")
    print()
