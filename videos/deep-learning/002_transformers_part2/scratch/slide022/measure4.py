from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB')).astype(int)

def xprofile(y0, y1, label, x0=40, x1=920, darkthr=170):
    band = im[y0:y1, x0:x1]
    lum = band.mean(axis=2)
    dark = (lum < darkthr).mean(axis=0)
    xs = np.arange(x0, x1)
    on = dark > 0.5
    # runs
    runs = []
    s = None
    for i, v in enumerate(on):
        if v and s is None: s = i
        if not v and s is not None:
            runs.append((xs[s], xs[i-1])); s = None
    if s is not None: runs.append((xs[s], xs[-1]))
    print(f"{label} y[{y0},{y1}] dark-x runs (n={len(runs)}):", runs[:24])

# the lines seen in scan
xprofile(109, 114, "blue line  ")
xprofile(117, 121, "gray line A")
xprofile(155, 159, "gray line B")
xprofile(185, 199, "blue line C")
# title ink bbox
def inkbbox(y0, y1, x0=40, x1=920, thr=150):
    band = im[y0:y1, x0:x1]
    lum = band.mean(axis=2)
    m = lum < thr
    ys, xs = np.where(m)
    if len(xs)==0: return None
    return (xs.min()+x0, ys.min()+y0, xs.max()+x0, ys.max()+y0)
print("title ink bbox:", inkbbox(58, 82))
print("subtitle ink bbox:", inkbbox(84, 106))
