import importlib.util
import matplotlib
matplotlib.use("Agg")
spec = importlib.util.spec_from_file_location("render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
import numpy as np
from PIL import Image
out='/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide026/scratch/sumtest.png'
info = mod.render(r'\sum_{j}', out, 20, '#000000')
im = Image.open(out); a = np.asarray(im)[:,:,3]>8
print('size',im.size)
rows = np.where(a.any(axis=1))[0]; cols=np.where(a.any(axis=0))[0]
# column profile of bottom third: is there ink below the sigma body, centered?
h = rows[-1]-rows[0]
print('ink h px', h, '-> check bottom-center ink (limits below?)')
bot = a[rows[0]+int(h*0.75):rows[-1]+1]
bc = np.where(bot.any(axis=0))[0]
print('bottom-quarter ink cols:', (bc.min(), bc.max()) if len(bc) else None, 'of full', (cols.min(),cols.max()))
