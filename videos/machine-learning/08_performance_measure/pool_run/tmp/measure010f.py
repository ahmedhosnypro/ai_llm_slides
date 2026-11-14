from PIL import Image
import numpy as np
im = Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/unique_slides/slide_010.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def colrange(x, y0, y1, cond, lab):
    col = a[y0:y1, x]
    m = cond(col)
    ys = np.where(m)[0]
    print(lab, 'x=', x, 'y:', (y0 + ys.min(), y0 + ys.max()) if len(ys) else 'none')

def rowrange(y, x0, x1, cond, lab):
    row = a[y, x0:x1]
    m = cond(row)
    xs = np.where(m)[0]
    print(lab, 'y=', y, 'x:', (x0 + xs.min(), x0 + xs.max()) if len(xs) else 'none')

gray = lambda c: (np.abs(c - 217).sum(axis=1) < 30)
yellow = lambda c: (c[:, 0] > 245) & (c[:, 1] > 230) & (c[:, 2] > 180) & (c[:, 2] < 225)
for x in [620, 630, 640, 650, 656, 660]:
    colrange(x, 111, 176, gray, 'gray band')
for x in [600, 610, 614, 617, 620, 630]:
    colrange(x, 199, 260, yellow, 'meaning box')
for y in [115, 130, 150, 170]:
    rowrange(y, 60, 700, gray, 'gray row')
for y in [205, 230, 250, 256]:
    rowrange(y, 60, 700, yellow, 'meaning row')
