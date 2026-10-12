from PIL import Image
import numpy as np
def runs(a, y0, y1, test, minlen=4):
    m = test(a[y0:y1]).sum(axis=0) >= (y1-y0)*0.5
    out=[]; s=None
    for x in range(len(m)):
        if m[x] and s is None: s=x
        elif not m[x] and s is not None:
            if x-s>=minlen: out.append((s,x-1))
            s=None
    if s is not None: out.append((s,len(m)-1))
    return out
yel = lambda seg: (seg[:,:,0]>200)&(seg[:,:,1]>200)&(seg[:,:,2]<170)
pnk = lambda seg: (seg[:,:,0]>200)&(seg[:,:,1]>90)&(seg[:,:,1]<210)&(seg[:,:,2]>90)&(seg[:,:,2]<210)&((seg[:,:,0]-seg[:,:,1])>40)
grn = lambda seg: (seg[:,:,1]>150)&(seg[:,:,0]<200)&(seg[:,:,2]<150)&((seg[:,:,1]-seg[:,:,0])>30)
gry = lambda seg: (np.abs(seg[:,:,0]-seg[:,:,1])<12)&(np.abs(seg[:,:,1]-seg[:,:,2])<25)&(seg[:,:,0]>170)&(seg[:,:,0]<235)
def sx(fx): return (fx-17.582)/0.962329
for fname, bands in [('045', [('top',170,181),('mid',275,287),('cont',379,391),('X',483,495)]),
                     ('046', [('final',68,79),('postFFN',175,186),('postLN',281,292),('outatt',387,398),('X',490,501)])]:
    a = np.asarray(Image.open(f'videos/deep-learning/002_transformers_part2/unique_slides/slide_{fname}.jpg').convert('RGB')).astype(int)
    print(f'=== {fname} ===')
    for bname, y0, y1 in bands:
        for cname, test in [('YEL',yel),('GRN',grn),('PNK',pnk),('GRY',gry)]:
            rr = runs(a, y0, y1, test)
            rr = [r for r in rr if 100 < r[0] < 910]
            if rr:
                # merge close runs for display: convert to slide
                print(f'  {bname:8s} {cname}: frame {rr} -> slide {[(round(sx(a1),1), round(sx(b1),1)) for a1,b1 in rr]}')
