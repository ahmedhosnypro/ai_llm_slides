import importlib.util, json
import matplotlib
matplotlib.use("Agg")
spec = importlib.util.spec_from_file_location("render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
import numpy as np
from PIL import Image
eq5 = r'\Delta w_{ji} = -\eta \dfrac{\partial E}{\partial Net_j} \, O_i'
for fontset in ('dejavusans','dejavuserif','stix','cm'):
    matplotlib.rcParams["mathtext.fontset"]=fontset
    out=f'/tmp/eq5_{fontset}.png'.replace('/tmp','/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide026/scratch')
    info = mod.render(eq5, out, 21.38, '#000000')
    print(fontset, 'ink %dx%d -> frame %.0fx%.0f' % (info['w_px']-16, info['h_px']-16, (info['w_px']-16)/600*72, (info['h_px']-16)/600*72), 'target 287x54')
