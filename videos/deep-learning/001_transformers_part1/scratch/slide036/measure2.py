from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def cc(mask, name, minpx=200):
    lab, n = ndimage.label(mask)
    out=[]
    for i in range(1, n+1):
        ys, xs = np.where(lab==i)
        if len(xs) < minpx: continue
        w = xs.max()-xs.min(); h = ys.max()-ys.min()
        if w < 20 or h < 8: continue
        out.append((xs.min(), ys.min(), xs.max(), ys.max(), len(xs)))
    out.sort(key=lambda t: (t[1], t[0]))
    print(f'--- {name} ---')
    for o in out:
        print(f'  bbox x{o[0]}..{o[2]} y{o[1]}..{o[3]} (w={o[2]-o[0]} h={o[3]-o[1]}) n={o[4]}  in: x={o[0]/72:.2f} y={o[1]/72:.2f} w={(o[2]-o[0])/72:.2f} h={(o[3]-o[1])/72:.2f}')

def close(target, tol):
    return (abs(a - np.array(target)).sum(axis=-1) <= tol)

cc(close((0,176,80),150), 'GREEN 00B050ish')
cc(close((192,0,0),120), 'RED C00000ish')
cc(close((26,26,26),90), 'BLACK 1A1A1Aish')
cc(close((192,64,192),140), 'MAGENTA C040C0ish')
