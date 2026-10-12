# m7: measure 001:19 frame's own chrome landmarks (is its capture exactly slide space?)
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

for tag, path in [('001:19', '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg'),
                  ('001:01', '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_001.jpg')]:
    im = np.asarray(Image.open(path).convert('RGB')).astype(float)
    L = h_centroid(im, 35, 50, 100, 450)
    R = h_centroid(im, 912, 928, 100, 450)
    T = v_centroid(im, 38, 53, 100, 850)
    B = v_centroid(im, 530, 540, 100, 850)
    print(f'{tag}: L={L:.2f} (house 42)  R={R:.2f} (919)  T={T:.2f} (45)  B={B:.2f} (540)')
