from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_046.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
def bands(mask_counts, thresh, minlen=1):
    out=[]; inb=False; y0=0
    for i,c in enumerate(mask_counts):
        if c>thresh and not inb: inb=True; y0=i
        elif c<=thresh and inb: inb=False; out.append((y0,i-1))
    if inb: out.append((y0,len(mask_counts)-1))
    return [b for b in out if b[1]-b[0]+1>=minlen]
# vertical navy lines: count per column of navy-ish (B>100, R<90, G<90), rows 40..515
sub = a[40:515]
navyish = (sub[:,:,2]>100) & (sub[:,:,0]<90) & (sub[:,:,1]<90)
colcnt = navyish.sum(axis=0)
vb = bands(colcnt, 120)
print('vertical navy-ish lines (cols >120):', vb)
# horizontal navy lines
rowcnt = navyish.sum(axis=1)
hb = bands(rowcnt, 300)
print('horizontal navy-ish bands (rows >300):', [(b[0]+40, b[1]+40) for b in hb])
# red-ish vertical lines
redish = (sub[:,:,0]>110) & (sub[:,:,1]<90) & (sub[:,:,2]<90)
print('vertical red lines (>120):', bands(redish.sum(axis=0), 120))
print('horizontal red bands (>300):', [(b[0]+40, b[1]+40) for b in bands(redish.sum(axis=1), 300)])
# orange-ish
oran = (np.abs(sub[:,:,0]-0xE8)<50) & (np.abs(sub[:,:,1]-0xA0)<50) & (sub[:,:,2]<90)
print('vertical orange (>60):', bands(oran.sum(axis=0), 60))
# gray bar rows restricted to x 200..400 (left of center text)
g = (np.abs(sub[:, 200:400] - 0xD9).max(axis=2) <= 16)
print('gray-band rows in x200..400 (>80):', [(b[0]+40, b[1]+40) for b in bands(g.sum(axis=1), 80)])
# container fill E2EFDA rows x 200..400
cf = (np.abs(sub[:, 200:400] - np.array([0xE2,0xEF,0xDA])).max(axis=2) <= 14)
print('cont-fill rows x200..400 (>80):', [(b[0]+40, b[1]+40) for b in bands(cf.sum(axis=1), 80)])
# green dashed border: green-ish px per row, x 140..900
gr = (sub[:,:,1]>120) & (sub[:,:,0]<110) & (sub[:,:,2]<110)
print('green rows x140..900 (>40):', [(b[0]+40, b[1]+40) for b in bands(gr[:,140:900].sum(axis=1), 40)])
# plus discs dark red rows x 150..880
dr = (np.abs(sub - np.array([0x99,0x00,0x00])).max(axis=2) <= 50)
print('dred rows x150..880 (>30):', [(b[0]+40, b[1]+40) for b in bands(dr[:,150:880].sum(axis=1), 30)])
