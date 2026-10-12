from PIL import Image
import numpy as np
from scipy import ndimage
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def flood(seed, tol=26, label=""):
    x, y = seed
    t = a[y, x].copy()
    m = np.abs(a - t).max(axis=2) <= tol
    lab, n = ndimage.label(m)
    L = lab[y, x]
    if L == 0:
        print(f"{label}: seed {seed} color {tuple(t)} -> no region (tol {tol})")
        return
    ys, xs = np.where(lab == L)
    med = np.median(a[ys, xs], axis=0).astype(int)
    print(f"{label:28s} seed={seed} fill#{med[0]:02X}{med[1]:02X}{med[2]:02X} bbox x[{xs.min()}..{xs.max()+1}) y[{ys.min()}..{ys.max()+1}) w={xs.max()-xs.min()+1} h={ys.max()-ys.min()+1} px={len(xs)}")

# candidate seeds (from label text positions and structure)
flood((110, 230), 26, "InputSamples box")
flood((240, 225), 26, "Pre processing box")
flood((360, 225), 26, "FeatureExtraction box")
flood((470, 225), 26, "FeatureSelection box")
flood((580, 235), 26, "Classification box")
flood((695, 225), 26, "PredictedLabels box")
flood((772, 220), 26, "PredictionError box")
flood((860, 230), 26, "SamplesLabels box")
flood((420, 130), 26, "ellipse")
flood((680, 280), 26, "area below predicted labels")
flood((300, 360), 26, "green annotation box")
flood((790, 400), 26, "starburst fill")
flood((130, 160), 26, "canvas white area left")
flood((500, 300), 26, "canvas white lower middle")
flood((600, 160), 26, "canvas white upper right")
