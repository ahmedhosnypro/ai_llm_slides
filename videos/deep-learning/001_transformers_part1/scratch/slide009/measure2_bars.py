#!/usr/bin/env python3
"""Pass 2: decoder + encoder internals in slide_009.jpg (bar groups via fill/edge masks)."""
from PIL import Image
import numpy as np
from scipy import ndimage

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(IM).convert("RGB"), dtype=np.int16)

def comps(m, min_area=40):
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    objs = ndimage.find_objects(lab)
    out = []
    for i, sl in enumerate(objs):
        ys, xs = sl
        area = int((lab[sl] == i + 1).sum())
        if area >= min_area:
            out.append((xs.start, ys.start, xs.stop, ys.stop, area))
    out.sort()
    return out

def show(name, m, min_area=40, limit=30):
    cs = comps(m, min_area)
    print(f"--- {name}: {len(cs)} comps")
    for x0, y0, x1, y1, area in cs[:limit]:
        print(f"    x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0}) area={area}")
    return cs

def near(color, tol):
    c = np.array(color)
    return (np.abs(a - c).sum(axis=2) <= tol)

# --- DECODER region (x480..915, y110..290) -------------------------------------
sub = np.zeros(a.shape[:2], bool); sub[110:290, 480:915] = True
print("== DECODER ==")
# green softmax bars: fill E8FF6E distinct from container FDFF85 via R+blue channel
g = near((232, 255, 110), 22) & sub
show("dec green fill E8ff6e", g, 40)
# hidden bars: FAEC69 (G236 B105) vs container FDFF85 (G255 B133)
h = near((250, 236, 105), 14) & sub
show("dec hidden fill FAEC69", h, 40)
# edges
show("dec green edge C2D64A", near((194, 214, 74), 30) & sub, 20)
show("dec hidden edge C2C744", near((194, 199, 68), 30) & sub, 20)
# container fill FDFF85 exact
show("dec container fill FDFF85", near((253, 255, 133), 12) & sub, 2000, 5)

# --- ENCODER region (x45..500, y300..505) ---------------------------------------
sub2 = np.zeros(a.shape[:2], bool); sub2[300:505, 45:500] = True
print("== ENCODER ==")
show("enc container fill F8D5AD", near((248, 213, 173), 10) & sub2, 2000, 5)
show("enc pink edge C29F77", near((194, 159, 119), 25) & sub2, 20)
show("enc tan edge C9A87B", near((201, 168, 123), 25) & sub2, 20)
# pink fill vs container: F2C7A7 (242,199,167) vs F8D5AD (248,213,173)
show("enc pink fill F2C7A7", near((242, 199, 167), 10) & sub2, 40)
show("enc tan fill F9D5A3", near((249, 213, 163), 8) & sub2, 40)
