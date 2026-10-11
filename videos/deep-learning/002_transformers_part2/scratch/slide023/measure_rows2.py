from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
X0, X1 = 62, 899

def report(y0, y1, name):
    ys = slice(y0, y1+1)
    print(f"===== {name} (rows {y0}..{y1})")
    ink = (abs(r[ys]-233) + abs(g[ys]-233) + abs(b[ys]-231)) > 60
    ink[:, :X0] = False; ink[:, X1:] = False
    rows = np.where(ink.any(axis=1))[0]
    print("  band y:", y0+rows.min(), "..", y0+rows.max())
    # white pixels (box fills)
    white = (r[ys]>242)&(g[ys]>242)&(b[ys]>242)
    white[:, :X0]=False; white[:, X1:]=False
    wc = white.sum(axis=0)
    runs=[]; inrun=False
    for i,v in enumerate(wc):
        if v>3 and not inrun: start=i; inrun=True
        elif v<=3 and inrun: runs.append((start,i-1)); inrun=False
    if inrun: runs.append((start,len(wc)-1))
    runs=[rn for rn in runs if rn[1]-rn[0]>=8]
    print("  white-box column runs:", runs)
    if runs:
        # row extent of boxes: white rows in first run
        for rn in runs[:2]:
            wr = white[:, rn[0]:rn[1]+1].sum(axis=1)
            rr = [i for i,v in enumerate(wr) if v > (rn[1]-rn[0])*0.5]
            if rr: print(f"    run {rn}: box rows {y0+rr[0]}..{y0+rr[-1]}")
    # left label ink (x < 150)
    lab = ink[:, :150]
    lr = np.where(lab.any(axis=1))[0]; lc = np.where(lab.any(axis=0))[0]
    if len(lr): print("  left-label band y:", y0+lr.min(),"..",y0+lr.max(), " x:", lc.min(),"..",lc.max())

report(108, 165, "ROW1")
report(180, 235, "ROW2")
report(255, 312, "ROW3")
