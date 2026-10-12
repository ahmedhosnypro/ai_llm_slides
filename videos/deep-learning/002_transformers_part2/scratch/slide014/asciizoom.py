from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_014.jpg').convert('RGB')
A = np.asarray(im).astype(int)
r = A[:,:,0]; g = A[:,:,1]; b = A[:,:,2]
cls = np.full(A.shape[:2], '.', dtype='<U1')
red   = (r>150)&(r-g>80)&(r-b>80)
blue  = (b-r>60)&(b-g>50)&(b>110)
green = (g-r>40)&(g-b>40)&(g>110)
mag   = (r-g>50)&(b-g>50)&(r>120)
wheat = (abs(r-242)<18)&(abs(g-222)<15)&(abs(b-184)<18)
peach = (abs(r-245)<16)&(abs(g-203)<18)&(abs(b-167)<20)
pink  = (r>235)&(abs(g-182)<22)&(abs(b-193)<22)&(r-g>45)
pgreen= (g-r>18)&(g-b>18)&(g>215)
yellow= (r>220)&(g>210)&(b<130)
lgreen= (g>210)&(abs(r-144)<40)&(abs(b-144)<45)
lcyan = (abs(r-173)<35)&(abs(g-216)<30)&(abs(b-230)<30)
orange= (r>210)&(g<180)&(b<90)&(r-b>120)
hatch = (abs(r-150)<45)&(abs(g-190)<45)&(abs(b-150)<45)&(g>r+20)&(g>b+20)
dark  = (r<95)&(g<95)&(b<95)
gray  = (abs(r-g)<12)&(abs(g-b)<12)&(r>110)&(r<190)
for m,c in [(dark,'k'),(red,'R'),(blue,'B'),(mag,'M'),(green,'G'),(orange,'O'),
            (yellow,'Y'),(pink,'P'),(wheat,'w'),(peach,'h'),(pgreen,'n'),
            (lgreen,'l'),(lcyan,'c'),(hatch,'s'),(gray,'g')]:
    cls[m] = c

def zoom(x0,y0,x1,y1,cw,ch,label):
    print(f"=== {label}: fx {x0}..{x1}, fy {y0}..{y1} (cell {cw}x{ch}) ===")
    Wc, Hc = (x1-x0)//cw, (y1-y0)//ch
    hdr = ''.join(str(((x0+i*cw))//100%10) if (x0+i*cw)%100<cw else ' ' for i in range(Wc))
    print('     '+hdr)
    for j in range(Hc):
        row=[]
        for i in range(Wc):
            cell = cls[y0+j*ch:y0+(j+1)*ch, x0+i*cw:x0+(i+1)*cw].ravel()
            vals, counts = np.unique(cell, return_counts=True)
            d = dict(zip(vals,counts)); d.pop('.',None)
            if not d: row.append('.')
            else:
                for pri in 'kRBMGOYPlchsngw':
                    if pri in d: row.append(pri); break
                else: row.append(list(d.items())[0][0])
        print(f"{y0+j*ch:4d} "+''.join(row))

zoom(55,95,300,515,3,5,"LEFT PANEL")
zoom(295,240,620,515,3,5,"SCHEMATIC LEFT (Y col + X col)")
zoom(600,240,910,515,3,5,"SCHEMATIC RIGHT (matrix+zero+brace)")
