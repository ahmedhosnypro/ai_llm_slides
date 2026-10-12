import json, os, importlib.util
import matplotlib
matplotlib.use("Agg")
spec = importlib.util.spec_from_file_location("render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
import numpy as np
from PIL import Image

ASSETS='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets'
DPI=600
# per-line font sizes (from clean cap-height fits, DejaVu cap 0.729em)
LINE_FS={'L1':19.2,'L2':20.0,'L3':19.0,'L4':19.4,'L5':19.9,'L6':19.9,'L7':20.2,'L8':20.0}
# name: (mathtext, anchor_x, mode, anchor_y, fit) ; fit = band(y0,y1) | ('line',L) | number
CHUNKS = [
 ('c101', r'Net_j \; = \; \sum_{i}', 112, 'base', 151.5, (131,170)),
 ('c102', r'(w_{ji} \;\, O_i)', 220, 'base', 151.5, ('line','L1')),
 ('c103', r'\dfrac{\partial Net_j}{\partial w_{ji}}', 363, 'bar', 152.5, (129,172)),
 ('c104', r'= \; O_i', 437, 'base', 158.5, ('line','L1')),
 ('c201', r'O_j \; = \; f(Net_j) \; = \; \dfrac{1}{1+e^{-Net_j}}', 99, 'base', 220.5, 20.0),
 ('c301', r'E', 102, 'base', 275.5, ('line','L3')),
 ('c302', r'=', 116, 'base', 275.5, ('line','L3')),
 ('c303', r'\dfrac{1}{2}', 145, 'bar', 270.5, (250,289)),
 ('c304', r'\sum_{j}', 162, 'base', 275.5, (256,296)),
 ('c305', r'(t_j \;\; - \;\; O_j)^2', 200, 'base', 275.5, ('line','L3')),
 ('c401', r'\Delta w_{ji} \; = \; -\eta', 109, 'base', 339.5, ('line','L4')),
 ('c402', r'\dfrac{\partial E}{\partial w_{ji}}', 265, 'bar', 333.5, (310,364)),
 ('c403', r'= \;\; - \;\, \eta', 331, 'base', 339.5, ('line','L4')),
 ('c404', r'\dfrac{\partial E}{\partial Net_j}', 409, 'bar', 333.5, (310,364)),
 ('c405', r'\dfrac{\partial Net_j}{\partial w_{ji}}', 512, 'bar', 333.5, (310,364)),
 ('c501', r'\Delta w_{ji}', 103, 'base', 416.5, ('line','L5')),
 ('c502', r'= \;\; - \;\, \eta', 183, 'base', 416.5, ('line','L5')),
 ('c503', r'\dfrac{\partial E}{\partial Net_j}', 260, 'bar', 410.0, (386,439)),
 ('c504', r'O_i', 364, 'base', 416.5, ('line','L5')),
 ('c601', r'\delta_j', 604, 'base', 416.5, ('line','L5')),
 ('c602', r'= \;\; -', 648, 'base', 416.5, ('line','L5')),
 ('c603', r'\dfrac{\partial E}{\partial Net_j}', 712, 'bar', 410.0, (386,439)),
 ('c701', r'\Delta w_{ji}', 125, 'base', 480.5, ('line','L7')),
 ('c702', r'= \; \eta', 186, 'base', 480.5, ('line','L7')),
 ('c703', r'\delta_j', 229, 'base', 480.5, ('line','L7')),
 ('c704', r'O_i', 303, 'base', 480.5, ('line','L7')),
 ('c801', r'w_{ji}^{new}', 562, 'base', 480.5, ('line','L8')),
 ('c802', r'=', 636, 'base', 480.5, ('line','L8')),
 ('c803', r'w_{ji}^{old}', 658, 'base', 480.5, ('line','L8')),
 ('c804', r'+ \; \Delta w_{ji}', 729, 'base', 480.5, ('line','L8')),
]

def ink_of(png):
    al = np.asarray(Image.open(png))[:,:,3]; ink = al>8
    rows=np.where(ink.any(axis=1))[0]; cols=np.where(ink.any(axis=0))[0]
    return rows,cols,ink

def bar_row(ink, rows):
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

entries=[]
for name, latex, ax, mode, ay, fit in CHUNKS:
    out=os.path.join(ASSETS, f'eq026_{name}.png')
    if isinstance(fit, tuple) and isinstance(fit[0], int):
        th=(fit[1]-fit[0]+1)*DPI/72.0
        info=mod.render(latex,out,21.0,'#000000')
        fs=21.0*th/(info['h_px']-16)
        info=mod.render(latex,out,round(fs,2),'#000000')
    elif isinstance(fit, tuple):
        fs=LINE_FS[fit[1]]
        info=mod.render(latex,out,round(fs,2),'#000000')
    else:
        fs=fit; info=mod.render(latex,out,round(fs,2),'#000000')
    rows,cols,ink=ink_of(out)
    iw=int(cols[-1]-cols[0]+1); ih=int(rows[-1]-rows[0]+1)
    e=dict(name=name,mathtext=latex,image=f'eq026_{name}.png',fs=round(fs,2),
           w_in=info['w_in'],h_in=info['h_in'],ink_w=iw,ink_h=ih,
           baseline_frac=info['baseline_frac'],baseline_px=info['baseline_px'],
           anchor_x=ax,mode=mode,anchor_y=ay)
    if mode=='bar':
        br,ln=bar_row(ink,rows); e['bar_row_png']=int(br); e['bar_len']=int(ln)
    e['x_in']=round(ax - cols[0]*72.0/DPI, 4)
    if mode=='bar':
        e['y_in']=round(ay - e['bar_row_png']*72.0/DPI, 4)
    else:
        e['y_in']=round(ay - e['baseline_px']*72.0/DPI, 4)
    entries.append(e)
    print('%s fs=%5.2f ink %3dx%3d  x %d..%d  (target span from %d)' % (name,fs,iw,ih,ax,ax+iw,ax))
man=dict(slides=[dict(slide=1, equations=entries)])
with open(os.path.join(ASSETS,'eq_026_manifest.json'),'w') as f: json.dump(man,f,indent=1)
print('manifest ok')
