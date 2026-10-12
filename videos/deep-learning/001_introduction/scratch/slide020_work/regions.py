from PIL import Image
import numpy as np
from scipy import ndimage

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def mask_near(target, tol):
    t = np.array(target)
    d = np.abs(a - t).max(axis=2)
    return d <= tol

def report(name, target, tol, minpix=30):
    m = mask_near(target, tol)
    lab, n = ndimage.label(m)
    objs = ndimage.find_objects(lab)
    sizes = ndimage.sum(m, lab, range(1, n+1))
    out = []
    for i, sl in enumerate(objs):
        if sizes[i] >= minpix:
            ys, xs = sl
            out.append((int(sizes[i]), xs.start, ys.start, xs.stop, ys.stop))
    out.sort(reverse=True)
    print(f"== {name} target={target} tol={tol} total_px={int(m.sum())}")
    for s, x0, y0, x1, y1 in out[:12]:
        print(f"   bbox x[{x0}..{x1}) y[{y0}..{y1}) w={x1-x0} h={y1-y0} px={s}")

report("canvas_white", (255,255,255), 12, 500)
report("outer_gray", (242,242,242), 6, 500)
report("tan_C9A66B", (201,166,107), 30, 100)
report("tan_ellipse_E8D4A2", (232,212,162), 20, 100)
report("container_FDE9D9", (253,233,217), 12, 100)
report("paleyellow_FFFFCC", (255,255,204), 14, 80)
report("paleblue_CCE5FF", (204,229,255), 14, 80)
report("palegreen_CCFFCC", (204,255,204), 14, 80)
report("darkred_990000", (153,0,0), 40, 80)
report("lavender_E6CCFF", (230,204,255), 16, 80)
report("pink_FFB3B3", (255,179,179), 16, 80)
report("ltgreen_box_E2EFDA", (226,239,218), 10, 100)
report("green_text_339933", (51,153,51), 45, 40)
report("starburst_FFFF99", (255,255,153), 16, 80)
report("black", (0,0,0), 60, 100)
report("blue_0000CC", (0,0,204), 60, 30)
report("green_009900", (0,153,0), 55, 30)
report("red_CC0000", (204,0,0), 55, 30)
