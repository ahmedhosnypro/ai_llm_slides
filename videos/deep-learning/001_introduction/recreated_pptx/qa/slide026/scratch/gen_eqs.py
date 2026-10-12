import json, os, sys, importlib.util
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# import the certified renderer's render() with STIX fontset
spec = importlib.util.spec_from_file_location("render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

ASSETS = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets'

EQS = {
 # name: (mathtext, target_ink_bbox_frame_px (x0,y0,x1,y1))
 'eq1a': (r'Net_j = \sum_{i} (w_{ji} O_i)', (113,132,297,169)),
 'eq1b': (r'\dfrac{\partial Net_j}{\partial w_{ji}} = O_i', (364,129,481,175)),
 'eq2':  (r'O_j = f(Net_j) = \dfrac{1}{1+e^{-Net_j}}', (100,194,365,244)),
 'eq3':  (r'E = \dfrac{1}{2}\sum_{j} (t_j - O_j)^2', (102,250,306,296)),
 'eq4':  (r'\Delta w_{ji} = -\eta \dfrac{\partial E}{\partial w_{ji}} = -\eta \dfrac{\partial E}{\partial Net_j} \, \dfrac{\partial Net_j}{\partial w_{ji}}', (109,307,592,364)),
 'eq5':  (r'\Delta w_{ji} = -\eta \dfrac{\partial E}{\partial Net_j} \, O_i', (104,386,390,439)),
 'eq6':  (r'\delta_j = -\dfrac{\partial E}{\partial Net_j}', (605,386,792,439)),
 'eq7':  (r'\Delta w_{ji} = \eta \, \delta_j \, O_i', (126,465,328,489)),
 'eq8':  (r'w_{ji}^{new} = w_{ji}^{old} + \Delta w_{ji}', (564,461,814,490)),
}
DPI=600
results={}
for name,(latex,(x0,y0,x1,y1)) in EQS.items():
    th = (y1-y0+1) * DPI/72.0    # target ink height px @600dpi
    tw = (x1-x0+1) * DPI/72.0
    # trial render at 21pt
    out = os.path.join(ASSETS, f'eq026_{name}.png')
    info = mod.render(latex, out, 21.0, '#000000') if False else None
    # render() uses default fontset (DejaVu); we need STIX -> patch rcParams via wrapper
    def render_stix(latex, out, fs, color):
        matplotlib.rcParams["mathtext.fontset"]="stix"
        return mod.render(latex, out, fs, color)
    info = render_stix(latex, out, 21.0, '#000000')
    ink_h = info['h_px'] - 16
    ink_w = info['w_px'] - 16
    fs2 = 21.0 * th / ink_h
    info = render_stix(latex, out, round(fs2,2), '#000000')
    ink_h2 = info['h_px']-16; ink_w2 = info['w_px']-16
    info['target_frame_bbox']=[x0,y0,x1,y1]
    info['mathtext']=latex
    with open(os.path.join(ASSETS, f'eq026_{name}.json'),'w') as f: json.dump(info,f,indent=1)
    results[name]=dict(fs=round(fs2,2), ink_w=ink_w2, ink_h=ink_h2, tgt_w=int(tw), tgt_h=int(th),
                       w_in=info['w_in'], h_in=info['h_in'], baseline_frac=info['baseline_frac'])
    print(name, 'fs=%.2f'%fs2, 'ink %dx%d vs target %dx%d'%(ink_w2,ink_h2,int(tw),int(th)), 'ratio w=%.3f'%(ink_w2/tw))
json.dump(results, open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide026/scratch/eq_fits.json','w'), indent=1)
