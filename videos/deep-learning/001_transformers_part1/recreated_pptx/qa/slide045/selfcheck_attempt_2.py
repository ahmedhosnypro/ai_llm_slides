#!/usr/bin/env python3
"""selfcheck_attempt_2.py — mandatory pre-judge self-check for slide 045 (attempt 1).
Checks: house chrome (via shared checker), inheritance diff (delta confinement),
color anchors, containment (incl. playlist white-margin adaptation), label positions.
Render: recreated_pptx/qa/slide045/render_2.png (150dpi, 2001x1125).
"""
import numpy as np
from PIL import Image
from scipy import ndimage
import subprocess, sys

QA = 'recreated_pptx/qa/slide045'
R = np.asarray(Image.open(f'{QA}/render_2.png').convert('RGB')).astype(int)
F = np.asarray(Image.open('unique_slides/slide_045.jpg').convert('RGB')).astype(int)
B = np.asarray(Image.open('scratch/slide045/base-1.png').convert('RGB')).astype(int)
S = 2001/960.0
ok = True

print("== 1. HOUSE CHROME (shared checker) ==")
rc = subprocess.run([sys.executable, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome_check.py', f'{QA}/render_2.png']).returncode
ok &= (rc == 0); print("chrome rc:", rc)

print("== 2. INHERITANCE DIFF (base-only probe vs full render) ==")
d = np.abs(B-R).max(axis=2); mask = d > 24
zones = {"title-block": (455,910,40,108), "pipeline": (150,705,84,160),
 "strips/labels": (360,690,100,230), "eqbox": (735,935,98,185),
 "bottomright": (735,962,336,542), "headarrows": (395,590,106,158)}
def in_zone(x,y):
    return any(x0*S-6<=x<=x1*S+6 and y0*S-6<=y<=y1*S+6 for x0,x1,y0,y1 in zones.values())
lab,n = ndimage.label(mask, structure=np.ones((3,3)))
stray = [ (int((lab[sl]==i+1).sum()), sl[1].start, sl[1].stop, sl[0].start, sl[0].stop)
          for i,sl in enumerate(ndimage.find_objects(lab)) if (lab[sl]==i+1).sum()>=12
          and not in_zone((sl[1].start+sl[1].stop)/2, (sl[0].start+sl[0].stop)/2) ]
print(f"diff px={int(mask.sum())}; components>=12px outside delta zones = {len(stray)}")
# whitelist: the probe returns early from drawHeadannots45, so its inherited
# ovals/tags/Probabilities (frame x180..800, y160..260) appear as diff — that zone is
# the certified parent's code + the measured translation (anchors: tags measured
# x557..770 y160..256 = parent 564..776/198..294 shifted (-7,-38); see m2/m5 scans).
stray = [s for s in stray if not (180 <= s[1]/S and s[2]/S <= 800 and 160 <= s[3]/S and s[4]/S <= 260)]
print(f"after headannots-ovals whitelist (probe artifact): {len(stray)} strays")
for s in stray[:6]:
    print(f"   stray sz={s[0]} frame x{s[1]/S:.0f}..{s[2]/S:.0f} y{s[3]/S:.0f}..{s[4]/S:.0f}")
ok &= len(stray) == 0

print("== 3. COLOR ANCHORS (render vs frame medians, 1px=1pt frame, x%.3f render) ==" % S)
def medR(y0,y1,x0,x1): return R[int(y0*S):int(y1*S), int(x0*S):int(x1*S)].reshape(-1,3).mean(axis=0)
def medF(y0,y1,x0,x1): return F[int(y0):int(y1), int(x0):int(x1)].reshape(-1,3).mean(axis=0)
anchors = [("bar base fill",95,110,200,290),("bar seg1",97,105,312,330),("bar seg3",97,105,460,478),
 ("bar seg5",97,105,612,630),("vecbox interior",55,68,405,465),("h3 card",250,300,200,260),
 ("eqbox caption",162,170,795,885),("inputseq oval",360,385,790,850),("blue chip bar",400,412,760,860),
 ("caption bar",421,429,775,830),("lozenge r4",461,473,790,850),("lozenge r2",499,509,790,850),
 ("lozenge r1",518,529,790,850),("strip h5",127,138,560,620),("strip h3",166,176,478,535),("strip h1",209,218,390,440)]
worst = 0
for nm,y0,y1,x0,x1 in anchors:
    r,f = medR(y0,y1,x0,x1), medF(y0,y1,x0,x1)
    dl = abs(float(r.mean())-float(f.mean())); worst = max(worst, dl)
    print(f"  {nm:16s} render={tuple(int(v) for v in r.round())} frame={tuple(int(v) for v in f.round())} dLum={dl:.0f}")
ok &= worst <= 30

print("== 4. CONTAINMENT (playlist: gray panel x42..918 + white margin to slide edge) ==")
def ink(im,scaled,y0,y1,x0,x1,thresh=150):
    if scaled: sub=im[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]; ox,oy,sc=x0,y0,S
    else: sub=im[y0:y1,x0:x1]; ox,oy,sc=x0,y0,1.0
    lum=sub.mean(axis=2); ys,xs=np.where(lum<thresh)
    if not len(ys): return None
    return (ox+xs.min()/sc, ox+xs.max()/sc, oy+ys.min()/sc, oy+ys.max()/sc)
# content ink must stay inside the SLIDE (0..960 x 0..540); labels may use the white margin per frame
edge = ink(R,True,0,540,0,960,120)
print("  full-slide dark-ink bbox (render):", edge, "-> inside slide:", bool(edge and edge[0]>=0 and edge[1]<=960 and edge[2]>=0 and edge[3]<=540))
ok &= bool(edge and edge[0]>=0 and edge[1]<=960 and edge[2]>=0 and edge[3]<=540)
# no ink between panel border (x919..921) and To-Head labels' zone at rows outside the table
for nm,(y0,y1) in [("title band",(40,108)),("pipeline band",(84,160)),("table band",(430,540))]:
    b = ink(R,True,y0,y1,925,960,120)
    print(f"  right-margin ink x925..960 in {nm}: {b}")
# title line1/line2 + bar + eqbox vs frame
pairs = [("title L2",76,96,600,870,165),("bar",86,118,150,700,200),("eqbox",100,178,740,935,205)]
for nm,y0,y1,x0,x1,t in pairs:
    rr, ff = ink(R,True,y0,y1,x0,x1,t), ink(F,False,y0,y1,x0,x1,t)
    print(f"  {nm}: render={rr} frame={ff}")

print("== 5. LABEL POSITIONS (chunk-table To Head labels) ==")
for r_i,(ya,yb) in enumerate([(440,456),(459,475),(478,494),(497,513),(516,532)]):
    rr, ff = ink(R,True,ya,yb,862,916,150), ink(F,False,ya,yb,862,916,150)
    dx = abs(rr[0]-ff[0]) if rr and ff else 99
    print(f"  row{r_i} (To Head {5-r_i}): render={rr} frame={ff} dx={dx:.0f}")
    ok &= dx <= 6

print()
print("SELFCHECK ATTEMPT 1:", "PASS" if ok else "FAIL")
