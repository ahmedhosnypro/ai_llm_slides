from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_014.jpg').convert('RGB')
A = np.asarray(im).astype(int)
H, W, _ = A.shape
# classify per 10x5 px cell
CW, CH = 10, 5
r = A[:,:,0]; g = A[:,:,1]; b = A[:,:,2]
cls = np.full((H,W), '.', dtype='<U1')
red   = (r>150)&(r-g>80)&(r-b>80)
blue  = (b-r>60)&(b-g>50)&(b>110)
green = (g-r>40)&(g-b>40)&(g>110)
mag   = (r-g>50)&(b-g>50)&(r>120)
wheat = (abs(r-242)<18)&(abs(g-222)<15)&(abs(b-184)<18)
peach = (abs(r-245)<14)&(abs(g-203)<16)&(abs(b-167)<18)
pink  = (r>235)&(abs(g-182)<20)&(abs(b-193)<20)&(r-g>50)
pgreen= (g-r>18)&(g-b>18)&(g>215)
yellow= (r>220)&(g>210)&(b<130)
lgreen= (g>210)&(abs(r-144)<40)&(abs(b-144)<45)
lcyan = (abs(r-173)<30)&(abs(g-216)<25)&(abs(b-230)<25)
orange= (r>210)&(abs(g-140)<35)&(b<80)&(g-r<-50)
dark  = (r<95)&(g<95)&(b<95)
for m,c in [(dark,'k'),(red,'R'),(blue,'B'),(mag,'M'),(green,'G'),(orange,'O'),
            (yellow,'Y'),(pink,'P'),(wheat,'w'),(peach,'h'),(pgreen,'n'),
            (lgreen,'l'),(lcyan,'c')]:
    cls[m] = c
Hc, Wc = H//CH, W//CW
print("cols: 1 char = 10px ; rows: 1 char = 5px ; header marks every 100px")
hdr = ''.join(str((i*CW)//100%10) if (i*CW)%100==0 else ' ' for i in range(Wc))
print('     '+hdr)
for j in range(Hc):
    row = []
    for i in range(Wc):
        cell = cls[j*CH:(j+1)*CH, i*CW:(i+1)*CW].ravel()
        vals, counts = np.unique(cell, return_counts=True)
        d = dict(zip(vals, counts))
        d.pop('.', None)
        if not d: row.append('.')
        else:
            # priority: strong inks over fills
            for pri in 'kRBMGOYPlchnw':
                if pri in d: row.append(pri); break
            else: row.append(list(d.items())[0][0])
    print(f"{j*CH:4d} "+''.join(row))
