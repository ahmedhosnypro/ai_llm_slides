from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def modal_color(mask, label):
    ys,xs = np.where(mask)
    if len(ys)==0: print(label,'EMPTY'); return
    px = a[ys,xs]
    q = Counter(map(tuple,(px//8*8)))
    print(label, 'n=',len(ys), 'modal:', q.most_common(5))

R = a[:,:,0]; G = a[:,:,1]; B = a[:,:,2]
redm  = (R-G>50)&(R-B>50)&(R>120)
bluem = (B-R>50)&(B-G>40)&(B>120)
modal_color(redm[55:82, 50:840], 'title1-red')
modal_color(redm[210:222, 390:580], 'sigmoid-note-red')
modal_color(redm[387:432, 460:500], 'Let-red')
modal_color(redm[462:488, 457:510], 'then-red')
modal_color(redm[128:165, 315:350], 'arrow1-red')
modal_color(bluem[86:112, 70:886], 'title2-blue')
modal_color(bluem[255:285, 340:570], 'only-note-blue')
modal_color(bluem[117:121, 200:700], 'container-top-border')
modal_color(bluem[200:400, 72:77], 'container-left-border')
modal_color(bluem[200:400, 884:889], 'container-right-border')
tanm = (R-G>-15)&(R-G<25)&(R-B>5)&(R-B<35)&(R>195)&(R<232)&(G>188)&(G<225)
modal_color(tanm[140:200, 90:300], 'tan-fill')
yelbm = (R>240)&(G>240)&(B>185)&(B<225)
modal_color(yelbm[315:350, 95:175], 'yellow-fill')
blk = (a.sum(axis=2)<250)
modal_color(blk[132:158, 115:295], 'eq-ink')
modal_color(blk[522:537, 200:800], 'footer')

# cap heights: helper measuring ink rows in a column window
def glyph_band(y0,y1,x0,x1,mask=None,thr=330):
    m = (a[y0:y1, x0:x1].sum(axis=2)<thr) if mask is None else mask[y0:y1,x0:x1]
    rows = np.where(m.sum(axis=1)>0)[0]
    cols = np.where(m.sum(axis=0)>0)[0]
    return (y0+rows.min(), y0+rows.max(), x0+cols.min(), x0+cols.max()) if len(rows) else None

print('title1 U glyph:', glyph_band(50,85, 55,80))
print('title1 p (desc):', glyph_band(50,85, 95,115))   # 'p' of Update
print('title2 G glyph:', glyph_band(80,125, 72,98))
print('title2 d asc?:', glyph_band(80,125, 250,270))
# eq1: N of Net (x113..)
print('eq1 N:', glyph_band(125,175, 112,133))
print('eq1 e:', glyph_band(125,175, 134,148))
print('eq1 t:', glyph_band(125,175, 148,160))
print('eq1 sum-region:', glyph_band(125,175, 165,210))
print('eq1 right: partial-frac N:', glyph_band(125,175, 364,390))
# eq2: O of O_j
print('eq2 O:', glyph_band(200,250, 98,122))
print('eq2 frac region:', glyph_band(200,250, 230,300))
# eq3: E
print('eq3 E:', glyph_band(250,295, 100,122))
print('eq3 sum:', glyph_band(250,295, 125,165))
# chain: D of Delta (x109)
print('chain Delta:', glyph_band(303,362, 107,140))
print('chain frac1 bar rows:', glyph_band(325,345, 250,300))
# final1: Delta
print('final1 Delta:', glyph_band(382,437, 102,135))
print('final1 frac:', glyph_band(382,437, 261,341))
print('final2 Delta:', glyph_band(455,495, 124,157))
# Let/then glyph bands
print('Let:', glyph_band(387,435, 460,500))
print('then:', glyph_band(460,492, 457,510))
# diag arrow per-row centers
blk2 = (a.sum(axis=2)<380)
print('arrow rows detail:')
for y in range(428,468):
    xs = np.where(blk2[y, 230:340])[0]
    if len(xs): print('  y',y,'x', 230+xs.min(), 230+xs.max(), 'n', len(xs))
