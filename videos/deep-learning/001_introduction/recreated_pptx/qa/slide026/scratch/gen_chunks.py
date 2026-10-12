import json, os, importlib.util
import matplotlib
matplotlib.use("Agg")
spec = importlib.util.spec_from_file_location("render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
import numpy as np
from PIL import Image

ASSETS='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets'
PAD=8; DPI=600

# name: (mathtext, anchor_x, mode, anchor_y, band(y0,y1) or None, extra)
# mode 'base': anchor_y = line baseline (frame px); 'bar': anchor_y = fraction bar row.
# band = measured ink band (frame px) for height fitting; None -> use line_fs.
CHUNKS = [
 # tan1 line 1 (baseline 151.5)
 ('c101', r'Net_j \; = \; \sum_{i}', 112, 'base', 151.5, (131,170), None),
 ('c102', r'(w_{ji} \;\, O_i)', 220, 'base', 151.5, (134,158), None),
 ('c103', r'\dfrac{\partial Net_j}{\partial w_{ji}}', 363, 'bar', 152.5, (129,172), None),
 ('c104', r'= \; O_i', 437, 'base', 155.0, (145,162), None),
 # tan1 line 2 (baseline 220.5)
 ('c201', r'O_j \; = \; f(Net_j) \; = \; \dfrac{1}{1+e^{-Net_j}}', 99, 'base', 220.5, (194,244), None),
 # tan1 line 3 (baseline 275.5)
 ('c301', r'E', 102, 'base', 275.5, (262,275), None),
 ('c302', r'=', 116, 'op', 275.5, None, 'L3'),
 ('c303', r'\dfrac{1}{2}', 145, 'bar', 270.5, (250,289), None),
 ('c304', r'\sum_{j}', 162, 'base', 275.5, (256,296), None),
 ('c305', r'(t_j \;\; - \;\; O_j)^2', 200, 'base', 275.5, (255,282), None),
 # chain box (baseline 339.5, bars 333.5)
 ('c401', r'\Delta w_{ji} \; = \; -\eta', 109, 'base', 339.5, (325,346), None),
 ('c402', r'\dfrac{\partial E}{\partial w_{ji}}', 265, 'bar', 333.5, (310,364), None),
 ('c403', r'= \;\; - \;\, \eta', 331, 'base', 339.5, (329,344), None),
 ('c404', r'\dfrac{\partial E}{\partial Net_j}', 409, 'bar', 333.5, (310,364), None),
 ('c405', r'\dfrac{\partial Net_j}{\partial w_{ji}}', 512, 'bar', 333.5, (310,364), None),
 # final box line 1 (baseline 416.5, bars 410)
 ('c501', r'\Delta w_{ji}', 103, 'base', 416.5, (400,425), None),
 ('c502', r'= \;\; - \;\, \eta', 183, 'base', 416.5, (405,425), None),
 ('c503', r'\dfrac{\partial E}{\partial Net_j}', 260, 'bar', 410.0, (386,439), None),
 ('c504', r'O_i', 364, 'base', 416.5, (400,422), None),
 ('c601', r'\delta_j', 604, 'base', 416.5, (399,425), None),
 ('c602', r'= \;\; -', 648, 'op', 416.5, None, 'L5'),
 ('c603', r'\dfrac{\partial E}{\partial Net_j}', 712, 'bar', 410.0, (386,439), None),
 # final box line 2 (baseline 480.5)
 ('c701', r'\Delta w_{ji}', 125, 'base', 480.5, (464,489), None),
 ('c702', r'= \; \eta', 186, 'op', 480.5, None, 'L7'),
 ('c703', r'\delta_j', 229, 'base', 480.5, (465,490), None),
 ('c704', r'O_i', 303, 'base', 480.5, (464,486), None),
 ('c801', r'w_{ji}^{new}', 562, 'base', 480.5, (460,491), None),
 ('c802', r'=', 636, 'op', 480.5, None, 'L8'),
 ('c803', r'w_{ji}^{old}', 658, 'base', 480.5, (460,491), None),
 ('c804', r'+ \; \Delta w_{ji}', 729, 'base', 480.5, (466,491), None),
]

def ink_bbox(png):
    im = Image.open(png); al = np.asarray(im)[:,:,3]
    ink = al > 8
    rows = np.where(ink.any(axis=1))[0]; cols = np.where(ink.any(axis=0))[0]
    return rows, cols, ink

def bar_row(ink, rows, cols):
    # longest horizontal run per row within ink; return row of the longest
    best=(0,-1)
    for r in rows:
        idx=np.where(ink[r])[0]
        if len(idx)==0: continue
        # longest contiguous
        s=p=idx[0]; mx=0
        for i in idx[1:]:
            if i>p+1:
                mx=max(mx,p-s+1); s=i
            p=i
        mx=max(mx,p-s+1)
        if mx>best[1]: best=(r,mx)
    return best

line_fs={}
entries=[]
for name, latex, ax, mode, ay, band, opref in CHUNKS:
    out=os.path.join(ASSETS, f'eq026_{name}.png')
    if band:
        th=(band[1]-band[0]+1)*DPI/72.0
        info=mod.render(latex,out,21.0,'#000000')
        fs=21.0*th/(info['h_px']-16)
        info=mod.render(latex,out,round(fs,2),'#000000')
    else:
        fs=line_fs[opref]
        info=mod.render(latex,out,round(fs,2),'#000000')
    line_fs.setdefault(name, fs)
    if name.startswith('c30') or name in ('c301','c304','c305'): line_fs.setdefault('L3', fs)
    if name in ('c501','c502','c503','c504'): line_fs.setdefault('L5', fs)
    if name in ('c701','c702','c703','c704'): line_fs.setdefault('L7', fs)
    if name in ('c801','c802','c803','c804'): line_fs.setdefault('L8', fs)
    rows, cols, ink = ink_bbox(out)
    iw=int(cols[-1]-cols[0]+1); ih=int(rows[-1]-rows[0]+1)
    e=dict(name=name, mathtext=latex, image=f'eq026_{name}.png',
           fs=round(fs,2), w_in=info['w_in'], h_in=info['h_in'],
           w_px=info['w_px'], h_px=info['h_px'], ink_w=iw, ink_h=ih,
           baseline_frac=info['baseline_frac'], baseline_px=info['baseline_px'],
           anchor_x=ax, mode=mode, anchor_y=ay)
    if mode=='bar':
        br,len_ = bar_row(ink, rows, cols)
        e['bar_row_png']=int(br); e['bar_len']=int(len_)
    entries.append(e)
    tw = f'{ax}..{ax+iw}' 
    print('%s fs=%5.2f ink %3dx%3d anchor x=%d %s y=%s' % (name, fs, iw, ih, ax, tw, ay))

# placement: x_img = anchor_x - (ink_x0)/600*72 ; ink_x0 = cols[0]
man=dict(slides=[dict(slide=1, equations=[])])
for e, (name, latex, ax, mode, ay, band, opref) in zip(entries, CHUNKS):
    png=os.path.join(ASSETS, e['image'])
    rows, cols, ink = ink_bbox(png)
    x_in = (ax - cols[0]*72.0/DPI)
    if mode=='bar':
        y_in = (ay - e['bar_row_png']*72.0/DPI)
    else:
        y_in = (ay - e['baseline_px']*72.0/DPI)
    e['x_in']=round(x_in,4); e['y_in']=round(y_in,4)
    man['slides'][0]['equations'].append(e)
with open(os.path.join(ASSETS,'eq_026_manifest.json'),'w') as f: json.dump(man,f,indent=1)
print('manifest written:', os.path.join(ASSETS,'eq_026_manifest.json'))
