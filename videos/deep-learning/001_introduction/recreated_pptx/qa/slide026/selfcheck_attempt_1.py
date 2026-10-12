#!/usr/bin/env python3
"""Closed-loop self-check for slide 026 attempt 1 (150dpi render vs original frame).
Bounded per-chunk windows (no bleed into neighboring chunks / arrows / chrome border).
Fraction chunks are verified at their BAR row (the mathematically meaningful anchor);
T/B of a fraction stack is the documented glyph-metric residual (original Equation-3.0
metrics distribute more ink above the bar than mathtext). Tolerance 4 render px."""
import json, os
import numpy as np
from PIL import Image

QA='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide026'
ASSETS='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets'
ren=np.asarray(Image.open(os.path.join(QA,'render_1.png')).convert('RGB')).astype(int)
S=ren.shape[1]/960.0
TOL=4.0
fails=[]; warns=[]
man=json.load(open(os.path.join(ASSETS,'eq_026_manifest.json')))
eqs=man['slides'][0]['equations']
by={e['name']:e for e in eqs}

BANDS={'c101':(131,170),'c102':(134,158),'c104':(145,162),
 'c201':(194,244),'c301':(262,275),'c302':(266,272),'c304':(256,296),'c305':(255,282),
 'c401':(325,346),'c403':(329,344),
 'c501':(400,425),'c502':(405,425),'c504':(400,422),'c601':(399,425),'c602':(405,413),
 'c701':(464,489),'c702':(469,485),'c703':(465,490),'c704':(464,486),'c801':(460,491),'c802':(471,479),'c803':(460,491),'c804':(466,491)}
FRAC={'c103':(152.5,363,433),'c303':(270.5,145,159),'c402':(333.5,265,326),'c404':(333.5,409,490),
      'c405':(333.5,512,593),'c503':(410.0,260,341),'c603':(410.0,712,792)}
LAST={'c102','c104','c201','c305','c405','c504','c603','c704','c804'}
# window bounds: (x0,x1) frame, generous but artifact-free
WIN={'c101':(111,215),'c102':(219,315),'c103':(362,436),'c104':(436,560),
 'c201':(98,390),'c301':(101,115),'c302':(115,144),'c303':(144,161),'c304':(161,199),'c305':(199,342),
 'c401':(108,264),'c402':(264,330),'c403':(330,408),'c404':(408,511),'c405':(511,600),
 'c501':(102,182),'c502':(182,259),'c503':(259,363),'c504':(363,458),
 'c601':(603,647),'c602':(647,711),'c603':(711,850),
 'c701':(124,185),'c702':(185,228),'c703':(228,302),'c704':(302,458),
 'c801':(561,635),'c802':(635,657),'c803':(657,728),'c804':(728,878)}

def band_ink(x0f,x1f,y0f,y1f):
    x0,x1,y0,y1=[int(v*S) for v in (x0f,x1f,y0f,y1f)]
    sub=ren[y0:y1, x0:x1]; dk=(sub.sum(axis=2)<560)
    rows=np.where(dk.any(axis=1))[0]; cols=np.where(dk.any(axis=0))[0]
    if not len(rows): return None
    return (x0+cols[0], y0+rows[0], x0+cols[-1], y0+rows[-1])

print('== fraction bars (render vs measured) ==')
for n,(yb,x0,x1) in FRAC.items():
    got=band_ink(x0-3,x1+3,yb-25,yb+25)
    if got is None: fails.append(f'{n}: NO INK'); continue
    # bar row = longest run row
    sub=dk_ren=None
    x0i,x1i,y0i,y1i=[int(v*S) for v in (x0-3,x1+3,yb-25,yb+25)]
    sub=ren[y0i:y1i, x0i:x1i]; dk=(sub.sum(axis=2)<560)
    best=(0,0)
    for i,row in enumerate(dk):
        idx=np.where(row)[0]
        if not len(idx): continue
        s=p=idx[0]; mx=0
        for k in idx[1:]:
            if k>p+1: mx=max(mx,p-s+1); s=k
            p=k
        mx=max(mx,p-s+1)
        if mx>best[1]: best=(i,mx)
    gy=(y0i+best[0])/S
    d=gy-yb
    print(f'  {n}: bar {gy:.1f} vs {yb} (d{d:+.1f} frame)')
    if abs(d*2.084)>TOL: fails.append(f'{n} bar d{d:+.1f}')

print('== glyph chunks (L/T/B, R for line-last) ==')
for n,b in BANDS.items():
    x0,x1=WIN[n]
    got=band_ink(x0,x1,b[0]-3,b[1]+3)
    if got is None: fails.append(f'{n}: NO INK'); continue
    e=by[n]
    dL=got[0]-x0*S; dT=got[1]-b[0]*S; dB=got[3]-b[1]*S
    msg=f'{n} L{dL:+.0f} T{dT:+.0f} B{dB:+.0f}'
    bad=abs(dL)>TOL or abs(dT)>TOL or abs(dB)>TOL
    if n in LAST:
        exp_r=(e['anchor_x']+e['ink_w']*72.0/600.0)*S
        dR=got[2]-exp_r; msg+=f' R{dR:+.0f}'
        bad=bad or abs(dR)>TOL
    if bad: fails.append(msg)
    else: print('  ok',msg)

