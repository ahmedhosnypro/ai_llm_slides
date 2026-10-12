# m8: measure 001 certified render_4 (2001x1125 @150dpi = build space x2.0833) borders,
# and raw pixel profiles of 001:01 frame left border to understand the 38.95 vs 42 gap.
from PIL import Image
import numpy as np

def redness(px):
    r, g, b = px[...,0], px[...,1], px[...,2]
    return np.clip(r - (g + b)/2, 0, None)

def h_centroid(img, x0, x1, y0, y1):
    band = img[y0:y1, x0:x1]
    w = redness(band).sum(axis=0)
    xs = np.arange(x0, x1)
    m = w > w.max()*0.15
    return float((xs[m]*w[m]).sum()/w[m].sum())

def v_centroid(img, y0, y1, x0, x1):
    band = img[y0:y1, x0:x1]
    w = redness(band).sum(axis=1)
    ys = np.arange(y0, y1)
    m = w > w.max()*0.15
    return float((ys[m]*w[m]).sum()/w[m].sum())

rend = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide019/render_4.png').convert('RGB')).astype(float)
print('render size', rend.shape)
L = h_centroid(rend, 70, 105, 200, 900)
R = h_centroid(rend, 1890, 1945, 200, 900)
T = v_centroid(rend, 75, 115, 200, 1800)
B = v_centroid(rend, 1100, 1125, 200, 1800)
print(f'render centroids px: L={L:.2f} R={R:.2f} T={T:.2f} B={B:.2f}')
print(f'  -> build pt (x0.48): L={L*0.48:.2f} (house 42) R={R*0.48:.2f} (919) T={T*0.48:.2f} (45) B={B*0.48:.2f} (540)')

f1 = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg').convert('RGB')).astype(int)
print('001:19 raw profile y=300, x 36..48:')
print('  ' + ' '.join(f'{x}:{tuple(f1[300,x])}' for x in range(36, 49)))
print('001:19 raw profile x=480, y 39..49:')
print('  ' + ' '.join(f'{y}:{tuple(f1[y,480])}' for y in range(39, 50)))
