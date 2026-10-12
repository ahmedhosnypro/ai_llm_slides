import json, os, importlib.util
import matplotlib
matplotlib.use("Agg")
spec = importlib.util.spec_from_file_location("render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
import numpy as np
from PIL import Image
ASSETS='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets'
DPI=600
def ink_of(png):
    al=np.asarray(Image.open(png))[:,:,3]; ink=al>8
    rows=np.where(ink.any(axis=1))[0]; cols=np.where(ink.any(axis=0))[0]
    return rows,cols,ink
def bar_row(ink,rows):
    best=(0,-1)
    for r in rows:
        idx=np.where(ink[r])[0]
        if len(idx)==0: continue
        s=p=idx[0]; mx=0
        for i in idx[1:]:
            if i>p+1: mx=max(mx,p-s+1); s=i
            p=i
        mx=max(mx,p-s+1)
        if mx>best[1]: best=(r,mx)
    return best
man=json.load(open(os.path.join(ASSETS,'eq_026_manifest.json')))
BANDS={'c103':(129,172),'c402':(310,364),'c404':(310,364),'c405':(310,364),'c503':(386,439),'c603':(386,439)}
NEWLATEX={'c103':r'\dfrac{\partial \; Net_j}{\partial \; w_{ji}}',
          'c402':r'\dfrac{\partial \; E}{\partial \; w_{ji}}',
          'c404':r'\dfrac{\partial \; E}{\partial \; Net_j}',
          'c405':r'\dfrac{\partial \; Net_j}{\partial \; w_{ji}}',
          'c503':r'\dfrac{\partial \; E}{\partial \; Net_j}',
          'c603':r'\dfrac{\partial \; E}{\partial \; Net_j}'}
for eq in man['slides'][0]['equations']:
    n=eq['name']
    if n in NEWLATEX:
        y0,y1=BANDS[n]; th=(y1-y0+1)*DPI/72.0
        out=os.path.join(ASSETS, eq['image'])
        info=mod.render(NEWLATEX[n],out,21.0,'#000000')
        fs=21.0*th/(info['h_px']-16)
        info=mod.render(NEWLATEX[n],out,round(fs,2),'#000000')
        rows,cols,ink=ink_of(out)
        br,ln=bar_row(ink,rows)
        eq.update(mathtext=NEWLATEX[n], fs=round(fs,2), w_in=info['w_in'], h_in=info['h_in'],
                  ink_w=int(cols[-1]-cols[0]+1), ink_h=int(rows[-1]-rows[0]+1),
                  baseline_frac=info['baseline_frac'], baseline_px=info['baseline_px'],
                  bar_row_png=int(br), bar_len=int(ln),
                  x_in=round(eq['anchor_x']-cols[0]*72.0/DPI,4),
                  y_in=round(eq['anchor_y']-br*72.0/DPI,4))
        print(n,'fs=%.2f ink %dx%d -> x %d..%d'%(fs,eq['ink_w'],eq['ink_h'],eq['anchor_x'],eq['anchor_x']+eq['ink_w']))
json.dump(man, open(os.path.join(ASSETS,'eq_026_manifest.json'),'w'), indent=1)
print('manifest updated')