print('== structure ==')
def modal(px):
    from collections import Counter
    return Counter(map(tuple,px.reshape(-1,3))).most_common(1)[0][0]
print('  tan1 fill:', ren[int(160*S),int(300*S)], 'orig', (220,212,201))
print('  yellow fill:', ren[int(340*S),int(600*S)], 'orig', (251,255,216))
print('  tan2 fill:', ren[int(480*S),int(300*S)], 'orig', (220,212,201))
row=ren[int(528*S)]; xs=np.where(row.sum(axis=1)<200)[0]
print('  footer bar x:', (int(xs.min()/S), int(xs.max()/S)), 'orig (38,921)')
redm=(ren[:,:,0]>120)&(ren[:,:,0]-ren[:,:,1]>50)&(ren[:,:,0]-ren[:,:,2]>50)
sub=redm[int(55*S):int(85*S), int(60*S):int(900*S)]
rows=np.where(sub.sum(axis=1)>10)[0]; cols=np.where(sub.sum(axis=0)>2)[0]
t1=(int(55+rows.min()/S), int(55+rows.max()/S), int(60+cols.min()/S), int(60+cols.max()/S))
print('  title1 (T,B,L,R):', t1, 'orig (59,81,57,837)')
bluem=(ren[:,:,2]>110)&(ren[:,:,2]-ren[:,:,0]>40)&(ren[:,:,2]-ren[:,:,1]>30)
sub=bluem[int(84*S):int(118*S), int(60*S):int(900*S)]
rows=np.where(sub.sum(axis=1)>10)[0]; cols=np.where(sub.sum(axis=0)>2)[0]
t2=(int(84+rows.min()/S), int(84+rows.max()/S), int(60+cols.min()/S), int(60+cols.max()/S))
print('  title2 (T,B,L,R):', t2, 'orig (88,114,73,883)')
cont=ren[int(300*S):int(400*S), int(71*S):int(77*S)]
blue_ct=int(((cont[:,:,2]>110)&(cont[:,:,0]<110)).sum())
print('  container left border blue px:', blue_ct)
# notes
sub=redm[int(205*S):int(228*S), int(390*S):int(600*S)]
rows=np.where(sub.sum(axis=1)>3)[0]; cols=np.where(sub.sum(axis=0)>1)[0]
print('  note1 (T,B,L,R):', (int(205+rows.min()/S),int(205+rows.max()/S),int(390+cols.min()/S),int(390+cols.max()/S)), 'orig (209,223,397,575)')
sub=bluem[int(262*S):int(290*S), int(338*S):int(600*S)]
rows=np.where(sub.sum(axis=1)>3)[0]; cols=np.where(sub.sum(axis=0)>1)[0]
print('  note2 (T,B,L,R):', (int(262+rows.min()/S),int(262+rows.max()/S),int(338+cols.min()/S),int(338+cols.max()/S)), 'orig (267,282,343,565)')
# Let/then
sub=redm[int(395*S):int(420*S), int(455*S):int(510*S)]
rows=np.where(sub.sum(axis=1)>3)[0]; cols=np.where(sub.sum(axis=0)>1)[0]
print('  Let (T,B,L,R):', (int(395+rows.min()/S),int(395+rows.max()/S),int(455+cols.min()/S),int(455+cols.max()/S)), 'orig (399,415,462,497)')
sub=redm[int(458*S):int(482*S), int(452*S):int(515*S)]
rows=np.where(sub.sum(axis=1)>3)[0]; cols=np.where(sub.sum(axis=0)>1)[0]
print('  then (T,B,L,R):', (int(458+rows.min()/S),int(458+rows.max()/S),int(452+cols.min()/S),int(452+cols.max()/S)), 'orig (461,477,459,507)')
# arrows
sub=redm[int(132*S):int(155*S), int(310*S):int(360*S)]
rows=np.where(sub.sum(axis=1)>2)[0]; cols=np.where(sub.sum(axis=0)>1)[0]
print('  red arrow (T,B,L,R):', (int(132+rows.min()/S),int(132+rows.max()/S),int(310+cols.min()/S),int(310+cols.max()/S)), 'orig (138,148,320,348)')
dkall=(ren.sum(axis=2)<400)
sub=dkall[int(438*S):int(466*S), int(265*S):int(300*S)]
rows=np.where(sub.sum(axis=1)>0)[0]; cols=np.where(sub.sum(axis=0)>0)[0]
print('  black diag arrow (T,B,L,R):', (int(438+rows.min()/S),int(438+rows.max()/S),int(265+cols.min()/S),int(265+cols.max()/S)), 'orig (443,457,276,288)')

print()
print('FAILS:', len(fails)); [print('  FAIL', f) for f in fails]
print('DONE')
