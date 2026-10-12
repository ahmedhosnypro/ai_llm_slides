import json, os, importlib.util
import matplotlib
matplotlib.use("Agg")
spec = importlib.util.spec_from_file_location("render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)   # default fontset = DejaVu (certified default)
ASSETS = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets'
EQS = {
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
DPI=600; results={}
for name,(latex,(x0,y0,x1,y1)) in EQS.items():
    th = (y1-y0+1)*DPI/72.0; tw=(x1-x0+1)*DPI/72.0
    out = os.path.join(ASSETS, f'eq026_{name}.png')
    info = mod.render(latex, out, 21.0, '#000000')
    fs2 = 21.0*th/(info['h_px']-16)
    info = mod.render(latex, out, round(fs2,2), '#000000')
    iw=info['w_px']-16; ih=info['h_px']-16
    info.update(mathtext=latex, target_frame_bbox=[x0,y0,x1,y1])
    json.dump(info, open(os.path.join(ASSETS,f'eq026_{name}.json'),'w'), indent=1)
    results[name]=dict(fs=round(fs2,2), ink_w=iw, ink_h=ih, tgt_w=int(tw), tgt_h=int(th),
                       w_in=info['w_in'], h_in=info['h_in'], baseline_frac=info['baseline_frac'])
    print('%s fs=%.2f ink %dx%d tgt %dx%d ratio w=%.3f h=%.3f' % (name,fs2,iw,ih,int(tw),int(th),iw/tw,ih/th))
json.dump(results, open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide026/scratch/eq_fits.json','w'), indent=1)
