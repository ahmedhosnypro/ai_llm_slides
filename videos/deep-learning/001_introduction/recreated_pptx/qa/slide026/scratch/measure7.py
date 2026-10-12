from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def modal(mask, label):
    ys,xs = np.where(mask)
    if len(ys)==0: print(label,'EMPTY'); return
    px = a[ys,xs]
    # strongest ink: darkest 30%
    s = px.sum(axis=1)
    idx = np.argsort(s)[:max(len(s)//3,1)]
    px = px[idx]
    q = Counter(map(tuple,(px//8*8)))
    print(label, 'n=',len(ys), 'modal-dark:', q.most_common(4))

# title line1 red ink
m = (a[:,:,0]>130)&(a[:,:,1]<120)&(a[:,:,2]<120)
modal(m[55:82, 50:840], 'title1-red')
modal(m[210:222, 390:580], 'sigmoid-note-red')
modal(m[385:435, 455:500], 'Let-red')
modal(m[460:490, 455:510], 'then-red')
modal(m[125:175, 310:355], 'arrow1-red')
b = (a[:,:,2]>110)&(a[:,:,0]<110)
modal(b[86:112, 70:886], 'title2-blue')
modal(b[250:292, 340:570], 'only-note-blue')
modal(b[115:122, 74:886], 'container-top-border-blue')
# container side border
modal(b[130:500, 72:76], 'container-left-border')
modal(b[130:500, 884:890], 'container-right-border')
# fills
tan = (a[:,:,0]>190)&(a[:,:,0]<235)&(a[:,:,1]>180)&(a[:,:,1]<225)&(a[:,:,2]>170)&(a[:,:,2]<215)
modal(tan[140:200, 90:300], 'tan-fill')
yel = (a[:,:,0]>232)&(a[:,:,1]>232)&(a[:,:,2]>170)&(a[:,:,2]<225)
modal(yel[315:355, 95:180], 'yellow-fill')
# black text ink
blk = (a.sum(axis=2) < 250)
modal(blk[130:160, 113:297], 'eq1-black-ink')
modal(blk[520:538, 100:900], 'footer-black')

# diagonal arrow fine scan rows 430..465, x 240..320 (thin strokes)
sub = blk[430:466, 230:330]
ys,xs = np.where(sub)
if len(ys):
    print('diag-arrow bbox rows', 430+ys.min(), 430+ys.max(), 'x', 230+xs.min(), 230+xs.max(), 'n', len(ys))
    # endpoints: topmost ink x, bottommost ink x
    top_row = 430+ys.min(); bot_row = 430+ys.max()
    tx = 230+xs[ys==ys.min()].mean(); bx = 230+xs[ys==ys.max()].mean()
    print('  arrow top x~', round(tx,1), 'bottom x~', round(bx,1))
else:
    print('no diag arrow ink in rows430-465 x230-330')
# wider scan for arrow anywhere rows 433..461 full box
sub = blk[433:462, 79:843]
ys,xs = np.where(sub)
if len(ys): print('between-lines ink bbox rows', 433+ys.min(), 433+ys.max(), 'x', 79+xs.min(), 79+xs.max(), 'n', len(ys))

# underline under ONLY: rows 282..292, x 500..560
sub = blk[280:295, 340:570]
ys,xs = np.where(sub)
print('note-area low ink rows', sorted(set((280+ys).tolist()))[:12])
# ONLY region: find 'ONLY' inside blue note (256..282 x343..565): column profile of blue
bn = (a[:,:,2]>110)&(a[:,:,0]<110)
sub = bn[255:285, 340:570]
cols = np.where(sub.sum(axis=0)>0)[0]+340
runs=[]
if len(cols):
    s=cols[0]; p=cols[0]
    for c in cols[1:]:
        if c>p+4: runs.append((int(s),int(p))); s=c
        p=c
    runs.append((int(s),int(p)))
print('blue note word runs:', runs)
